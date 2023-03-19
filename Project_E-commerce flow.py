# E-commerce automation testing
# Target: Test flow of ordering from E-store: ("https://www.saucedemo.com/")

# St 1. Log-in with Username (standard_user), password (secret_sauce)
# St 2. Verify min 6 items displayed on page
# St 3. Add to cart first, last, and a different random item and go to cart
# St 4. Verify cart icon displays correct number of items in it (3), go to Cart page
# St 5. Verify 3 items are on the Cart page and proceed to Ceckout page
# St 6. Fill out First, Last name, ZIP Code and Continue to Checkout: Overview
# St 7.  On Checkout: Overview page verify:
    # There are 3 items on page,
    # Payment Information contains text "SauceCard #31337"
    # Shipping Information contains "Free Pony Express Delivery!"
    # Item Total is real sum of items prices
    # Tax is 8%
    # Total is Item Total + Tax
# St 8. Click "Finish" button and verify next page shows messages:
    # "Thank you for your order!
    # Your order has been dispatched, and will arrive just as fast as the pony can get there!"
# St 9. Click "Back home" button and verify home URL of next page

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver_path = "\Disk D\Draft\QA Tester\Chrome_webdriver\chromedriver"
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chr_options)
driver.get("https://www.saucedemo.com/")
driver.implicitly_wait(5)  # wait for 5 sec if element is not found

# St 1. Log-in with Username (standard_user), password (secret_sauce)
driver.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
driver.find_element(By.CSS_SELECTOR, ".input_error[type='password']").send_keys("secret_sauce")
driver.find_element(By.CSS_SELECTOR, "#login-button").click()

# St 2. Verify min x items displayed on page
x = 6
def count_items(x):
    items_list = driver.find_elements(By.CSS_SELECTOR, ".inventory_item")
    items_displayed = len(items_list)
    assert items_displayed >= x
    return items_list, items_displayed


# St 3. Add to cart first, last, and random item and go to cart
import random
# call count_items(x) func to retrieve list and its length
items_list, items_displayed = count_items(x)

# List with indexes for first, last and random in items_list
purchase_index_list = [0, items_displayed - 1, random.randrange(1, items_displayed - 1)]

for index in purchase_index_list:
    # chaining for buttons.
    # Call (list, not driver) by extension only since " div button" is  nested in ".inventory_item"
    # full CSS locator for buttons is ".inventory_item div button"
    items_list[index].find_element(By.CSS_SELECTOR, " div button").click()

# St 4. Verify cart icon displays correct number of items in it (3), go to Cart page
# convert extracted text str->int
assert int(driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text) == 3

driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

# St 5. Verify 3 items are on the Cart page and proceed to Ceckout page
assert len(driver.find_elements(By.CSS_SELECTOR, ".cart_item")) == 3
driver.find_element(By.ID, "checkout").click()

# St 6. Fill out First, Last name, ZIP Code and Continue to Checkout: Overview
f_name = "Agura"
l_name = "McDonalds"
z_code = "Q1D2Y8"

driver.find_element(By.ID, "first-name").send_keys(f_name)
driver.find_element(By.ID, "last-name").send_keys(l_name)
driver.find_element(By.ID, "postal-code").send_keys(z_code)
driver.find_element(By.ID, "continue").click()

# St 7.  On Checkout: Overview page verify:
    # There are 3 items on page,
    # Payment Information contains text "SauceCard #31337"
    # Shipping Information contains "Free Pony Express Delivery!"
    # Item Total is real sum of items prices
    # Tax is 8%
    # Total is Item Total + Tax


# There are 3 items on page
assert len(driver.find_elements(By.CLASS_NAME, "cart_item")) == 3

# Payment Information contains text "SauceCard #31337"
assert driver.find_element(By.CSS_SELECTOR, "div.summary_info div:nth-child(2)").text == "SauceCard #31337"

# Shipping Information contains "Free Pony Express Delivery!"
assert driver.find_element(By.CSS_SELECTOR, "div.summary_info div:nth-child(4)").text == "Free Pony Express Delivery!"


# Item Total is real sum of items prices
# Tax is 8 %
# Total is Item Total + Tax

# list of the items in cart
text_list = driver.find_elements(By.XPATH, "//div[@class='inventory_item_price']")

# select only text (price) from text_list to the price_list
price_list = [tex.text for tex in text_list]

# delete (replace) $-sign from text (price)
new_price_list = []
for price in price_list:
    new_price_list.append(price.replace("$", ""))

# calculate sum of prices in cart
# use try/except block to make sure are prices are iterable
item_total = 0
for price in new_price_list:
    try:
       item_total += float(price)
    except ValueError:
        print(f"Invalid price: {price}")

# function to validate if extracted text (price) can be converted into float
# text containing string with number (price)
import re

def extract_float(text):
    pattern = r'[-+]?\d*\.\d+|\d+'
    match = re.search(pattern, text)
    if match:
        return float(match.group())
    else:
        raise ValueError(f"Could not extract float from '{text}'.")


# call system calculated sum of prices in cart (item_total)
# item_total = call func to validate, trim and convert string with sum from Checkout: Overview page into float
item_total_page = extract_float(driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text)

# the same for tax and grand total
tax_page = extract_float(driver.find_element(By.CLASS_NAME, "summary_tax_label").text)
grand_total_page = extract_float(driver.find_element(By.CLASS_NAME, "summary_total_label").text)

# asserting system calculated sum of prices is correct
# asserting system calculated grand total is correct
# asserting system calculated tax = 8% is correct
assert item_total_page == item_total
assert grand_total_page == round(item_total * 1.08, 2)  # round result or multiplying to 2 decimals
assert tax_page == round(grand_total_page - item_total_page, 2)


# St 8. Click "Finish" button and verify next page shows messages:
    # "Thank you for your order!"
    # "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
driver.find_element(By.ID, "finish").click()


assert "Thank you for your order!" in driver.find_element(By.CLASS_NAME, "complete-header").text
assert "Your order has been dispatched" in driver.find_element(By.CLASS_NAME, "complete-text").text


# St 9. Click "Back home" button and verify home URL of next page
driver.find_element(By.ID, "back-to-products").click()
assert "inventory.html" in driver.current_url

# Process finished with exit code 0
