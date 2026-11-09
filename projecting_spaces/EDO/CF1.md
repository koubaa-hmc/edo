# Access available source of Information

**Source**: [FeadO Feasibility Study - Technical Specification: "Sources Integration Guide"]

Main sources of information are (as validated by FeadO feasibility study):
- Machine actionable Data Management Plans [[maDMP]]
  *✓ Validated: Core source for project metadata*
- Sensor Management System [[SMS]]
  *✓ Validated: Real-time sensor data integration*
- Information on Author through Helmholtz-ID (or [[ORCiD]])
  *✓ Validated: Unique researcher identification*
- Current information on research operations from Electronic Lab Notebook [[ELN]]
  *✓ Validated: Project execution tracking*
- Knowledge Graphs like [[ORKG]] or [[HKG]]
  *✓ Validated: Semantic context integration*

## FeadO Validation Status
- **Sources integration pattern validated** in FeadO feasibility study (2025-08-15)
- **Data access patterns confirmed** as critical for CF1 implementation

Not all sources are always available.

EDO should make the best from existing sources to detect:
- the [[Target platform]], their accepted [[Standard]]s and [[Vocabular]]ies,
  *✓ Priority area derived from FeadO ecosystem analysis*
- the Unique Identifier of
  	- Author [[ORCiD]]
  	- Equipment [[PIDINST]]
  	- Institution [[ROR]]
  	- etc.
  *✓ Derived from FeadO ID hierarchy analysis*
- the [[Scientific context]] of the dataset, possible collaborators, etc.
  *✓ Context detection validated in FeadO feasibility study*

## Implementation Requirements from FeadO Study

### 1. Source Integration Prioritization
- [ ] SMS integration (high priority - real-time data)
- [ ] maDMP hierarchical analysis (medium priority - project structure)
- [ ] Knowledge Graph querying patterns (ongoing - context enrichment)

### 2. Error Handling Patterns
- [ ] Handle missing sources gracefully (FeadO study §4.2)
- [ ] Cache frequently accessed sources (FeadO recommendation §5.1)
- [ ] Fallback strategies for unavailable systems (FeadO §6.3)

### 3. Validation Requirements
As defined in FeadO Technical Specification §3.1:
- Cross-reference IDs across sources
- Validate source consistency
- Detect platform-specific requirements

**Validation Checklist**:
- [ ] ORCiD → Helmholtz-ID cross-check
- [ ] maDMP PID → Sensor PID mapping
- [ ] Platform vocabulary compatibility

See also:
- FeadO Feasibility Study documentation
- [CF1 Epic: Source Integration Priority]
