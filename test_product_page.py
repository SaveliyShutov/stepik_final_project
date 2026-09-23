import time

import pytest

from .pages.basket_page import BasketPage
from .pages.login_page import LoginPage
from .pages.product_page import ProductPage

PRODUCT_LINK = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
PROMO_LINK = PRODUCT_LINK + "?promo=offer{}"
LOGIN_LINK = "http://selenium1py.pythonanywhere.com/accounts/login/"
BUGGED_OFFER = 7


@pytest.mark.need_review
@pytest.mark.parametrize("link", [
    PROMO_LINK.format(number) if number != BUGGED_OFFER
    else pytest.param(PROMO_LINK.format(number), marks=pytest.mark.xfail(reason="wrong product name in message"))
    for number in range(10)
])
def test_guest_can_add_product_to_basket(browser, link):
    page = ProductPage(browser, link)
    page.open()
    product_name = page.get_product_name()
    product_price = page.get_product_price()
    page.add_product_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_product_name_in_success_message(product_name)
    page.should_be_basket_total_equal_to_price(product_price)


@pytest.mark.xfail(reason="success message is shown after adding product")
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.add_product_to_basket()
    page.should_not_be_success_message()


def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.should_not_be_success_message()


@pytest.mark.xfail(reason="success message does not disappear")
def test_message_disappeared_after_adding_product_to_basket(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.add_product_to_basket()
    page.should_disappear_success_message()


def test_guest_should_see_login_link_on_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.should_be_login_link()


@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_not_be_items_in_basket()
    basket_page.should_be_empty_basket_text()


@pytest.mark.login
class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        email = str(time.time()) + "@fakemail.org"
        password = "Str0ngPassw0rd!" + str(int(time.time()))
        login_page = LoginPage(browser, LOGIN_LINK)
        login_page.open()
        login_page.register_new_user(email, password)
        login_page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser):
        page = ProductPage(browser, PRODUCT_LINK)
        page.open()
        page.should_not_be_success_message()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        page = ProductPage(browser, PRODUCT_LINK)
        page.open()
        product_name = page.get_product_name()
        product_price = page.get_product_price()
        page.add_product_to_basket()
        page.should_be_product_name_in_success_message(product_name)
        page.should_be_basket_total_equal_to_price(product_price)
