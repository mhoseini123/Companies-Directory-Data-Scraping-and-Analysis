
import json
import pandas as pd
import re
import numpy as np

def extract_money_value(value_str):
    """
    Extracts an integer money value from a string, handling currencies and scales.
    Converts all values to Euro.
    """
    if pd.isna(value_str) or not isinstance(value_str, str):
        return None

    convert_currencies = {"€": 1, "Euro": 1, "EUR": 1, "$": 0.93, "CHF": 1.05}
    currency_rate = 1 # Default currency as Euro

    # Find and apply currency rate
    for currency in convert_currencies.keys():
        if currency in value_str:
            currency_rate = convert_currencies[currency]
            value_str = value_str.replace(currency, '')
            break # Assume only one currency symbol per string

    # Handle explicit NaN/None after currency replacement if it becomes empty
    if not value_str.strip(): # Check if string is empty or just whitespace
        return None

    # Try to get the amount in the formats like million, billion, etc.
    match = re.search(r'(\d+[.,]?\d*)\s*(M B Mio millionen million|Mill\.|Billion|Bill\.|Mrd)',
                      value_str, re.IGNORECASE)

    num_str = None
    scale_str = None

    if match:
        num_str = match.group(1).replace(',', '.') # Get the numerical part
        # Check if scale part exists before trying to access it
        if match.lastindex > 1:
            scale_str = match.group(2).strip()

    # If no scale match, try to find a simple number
    if not num_str:
        simple_num_match = re.search(r'(\d+[.,]?\d*)', value_str)
        if simple_num_match:
            num_str = simple_num_match.group(1).replace(',', '.')

    if not num_str:
        return None

    try:
        num = float(num_str)
    except ValueError:
        return None

    # Multiply the number based on the scale
    if scale_str:
        scale_str = scale_str.lower()
        if scale_str in ['mio', 'million', 'millionen', 'mill.', 'm']:
            num *= 1e6
        elif scale_str in ['mrd', 'billion', 'bill.', 'b']:
            num *= 1e9

    final_num = num * currency_rate
    return int(final_num) # Return as integer as per original code

def extract_year(value_str):
    """
    Extracts a four-digit year from a string.
    """
    if pd.isna(value_str) or not isinstance(value_str, str):
        return None
    match = re.search(r'\b\d{4}\b', value_str)
    if match:
        return int(match.group(0))
    else:
        return None

def extract_employee_count(value_str):
    """
    Extracts number of employees as an integer, handling ranges.
    """
    if pd.isna(value_str) or not isinstance(value_str, str):
        return None
    # Remove thousand separators
    value_str = value_str.replace(',', '').replace('.', '')

    # Search for range of numbers (e.g., "100-200" or "100 -- 200")
    range_match = re.search(r'(\d+)\s*[-–—]\s*(\d+)', value_str)
    if range_match:
        lower_bound = int(range_match.group(1))
        upper_bound = int(range_match.group(2))
        return int((lower_bound + upper_bound) / 2)
    else:
        # Search for one or more digits
        match = re.search(r'\d+', value_str)
        if match:
            return int(match.group(0))
        else:
            return None

def preprocess_company_data(input_file_path, output_file_path):
    """
    Preprocesses raw company data from input_file_path and saves
    the cleaned data to output_file_path.
    """
    print(f"Starting data preprocessing from {input_file_path}...")
    with open(output_file_path, 'w', encoding='utf-8') as fout:
        for line in open(input_file_path, 'r', encoding='utf-8'):
            company_info = json.loads(line)
            processed_data = dict()

            for key, value in company_info.items():
                if key == "employees":
                    processed_data[key] = extract_employee_count(value)
                elif key == "establish_date":
                    processed_data[key] = extract_year(value)
                elif key == "money":
                    if value and "Kunden" in value: # Skip specific known bad values
                        processed_data[key] = None # Explicitly set to None
                    else:
                        processed_data[key] = extract_money_value(value)
                else:
                    processed_data[key] = value # For other attributes, no action is done

            json.dump(processed_data, fout, ensure_ascii=False)
            fout.write('\n')
    print(f"Preprocessing complete. Processed data saved to {output_file_path}")

if __name__ == "__main__":
    # Example usage if you run this script directly
    # Ensure 'data/output.json' exists for this to work
    input_json_path = 'data/output.json'
    output_json_path = 'data/preprocessed-dataset.json'

    # Create data directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Dummy output.json for testing if you don't have it yet
    # In a real scenario, this would be generated by your scraper
    if not os.path.exists(input_json_path):
        print(f"Warning: {input_json_path} not found. Creating a dummy file for demonstration.")
        dummy_data = [
            {"company_name": "Test Inc.", "employees": "100-200", "establish_date": "Founded 1990", "money": "10 Mio. €", "phone": "+49 123456", "url": "test.com"},
            {"company_name": "Another Corp", "employees": "50", "establish_date": "Est. 2005", "money": "$5 Million", "phone": "+1 987654", "url": "another.com"},
            {"company_name": "Third Company", "employees": "N/A", "establish_date": "unknown", "money": "2 Mrd. CHF", "phone": "+41 112233", "url": "third.com"},
            {"company_name": "Customer Focused", "employees": "20", "establish_date": "2010", "money": "Kundenbetreuung", "phone": "+49 998877", "url": "customer.com"}
        ]
        with open(input_json_path, 'w', encoding='utf-8') as f:
            for item in dummy_data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
        print("Dummy output.json created.")

    preprocess_company_data(input_json_path, output_json_path)
