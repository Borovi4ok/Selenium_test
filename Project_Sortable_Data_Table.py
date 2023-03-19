from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver_path = "\Disk D\Draft\QA Tester\Chrome_webdriver\chromedriver"
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chr_options)
driver.get("https://the-internet.herokuapp.com/tables")
driver.implicitly_wait(5)  # wait for 5 sec if element is not found

# Check whether all columns in the table 1 can be correctly sorted alphabetically

# takes list of sorted in table Webelements and extract text into string_original_list
# call check_if_alphabetic() to see if sorted correctly
def extract_text(elements_list):
    string_original_list = [value.text for value in elements_list]
    check_if_alphabetic(string_original_list)

# takes list of sorted in table Webelements and extract text (convert into float) into number_original_list
# call check_if_alphabetic() to see if sorted correctly
def extract_number(elements_list):
    number_original_list = [float(value.text.split("$")[1]) for value in elements_list]
    check_if_alphabetic(number_original_list)

# create sorted by Py list "sorted_list" out of "original_list"
# using sorted() method (to get it in a new array) since sort() method will sort inside of current array
# assert if they both are the same (arrange alphabetically)
def check_if_alphabetic(original_list):
    sorted_list = sorted(original_list)
    assert sorted_list == original_list, f"Error: the list {original_list} was not sorted correctly"


# loop through column headers to get them sorted alphabetically
# i = number of header tag (th) and column tag (td) in HTML DOM
for i in range(1, 6):
    # xpath var concatenates Xpath with 'i' as Number
    # clock a header and sort its column
    xpath_header = f"//table[@id='table1']/thead/tr/th[{i}]"
    driver.find_element(By.XPATH, xpath_header).click()

    # get list of sorted items in this column (with the same index 'i' for all (td) in DOM
    xpath_column = f"//table[@id='table1']/tbody/tr/td[{i}]"
    elements_list = driver.find_elements(By.XPATH, xpath_column)

    # different func depending on list contains str or float
    # if i = 4 - column with numeric prices
    if i == 4:
        # send list to "extract_numbers" and remove $ sign
        extract_number(elements_list)
    else:
        # send lict to extract text from WebElements
        extract_text(elements_list)

driver.quit()