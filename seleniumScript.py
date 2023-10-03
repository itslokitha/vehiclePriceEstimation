from selenium import webdriver

# Set up WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Optional: Run in headless mode

# If you included the ChromeDriver executable in your repository
chrome_path = "./chromedriver"  # Adjust the path as needed

# Initialize WebDriver
driver = webdriver.Chrome(chrome_path, options=chrome_options)

# Load the GitHub-hosted page
driver.get("https://github.com/SeleniumHQ/Selenium")

# Use Selenium to interact with the page
# For example, find an element and extract information

# Don't forget to close the WebDriver
driver.quit()