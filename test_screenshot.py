from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
options.headless = True

# Use snap path directly
service = Service(executable_path="/snap/bin/geckodriver")

try:
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1366, 768)
    driver.get("https://example.com")
    driver.save_screenshot("test.png")
    driver.quit()
    print("✅ Screenshot saved as test.png")
except Exception as e:
    print("❌ Error:", str(e))
