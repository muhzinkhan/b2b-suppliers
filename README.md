# TradeWheel B2B Supplier Scraper (Selenium)

## Overview

This Python script is designed to extract valuable information about global B2B suppliers from the website [TradeWheel.com](https://www.tradewheel.com/). This script leverages the Selenium library to interact with the website dynamically, allowing for data extraction even from pages with JavaScript-driven content.

## Features

- Utilizes Selenium for dynamic web scraping of B2B supplier information.
- Extracts data fields such as _Category, Business Type, Supplier, Country, Main Products, Established Year, Total Employees, Total Estimated Revenue_, and _Export Percentage_.
- Organizes data into a structured CSV file for easy analysis.

## Requirements

- Python 3.x
- Selenium
- ChromeDriver (or suitable WebDriver for your preferred browser)

## Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python 3.x installed on your system.
3. Install the Selenium
4. Download and install the appropriate WebDriver for your browser:

- [ChromeDriver](https://sites.google.com/chromium.org/driver/home)
- [GeckoDriver (for Firefox)](https://github.com/mozilla/geckodriver/releases)
- [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

Ensure the WebDriver executable is in your system's PATH.

## Output

The script generates a CSV file named `suppliers_list.csv` that contains the scraped information about B2B suppliers. The data is organized into columns for each of the following fields:

- Category
- Business Type
- Supplier
- Country
- Main Products
- Established Year
- Total Employees
- Total Estimated Revenue
- Export Percentage
