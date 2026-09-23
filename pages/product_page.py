from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def add_product_to_basket(self):
        self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON).click()

    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def should_be_basket_total_equal_to_price(self, product_price):
        basket_total = self.browser.find_element(*ProductPageLocators.BASKET_TOTAL_MESSAGE).text
        assert basket_total == product_price, \
            f"Basket total is {basket_total}, expected {product_price}"

    def should_be_product_name_in_success_message(self, product_name):
        name_in_message = self.browser.find_element(*ProductPageLocators.SUCCESS_MESSAGE).text
        assert name_in_message == product_name, \
            f"Product name in message is '{name_in_message}', expected '{product_name}'"

    def should_disappear_success_message(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is still presented, but should disappear"

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is presented, but should not be"
