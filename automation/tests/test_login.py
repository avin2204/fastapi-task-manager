from automation.pages.login_page import LoginPage


def test_swagger_login(driver):

    login_page = LoginPage(driver)

    login_page.open_swagger()

    login_page.login()

    login_page.verify_login_success()

    print(
        "\nSwagger Login Automation Successful 😎🔥"
    )