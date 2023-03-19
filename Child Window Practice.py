from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver_path = "\Disk D\Draft\QA Tester\Chrome_webdriver\chromedriver"
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chr_options)
driver.get("https://rahulshettyacademy.com/loginpagePractise/")
driver.implicitly_wait(5)  # wait for 5 sec if element is not found

# click link
driver.find_element(By.LINK_TEXT, "Free Access to InterviewQues/ResumeAssistance/Material").click()

# capture a list of opened windows
openedPagesList = driver.window_handles

# switch focus to a child window ind[1] - second in list
driver.switch_to.window(openedPagesList[1])

# extract text containing user email
capturedText = driver.find_element(By.CSS_SELECTOR, 'div p.im-para.red').text

# safe user email to "username" var where capturedText[19:48] is string trimmed to email only
userName = capturedText[19:48]
# or userNam = message.split("at")[1].strip().split(" ")[0]

# close child window
driver.close()

# switch to parent window
driver.switch_to.window(openedPagesList[0])

# username input
driver.find_element(By.ID, "username").send_keys(userName)

# password input
driver.find_element(By.ID, "password").send_keys("password")

# terms checkbox
driver.find_element(By.ID, "terms").click()

# click "Sign In" button
driver.find_element(By.ID, "signInBtn").click()

# wait for error message visibility
wait = WebDriverWait(driver,10)
wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger")))

# get text from error message
errorMessage = driver.find_element(By.CSS_SELECTOR, ".alert-danger").text

driver.get_screenshot_as_file("name.png")
# assert error message
assert "Incorrect username/password." in errorMessage


