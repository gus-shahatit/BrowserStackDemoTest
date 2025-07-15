import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# No credentials or capabilities are hardcoded here

options = webdriver.ChromeOptions()
options.set_capability('sessionName', 'My BStack Test')
driver = webdriver.Chrome(options=options)

try:
    # 1. Test Login first
    driver.get("https://www.bstackdemo.com/")
    print(f"\n--- Navigated to: {driver.current_url} ---")
    time.sleep(1)

    signin_btn = driver.find_element(By.CSS_SELECTOR, "#signin")
    signin_btn.click()

    username = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "username"))
    )
    username.click()
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-select-2-option-0-0"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", username_input)
    driver.execute_script("arguments[0].click();", username_input)
    print("username setup")

    password = driver.find_element(By.ID, "password")
    password.click()
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-select-3-option-0-0"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", password_input)
    driver.execute_script("arguments[0].click();", password_input)
    print("password setup")

    login_btn = driver.find_element(By.ID, "login-btn")
    login_btn.click()
    driver.implicitly_wait(10)
    print("click setup")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "orders")))
    print("Successfully logged in (Orders link visible).")

    # 2. Filter Samsung
    samsung_checkbox_locator = (By.XPATH, "//input[@type='checkbox' and @value='Samsung']/following-sibling::span[@class='checkmark']")
    samsung_checkbox = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(samsung_checkbox_locator),
        message="Samsung checkbox not found in DOM within 20 seconds."
    )
    samsung_checkbox.click()
    print("Samsung filter applied successfully.")
    time.sleep(5)
    product_titles = driver.find_elements(By.CLASS_NAME, "shelf-item__details")
    for title_element in product_titles:
        product_name = title_element.find_element(By.CLASS_NAME, "shelf-item__title").text
        assert "Samsung" in product_name, f"Product '{product_name}' found, but should be Samsung only."
    print("Verified that only Samsung products are displayed.")

    # 3. Favorite Galaxy S20+
    galaxy_s20_plus_button_xpath = (
        "//div[@data-sku='samsung-S20+-device-info.png']//button[contains(@class, 'MuiIconButton-root')]"
    )
    print("Waiting for the Galaxy S20+ favourite button to be clickable...")
    favourite_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, galaxy_s20_plus_button_xpath))
    )
    print("Galaxy S20+ favourite button found and is clickable.")
    favourite_button.click()
    print("Clicked the favourite button for Samsung S20+.")
    time.sleep(5)

    try:
        favorite_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "favourites"))
        )
        favorite_link.click()
        print("Clicked favourites link.")
    except:
        print("favourites link not found or not needed, proceeding to login fields.")

    # If all steps pass:
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Congratulations! Your test has passed!"}}'
    )

except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}'
    )
    raise
finally:
    driver.quit()
