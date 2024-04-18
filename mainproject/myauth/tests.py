
# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# class LoginTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def test_successful_login(self):
#         self.driver.get('http://127.0.0.1:8000/myauth/login/')
#         username_input = self.driver.find_element(By.ID, 'email')
#         password_input = self.driver.find_element(By.ID, 'password')

#         # Replace 'valid_username' and 'valid_password' with actual credentials
#         username_input.send_keys('roshangeorge2024b@mca.ajce.in')
#         password_input.send_keys('Pranav@2002')

#         login_button = self.driver.find_element(By.ID, 'submit')
#         login_button.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Check if redirected to the ownerpage
#         self.assertIn('http://127.0.0.1:8000/myauth/delivery_login/', self.driver.current_url.lower())





# add to cart
# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def test_successful_login(self):
#         self.driver.get('http://127.0.0.1:8000/myauth/login/')
#         username_input = self.driver.find_element(By.ID, 'email')
#         password_input = self.driver.find_element(By.ID, 'password')

#         # Replace 'valid_username' and 'valid_password' with actual credentials
#         username_input.send_keys('pranavpk2024b@mca.ajce.in')
#         password_input.send_keys('pRANAV@2002')

#         login_button = self.driver.find_element(By.ID, 'submit')
#         login_button.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Check if redirected to the owner page
#         self.assertIn('http://127.0.0.1:8000/myauth/home/', self.driver.current_url.lower())

#         # Click on the "All Collections" link
#         all_collections_link = self.driver.find_element(By.XPATH, "//a[contains(text(),'All Collections')]")
#         all_collections_link.click()
#         time.sleep(2)  # Adjust the time as needed
#         self.assertIn('http://127.0.0.1:8000/myauth/productallview/', self.driver.current_url.lower())

#         # Scroll to the "Add to Cart" button
#         add_to_cart_button = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//a[contains(@class,'btn-wishlist') and contains(text(),'Add to Cart')]"))
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView();", add_to_cart_button)

#         # Click on the "Add to Cart" button using JavaScript
#         self.driver.execute_script("arguments[0].click();", add_to_cart_button)

#         # Wait for the cart page to load
#         WebDriverWait(self.driver, 10).until(
#             EC.url_contains('http://127.0.0.1:8000/myauth/view_cart/')
#         )
#         time.sleep(2)  # Adjust the time as needed


#         # Assert that the cart page URL is loaded
#         self.assertIn('http://127.0.0.1:8000/myauth/view_cart/', self.driver.current_url.lower())

#         # You can add assertions or further actions here if needed


# if __name__ == "__main__":
#     unittest.main()





# not corrected
# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains

# class LoginTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def test_successful_login(self):
#         self.driver.get('http://127.0.0.1:8000/myauth/login/')
#         username_input = self.driver.find_element(By.ID, 'email')
#         password_input = self.driver.find_element(By.ID, 'password')

#         # Replace 'valid_username' and 'valid_password' with actual credentials
#         username_input.send_keys('pranavpk2024b@mca.ajce.in')
#         password_input.send_keys('pRANAV@2002')

#         login_button = self.driver.find_element(By.ID, 'submit')
#         login_button.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Check if redirected to the home page
#         self.assertIn('http://127.0.0.1:8000/myauth/home/', self.driver.current_url.lower())

#         # Click on the customer icon
#         customer_icon = self.driver.find_element(By.XPATH, "//a[@href='/myauth/customer/']")
#         customer_icon.click()

#         # Wait for the customer page to load
#         WebDriverWait(self.driver, 10).until(
#             EC.url_contains('http://127.0.0.1:8000/myauth/customer/')
#         )

#         time.sleep(2)  # Adjust the time as needed

#         # Assert that the customer page URL is loaded
#         self.assertIn('http://127.0.0.1:8000/myauth/customer/', self.driver.current_url.lower())

#         # Click on the "View Wallet" link
#         view_wallet_link = self.driver.find_element(By.XPATH, "//a[@href='/myauth/wallet/update/']")
        
#         # Scroll the element into view
#         actions = ActionChains(self.driver)
#         actions.move_to_element(view_wallet_link).perform()
        
#         view_wallet_link.click()

