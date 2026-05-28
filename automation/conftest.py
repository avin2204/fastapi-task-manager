import pytest

import os

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver(request):

    # =========================
    # CHROME OPTIONS
    # =========================

    chrome_options = Options()

    chrome_options.add_argument(
        "--headless"
    )

    chrome_options.add_argument(
        "--disable-gpu"
    )

    chrome_options.add_argument(
        "--window-size=1920,1080"
    )

    chrome_options.add_argument(
        "--no-sandbox"
    )

    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )

    # =========================
    # CREATE DRIVER
    # =========================

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=chrome_options
    )

    driver.maximize_window()

    yield driver

    # =========================
    # SCREENSHOT ON FAILURE
    # =========================

    if request.node.rep_call.failed:

        screenshot_dir = (
            "automation/screenshots"
        )

        os.makedirs(
            screenshot_dir,
            exist_ok=True
        )

        screenshot_path = os.path.join(
            screenshot_dir,
            f"{request.node.name}.png"
        )

        driver.save_screenshot(
            screenshot_path
        )

        print(
            f"\nScreenshot saved: {screenshot_path}"
        )

    driver.quit()


# =========================
# PYTEST HOOK
# =========================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call
):

    outcome = yield

    rep = outcome.get_result()

    setattr(
        item,
        "rep_" + rep.when,
        rep
    )