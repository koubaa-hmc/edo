# RDA maDMP Common Standard: Transformation & Serialisation

## Overview
This repository contains among others the master schema definitions and the automated transformation pipeline used to convert the **RDA maDMP Common Standard (v1.2)** from its native JSON Schema format into unified, machine-actionable LinkML models and semantic RDF serialisations.

## Directory Structure
* `Models/`:
  * `maDMP-model-1.2.yaml` & `maDMP-model-1.2.puml`: are the generated model files.
* `Structures/`:
    * `maDMP-schema-1.2.json`: The authoritative JSON Schema source.
    * `maDMP-schema-normalised-lifted.json`: Addresses specific serialization challenges that arise when mapping JSON Schema to a formal data model
* `Translation-Bindings/`:
    * `maDMP-pre-process.py`: Generates the normalized lifted schema.

## Pre-processing Script: `maDMP-pre-process.py`
This script serves as a structural mediator that transforms the `maDMP-schema-1.2.json` into a format optimized for
the schema-automator tool. It addresses specific serialization challenges that arise when mapping JSON Schema to a
formal data model.

### Core Transformations
* **OneOf Normalization**: Simplifies complex `OneOf` unions into standard array types, ensuring a deterministic
`multivalued: true` translation in the resulting LinkML model.

* **Definition Registry (`$defs`) Cleanup**: The script performs a deep-traversal discovery, ensuring that all
entities—regardless of their nesting depth—are registered as top-level definitions in `$defs`.
This creates a flat, clean registry for the generator.

* **Reification of Array Containers**: The script identifies *wrapper* structures (like Costs or Datasets) that are
defined as raw arrays in the original schema. It transforms these into explicit object classes with an items property.

    * **Result**: This forces the LinkML generator to treat these containers as formal Classes rather than primitive types,
enabling the generation of explicit composition relationships (e.g., `Costs *--> Cost`).

### Impact on Generated Model
By applying these transformations before the `schema-automator` import, the script ensures:

1. **Elimination of Inlining Artifacts**: By centralizing all references in $defs, the script removes the
redundant "inlined class" duplication (often appearing as (i) suffixes) in generated diagrams.

2. **Explicit Class Hierarchy**: Because array containers are reified into objects, the resulting `maDMP-model.yaml`
contains formal slot definitions. This bridges the gap between disconnected classes, allowing the PlantUML generator
to draw accurate composition arrows between container classes and their constituent items.

3. **Deterministic Relationships**: The modeler gains full control over the cardinality and range of every property,
as the generator no longer needs to infer types from anonymous nested structures.

## Transformation Workflow
To maintain interoperability between local RDMO instances and the global RDA standard, the build pipeline is
automated:
* The script is designed to be run as the first step in the pipeline:
  * Input: Structure/maDMP-schema-1.2.json
  * Process: Normalization $\rightarrow$ Registry Discovery $\rightarrow$ Array Reification
  * Output: Structure/maDMP-schema-normalised-lifted.json
  * This output file is then used as the source for schema-automator import-json-schema, ensuring a structurally sound
  model suitable for downstream documentation and code generation.


## Mapping & Usage
The generated `maDMP-model.yaml` is designed for direct RDF/OWL serialisation. Domain-specific attributes required for KIT research infrastructure follow the `https://kit.edu/terms/` URI namespace to ensure global identifier uniqueness and schema alignment with existing triple stores.

---
*Maintained by: A. Koubaa, Karlsruhe Institute of Technology*