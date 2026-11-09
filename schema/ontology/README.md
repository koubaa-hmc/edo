# regimo-ontology
Regimo-Ontology: The semantic backbone for the Regimo Energy Data Orchestrator. Contains OWL/TTL models and schema
bindings for ontology-aware Kafka communication.

## Overview
This repository hosts the formal semantic models and schema definitions for **Regimo**, an Energy Data Orchestrator
developed at the **Karlsruhe Institute of Technology (KIT)**. It serves as the central "source of truth" for the
ontology-aware sockets, ensuring standardised data exchange across the Kafka message bus.

## Purpose
The Regimo Ontology (referencing **KITopen-ID: 1000168804**) provides the vocabulary and relationship rules required to:

* **Contextualise Energy Data:** Define properties for power, load, and grid topology.
* **Enable Interoperability:** Allow heterogeneous microservices to interpret data streams without hard-coded
schema mapping.
* **Enforce Validation:** Provide the basis for automated message validation within the orchestrator's sockets.

## Contents
* `model/`: Core ontology files in OWL/TTL (Turtle) format.
* `schemas/`: Derived JSON or Avro schemas for high-performance Kafka serialisation.
* `bindings/`: Automatically generated language bindings (e.g., linkml models, Python Pydantic classes or Java POJOs) 
  to be used by Regimo sockets.

## Usage in the Ecosystem
This repository is typically integrated into the main **EDO** (Energy Data Orchestrator) environment
as a **Git Submodule**, ensuring that all microservices stay synchronised with the latest semantic definitions.