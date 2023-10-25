import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


category = "Agriculture"
next_in_category_link = "https://www.tradewheel.com/suppliers/agriculture/?page=1"
df = pd.DataFrame(
    columns=[
        "Category",
        "Business Type",
        "Supplier",
        "Country",
        "Main Products",
        "Established Year",
        "Total Employees",
        "Total Estimated Revenue",
        "Export Percentage",
    ]
)

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument(f"user-agent={user_agent}")
# Translation-----------------
# prefs = {
#     "translate_whitelists": {"zh-CN": "en"},
#     "translate": {"enabled": "true"},
# }
# options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.get(next_in_category_link)


# page_numbers = driver.find_elements(
#     By.CSS_SELECTOR,
#     "body > div:nth-child(5) > div:nth-child(2) > div.col-md-10.col-lg-10.col-sm-12.col-xs-12 > div:nth-child(2) > div.col-xs-12.text-center.pagination-container > nav > ul > li.page-item",
# )


# company_names_on_current_page
company_links_on_page = []
finished_category = True
while finished_category:
    # company names list page--------------
    company_names_on_current_page = driver.find_elements(
        By.CSS_SELECTOR,
        "div.comp-listitem > h2.comp-name > a",
    )

    company_links_on_page = [
        company.get_attribute("href") for company in company_names_on_current_page
    ]
    for company_link in company_links_on_page:
        driver.get(company_link)
        # time.sleep(5)
        # --------------Extracting singular row--------------

        # Company Information--------------
        business_type = driver.find_element(
            By.CSS_SELECTOR,
            "#comp_info > div:nth-child(1) > div > table > tbody > tr:nth-child(1) > td:nth-child(2)",
        )
        company_name = driver.find_element(
            By.CSS_SELECTOR,
            "#comp_info > div:nth-child(1) > div > table > tbody > tr:nth-child(2) > td:nth-child(2)",
        )
        main_products = driver.find_element(
            By.CSS_SELECTOR,
            "#comp_info > div:nth-child(1) > div > table > tbody > tr:nth-child(3) > td:nth-child(2)",
        )
        established_year = driver.find_element(
            By.CSS_SELECTOR,
            "#comp_info > div:nth-child(1) > div > table > tbody > tr:nth-child(4) > td:nth-child(2)",
        )
        country = driver.find_element(
            By.CSS_SELECTOR,
            "#comp_info > div:nth-child(1) > div > table > tbody > tr:nth-child(6) > td:nth-child(2)",
        )
        total_employees = driver.find_element(
            By.CSS_SELECTOR,
            "#comp_info > div:nth-child(1) > div > table > tbody > tr:nth-child(8) > td:nth-child(2)",
        )

        company_info = [
            business_type.text.replace(",", "").replace("-", ""),
            company_name.text.replace(",", ""),
            country.text.replace(",", ""),
            main_products.text.replace(",", ""),
            established_year.text.replace(",", ""),
            total_employees.text.replace(",", ""),
        ]

        try:
            # Trading Information--------------
            total_revenue = driver.find_element(
                By.CSS_SELECTOR,
                "#comp_info > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(2)",
            )
            export_precentage = driver.find_element(
                By.CSS_SELECTOR,
                "#comp_info > div:nth-child(2) > div > table > tbody > tr:nth-child(2) > td:nth-child(2)",
            )

            trading_info = [
                total_revenue.text.replace(",", ""),
                export_precentage.text.replace(",", ""),
            ]

        except NoSuchElementException:
            trading_info = ["", ""]
            print("Element Not Found!")

        row = company_info + trading_info
        row.insert(0, category)
        print("\n", row, "\n")

        # Writing to df--------------
        df.loc[len(df.index)] = row

    # click next page button
    driver.get(next_in_category_link)
    try:
        next_page = driver.find_element(
            By.CSS_SELECTOR, "ul > li.page-item > a[rel='next']"
        )
        next_in_category_link = next_page.get_attribute("href")
        print("\nNext Page Clicked!\n")
        driver.get(next_in_category_link)
        time.sleep(1)
    except NoSuchElementException:
        finished_category = False
        print("Element Not Found!")

# --------------Writing to csv--------------
df.to_csv("suppliers_list.csv", index=False)
