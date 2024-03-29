#############################
# PYTHON VIRTUAL ENVIRONMENT
#############################
ifeq (, $(shell which python3))
$(error Python3 Installation Not Found!)
else
export PYTHON3 := $(shell which python3)
endif

ifeq (, $(shell which virtualenv))
$(error Virtual Environment Installation Not Found!)
else
export VENV := $(shell which virtualenv)
endif

$(info Creating Virtual Envrionment...)
VENV_NAME := venv
CREATE_VENV := $(shell $(VENV) -p python3 ./{VENV_NAME})
VENV_ACTIVATE := ./{VENV_NAME}/bin/activate
PYTHON3 := ./{VENV_NAME}/bin/python3
PIP3 := ./{VENV_NAME}/bin/pip3
REQUIREMENTS := $(shell ${PIP3} install -r ./requirements.txt)
$(info Virtual Environment Created!)


#############################
#       PATHS SHORCUTS
#############################
PIPELINE_DIRECTORY := ./.pipeline
SCRIPTS_DIRECTORY := ./$(PIPELINE_DIRECTORY)/scripts
ARTIFACTS_DIRECTORY := ./$(PIPELINE_DIRECTORY)/artifacts


#############################
#      CONFIGURATIONS
#############################
INPUT_HANDLER_SCRIPT := ./$(SCRIPTS_DIRECTORY)/input_handler.py
DATA_CLEANING_SCRIPT := ./$(SCRIPTS_DIRECTORY)/data_cleaning.py
GENERATE_ROUTE_SCRIPT := ./$(SCRIPTS_DIRECTORY)/generate_route.py
OUTPUT_HANDLER_SCRIPT := ./$(SCRIPTS_DIRECTORY)/output_handler.py


#############################
#         PIPELINE
#############################
input:
	@echo "Handling Input Data"

data_cleaning:
	@echo "Cleaning Data Sets"

generate_route:
	@echo "Generating Route"

output:
	@echo "Output Data"

# master command
run: input data_cleaning generate_route output
