# Define paths for clarity and ease of maintenance
TRANSFORMER_SPEC = Tranlation-Binding/v2dmp_v01.yaml
SOURCE_SCHEMA = Model/project-values-model.yaml
TARGET_SCHEMA = ../Models/maDMP-model-1.2.yaml
INPUT_DATA = Metadata/project_values_nested.json
SPEC_SUFFIX := $(shell basename $(basename $(TRANSFORMER_SPEC)) | rev | cut -c 1-3 | rev)
TIMESTAMP := $(shell date +%Y%m%d_%H%M)
OUTPUT_DATA = Metadata/madmp_output_$(SPEC_SUFFIX)_$(TIMESTAMP).json

# Default target
all: map

# Command to execute the transformation
map:
	@echo "Running LinkML transformation..."
	linkml-map map-data \
		--transformer-specification $(TRANSFORMER_SPEC) \
		--schema $(SOURCE_SCHEMA) \
		--target-schema $(TARGET_SCHEMA) \
		--source-type Project \
		--output $(OUTPUT_DATA) \
		$(INPUT_DATA)
	@echo "Transformation complete: $(OUTPUT_DATA)"

# Clean up output
clean:
	rm -f Metadata/madmp_output_*.json