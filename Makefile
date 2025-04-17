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
REQUIREMENTS = selenium beautifulsoup4 requests Pillow
SCRIPT = main.py

# 📌 Arguments
URL =
BOOST =

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

# ▶️ Run the script with URL and optional BOOST
run: all
	@if [ -z "$(URL)" ]; then \
		echo "$(RED)❌ Missing URL. Usage: make run URL=https://your-url.com [BOOST=vivid|ultra-vivid]$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)▶️ Running script with URL: $(URL) BOOST: $(BOOST)$(RESET)"
	@if [ -z "$(BOOST)" ]; then \
		$(PYTHON) $(SCRIPT) "$(URL)"; \
	else \
		$(PYTHON) $(SCRIPT) "$(URL)" "$(BOOST)"; \
	fi

# 🧹 Clean environment
clean:
	@rm -rf $(VENV_DIR)
	@echo "$(RED)🧼 Environment removed: $(VENV_DIR)$(RESET)"

# 🔁 Full reset
re: clean all

# 📖 Help
help:
	@echo "$(MAGENTA)🛠 Available commands:$(RESET)\n"
	@echo "$(CYAN)make all$(RESET)          - Create venv and install dependencies"
	@echo "$(CYAN)make run URL=... [BOOST=vivid|ultra-vivid]$(RESET) - Run script with URL (and optional color boost)"
	@echo "$(CYAN)make clean$(RESET)       - Remove virtual environment"
	@echo "$(CYAN)make re$(RESET)          - Clean and reinstall"
	@echo "$(CYAN)make help$(RESET)        - Show this help message"

.PHONY: all venv install run clean re help
