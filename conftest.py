import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# ─────────────────────────────────────────────────────────────────────────────
# FASE 5 – Hook: captura de pantalla automática cuando un test falla
# ─────────────────────────────────────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Se ejecuta después de cada test.
    Si el test FALLÓ, toma un screenshot y lo incrusta en el reporte HTML.
    """
    outcome = yield
    report  = outcome.get_result()
    extras  = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        # Obtener el driver desde la fixture del test
        driver = item.funcargs.get("driver")
        if driver:
            # Convertir la captura a base64 para incrustarla en el HTML
            screenshot = driver.get_screenshot_as_base64()
            html_img = (
                '<div>'
                f'<img src="data:image/png;base64,{screenshot}" '
                'alt="screenshot" '
                'style="width:600px; border:2px solid red; cursor:pointer;" '
                'onclick="window.open(this.src)" />'
                '</div>'
            )
            extras.append(pytest_html.extras.html(html_img))

    report.extra = extras


# ─────────────────────────────────────────────────────────────────────────────
# Fixture del navegador (compartida con todos los tests)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def driver():
    """
    Inicializa Chrome.
    - En local:      abre una ventana visible normal.
    - En CI/GitHub:  activa modo headless (sin pantalla física).
    El modo headless se activa automáticamente si existe la variable
    de entorno CI (GitHub Actions la define por defecto).
    """
    import os
    options = Options()

    if os.getenv("CI"):          # Variable que GitHub Actions define sola
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    options.add_argument("--disable-extensions")

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.maximize_window()

    yield chrome_driver          # Entrega el driver al test

    chrome_driver.quit()         # Limpieza al terminar