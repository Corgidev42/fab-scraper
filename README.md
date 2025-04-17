# 🕷 Fabrary Image Scraper - Web Scraping with Selenium

## 📌 Description

**Fabrary Image Scraper** is a lightweight Python tool that extracts all card images from a **Fabrary.net deck page**.

It uses **Selenium** to fully render the page (since images are loaded via JavaScript), then scrapes all `<img>` elements with a specific class and downloads them locally.

Duplicate images are **allowed** and automatically renamed to avoid conflicts.
All images are stored in a folder named after the **first card detected** on the page.

---

## 🎮 Features

-   ⚙️ **JavaScript rendering** handled via Chrome and Selenium
-   📸 **Targeted image scraping** (via CSS class `.css-1ur2xev`)
-   🔁 **Duplicate-friendly** (auto-renamed with suffixes)
-   🖨️ **Print-ready export** (300 DPI, 69×94 mm with 3mm bleed, CMYK `.tif`)
-   📄 **Deck PDF creation** (one page per card)
-   🎨 **Color boost options** (vivid, ultra-vivid) for better print results
-   🧼 **Interactive cleanup prompt** after generation
-   📁 **Clean directory structure** based on the first card’s name
-   🐍 **Automatic dependency installation** (if not already installed)
-   🔧 **Makefile support** for easy automation (venv, install, run)

---

## 🛠 Requirements

- Python 3
- Google Chrome installed
- [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) matching your Chrome version, placed in `/usr/local/bin/` or accessible globally

---

## ▶️ Running the script (manual method)

```bash
python main.py "https://fabrary.net/decks/..." [vivid|ultra-vivid]
```

- If no boost option is given, the images are processed normally.
- Adding vivid will enhance color saturation, contrast, and brightness moderately.
- Adding ultra-vivid will apply a strong color boost for very vivid prints.

The script will automatically create a folder using the name of the first card found, download all images, generate print-ready .tif files, and compile a PDF.

---

### 💡 Example

If the first card found is `Death Touch`, you’ll get:

```
./Death_Touch/Death_Touch.webp
./Death_Touch/Infecting_Shot.webp
./Death_Touch/Death_Touch_print_ready.tif
./Death_Touch/Death_Touch_print.pdf
...
```

---

## 🖨️ Print Output Format

Each card is converted to:

- 63 mm × 88 mm **trimmed card**
- +3 mm **bleed** on each side → total **69 mm × 94 mm**
- Exported as **816×1110 px @ 300 DPI**, **CMYK TIFF**

### Print Zones

| Zone              | Millimeters       | Pixels (@300 DPI)   | Description                      |
|-------------------|-------------------|----------------------|----------------------------------|
| Safe zone         | 57 × 82 mm        | 674 × 968 px         | Text and core elements           |
| Trimmed size      | 63 × 88 mm        | 744 × 1039 px        | Final visible card size          |
| Full bleed area   | **69 × 94 mm**    | **816 × 1110 px**    | Printed area before cutting ✅   |
| Bleed per side    | 3 mm              | ~35 px               | Extra margin to avoid white edge |

---

## 🧼 Cleanup Options (interactive)

After the PDF is created, the script will ask:

```
❓ What do you want to delete? [a/o/n]
a → Delete ALL (TIFF + original webp/jpg)
o → Delete only TIFFs
n → Keep everything
```

This ensures you can keep the assets you want without accidentally deleting them.

---

## 🔁 Run with Makefile (recommended)

A `Makefile` is provided to handle:
- Virtual environment creation
- Python dependencies installation
- Script execution with arguments

### ✅ Example usage:

```bash
make run URL="https://fabrary.net/decks/..."
make run URL="https://fabrary.net/decks/..." BOOST=vivid
make run URL="https://fabrary.net/decks/..." BOOST=ultra-vivid
```

If you want boosted colors for print, simply add BOOST=vivid or BOOST=ultra-vivid as a parameter.


---

## 📂 Project Structure

```
fabrary-scraper/
├── main.py          # Main scraper script
├── Makefile         # Automation (venv, install, run)
├── .gitignore       # Excludes .venv, __pycache__, etc.
├── README.md        # Project documentation
└── .venv/           # Local Python environment (not tracked by Git)
```

---

## 📜 License & Disclaimer

This project is for personal and educational use only.
It is not affiliated with or endorsed by **Fabrary.net**.
Please respect copyright and scraping rules.

---

## 👤 Author

-   **Vincent B.** (`vbonnard.dev@gmail.com`)

---

## 🚀 Contributions

Feel free to fork, improve, or adapt the project for other websites or use cases.
Pull requests and ideas are welcome!
