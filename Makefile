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
CREATE_VENV := $(shell $(VENV) -p python3 ./$(VENV_NAME))
VENV_ACTIVATE := ./$(VENV_NAME)/bin/activate
PYTHON3 := ./$(VENV_NAME)/bin/python3
PIP3 := ./$(VENV_NAME)/bin/pip3
REQUIREMENTS := $(shell ${PIP3} install -r ./requirements.txt)
$(info Virtual Environment Created!)


#############################
#   ENVIRONMENT VARIABLES
#############################
ifeq ($(origin IMAGE), undefined)
$(info [WARNING] 'IMAGE' is not set, default to 'dafualt_image')
IMAGE := ./$(IMAGES_DIRECTORY)/default_image.jpg
else
$(info [INFO] 'IMAGE'= $(IMAGE))
endif

ifeq ($(origin FAMILY_MODE), undefined)
$(info [WARNING] 'FAMILY_MODE' is not set, default to 'False')
FAMILY_MODE := False
else
$(info [INFO] 'FAMILY_MODE'= $(FAMILY_MODE))
endif

ifeq ($(origin OUTPUT), undefined)
$(info [WARNING] 'OUTPUT' is not set, default to 'output')
OUTPUT := ./output
else
$(info [INFO] 'OUTPUT'= $(OUTPUT))
endif

ifeq ($(origin MAX_DISTANCE), undefined)
$(info [WARNING] 'MAX_DISTANCE' is not set, default to '0.5')
MAX_DISTANCE := 0.5
else
$(info [INFO] 'MAX_DISTANCE'= $(MAX_DISTANCE))
endif

ifeq ($(origin INTERESTINGNESS), undefined)
$(info [WARNING] 'INTERESTINGNESS' is not set, default to '2.5')
INTERESTINGNESS := 2.5
else
$(info [INFO] 'INTERESTINGNESS'= $(INTERESTINGNESS))
endif

ifeq ($(origin HUNGRINESS), undefined)
$(info [WARNING] 'HUNGRINESS' is not set, default to '7')
HUNGRINESS := 7
else
$(info [INFO] 'HUNGRINESS'= $(HUNGRINESS))
endif


#############################
#       PATHS SHORCUTS
#############################
PIPELINE_DIRECTORY := ./.pipeline
SCRIPTS_DIRECTORY := ./$(PIPELINE_DIRECTORY)/scripts
ARTIFACTS_DIRECTORY := ./$(PIPELINE_DIRECTORY)/artifacts
IMAGES_DIRECTORY := ./images


#############################
#      CONFIGURATIONS
#############################
DATA := ./$(PIPELINE_DIRECTORY)/assets/amenities-vancouver.json.gz
INPUT_HANDLER_SCRIPT := ./$(SCRIPTS_DIRECTORY)/input_handler.py
DATA_CLEANING_SCRIPT := ./$(SCRIPTS_DIRECTORY)/data_cleaning.py
GENERATE_ROUTE_SCRIPT := ./$(SCRIPTS_DIRECTORY)/generate_route.py
OUTPUT_HANDLER_SCRIPT := ./$(SCRIPTS_DIRECTORY)/output_handler.py
SCRIPT_ARGS := --data $(DATA) --image $(IMAGE) --family_mode $(FAMILY_MODE) --output $(OUTPUT) --max_distance $(MAX_DISTANCE) --interestingness $(INTERESTINGNESS) --hungriness $(HUNGRINESS)


#############################
#         PIPELINE
#############################
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  run            to run the whole pipeline"
	@echo "  input          to handle input data"
	@echo "  data_cleaning  to handle input data"
	@echo "  generate_route to generate route"
	@echo "  output         to output data"
	@echo "with environment variables"
	@echo "  IMAGE=           path to the image"
	@echo "  FAMILY_MODE=     family mode"
	@echo "  OUTPUT=          path to the output"
	@echo "  MAX_DISTANCE=    max distance"
	@echo "  INTERESTINGNESS= interestingness"
	@echo "  HUNGRINESS=      hungriness"

# example run
# make run IMAGE=./images/default_image.jpg FAMILY_MODE=False OUTPUT=./output MAX_DISTANCE=0.5 INTERESTINGNESS=2.5 HUNGRINESS=7

input:
	@echo "Handling Input Data"
	@$(PYTHON3) $(INPUT_HANDLER_SCRIPT) $(SCRIPT_ARGS)

data_cleaning:
	@echo "Cleaning Data Sets"
	@$(PYTHON3) $(DATA_CLEANING_SCRIPT) $(SCRIPT_ARGS)

generate_route:
	@echo "Generating Route"
	@$(PYTHON3) $(GENERATE_ROUTE_SCRIPT) $(SCRIPT_ARGS)

output:
	@echo "Output Data"
	@$(PYTHON3) $(OUTPUT_HANDLER_SCRIPT) $(SCRIPT_ARGS)

# master command
run: input data_cleaning generate_route output
