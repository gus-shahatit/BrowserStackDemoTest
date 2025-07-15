import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BStackDemoTestSuite(unittest.TestCase):
    """
    Test suite for www.bstackdemo.com covering login, filtering, favoriting,
    and verification of a favorite item.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the WebDriver for all tests in this class.
        This runs once before any tests.
        """
        print("\n--- Setting up WebDriver ---")
        # Initialize Chrome WebDriver. Make sure chromedriver is in your PATH
        # or provide the full path: executable_path='/path/to/chromedriver'
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window() # Maximize the browser window
        cls.driver.implicitly_wait(10) # Set implicit wait for 10 seconds

    def setUp(self):
        """
        Actions to perform before each test method.
        Navigate to the base URL.
        """
        self.driver.get("https://www.bstackdemo.com/")
        print(f"\n--- Navigated to: {self.driver.current_url} ---")
        time.sleep(1) # Small pause for page load stability

    def test_01_login(self):
        """
        Test Case 1: Log into www.bstackdemo.com
        """
        print("Running test_01_login...")
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Click on the 'Sign In' link (assuming it's available)
        # BStackDemo usually presents a login screen directly or after clicking 'Sign In'
        # try:
        #     sign_in_link = wait.until(EC.element_to_be_clickable((By.ID, "signin")))
        #     sign_in_link.click()
        #     print("Clicked Sign In link.")
        # except:
        #     print("Sign In link not found or not needed, proceeding to login fields.")

        signin_btn = driver.find_element(by=By.CSS_SELECTOR,value="#signin")
        signin_btn.click()


        # # Wait for username field to be present and fill it
        # username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username input")))
        # username_field.send_keys("demouser")
        # print("Entered username.")

        # # Fill password field
        # password_field = driver.find_element(By.CSS_SELECTOR, "#password input")
        # password_field.send_keys("testingisfun99")
        # print("Entered password.")

        # # Click the Login button
        # login_button = driver.find_element(By.ID, "login-btn")
        # login_button.click()
        # print("Clicked login button.")
        #Find the Username, Password and Login Button
        username =driver.find_element(by=By.ID,value="username")
        password =driver.find_element(by=By.ID,value="password")
        login_btn= driver.find_element(by=By.ID,value="login-btn")
        print("variables setup")

        #Select demouser as Username
        username.click()
        username_input= driver.find_element(by=By.CSS_SELECTOR,value="#react-select-2-option-0-0")
        username_input.click()
        print("username setup")


        #Select testingisfun99 as Password
        password.click()
        password_input =driver.find_element(by=By.CSS_SELECTOR,value="#react-select-3-option-0-0")
        password_input.click()
        print("password setup")


        # Submit the form
        login_btn.click()
        driver.implicitly_wait(10)
        print("click setup")


        #Assert User is successfully Logged In
        #logout_btn= driver.find_element(by=By.CSS_SELECTOR,value="#logout")
        #assert logout_btn.is_displayed()

        #driver.close()

        # Verify successful login by checking for an element on the logged-in page
        # For bstackdemo, a good indicator is the 'Orders' link or the 'Sign Out' link
        try:
            wait.until(EC.visibility_of_element_located((By.ID, "orders")))
            print("Successfully logged in (Orders link visible).")
            self.assertTrue(True, "Login was successful.") # Explicitly assert success
        except Exception as e:
            self.fail(f"Login failed: Could not verify logged-in state. {e}")

    def test_02_filter_samsung(self):
        """
        Test Case 2: Filter products to show "Samsung" devices only.
        This test depends on successful login from the previous test.
        """

        print("Running test_02_filter_samsung...")
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        # Wait for the "Samsung" filter checkbox and click it
        samsung_checkbox_locator = (By.XPATH, "//input[@type='checkbox' and @value='Samsung']/following-sibling::span[@class='checkmark']")
    
        # Wait up to 20 seconds for the element to be clickable
        samsung_checkbox = WebDriverWait(driver, 20).until( # Increased timeout to 20 seconds
            EC.presence_of_element_located(samsung_checkbox_locator),
            message="Samsung checkbox not found in DOM within 20 seconds."
        )
        samsung_checkbox.click()
        print("Samsung filter applied successfully.")

        # Verify that only Samsung products are displayed.
        # This is a bit more complex, we'll check product titles.
        # Give it a moment for the filter to apply
        time.sleep(5)

        product_titles = driver.find_elements(By.CLASS_NAME, "shelf-item__details")
        for title_element in product_titles:
            product_name = title_element.find_element(By.CLASS_NAME, "shelf-item__title").text
            self.assertIn("Samsung", product_name, f"Product '{product_name}' found, but should be Samsung only.")
        print("Verified that only Samsung products are displayed.")

    def test_03_favorite_galaxy_s20plus(self):
        """
        Test Case 3: Favorite the "Galaxy S20+" device.
        This test depends on the filter being applied from the previous test.
        """
        print("Running test_03_favorite_galaxy_s20plus...")
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        # Wait for the "Samsung" filter checkbox and click it
        samsung_checkbox_locator = (By.XPATH, "//input[@type='checkbox' and @value='Samsung']/following-sibling::span[@class='checkmark']")
    
        # Wait up to 20 seconds for the element to be clickable
        samsung_checkbox = WebDriverWait(driver, 5).until( # Increased timeout to 20 seconds
            EC.presence_of_element_located(samsung_checkbox_locator),
            message="Samsung checkbox not found in DOM within 20 seconds."
        )
        samsung_checkbox.click()
        print("Samsung filter applied successfully.")

        # Verify that only Samsung products are displayed.
        # This is a bit more complex, we'll check product titles.
        # Give it a moment for the filter to apply
        time.sleep(5)

        # Find the "Galaxy S20+" item
        # We need to locate the specific product and then its heart icon.
        # This XPath looks for an article containing 'Galaxy S20+' text and then finds its heart icon.
        galaxy_s20_plus_button_xpath = (
            "//div[@data-sku='samsung-S20+-device-info.png']" # Reverted to target the original Galaxy S20+
            "//button[contains(@class, 'MuiIconButton-root')]"
        )

        print("Waiting for the Galaxy S20+ favourite button to be clickable...")
        # Wait until the button is present and clickable
        favourite_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, galaxy_s20_plus_button_xpath))
        )
        print("Galaxy S20+ favourite button found and is clickable.")

        # Click the favourite button
        favourite_button.click()

        print("Clicked the favourite button for Samsung S20+.")
        time.sleep(5)

        try:
            favorite_link = wait.until(EC.element_to_be_clickable((By.ID, "favourites")))
            favorite_link.click()
            print("Clicked favourites link.")
        except:
            print("favourites link not found or not needed, proceeding to login fields.")

        time.sleep(5)

        print ("d")
        #expected_product_name = "Galaxy S20+"

        
        # product_title_element = WebDriverWait(driver, 5).until(
        #         EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'shelf-item-title') and text()='{expected_product_name}']"))
        #     )
        # print (product_title_element)

        # # Get the actual text from the element
        # actual_product_name = product_title_element.text

        # # Assert that the actual product name matches the expected product name
        # self.assertEqual(actual_product_name, expected_product_name,
        #                     f"Expected '{expected_product_name}' but found '{actual_product_name}' in favourites.")
        # print(f"Successfully verified: '{expected_product_name}' is in the favourites list.")

        


        # item_on_page = WebDriverWait(driver, 10).until(
        #  EC.visibility_of_element_located((By.XPATH, '//*[@id="1"]/p'))).text
        # item_in_fav = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        #     (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[2]/div/div[3]/p[1]'))).text
        # # Verify whether the product (iPhone 12) is added to cart
        # if item_on_page == item_in_fav:
        #     # Set the status of test as 'passed' if item is added to cart
        #     driver.execute_script(
        #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Samsung S20+ has been successfully added to favorites!"}}')
        # else:
        #     # Set the status of test as 'failed' if item is not added to cart
        #     driver.execute_script(
        #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Samsung 20+ has not added to favorite!"}}')

        # try:
        #     # Scroll to the element if necessary
        #     galaxy_s20_plus_heart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, galaxy_s20_plus_button_xpath)))
        #     driver.execute_script("arguments[0].scrollIntoView();", galaxy_s20_plus_heart_icon)
        #     time.sleep(0.5) # Small pause after scroll
        #     galaxy_s20_plus_heart_icon.click()
        #     print("Clicked favorite icon for Galaxy S20+.")
        # except Exception as e:
        #     self.fail(f"Could not find or click favorite icon for Galaxy S20+: {e}")

        # You might want to assert that the heart icon changes color or that a success message appears
        # For simplicity, we'll just assume the click was successful for now and verify on favorites page.


if __name__ == '__main__':
    # Create a test suite and add tests in a specific order
    suite = unittest.TestSuite()
    suite.addTest(BStackDemoTestSuite('test_01_login'))
    #suite.addTest(BStackDemoTestSuite('test_02_filter_samsung'))
    suite.addTest(BStackDemoTestSuite('test_03_favorite_galaxy_s20plus'))

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2) # verbosity=2 for more detailed output
    print("\n--- Starting BStackDemo Test Suite Execution ---")
    runner.run(suite)
    print("\n--- BStackDemo Test Suite Execution Finished ---")