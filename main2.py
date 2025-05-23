from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://cris.utec.edu.pe/es/persons/")
time.sleep(5)  # espera a que cargue el JS

# Obtener todos los perfiles visibles
profile_links = driver.find_elements(By.CSS_SELECTOR, '.list-result-item .title a')
urls = [link.get_attribute('href') for link in profile_links]

data = []

for url in urls:
    driver.get(url)
    time.sleep(2)

    try:
        name = driver.find_element(By.TAG_NAME, 'h1').text.strip()

        try:
            email = driver.find_element(By.PARTIAL_LINK_TEXT, '@utec.edu.pe').text.strip()
        except:
            email = 'No disponible'

        try:
            department = driver.find_element(By.XPATH, "//dt[text()='Departamento académico']/following-sibling::dd[1]").text.strip()
        except:
            department = 'No disponible'

        try:
            areas = driver.find_element(By.XPATH, "//dt[text()='Palabras clave']/following-sibling::dd[1]").text.strip()
        except:
            areas = 'No disponible'

        data.append({
            "ProfessorID": email,
            "Name": name,
            "Department": department,
            "ResearchAreas": areas
        })
        print(f"✓ {name}")

    except Exception as e:
        print(f"Error leyendo {url}: {e}")

driver.quit()

# Guardar como CSV
df = pd.DataFrame(data)
df.to_csv("profesores_utec.csv", index=False, encoding='utf-8-sig')
print("✅ Datos guardados en 'profesores_utec.csv'")
