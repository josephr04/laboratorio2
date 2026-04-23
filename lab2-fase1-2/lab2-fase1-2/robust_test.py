from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options

# ========== CONFIGURACIÓN PARA EVITAR POPUP ==========
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Modo incógnito
chrome_options.add_argument("--disable-features=PasswordImport")
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

# ========== CONFIGURACIÓN DEL DRIVER ==========
driver = webdriver.Chrome(options=chrome_options) 
wait = WebDriverWait(driver, 10) 

try: 
    # ========== CASO 1: Login Seguro ==========
    print("\n[CASO 1] Ejecutando Login exitoso...")
    driver.get("https://www.saucedemo.com") 
    
    # Esperamos a que el campo de usuario sea visible antes de escribir
    user_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name"))) 
    user_input.send_keys("standard_user") 
    driver.find_element(By.ID, "password").send_keys("secret_sauce") 
    driver.find_element(By.ID, "login-button").click() 
    
    # Verificamos que se cargó el inventario
    wait.until(EC.url_contains("inventory.html"))
    print("✅ CASO 1 completado con éxito.")
    driver.save_screenshot("robust_caso1.png")

    # ========== CASO 2: Agregar al Carrito ==========
    print("\n[CASO 2] Ejecutando Agregar producto...")
    
    # Esperamos a que el botón sea "clicable"
    btn_add = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))) 
    btn_add.click() 
    
    # Verificamos que el contador del carrito aparezca
    badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))) 
    assert badge.text == "1"
    print(f"✅ CASO 2 completado: Carrito tiene {badge.text} producto(s).")
    driver.save_screenshot("robust_caso2.png")

    # ========== CASO 3: Validación de Error de Bloqueo ==========
    print("\n[CASO 3] Ejecutando Login fallido...")
    driver.get("https://www.saucedemo.com") 
    
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user") 
    driver.find_element(By.ID, "password").send_keys("secret_sauce") 
    driver.find_element(By.ID, "login-button").click() 
    
    # Esperamos a que el mensaje de error sea visible
    error_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))) 
    assert "locked out" in error_container.text.lower()
    print(f"✅ CASO 3 completado: {error_container.text}")
    driver.save_screenshot("robust_caso3.png")
    
    print("\n" + "="*50)
    print("✅ ROBUST TEST - 3/3 PRUEBAS EXITOSAS")
    print("="*50)

except Exception as e:
    print(f"\n❌ Error: {e}")
    driver.save_screenshot("robust_error.png")

finally: 
    driver.quit()