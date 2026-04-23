from selenium import webdriver
from login_page import LoginPage # Importamos nuestra clase

def test_ejecucion_pom():
   
    driver = webdriver.Chrome() 
    driver.get("https://saucedemo.com") 
    
    # Instanciamos la página 
    login = LoginPage(driver) 
    
    # Caso de Uso: Login Fallido 
    print("Ejecutando prueba de Login con usuario bloqueado...")
    login.ingresar_credenciales("locked_out_user", "secret_sauce") 
    login.click_login() 
    # Obtener y mostrar el resultado 
    mensaje = login.obtener_error() 
    print(f"Resultado de la prueba: {mensaje}")

    # Cerrar el navegador y limpiar recursos
    driver.quit() 

if __name__ == "__main__":
    test_ejecucion_pom() 