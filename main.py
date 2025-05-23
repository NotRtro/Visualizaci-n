import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://cris.utec.edu.pe"
people_url = f"{base_url}/es/persons/"
headers = {"User-Agent": "Mozilla/5.0"}

# Lista para almacenar los datos
data = []

def extract_profile_data(profile_url):
    """Extrae datos de un perfil individual"""
    res = requests.get(profile_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    name = soup.find('h1').text.strip()
    
    # Email
    email_tag = soup.find('a', href=lambda x: x and 'mailto:' in x)
    email = email_tag.text.strip() if email_tag else 'No disponible'
    
    # Departamento
    department = 'No disponible'
    department_tag = soup.find('dt', string='Departamento académico')
    if department_tag:
        department = department_tag.find_next_sibling('dd').text.strip()

    # Áreas de investigación
    research_areas = []
    interests_tag = soup.find('dt', string='Palabras clave')
    if interests_tag:
        research_areas = [tag.strip() for tag in interests_tag.find_next_sibling('dd').text.split(',')]

    return {
        "ProfessorID": email,
        "Name": name,
        "Department": department,
        "ResearchAreas": "; ".join(research_areas)
    }

# Página principal
response = requests.get(people_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Obtener todos los enlaces de perfiles
profile_links = soup.select('.grid-item a[href^="/es/persons/"]')
profile_urls = list({base_url + a['href'] for a in profile_links})  # usar set para evitar duplicados

# Recorrer cada perfil y extraer información
print(f"Encontrados {len(profile_urls)} perfiles. Extrayendo información...")

for url in profile_urls:
    try:
        person = extract_profile_data(url)
        data.append(person)
        print(f"✓ {person['Name']}")
        time.sleep(1)  # para evitar ser bloqueado por demasiadas peticiones rápidas
    except Exception as e:
        print(f"Error procesando {url}: {e}")

# Guardar en CSV
df = pd.DataFrame(data)
df.to_csv("profesores_utec.csv", index=False, encoding='utf-8-sig')
print("✅ Datos guardados en 'profesores_utec.csv'")
