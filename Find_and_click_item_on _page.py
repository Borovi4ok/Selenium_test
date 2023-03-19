from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver_path = "\Disk D\Draft\QA Tester\Chrome_webdriver\chromedriver"
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chr_options)
driver.get("https://rahulshettyacademy.com/angularpractice/shop")
driver.implicitly_wait(5)  # wait for 5 sec if element is not found

# find on the product list page item named "Blackberry" and put it in the cart

# assert Cart is empty
checkout_before = driver.find_element(By.XPATH, "//a[@class='nav-link btn btn-primary']").text
assert "Checkout ( 0 )" in checkout_before

# list of entire elements(items) on the page
page_elements_list = driver.find_elements(By.XPATH, "//*[@class='col-lg-3 col-md-6 mb-3']")

# loop through and find item named "Blackberry"
for element in page_elements_list:
    if 'Blackberry' in element.text:
        # find button inside of element and click it
        element.find_element(By.XPATH, "//button[@class='btn btn-info']").click()

# assert there is 1 item in cart
checkout_after = driver.find_element(By.XPATH, "//a[@class='nav-link btn btn-primary']").text
assert "Checkout ( 1 )" in checkout_after

driver.quit()