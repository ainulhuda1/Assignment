from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import traceback

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Step 1: Open the website
    driver.get("https://automationexercise.com/")
    driver.maximize_window()

    # Step 2: Verify homepage is visible successfully
    wait = WebDriverWait(driver, 20)  # Increased wait time
    homepage_logo = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='logo pull-left']")))
    assert homepage_logo.is_displayed(), "Homepage is not visible!"
    print("Test Passed: Homepage is visible.")

    # Step 3: Click 'View Product' for any product on the homepage
    view_product_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//a[contains(text(),'View Product')])[1]"))
    )  # Clicks on the first 'View Product' link
    view_product_button.click()

    # Step 4: Verify that the product details page opened
    product_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-information']/h2")))
    print(f"Test Passed: Product details page for '{product_title.text}' is displayed.")

    # Step 5: Verify product detail in the opened page
    assert product_title.is_displayed(), "Product title is not visible in the details page."
    print(f"Product '{product_title.text}' is visible in the details page.")

    # Step 6: Increase quantity to 4
    quantity_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='quantity']")))
    quantity_input.clear()
    quantity_input.send_keys("4")
    print("Quantity increased to 4.")

    # Step 7: Click 'Add to Cart' button
    add_to_cart_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='btn btn-default cart']"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button)  # Use JS to click in case it's not interactable
    print("Clicked 'Add to Cart'.")

    # Step 8: Click 'View Cart' button
    view_cart_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//u[contains(text(),'View Cart')]"))
    )
    view_cart_button.click()
    print("Clicked 'View Cart'.")

    # Step 9: Verify that the product is displayed in the cart page with the correct quantity
    cart_product_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[@class='cart_description']/p/a")))
    cart_quantity = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[@class='cart_quantity']/input")))

    assert cart_product_title.text.strip().lower() == product_title.text.strip().lower(), "Product name in cart is incorrect."
    assert cart_quantity.get_attribute("value") == "4", "Quantity in cart is not 4."
    print("Test Passed: Product and quantity verified in cart.")

except Exception as e:
    print(f"Test Failed: {str(e)}")
    traceback.print_exc()  # This will print the full error stack trace for better diagnosis
    driver.save_screenshot('screenshot.png')  # Save screenshot for inspection
    print(driver.page_source)  # Print page source for debugging

finally:
    # Close the browser
    driver.quit()
