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

# if venv already exists, skip creating it
ifneq (, $(wildcard ./venv))
$(info Virtual Environment Already Exists!)
else
$(info Creating Virtual Envrionment...)
VENV_NAME := venv
CREATE_VENV := $(shell $(VENV) -p python3 ./$(VENV_NAME))
VENV_ACTIVATE := ./$(VENV_NAME)/bin/activate
PYTHON3 := ./$(VENV_NAME)/bin/python3
PIP3 := ./$(VENV_NAME)/bin/pip3
REQUIREMENTS := $(shell ${PIP3} install -r ./requirements.txt)
$(info Virtual Environment Created!)
endif


#############################
#   ENVIRONMENT VARIABLES
#############################
ifeq ($(origin IMAGE), undefined)
$(info [WARNING] 'IMAGE' is not set, default to 'default_image')
IMAGE := ./images/default_image.jpg
else
$(info [INFO] 'IMAGE'= $(IMAGE))
endif

ifeq ($(origin FAMILY_MODE), undefined)
$(info [WARNING] 'FAMILY_MODE' is not set, default to 'False')
FAMILY_MODE := False
else
$(info [INFO] 'FAMILY_MODE'= $(FAMILY_MODE))
endif

ifeq ($(origin DURATION), undefined)
$(info [WARNING] 'DURATION' is not set, default to '3')
DURATION := 5
else
$(info [INFO] 'DURATION'= $(DURATION))
endif

ifeq ($(origin INTERESTINGNESS), undefined)
$(info [WARNING] 'INTERESTINGNESS' is not set, default to '2.5')
INTERESTINGNESS := 2
else
$(info [INFO] 'INTERESTINGNESS'= $(INTERESTINGNESS))
endif

ifeq ($(origin HUNGRINESS), undefined)
$(info [WARNING] 'HUNGRINESS' is not set, default to '7')
HUNGRINESS := 7
else
$(info [INFO] 'HUNGRINESS'= $(HUNGRINESS))
endif

ifeq ($(origin POINT_TIME), undefined)
$(info [WARNING] 'POINT_TIME' is not set, default to '0.2')
POINT_TIME := 0.3
else
$(info [INFO] 'POINT_TIME'= $(POINT_TIME))
endif


#############################
#       PATHS SHORCUTS
#############################
PIPELINE_DIRECTORY := ./.pipeline
SCRIPTS_DIRECTORY := ./$(PIPELINE_DIRECTORY)/scripts
ARTIFACTS_DIRECTORY := ./$(PIPELINE_DIRECTORY)/artifacts


#############################
#      CONFIGURATIONS
#############################
DATA := $(PIPELINE_DIRECTORY)/artifacts/amenities-vancouver.json.gz
OUTPUT := ./output
INPUT_HANDLER_SCRIPT := $(SCRIPTS_DIRECTORY)/input_handler.py
DATA_CLEANING_SCRIPT := $(SCRIPTS_DIRECTORY)/data_cleaning.py
GENERATE_ROUTE_SCRIPT := $(SCRIPTS_DIRECTORY)/generate_route.py
OUTPUT_HANDLER_SCRIPT := $(SCRIPTS_DIRECTORY)/output_handler.py
SCRIPT_ARGS := --data $(DATA) --image $(IMAGE) --family_mode $(FAMILY_MODE) --output $(OUTPUT) --duration $(DURATION) --interestingness $(INTERESTINGNESS) --hungriness $(HUNGRINESS) --point_time $(POINT_TIME)


#############################
#         PIPELINE
#############################
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  run             to run the whole pipeline"
	@echo "  input_handler   to handle input data"
	@echo "  data_cleaning   to handle input data"
	@echo "  generate_route  to generate route"
	@echo "  output_handler  to output data"
	@echo "with environment variables"
	@echo "  IMAGE=           path to the image"
	@echo "  FAMILY_MODE=     family mode"
	@echo "  OUTPUT=          path to the output"
	@echo "  DURATION=    	  duration"
	@echo "  INTERESTINGNESS= interestingness"
	@echo "  HUNGRINESS=      hungriness"
	@echo "  POINT_TIME=      average hours spent at each point"

# example run
# make run IMAGE=./images/default_image.jpg FAMILY_MODE=False OUTPUT=./output MAX_DISTANCE=0.5 INTERESTINGNESS=2.5 HUNGRINESS=7

input_handler:
	@echo "[INFO] Handling Input Data"
	@$(PYTHON3) $(INPUT_HANDLER_SCRIPT) $(SCRIPT_ARGS)

data_cleaning:
	@echo "[INFO] Cleaning Data Sets"
	@$(PYTHON3) $(DATA_CLEANING_SCRIPT) $(SCRIPT_ARGS)

generate_route:
	@echo "[INFO] Generating Route"
	@$(PYTHON3) $(GENERATE_ROUTE_SCRIPT) $(SCRIPT_ARGS)

output_handler:
	@echo "[INFO] Output Data"
	@$(PYTHON3) $(OUTPUT_HANDLER_SCRIPT) $(SCRIPT_ARGS)

# master command
run: input_handler data_cleaning generate_route output_handler
