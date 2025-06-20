
import scrapy
import json 

class CompanyInfoSpider(scrapy.Spider):
    name = "companyInfoSpider"   # Spider name
    # The initial URL to scrape
    start_urls = ["https://industrie.de/firmenverzeichnis/"]

    # Scrape the list of company URLs from the initial page
    def parse(self, response):
        # Extract all company URLs
        company_urls = response.css("div.infoservice-entry-holder > a::attr(href)").getall()

        # Loop through each URL to scrape contact info
        for url in company_urls:
            # Use response.urljoin to handle relative URLs correctly
            yield scrapy.Request(response.urljoin(url), callback=self.parse_company)

        # Pagination: Find the "Next Page" link and follow it
        # Need to inspect the HTML of industrie.de/firmenverzeichnis/ to get the
        # EXACT CSS selector for the next page link.
        # Common selectors: a.next, a.next-page, li.next a, a[rel="next"]
        next_page_link = response.css('a.next.page-numbers::attr(href)').get() # A common selector, verify for industrie.de

        if next_page_link is not None:
            yield scrapy.Request(response.urljoin(next_page_link), callback=self.parse)
            self.logger.info(f"Following next page: {next_page_link}") # Log when moving to next page

    # Scrape details for each company
    def parse_company(self, response):
        company_information = dict()   # Dictionary to hold the scraped data
        company_information['url'] = response.url # Store the URL of the company page

        # Extract company name from the main heading (adjust selector if needed)
        company_information['company_name'] = response.css('h1.page-title::text').get(default="N/A").strip()

        # Check if the page contains contact data
        # Assuming "Daten und Kontakte" is within a specific heading or span
        contact_section_title = response.css("#infoservice-sidebar1 > div.widget-title.h6 > span::text").get()

        if contact_section_title == "Daten und Kontakte":
            icon_types = {
                "fa fa-globe": "website",
                "fa fa-envelope": "email",
                "fa fa-phone": "phone",
                "fa fa-fax": "fax",
                "fa fa-group": "employees",
                "fa fa-flag": "establish_date",
                "fa fa-euro": "money", # Add money if it has a consistent icon
                "fa fa-map-marker": "address" # Assuming address also has an icon for robust extraction
            }

            # Iterate through each 'dd' element within the 'dl' of the contact section
            # This is more robust than relying on nth-child for all fields
            for dl_item in response.css('#infoservice-sidebar1 div.textwidget dl dd'):
                icon_class = dl_item.css('i::attr(class)').get()
                if icon_class and icon_class in icon_types:
                    info_type = icon_types[icon_class]
                    
                    if info_type == "address":
                        # For address, get all text nodes and join them
                        info = ' '.join(dl_item.css('::text').getall()).strip()
                    else:
                        # For other types, get the direct text content (adjust if text is inside a specific tag like 'a')
                        info = dl_item.css('::text').get(default="N/A").strip()
                        # If the text is empty after stripping, and there's a link inside, try getting text from link
                        if not info or info == "N/A":
                             info = dl_item.css('a::text').get(default="N/A").strip()


                    company_information[info_type] = info
        else:
            # If the page doesn't have the contact information or the section title is different
            # Log an error or handle accordingly. For now, store a message.
            company_information["scrape_status"] = "Contact section NOT found or title mismatch."
            self.logger.warning(f"Contact section not found for {response.url}. Title: {contact_section_title}")


        # Instead of manual file writing, yield the item (dictionary)
        # Scrapy's Feed Exporter will handle writing to output.json if configured.
        yield company_information
