# 🎨 Couleurs
RESET   = \033[0m
RED     = \033[31m
GREEN   = \033[32m
YELLOW  = \033[33m
BLUE    = \033[34m
MAGENTA = \033[35m
CYAN    = \033[36m
BOLD    = \033[1m

# 🔧 Python & venv
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
REQUIREMENTS = selenium beautifulsoup4 requests Pillow python-docx
SCRIPT = main.py

# 📌 Arguments
URL =
BOOST =
DEDUP = false

# 🧱 Initialisation
all: venv install

venv:
	@echo "$(CYAN)🐍 Creating virtual environment...$(RESET)"
	@python3 -m venv $(VENV_DIR)

install: venv
	@echo "$(YELLOW)📦 Installing Python dependencies...$(RESET)"
	@$(PIP) install --upgrade pip > /dev/null
	@$(PIP) install $(REQUIREMENTS) > /dev/null
	@echo "$(GREEN)✅ Environment ready!$(RESET)"

# ▶️ Exécuter le script
run: all
	@if [ -z "$(URL)" ]; then \
		echo "$(RED)❌ Missing URL. Usage: make run URL=\"https://...\" BOOST=\"vivid\" DEDUP=true$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)▶️ Running script with URL: $(URL), BOOST: $(BOOST), DEDUP: $(DEDUP)$(RESET)"
	@CMD="$(PYTHON) $(SCRIPT) \"$(URL)\""; \
	if [ -n "$(BOOST)" ]; then \
		CMD="$$CMD \"$(BOOST)\""; \
	fi; \
	if [ "$(DEDUP)" = "true" ]; then \
		CMD="$$CMD --dedup"; \
	fi; \
	eval $$CMD

# 🧹 Nettoyage du venv uniquement
clean:
	@rm -rf $(VENV_DIR)
	@echo "$(RED)🧼 Virtual environment removed: $(VENV_DIR)$(RESET)"

# 🧹 Nettoyage total (venv + tous les dossiers et fichiers générés)
fclean: clean
	@rm -rf $(wildcard *_*/ batch_cards/ output/ *.pdf *.docx)
	@echo "$(RED)🧹 Fully cleaned generated folders and files$(RESET)"

# 🔁 Réinitialisation complète
re: fclean all

# 📖 Aide
help:
	@echo "$(MAGENTA)🛠 Available commands:$(RESET)\n"
	@echo "$(CYAN)make all$(RESET)          - Create venv and install dependencies"
	@echo "$(CYAN)make run URL=... [BOOST=vivid] [DEDUP=true]$(RESET) - Run script with URL (color boost optional, dedup mode optional)"
	@echo "$(CYAN)make clean$(RESET)       - Remove virtual environment only"
	@echo "$(CYAN)make fclean$(RESET)      - Full clean (venv + generated files)"
	@echo "$(CYAN)make re$(RESET)          - Full reset (fclean + install)"
	@echo "$(CYAN)make help$(RESET)        - Show this help message"

.PHONY: all venv install run clean fclean re help
