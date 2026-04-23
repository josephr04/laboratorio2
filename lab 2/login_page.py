# Importamos 'By' para poder localizar elementos en el HTML (por ID, CSS, etc.)
from selenium.webdriver.common.by import By 
# Importamos 'WebDriverWait' para manejar esperas explícitas y no saturar el navegador
from selenium.webdriver.support.ui import WebDriverWait 
# Importamos 'expected_conditions' para definir qué evento estamos esperando (que algo sea visible, por ejemplo)
from selenium.webdriver.support import expected_conditions as EC 

class LoginPage: 
    def __init__(self, driver): 
        """Constructor de la clase: Inicializa el driver y las esperas"""
        self.driver = driver 
        # Configuramos una espera máxima de 10 segundos para elementos dinámicos
        self.wait = WebDriverWait(driver, 10) 
        
        # --- SECCIÓN DE SELECTORES (LOCATORS) ---
        # Definimos las rutas a los elementos aquí para que, si la web cambia, solo editemos esta parte.
        self.username_field = (By.ID, "user-name") 
        self.password_field = (By.ID, "password") 
        self.login_button = (By.ID, "login-button") 
        # Usamos CSS_SELECTOR para capturar el atributo personalizado 'data-test' de SauceDemo
        self.error_msg = (By.CSS_SELECTOR, "[data-test='error']")

    def ingresar_credenciales(self, usuario, password): 
        """Acción: Escribe el nombre de usuario y la contraseña"""
        # Esperamos a que el campo de usuario sea visible antes de escribir
        self.wait.until(EC.visibility_of_element_located(self.username_field)).send_keys(usuario) 
        # Localizamos el campo de contraseña y enviamos el texto
        self.driver.find_element(*self.password_field).send_keys(password) 

    def click_login(self): 
        """Acción: Hace clic en el botón de ingresar"""
        # El '*' desempaqueta la tupla (By.ID, "login-button") para que find_element la entienda
        self.driver.find_element(*self.login_button).click() 

    def obtener_error(self): 
        """Acción: Captura y devuelve el texto del mensaje de error si aparece"""
        # Esperamos a que el mensaje de error sea visible y extraemos su texto
        return self.wait.until(EC.visibility_of_element_located(self.error_msg)).text