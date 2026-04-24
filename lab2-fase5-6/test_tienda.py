import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_page import LoginPage

BASE_URL = "https://www.saucedemo.com"


# ─────────────────────────────────────────────────────────────────────────────
# Test 1 – Login exitoso
# ─────────────────────────────────────────────────────────────────────────────
def test_login_exitoso(driver):
    """El usuario estándar debe llegar al inventario de productos."""
    driver.get(BASE_URL)
    login = LoginPage(driver)

    login.ingresar_credenciales("standard_user", "secret_sauce")
    login.click_login()

    assert "inventory.html" in driver.current_url, (
        f"Se esperaba llegar a inventory.html pero la URL fue: {driver.current_url}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Test 2 – Agregar producto al carrito
# ─────────────────────────────────────────────────────────────────────────────
def test_agregar_al_carrito(driver):
    """Tras el login, al agregar un producto el carrito debe mostrar '1'."""
    driver.get(BASE_URL)
    login = LoginPage(driver)
    login.ingresar_credenciales("standard_user", "secret_sauce")
    login.click_login()

    wait = WebDriverWait(driver, 10)

    # Esperar a que el botón sea clicable y hacer clic
    btn_add = wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    btn_add.click()

    # Verificar que el badge del carrito muestre "1"
    badge = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert badge.text == "1", f"Se esperaba '1' en el carrito pero se obtuvo: '{badge.text}'"


# ─────────────────────────────────────────────────────────────────────────────
# Test 3 – Login fallido (usuario bloqueado)
# ─────────────────────────────────────────────────────────────────────────────
def test_login_fallido(driver):
    """Un usuario bloqueado debe ver un mensaje de error."""
    driver.get(BASE_URL)
    login = LoginPage(driver)

    login.ingresar_credenciales("locked_out_user", "secret_sauce")
    login.click_login()

    error_text = login.obtener_error()
    assert "locked out" in error_text.lower(), (
        f"No se encontró el mensaje de bloqueo. Texto obtenido: '{error_text}'"
    )