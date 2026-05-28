from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import time


class LoginPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            60
        )

    # =========================
    # OPEN SWAGGER
    # =========================

    def open_swagger(self):

        self.driver.get(
            "https://fastapi-task-manager-lt6l.onrender.com/docs"
        )

    # =========================
    # LOGIN AUTOMATION
    # =========================

    def login(self):

        # Wait Swagger UI
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "swagger-ui"
                )
            )
        )

        # Expand login
        login_section = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(text(),'/login')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            login_section
        )

        # Try it out
        try_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "(//button[contains(text(),'Try it out')])[1]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            try_button
        )

        # Textarea
        textarea = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.TAG_NAME,
                    "textarea"
                )
            )
        )

        textarea.clear()

        login_payload = '''
{
  "email": "admin@test.com",
  "password": "123456"
}
'''

        textarea.send_keys(
            login_payload
        )

        # Execute
        execute_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(text(),'Execute')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            execute_button
        )

        time.sleep(5)

    # =========================
    # VALIDATE RESPONSE
    # =========================

    def verify_login_success(self):

        response = self.driver.page_source

        assert "Login Successful" in response
        #assert "INVALID_TEXT" in response