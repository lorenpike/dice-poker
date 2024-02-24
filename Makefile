# To run this makefile you will need make and cygwin install on your PC


# COLORS
BLUE = \e[1;36m
GREEN = \e[1;32m
GRAY = \e[38;5;247m
RESET = \e[0m

# VARIABLES 
CYGWIN_PATH := C:\cygwin64 # Modify this to the proper cygwin path
SHELL := $(CYGWIN_PATH)\bin\bash
FIND := $(CYGWIN_PATH)\bin\find
SRC := src
VENV := venv
PYTHON := ./$(VENV)/Scripts/python.exe
UVICORN := ./$(VENV)/Scripts/uvicorn.exe


.PHONY: help
help: 
	@echo -e 'Dice Poker Makefile$(GRAY)'
	@echo 'Usage:'
	@echo '	make install	Install dependencies and src into a venv.'
	@echo '	make format	Format the source code in python.'
	@echo '	make server	Run up the test server.'
	@echo -e '	make clean	Remove all python-generated files.$(RESET)'

.PHONY: clean
clean:
	@echo 'Cleaning up...'
	@$(FIND) $(SRC) -regex '^.*\(__pycache__\|\.py[co]\)$ ' -delete
	@rm -rf $(SRC)/*.egg-info .pytest_cache $(VENV)
	@echo 'Done!'

.PHONY: install
install: $(VENV)/.install-stamp
	@echo -e '$(RESET)Finished install!'
	@echo -e 'Activate venv with: $(BLUE)source ./$(VENV)/bin/activate$(RESET)'


.PHONY: format
format: $(PYTHON)
	@echo 'Formatting the $(SRC) directory...'
	@$(PYTHON) -m black $(SRC)

.PHONY: server
server: $(PYTHON)
	@echo 'Running up dev server...'
	@$(UVICORN) dice_poker.server:combined_asgi_app --reload

$(PYTHON):
	@echo 'Creating virtual environment...'
	@python -m venv $(VENV)
	@$(PYTHON) -m pip install -q --upgrade pip

$(VENV)/.install-stamp: $(PYTHON) pyproject.toml
	@echo -e 'Installing the local package and dependencies...$(GRAY)'
	@$(PYTHON) -m pip install -e .
	@touch $@
