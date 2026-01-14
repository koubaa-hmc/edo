# edo
An Ontology-Aware Energy Data Orchestrator. A microservice-based framework for intelligent energy system integration via Kafka. Developed at Karlsruhe Institute of Technology (KIT).

The Repository has a Service-Oriented Structure. This approach ensures that ontology definitions, infrastructure 
(Kafka), and functional microservices remain decoupled yet easy to orchestrate.

## 1. Core & Semantic Definitions
Since the components are "ontology aware", the semantic models must be the "single source of truth".

- `regimo-ontology`: Contains the OWL/TTL files, schema definitions, and generated class libraries (e.g., linkml 
models, Python Pydantic models or Java POJOs) used by the sockets.
- `regimo-common-lib`: Shared logic for Kafka producer/consumer patterns and common socket interfaces to ensure consistency across the orchestrator.

## 2. Microservice Repositories (The Sockets)
Instead of a single massive repository (monorepo), use individual repositories for each microservice to allow 
independent scaling and deployment cycles.

- `socket-[service-name]`: e.g., `socket-rdmo`, `socket-orkg`.
- `socket-template`: A boilerplate 
  repository containing the Kafka bus connection logic and ontology parsing. This allows KIT researchers to quickly spin up new components.

## 3. Infrastructure & Orchestration
regimo-deploy: Contains Docker Compose files, Kubernetes manifests, or Helm charts. This repository defines how the Kafka bus and the sockets are wired together in a production or research environment.

regimo-docs: Centralised documentation using GitHub Pages (MkDocs or Sphinx), detailing the architectural flow of the energy data.

## Repository Naming Convention
The Regimo ecosystem is organised into functional categories to maintain modularity and ease of orchestration.

| Category | Repository Name Pattern | Description |
| :--- | :--- | :--- |
| **Core** | `regimo-core` | Base abstractions and internal libraries for the orchestrator. |
| **Logic** | `socket-<functional-unit>` | Microservices (Sockets) handling specific energy data tasks. |
| **Schema** | `regimo-ontology` | The semantic backbone and shared ontology definitions. |
| **Ops** | `regimo-infrastructure` | Kafka configurations, Zookeeper/KRaft setups, and CI/CD pipelines. |

## Managing the Kafka Bus Integration
Since Kafka acts as the backbone, using GitHub Packages to host a private or public "Regimo-Bus-Adapter" library. This library should be included as a dependency in every socket repository to handle:

- Standardised message headers for ontology metadata.
- Automatic serialisation/deserialisation based on your KITopen-documented schemas.

## Essential Commands for the Development Team

When cloning the main **edo** repository, specific flags must be used to ensure the submodules (ontology and sockets) are correctly populated rather than remaining as empty directories.

### 1. Initial Setup
To clone the entire orchestrator ecosystem, including all microservices and the ontology:
```bash
git clone --recurse-submodules git@github.com:koubaa-hmc/edo.git
```

### 2. Updating Components
Because the `edo` repository only stores a "pointer" to a specific commit in each submodule, you must manually pull updates when a colleague modifies a component like `regimo-ontology`.

To pull the latest changes for all sockets and the ontology into your local orchestrator environment, run:

```bash
git submodule update --remote --merge
```

### 3. Development Workflow (Inside a Submodule)

If you are modifying a component (such as the ontology or a specific socket) while working within the `edo` repository, you must commit your changes twice: once within the component itself and once in the parent repository to update the "pointer".

Follow this sequence:

```bash
# 1. Navigate to the specific component directory
cd schema/ontology

# 2. Make your changes and push them to the component's independent repository
git add .
git commit -m "Update energy ontology terms"
git push origin main

# 3. IMPORTANT: Update the 'edo' parent repository
# This records the new version of the submodule in the main orchestrator
cd ../..
git add schema/ontology
git commit -m "Update edo pointer to latest ontology version"
git push origin main
```

## Workflow Summary

Use the following table as a quick reference for managing the Regimo microservices and ontology submodules.

| Action | Command |
| :--- | :--- |
| **Add new component** | `git submodule add <url> <path>` |
| **First-time setup** | `git submodule update --init --recursive` |
| **Update all components** | `git submodule update --remote --merge` |
| **Run command on all** | `git submodule foreach 'git pull origin main'` |
