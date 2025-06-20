# Companies Directory Data Scraping and Analysis

    This project focuses on scraping, preprocessing, and analyzing company data from `industrie.de/firmenverzeichnis/`.

## Project Overview

This project focuses on building a complete data pipeline for extracting and analyzing structured information from a dynamic website. It consists of three main components:

    -Web Scraping: Utilizes the Scrapy framework to extract structured data from a dynamic website, capturing information such as company names, financial figures, employee counts, and founding dates.

    -Data Preprocessing & Cleaning: Transforms the raw, unstructured text data into a clean, analysis-ready format. This includes parsing and converting monetary values, standardizing date formats, and handling missing or inconsistent entries.

    -Exploratory Data Analysis (EDA): Applies statistical summaries and visualizations to uncover patterns and trends in the cleaned data, laying the foundation for further analysis or machine learning applications.


## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mhoseini123/Companies-Directory-Data-Scraping-and-Analysis.git
    cd Companies-Directory-Scraping-Data-and-Analysis
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Web Scraping

To scrape the raw company data from `industrie.de/firmenverzeichnis/`:

    ```bash
    # Navigate to the Scrapy project folder
    cd scrapy_spider
    # Run the spider
    scrapy crawl companyInfoSpider -o ../data/output.json -t jsonlines
    # Go back to the project root
    cd ..


Note: The website structure may change, requiring updates to CSS selectors in scrapy_spider/companyInfo/spiders/companyInfoSpider.py.

### 2. Data Preprocessing & EDA
To preprocess the scraped data and perform exploratory data analysis:

    Open the Jupyter Notebook:

    Bash:
    jupyter notebook notebooks/eda_notebook.ipynb

    Follow the steps in the notebook to:
        Load data/output.json
        Apply preprocessing functions from src/data_processor.py
        Generate statistical summaries and visualizations (saved to plots/)


Technologies Used
    Python 3.x
    Scrapy
    Pandas
    NumPy
    Matplotlib
    Seaborn

    
Contact:
    Mohamad Hoseini
    Github: https://github.com/mhoseini123
    LinkedIn: https://www.linkedin.com/in/hoseini-mhd/


