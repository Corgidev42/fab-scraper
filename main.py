import subprocess
import sys

# === Auto-installation des modules requis ===
required_modules = ['selenium', 'beautifulsoup4', 'requests', 'Pillow']

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
from PIL import Image

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

	# Gestion des doublons
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

# === Traitement impression : CMJN + fond perdu + gabarit fixe ===
def prepare_images_for_print(folder):
	from PIL import Image

	# Gabarit final avec bleed inclus (816x1110 px à 300 DPI)
	dpi = 300
	width_mm, height_mm = 69, 94  # 63x88 + 3mm de chaque côté
	final_width = int(width_mm / 25.4 * dpi)   # 816 px
	final_height = int(height_mm / 25.4 * dpi) # 1110 px
	content_width = int(63 / 25.4 * dpi)       # 744 px
	content_height = int(88 / 25.4 * dpi)      # 1039 px
	bleed = int(3 / 25.4 * dpi)                # 35 px

	output_suffix = "_print_ready"
	output_format = "TIFF"

	print(f"\n🖨️  Preparing images for print...")
	print(f"📐 Each image will be resized to: {final_width}x{final_height} px (69x94 mm @ 300 DPI)")

	for filename in os.listdir(folder):
		if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
			original_path = os.path.join(folder, filename)
			try:
				img = Image.open(original_path).convert("RGB")

				# Resize to content area: 744x1039 px
				resized = img.resize((content_width, content_height), Image.LANCZOS)

				# Create blank canvas with full bleed size: 816x1110 px
				final_img = Image.new("RGB", (final_width, final_height), (255, 255, 255))
				final_img.paste(resized, (bleed, bleed))

				# Convert to CMYK
				cmyk_img = final_img.convert("CMYK")

				# Save
				output_name = os.path.splitext(filename)[0] + output_suffix + ".tif"
				output_path = os.path.join(folder, output_name)
				cmyk_img.save(output_path, output_format, dpi=(dpi, dpi))
				print(f"🟢 Ready for print: {output_name}")
			except Exception as e:
				print(f"❌ Error processing {filename}: {e}")

prepare_images_for_print(folder_name)

# === Génération PDF final ===
def export_images_to_pdf(folder):
	print(f"\n📄 Création du PDF d'impression...")
	tiff_files = sorted([
		f for f in os.listdir(folder)
		if f.lower().endswith("_print_ready.tif")
	])

	if not tiff_files:
		print("⚠️ Aucune image print-ready trouvée.")
		return

	first_image = Image.open(os.path.join(folder, tiff_files[0]))
	other_images = [Image.open(os.path.join(folder, f)) for f in tiff_files[1:]]

	pdf_path = os.path.join(folder, f"{folder}_print.pdf")
	first_image.save(pdf_path, "PDF", save_all=True, append_images=other_images)
	print(f"✅ PDF final prêt : {pdf_path}")

export_images_to_pdf(folder_name)
