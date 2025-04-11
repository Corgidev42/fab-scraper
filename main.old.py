import subprocess
import sys

# === Auto-installation des modules requis ===
required_modules = ['selenium', 'beautifulsoup4', 'requests']

for module in required_modules:
	try:
		__import__(module if module != 'beautifulsoup4' else 'bs4')
	except ImportError:
		print(f"📦 Module manquant : {module} → installation...")
		subprocess.check_call([sys.executable, "-m", "pip", "install", module])


import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# === Vérification des arguments ===
if len(sys.argv) < 2:
	print("❌ Utilisation : python main.py <URL>")
	sys.exit(1)

url = sys.argv[1]
delay = 5  # secondes pour attendre le JS

# === Setup de Selenium headless ===
options = Options()
options.headless = True
print("🚀 Lancement de Chrome...")
driver = webdriver.Chrome(options=options)

print(f"🌐 Ouverture de l'URL : {url}")
driver.get(url)
print(f"⏳ Attente de {delay} secondes pour chargement JS...")
time.sleep(delay)

# === Analyse de la page ===
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

img_tags = soup.find_all('img', class_='css-1ur2xev')
print(f"📸 {len(img_tags)} image(s) trouvée(s).")

if not img_tags:
	print("❌ Aucune image détectée. Vérifie le chargement ou le sélecteur CSS.")
	sys.exit(1)

# === Dossier basé sur la première carte ===
first_alt = img_tags[0].get('alt', 'deck_sans_nom')
folder_name = first_alt.replace(" ", "_").replace(",", "").replace("'", "").replace("/", "-")
os.makedirs(folder_name, exist_ok=True)
print(f"📂 Dossier de sortie : {folder_name}")

# === Téléchargement des images ===
for img in img_tags:
	img_url = img.get('src')
	alt = img.get('alt', 'image_sans_nom')

	if not img_url:
		continue

	# Nettoyage du nom de fichier
	base_filename = alt.replace(" ", "_").replace(",", "").replace("'", "").replace("/", "-")
	extension = img_url.split('.')[-1].split('?')[0]
	filepath = f"{folder_name}/{base_filename}.{extension}"

	# Gestion des doublons : ajout d'un suffixe si le fichier existe
	counter = 1
	while os.path.exists(filepath):
		filepath = f"{folder_name}/{base_filename}-{counter}.{extension}"
		counter += 1

	try:
		img_data = requests.get(img_url).content
		with open(filepath, 'wb') as f:
			f.write(img_data)
		print(f"✅ Téléchargée : {filepath}")
	except Exception as e:
		print(f"❌ Erreur pour {img_url} : {e}")