#         # Wait for the wallet update page to load
#         WebDriverWait(self.driver, 10).until(
#             EC.url_contains('http://127.0.0.1:8000/myauth/wallet/update/')
#         )

#         time.sleep(2)  # Adjust the time as needed

#         # Assert that the wallet update page URL is loaded
#         self.assertIn('http://127.0.0.1:8000/myauth/wallet/update/', self.driver.current_url.lower())

#         amount_input = self.driver.find_element(By.ID, 'balance')
#         amount_input.send_keys('100')  # You can replace '100' with the desired amount

#         # Click on the "Update Wallet" button
#         update_wallet_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
#         update_wallet_button.click()
#         time.sleep(2)  # Adjust the time as needed


#         # You can add assertions or further actions here if needed

# if __name__ == "__main__":
#     unittest.main()



#wallet payment

# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def test_successful_login(self):
#         self.driver.get('http://127.0.0.1:8000/myauth/login/')
#         username_input = self.driver.find_element(By.ID, 'email')
#         password_input = self.driver.find_element(By.ID, 'password')

#         # Replace 'valid_username' and 'valid_password' with actual credentials
#         username_input.send_keys('pranavpk2024b@mca.ajce.in')
#         password_input.send_keys('pRANAV@2002')

#         login_button = self.driver.find_element(By.ID, 'submit')
#         login_button.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Check if redirected to the owner page
#         self.assertIn('http://127.0.0.1:8000/myauth/home/', self.driver.current_url.lower())

#         # Click on the "All Collections" link
#         all_collections_link = self.driver.find_element(By.XPATH, "//a[contains(text(),'All Collections')]")
#         all_collections_link.click()
#         time.sleep(2)  # Adjust the time as needed
#         self.assertIn('http://127.0.0.1:8000/myauth/productallview/', self.driver.current_url.lower())

#         # Scroll to the "Add to Cart" button
#         add_to_cart_button = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//a[contains(@class,'btn-wishlist') and contains(text(),'Add to Cart')]"))
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView();", add_to_cart_button)

#         # Click on the "Add to Cart" button using JavaScript
#         self.driver.execute_script("arguments[0].click();", add_to_cart_button)

#         # Wait for the cart page to load
#         WebDriverWait(self.driver, 10).until(
#             EC.url_contains('http://127.0.0.1:8000/myauth/view_cart/')
#         )
#         time.sleep(2)  # Adjust the time as needed

#         # Assert that the cart page URL is loaded
#         self.assertIn('http://127.0.0.1:8000/myauth/view_cart/', self.driver.current_url.lower())

#         # Scroll to the "Checkout" button
#         checkout_button = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CLASS_NAME, 'checkout-btn'))
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView();", checkout_button)

#         # Click on the "Checkout" button using JavaScript
#         self.driver.execute_script("arguments[0].click();", checkout_button)

#         # Wait for the checkout page to load
#         WebDriverWait(self.driver, 10).until(
#             EC.url_contains('http://127.0.0.1:8000/myauth/checkout/')
#         )
#         time.sleep(2)  # Adjust the time as needed

#         # Assert that the checkout page URL is loaded
#         self.assertIn('http://127.0.0.1:8000/myauth/checkout/', self.driver.current_url.lower())

#         # Click on the checkbox to use wallet
#         use_wallet_checkbox = self.driver.find_element(By.ID, 'use-wallet-checkbox')
#         use_wallet_checkbox.click()

#         # Scroll to the "Checkout Wallet" button
#         checkout_wallet_button = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.ID, 'wallet-link'))
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView();", checkout_wallet_button)
#         time.sleep(2)  # Adjust the time as needed


#         # Click on the "Checkout Wallet" button using JavaScript
#         self.driver.execute_script("arguments[0].click();", checkout_wallet_button)
#         time.sleep(2)  # Adjust the time as needed
#         self.assertIn('http://127.0.0.1:8000/myauth/wallet/payment/success/', self.driver.current_url.lower())


#         # You can add assertions or further actions here if needed

# if __name__ == "__main__":
#     unittest.main()




#update   stock

# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# class LoginTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def test_successful_login(self):
#         self.driver.get('http://127.0.0.1:8000/myauth/login/')
#         username_input = self.driver.find_element(By.ID, 'email')
#         password_input = self.driver.find_element(By.ID, 'password')

#         # Replace 'valid_username' and 'valid_password' with actual credentials
#         username_input.send_keys('prxnv2832@gmail.com')
#         password_input.send_keys('Pranav@2002')

#         login_button = self.driver.find_element(By.ID, 'submit')
#         login_button.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Check if redirected to the ownerpage
#         self.assertIn('http://127.0.0.1:8000/myauth/seller_dashboard/', self.driver.current_url.lower())

#         # Click on "Products Details"
#         products_details_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Products Details')]")
#         products_details_link.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Click on "Update Stock"
#         update_stock_link = self.driver.find_element(By.XPATH, "//a[@href='http://127.0.0.1:8000/myauth/seller_prodview/']")
#         update_stock_link.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Assert if redirected to the update stock page
#         self.assertIn('http://127.0.0.1:8000/myauth/seller_prodview/', self.driver.current_url.lower())

#         # Input values into the "Stock" field
#         stock_input = self.driver.find_element(By.NAME, 'stock')
#         stock_input.clear()  # Clear any existing value
#         stock_input.send_keys('100')  # Input desired stock value

#         # Click the "Update" button
#         update_button = self.driver.find_element(By.CLASS_NAME, 'button_upd')
#         update_button.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Assuming you want to assert something after updating, you can add assertions here

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()








#delivery_activation_not_complete
# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def test_successful_login(self):
#         self.driver.get('http://127.0.0.1:8000/myauth/login/')
#         username_input = self.driver.find_element(By.ID, 'email')
#         password_input = self.driver.find_element(By.ID, 'password')

#         # Replace 'valid_username' and 'valid_password' with actual credentials
#         username_input.send_keys('pranavpk672@gmail.com')
#         password_input.send_keys('Pranav@2002')

#         login_button = self.driver.find_element(By.ID, 'submit')
#         login_button.click()

#         time.sleep(2)  # Adjust the time as needed

#         # Check if redirected to the ownerpage
#         self.assertIn('http://127.0.0.1:8000/myauth/adminreg/', self.driver.current_url.lower())

#         # Click on the "View Deliveryboy Details" link
#         deliveryboy_details_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="View Deliveryboy Details"]')))
#         deliveryboy_details_link.click()
#         time.sleep(2)  # Adjust the time as needed

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()









#add to wishlist
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_successful_login(self):
        self.driver.get('http://127.0.0.1:8000/myauth/login/')
        username_input = self.driver.find_element(By.ID, 'email')
        password_input = self.driver.find_element(By.ID, 'password')

        # Replace 'valid_username' and 'valid_password' with actual credentials
        username_input.send_keys('pranavpk2024b@mca.ajce.in')
        password_input.send_keys('pRANAV@2002')

        login_button = self.driver.find_element(By.ID, 'submit')
        login_button.click()

        time.sleep(2)  # Adjust the time as needed

        # Check if redirected to the owner page
        self.assertIn('http://127.0.0.1:8000/myauth/home/', self.driver.current_url.lower())

        # Click on the "All Collections" link
        all_collections_link = self.driver.find_element(By.XPATH, "//a[contains(text(),'All Collections')]")
        all_collections_link.click()
        time.sleep(2)  # Adjust the time as needed
        self.assertIn('http://127.0.0.1:8000/myauth/productallview/', self.driver.current_url.lower())

        # Scroll to the "Add to Wishlist" button
        add_to_wishlist_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@class,'btn-wishlist') and contains(text(),'Add to Wishlist')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", add_to_wishlist_button)

        # Click on the "Add to Wishlist" button using JavaScript
        self.driver.execute_script("arguments[0].click();", add_to_wishlist_button)

        # Wait for the wishlist page to load
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('http://127.0.0.1:8000/myauth/view_wishlist/')
        )
        time.sleep(2)  # Adjust the time as needed

        # Assert that the wishlist page URL is loaded
        self.assertIn('http://127.0.0.1:8000/myauth/view_wishlist/', self.driver.current_url.lower())

        # You can add assertions or further actions here if needed


if __name__ == "__main__":
    unittest.main()
