import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


HOME_URL = "https://www.tradewheel.com/suppliers/"
is_scraped = False
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

driver = webdriver.Chrome(options=options)
driver.get(HOME_URL)

# --------------Scraping categories--------------

categories = driver.find_elements(
    By.CSS_SELECTOR,
    "div.wbg > div:nth-child(5) > div.col-xs-6.col-sm-4.col-md-3.link_box.ind_box > a",
)
print(f"\nSession started\n")
category_names, category_links = [], []
for company in categories[:-1]:
    category_names.append(company.text.replace(",", ""))
    category_links.append(company.get_attribute("href"))

# --------------Looping through categories--------------
try:
    for i in range(len(category_links)):
        next_in_category_link = category_links[i]
        category_name = category_names[i]

        driver.get(next_in_category_link)

        # Company_names_on_current_page
        company_links_on_page = []
        finished_category = True
        while finished_category:
            # Company names list page--------------
            company_names_on_current_page = driver.find_elements(
                By.CSS_SELECTOR,
                "div.comp-listitem > h2.comp-name > a",
            )

            company_links_on_page = [
                company.get_attribute("href")
                for company in company_names_on_current_page
            ]

            # --------------Extracting singular row/single company info--------------
            for company_link in company_links_on_page:
                driver.get(company_link)

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
                row.insert(0, category_name)
                print("\n", row, "\n")

                # Writing to df--------------
                df.loc[len(df.index)] = row

            time.sleep(2)
            driver.get(next_in_category_link)

            # got to next page in the current category
            try:
                next_page = driver.find_element(
                    By.CSS_SELECTOR, "ul > li.page-item > a[rel='next']"
                )
                next_in_category_link = next_page.get_attribute("href")
                print("\nNext Page Clicked!\n")
                time.sleep(2)
                driver.get(next_in_category_link)
            except NoSuchElementException:
                finished_category = False
                print("Element Not Found!")
                time.sleep(2)
        time.sleep(5)
except NoSuchElementException:
    # --------------Writing to csv if no element found--------------
    df.to_csv("zp.csv", index=False)
    driver.get_screenshot_as_file("filename.png")
    print(f"\nPartially Scraped!")
    is_scraped = True


# --------------Writing to csv--------------
if not is_scraped:
    df.to_csv("z.csv", index=False)
    print(f"\nSuccussfully Scraped!")
