import pytest
from datetime import datetime

# Este es un "Hook" (gancho) de Pytest. Se ejecuta automáticamente para reportar el estado de cada prueba.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 'yield' permite que la prueba se ejecute primero antes de que este código continúe.
    outcome = yield
    # Obtenemos el resultado final de la ejecución (si pasó, falló o saltó).
    report = outcome.get_result()

    # 'report.when == call' significa que el error ocurrió durante la ejecución del test (no en la configuración inicial).
    # 'report.failed' confirma que la prueba falló (el assert fue falso o hubo un error).
    if report.when == 'call' and report.failed:
        
        # 'item.funcargs' es un diccionario que contiene los argumentos de la función de prueba.
        # Aquí intentamos extraer el 'driver' que definiste en tu fixture.
        driver = item.funcargs.get('driver')
        
        if driver:
            # Generamos una estampa de tiempo (año-mes-día_hora-minuto-segundo) 
            # para que cada captura tenga un nombre único y no se sobrescriban.
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            
            # El nombre del archivo incluirá el nombre del test fallido (head_line) y la fecha/hora.
            file_name = f"error_{report.head_line}_{now}.png".replace(" ", "_")
            
            # Ordenamos a Selenium que guarde la imagen de lo que está viendo en ese instante.
            driver.save_screenshot(file_name)
            
            # Imprimimos en la consola para saber que la captura se generó con éxito.
            print(f"\n[ERROR DETECTADO] Captura de pantalla guardada: {file_name}")