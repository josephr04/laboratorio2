from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
import time 

# ========== CONFIGURACIÓN PARA EVITAR POPUP ==========
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Modo incógnito
chrome_options.add_argument("--disable-features=PasswordImport")
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

# Configuración inicial 
driver = webdriver.Chrome(options=chrome_options) 
driver.implicitly_wait(10) 

def ejecutar_pruebas(): 
    try: 
        # --- CASO 1: Login Exitoso --- 
        print("Ejecutando Caso 1: Login...") 
        driver.get("https://www.saucedemo.com") 
        driver.find_element(By.ID, "user-name").send_keys("standard_user") 
        driver.find_element(By.ID, "password").send_keys("secret_sauce") 
        driver.find_element(By.ID, "login-button").click() 
         
        assert "inventory.html" in driver.current_url 
        print("✅ Caso 1 completado con éxito.") 
        driver.save_screenshot("caso1_login_exitoso.png")

        # --- CASO 2: Agregar al Carrito --- 
        print("Ejecutando Caso 2: Agregar producto...") 
        boton_agregar = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack") 
        boton_agregar.click() 
         
        badge_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text 
        assert badge_carrito == "1" 
        print("✅ Caso 2 completado con éxito.") 
        driver.save_screenshot("caso2_carrito.png")

        # --- CASO 3: Login Fallido (Usuario Bloqueado) --- 
        print("Ejecutando Caso 3: Login fallido...") 
        driver.delete_all_cookies() 
        driver.get("https://www.saucedemo.com") 
        
        time.sleep(1)
         
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user") 
        driver.find_element(By.ID, "password").send_keys("secret_sauce") 
        driver.find_element(By.ID, "login-button").click() 
        
        time.sleep(2)
        
        error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text 
        assert "locked out" in error_msg.lower() 
        print("✅ Caso 3 completado con éxito.") 
        driver.save_screenshot("caso3_login_fallido.png")
        
        print("\n" + "="*40)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*40)

    except Exception as e: 
        print(f"❌ Error durante la ejecución: {e}")
        driver.save_screenshot("error.png")
    
    finally: 
        driver.quit() 

if __name__ == "__main__": 
    ejecutar_pruebas()