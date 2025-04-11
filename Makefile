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
REQUIREMENTS = selenium beautifulsoup4 requests
SCRIPT = main.py

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

# ▶️ Run the script with URL as argument
run:
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "$(RED)❌ Missing URL. Usage: make run https://your-url.com$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)▶️ Running script with URL: $(word 2, $(MAKECMDGOALS))$(RESET)"
	@$(PYTHON) $(SCRIPT) "$(word 2, $(MAKECMDGOALS))"

# 🧹 Clean environment
clean:
	@rm -rf $(VENV_DIR)
	@echo "$(RED)🧼 Environment removed: $(VENV_DIR)$(RESET)"

# 🔁 Full reset
re: clean all

.PHONY: all venv install run clean re

# ✅ Ignore URL as target so Make doesn't try to run it as a command
%:
	@:
