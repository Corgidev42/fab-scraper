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
python main.py "https://fabrary.net/decks/..."
```

> The script will automatically create a folder using the name of the first card found, and store all downloaded images there.

---

### 💡 Example

If the first card found is `Death Touch`, you’ll get:

```
./Death_Touch/Death_Touch.webp
./Death_Touch/Infecting_Shot.webp
./Death_Touch/Death_Touch-1.webp
...
```

---

## 🔁 Run with Makefile (recommended)

A `Makefile` is provided to handle:
- Virtual environment creation
- Python dependencies installation
- Script execution with arguments

### ✅ Example usage:

```bash
make run URL="https://fabrary.net/decks/..."
```

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

## ⚙️ How it works

- All images are extracted from rendered HTML using BeautifulSoup
- Downloads are handled by `requests`
- Duplicate files are renamed with `-1`, `-2`, etc.
- File and folder names are cleaned of unsafe characters

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
