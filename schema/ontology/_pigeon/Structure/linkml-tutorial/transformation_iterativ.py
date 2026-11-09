from datetime import datetime
from pathlib import Path

from linkml_map.session import Session
from linkml_map.utils.loaders import load_specification
from linkml_runtime.utils.schemaview import SchemaView

# Base directory for the project (adjust as needed)
base_dir = Path(__file__).resolve().parent.parent.parent

# Define paths
transformer_spec_path = base_dir / 'Tranlation-Binding' / 'v2dmp_v03.yaml'
source_schema_path = base_dir / 'Model' / 'project-values-model.yaml'
target_schema_path = base_dir.parent / 'Models' / 'maDMP-model-1.2.yaml'
input_data = base_dir / 'Metadata' / 'project_values_nested.json'
# Extracts the last 3 characters of the filename (e.g., 'v01')
spec_suffix = transformer_spec_path.stem[-3:]
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
# Define output path
output_filename = f"transfo_graph_{spec_suffix}_{timestamp}"
output_data = base_dir / 'Metadata' / output_filename


if __name__ == "__main__":

    session = Session()

    # Load the definitions
    source_schema_view = SchemaView(source_schema_path)
    target_schema_view = SchemaView(target_schema_path)
    transformation_specification = load_specification(transformer_spec_path)

    session.set_source_schema(source_schema_view)
    session.set_object_transformer(transformation_specification)

    graph = session.graphviz()
    graph.render(output_data, format='png', cleanup=True)
