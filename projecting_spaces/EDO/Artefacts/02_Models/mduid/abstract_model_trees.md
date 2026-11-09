# Abstract Model Trees for EDO User Interface

*Generated: 2026-08-12*

This document defines the Abstract Model Trees for Model-Driven User Interface Development (MDUID) in EDO. The models describe the user interface structure required to realize user cases derived from the Core Functions (CF1-CF4), organized by FAIR Data Lifecycle phases and constrained by user roles.

---

## Modeling Approach

### Model-Driven User Interface Development (MDUID)

Following the Cameleon Reference Framework, EDO UIs are modeled at multiple abstraction levels:

```
┌────────────────────────────────────────────────────────────┐
│              MDUID ABSTRACTION LEVELS                      │
│                                                            │
│   Task Model → Abstract UI → Concrete UI → Final UI        │
│       ↓             ↓            ↓             ↓           │
│      WHAT       STRUCTURE      LOOK         RENDERED       │
│      TO DO      & FLOW         & FEEL       INTERFACE      │
└────────────────────────────────────────────────────────────┘
```

This document focuses on **Abstract UI Models** (AUI), which define:
- Interface structure independent of platform (web, mobile, desktop)
- Navigation flows between tasks
- Information presentation patterns
- Interaction primitives

### Integration with Other Models

| Source Document           | Contribution to Abstract Model Trees     |
| ------------------------- | ---------------------------------------- |
| [[core_functions_resume]] | Functional requirements per CF1-CF4      |
| [[edo_roles]]             | Access control per role                  |
| [[fair_data_lifecycle]]   | Workflow structure and phase transitions |

---

## Role-Based Access Control Matrix

Here is the Markdown table converted from your text:

| **Model**                    | **FAIR Phase**   | **Core Functions** | **Primary Roles**                           |
| ---------------------------- | ---------------- | ------------------ | ------------------------------------------- |
| **1. BrowseCatalog**         | SHARE/REUSE      | CF1, CF2, CF4      | guest_viewer, research_fellow, data_steward |
| **2. ViewDatasetDetail**     | REUSE            | CF1, CF2, CF4      | all roles (read-only for guests)            |
| **3. CreateMetadataWizard**  | PLAN/COLLECT     | CF1, CF2, CF3      | research_fellow, data_steward               |
| **4. EditMetadata**          | PROCESS/PRESERVE | CF1–CF4            | research_fellow, data_steward               |
| **5. ReviewDashboard**       | PRESERVE         | CF2–CF4            | data_steward                                |
| **6. ReviewDetail**          | PRESERVE         | CF2–CF4            | data_steward                                |
| **7. PlatformConfiguration** | SHARE            | CF2, CF4           | admin, data_steward (limited)               |
| **8. SystemAdministration**  | Infrastructure   | CF1, CF2, CF4      | admin                                       |

Access to Abstract UI Components is determined by user roles:

| AUI Component      | guest_viewer | research_fellow | data_steward | admin |
| ------------------ | ------------ | --------------- | ------------ | ----- |
| BrowseCatalog      | ✅            | ✅               | ✅            | ✅     |
| SearchDatasets     | ✅            | ✅               | ✅            | ✅     |
| CreateMetadata     | ❌            | ✅               | ✅            | ❌     |
| EditOwnMetadata    | ❌            | ✅               | ✅            | ❌     |
| ReviewMetadata     | ❌            | ❌               | ✅            | ❌     |
| ConfigurePlatforms | ❌            | ❌               | ⚠️ Select    | ✅     |
| ManagePlugins      | ❌            | ❌               | ❌            | ✅     |
| SystemConfig       | ❌            | ❌               | ❌            | ✅     |
| UserManagement     | ❌            | ❌               | ❌            | ✅     |

*⚠️ = Limited capability (selection only, no configuration)*

---

## Abstract Model Tree 1: Catalog Browsing (FAIR Phase: SHARE/REUSE)

**Supported Core Functions:** CF1, CF2, CF4  
**Primary Roles:** `guest_viewer`, `research_fellow`, `data_steward`

```
AbstractUI: BrowseCatalog
├── NavigationBar
│   ├── Logo [link: Home]
│   ├── SearchBox [action: SearchDatasets]
│   ├── BrowseMenu
│   │   ├── ByDomain
│   │   ├── ByInstitution
│   │   ├── ByAuthor
│   │   └── RecentlyPublished
│   └── AuthMenu
│       ├── Login [roles: research_fellow, data_steward, admin]
│       └── UserProfile [roles: authenticated]
│
├── MainContent
│   ├── FilterPanel
│   │   ├── DomainFilter [multi-select]
│   │   ├── DateRangeFilter [start, end]
│   │   ├── LicenseFilter [checkboxes]
│   │   └── AccessTypeFilter [open, embargoed, restricted]
│   │
│   ├── ResultsGrid
│   │   └── DatasetCard [repeater]
│   │       ├── Title [link: ViewDatasetDetail]
│   │       ├── Authors [list with ORCiD badges]
│   │       ├── Institution [ROR badge]
│   │       ├── PublicationDate
│   │       ├── DOI [link: resolver]
│   │       ├── License [badge]
│   │       └── ReuseCount [metric]
│   │
│   └── Pagination
│       ├── PageSizeSelector [10, 25, 50, 100]
│       └── PageNavigator [prev, next, jump]
│
└── Footer
    ├── AboutLink
    ├── API docsLink
    └── ContactLink
```

**Role Constraints:**
- `guest_viewer`: Full access to BrowseCatalog
- All authenticated roles: Additional personalized features (saved searches, alerts)

---

## Abstract Model Tree 2: Dataset Detail View (FAIR Phase: REUSE)

**Supported Core Functions:** CF1, CF2, CF4  
**Primary Roles:** `guest_viewer`, `research_fellow`, `data_steward`

```
AbstractUI: ViewDatasetDetail
├── BreadcrumbNav
│   └── Path: Home > Domain > Dataset Title
│
├── HeaderSection
│   ├── Title [h1]
│   ├── DOI [with copy button]
│   ├── BadgeCluster [domain, license, access-type]
│   └── ActionToolbar [role-dependent]
│       ├── CiteButton [all roles]
│       ├── ExportButton [all roles] → ExportFormatModal
│       ├── EditButton [roles: research_fellow (own), data_steward]
│       └── FlagButton [all roles] → ReportIssueModal
│
├── TabbedContent
│   ├── Tab: Overview
│   │   ├── Description [rich text]
│   │   ├── Keywords [linked tags]
│   │   ├── FundingInformation [grant IDs]
│   │   └── RelatedPublications [list with DOIs]
│   │
│   ├── Tab: Metadata
│   │   ├── SchemaInfo [name, version]
│   │   ├── MetadataTable [key-value pairs]
│   │   │   ├── Creator [ORCiD-linked]
│   │   │   ├── Contributor [list]
│   │   │   ├── Publisher
│   │   │   ├── PublicationYear
│   │   │   ├── Subject [controlled vocabulary]
│   │   │   ├── Instrument [PIDINST-linked]
│   │   │   └── CustomFields [schema-dependent]
│   │   └── ProvenanceGraph [visual]
│   │
│   ├── Tab: Files
│   │   ├── FileList [repeater]
│   │   │   ├── FileName [download link if accessible]
│   │   │   ├── FileType [icon + MIME]
│   │   │   ├── FileSize [human-readable]
│   │   │   └── Checksum [algorithm:value]
│   │   └── DownloadOptions
│   │       ├── DownloadAll [if accessible]
│   │       └── RequestAccess [if restricted] → AccessRequestModal
│   │
│   ├── Tab: Usage
│   │   ├── CitationRecommendation [multiple formats]
│   │   ├── MetricsDashboard
│   │   │   ├── ViewCount
│   │   │   ├── DownloadCount
│   │   │   └── CitationCount
│   │   └── ReuseExamples [list of citing works]
│   │
│   └── Tab: Similar Datasets [CF4 interactive search]
│       ├── SimilarityCriteria [selectable]
│       │   ├── SameAuthor
│       │   ├── SameDomain
│       │   ├── SameInstrument
│       │   └── SemanticSimilarity
│       │
│       └── SimilarResults [repeater of DatasetCard]
│           └── [link: ViewDatasetDetail] (recursive)
│
└── Sidebar
    ├── AuthorProfileCard
    │   ├── Name
    │   ├── ORCiD [link]
    │   ├── Institution [ROR link]
    │   └── OtherDatasets [count + link]
    │
    └── ShareWidget
        ├── SocialShareButtons
        └── EmbedCodeGenerator
```

**Role Constraints:**
- `guest_viewer`: Read-only access; DownloadFiles only if open access
- `research_fellow`: Full access + EditButton for own datasets
- `data_steward`: Full access + EditButton for all datasets (review mode)

---

## Abstract Model Tree 3: Metadata Creation Wizard (FAIR Phase: PLAN/COLLECT)

**Supported Core Functions:** CF1, CF2, CF3  
**Primary Roles:** `research_fellow`, `data_steward`

```
AbstractUI: CreateMetadataWizard
├── WizardHeader
│   ├── Title: "Create New Dataset Metadata"
│   ├── ProgressIndicator [steps 1-6]
│   └── SaveDraftButton [all steps]
│
├── Step1: SelectTemplate
│   ├── TemplateGallery [grid]
│   │   └── TemplateCard [repeater]
│   │       ├── SchemaName [e.g., DataCite, DCAT, domain-specific]
│   │       ├── DomainBadge
│   │       ├── FieldCount
│   │       └── SelectButton [action: load template]
│   │
│   └── CustomSchemaOption [upload JSON schema]
│
├── Step2: BasicInformation [CF3 - context-aware UI]
│   ├── FormGroup: Identification
│   │   ├── Title [text, required]
│   │   ├── AlternateIdentifier [repeating group]
│   │   └── DOI [auto-generate option]
│   │
│   ├── FormGroup: Creators [CF1 - ORCiD integration]
│   │   └── CreatorRepeater
│   │       ├── Name [text]
│   │       ├── ORCiDLookup [search widget] → ORCiDSearchModal
│   │       ├── Affiliation [ROR lookup] → RORSearchModal
│   │       └── NameType [person | organization]
│   │
│   └── FormGroup: Descriptions
│       ├── Abstract [textarea, min 50 chars]
│       └── AdditionalDescriptions [repeating, type-selector]
│
├── Step3: ScientificContext [CF1, CF3 - recommendations]
│   ├── FormGroup: DomainClassification
│   │   ├── DisciplinePicker [hierarchical tree]
│   │   └── SubjectKeywords [tag input with vocabulary suggestions]
│   │
│   ├── FormGroup: ProjectContext
│   │   ├── GrantInformation [funder lookup]
│   │   ├── ProjectTitle [text]
│   │   └── ProjectWebsite [URL]
│   │
│   ├── FormGroup: Methodology
│   │   ├── InstrumentSelection [PIDINST lookup] → InstrumentSearchModal
│   │   ├── MethodDescription [textarea]
│   │   └── StandardOperatingProcedure [file upload or URL]
│   │
│   └── RecommendationPanel [CF3 - from iKG]
│       ├── SuggestedVocabularies [click-to-apply]
│       ├── SimilarDatasets [for reference]
│       └── MissingContextAlerts [validation-driven]
│
├── Step4: TechnicalMetadata [CF1 - ELN/SMS integration]
│   ├── DataSourceSelector
│   │   ├── ManualEntry [default]
│   │   ├── ImportFromELN [button] → ELNConnectionModal
│   │   ├── ImportFrommaDMP [button] → DMPImportModal
│   │   └── ImportFromSMS [button] → SMSConnectionModal
│   │
│   ├── FormGroup: DataCharacteristics
│   │   ├── DataTypes [checkboxes: numerical, textual, images, etc.]
│   │   ├── DataVolume [size + unit]
│   │   ├── FileFormats [list with version]
│   │   └── TemporalCoverage [start, end]
│   │
│   └── FormGroup: SpatialCoverage
│       ├── GeoLocationPicker [map widget]
│       ├── PlaceName [geonames lookup]
│       └── Coordinates [lat/lon input]
│
├── Step5: AccessAndReuse [CF2 - transformation prep]
│   ├── FormGroup: AccessConditions
│   │   ├── AccessType [radio: open | embargoed | restricted | closed]
│   │   ├── EmbargoDate [date picker, shown if embargoed]
│   │   ├── AccessRequestProcedure [textarea, shown if restricted]
│   │   └── AuthenticationRequirement [dropdown]
│   │
│   ├── FormGroup: Licensing
│   │   ├── LicenseSelector [Creative Commons wizard]
│   │   ├── CustomLicenseTerms [textarea]
│   │   └── RightsHolder [text]
│   │
│   └── FormGroup: ReuseSupport
│       ├── CitationGuidance [textarea]
│       ├── AcknowledgementRequirements [textarea]
│       └── DocumentationLinks [repeating URL]
│
├── Step6: TargetPlatforms [CF4 - publication config]
│   ├── PlatformSelector [multi-select with plugin status]
│   │   └── PlatformCheckbox [repeater]
│   │       ├── PlatformName
│   │       ├── PluginStatus [installed | missing → InstallButton]
│   │       ├── SchemaCompatibility [compatible | requires mapping]
│   │       └── PreviewMappingButton → MappingPreviewModal
│   │
│   ├── MappingConfiguration [per selected platform]
│   │   ├── FieldMappingTable [source → target]
│   │   ├── TransformationRules [editable]
│   │   └── ValidationPreview [errors/warnings]
│   │
│   └── PublicationSchedule
│       ├── PublishNow [radio]
│       ├── SchedulePublication [datetime picker]
│       └── SaveAsDraft [radio]
│
└── WizardFooter
    ├── BackButton [disabled on step 1]
    ├── NextButton [enabled if step valid]
    ├── SubmitButton [step 6 only]
    └── CancelButton [with unsaved warning]
```

**Role Constraints:**
- `research_fellow`: Full wizard access for own datasets
- `data_steward`: Full wizard access + ability to create on behalf of researchers
- `guest_viewer`, `admin`: No access

**Validation Rules:**
- Required fields enforced per schema
- Cross-field validation (e.g., embargo date must be future)
- PID format validation (ORCiD, DOI, ROR, PIDINST)

---

## Abstract Model Tree 4: Metadata Editor (FAIR Phase: PROCESS/PRESERVE)

**Supported Core Functions:** CF1, CF2, CF3, CF4  
**Primary Roles:** `research_fellow`, `data_steward`

```
AbstractUI: EditMetadata
├── EditorHeader
│   ├── DatasetTitle [editable inline]
│   ├── StatusBadge [draft | published | under-review]
│   ├── VersionInfo [v1.2 | compare versions link]
│   └── ActionToolbar
│       ├── PreviewButton
│       ├── ValidateButton → ValidationResultPanel
│       ├── SaveButton
│       ├── PublishButton [if not published]
│       └── DiscardChangesButton
│
├── TwoColumnLayout
│   ├── LeftPanel: FormEditor [CF3 - RO-Crate based]
│   │   ├── SectionTabs [grouped by schema]
│   │   │   ├── Identification
│   │   │   ├── Creators
│   │   │   ├── Content
│   │   │   ├── Context
│   │   │   ├── Technical
│   │   │   ├── Access
│   │   │   └── Distribution
│   │   │
│   │   ├── DynamicFormFields [schema-driven]
│   │   │   ├── TextField
│   │   │   ├── TextArea
│   │   │   ├── Dropdown [with vocabulary lookup]
│   │   │   ├── MultiSelect [tags]
│   │   │   ├── DatePicker
│   │   │   ├── URLInput
│   │   │   ├── FileUpload
│   │   │   └── RepeatingGroup [add/remove items]
│   │   │
│   │   └── InlineValidation
│   │       ├── RequiredFieldMarkers [*]
│   │       ├── FormatValidationMessages
│   │       └── SuggestionHints [from iKG]
│   │
│   └── RightPanel: AssistanceTools [CF1, CF3, CF4]
│       ├── RecommendationsWidget [CF3]
│       │   ├── SuggestedKeywords [click-to-add]
│       │   ├── RecommendedVocabularies
│       │   └── CompletenessScore [progress ring]
│       │
│       ├── SimilarDatasetsWidget [CF4]
│       │   ├── SearchCriteriaSummary
│       │   ├── SimilarResults [mini cards]
│       │   └── CompareButton → ComparisonModal
│       │
│       ├── ExternalSourcesWidget [CF1]
│       │   ├── ORCiDLookup [quick search]
│       │   ├── RORLookup
│       │   ├── PIDINSTLookup
│       │   └── PublicationImporter [DOI search]
│       │
│       └── ChangeHistoryWidget
│           ├── RecentChanges [timeline]
│           └── CompareVersionsButton
│
└── BottomPanel: RO-CratePreview
    ├── JSON-LDView [collapsible code editor]
    ├── GraphVisualization [nodes: entities, edges: relationships]
    └── ExportOptions [download RO-Crate package]
```

**Role Constraints:**
- `research_fellow`: Edit own datasets only
- `data_steward`: Edit all datasets (review/correction mode)
- `guest_viewer`, `admin`: No access

**Interaction Patterns:**
- Auto-save every 30 seconds
- Conflict detection for concurrent edits
- Undo/redo stack (last 20 actions)

---

## Abstract Model Tree 5: Metadata Review Dashboard (FAIR Phase: PRESERVE)

**Supported Core Functions:** CF2, CF3, CF4  
**Primary Roles:** `data_steward`

```
AbstractUI: ReviewDashboard
├── DashboardHeader
│   ├── Title: "Metadata Review Queue"
│   ├── FilterBar
│   │   ├── StatusFilter [pending | in-review | approved | revisions-requested]
│   │   ├── DateRangeFilter
│   │   ├── DomainFilter
│   │   └── ResearcherFilter [search]
│   │
│   └── StatsWidgets [row]
│       ├── PendingCount
│       ├── AvgReviewTime
│       ├── ApprovalRate
│       └── MyQueueCount
│
├── ReviewQueueTable
│   ├── TableHeaders
│   │   ├── DatasetTitle [sortable]
│   │   ├── Submitter [sortable]
│   │   ├── SubmissionDate [sortable]
│   │   ├── Domain [sortable]
│   │   ├── CompletenessScore [sortable]
│   │   ├── Status [sortable]
│   │   └── Actions
│   │
│   └── QueueRows [repeater]
│       ├── TitleCell [link: ReviewDetail]
│       ├── SubmitterCell [with ORCiD]
│       ├── DateCell
│       ├── DomainCell [badge]
│       ├── ScoreCell [progress bar]
│       ├── StatusCell [badge with color]
│       └── ActionsCell
│           ├── ReviewButton [primary]
│           └── QuickPreviewButton
│
└── BulkActionsBar [shown when items selected]
    ├── SelectAllCheckbox
    ├── AssignToMeButton
    ├── BatchApproveButton [if all pass validation]
    ├── BatchRequestRevisionsButton
    └── ExportSelectionButton
```

---

## Abstract Model Tree 6: Review Detail View (FAIR Phase: PRESERVE)

**Supported Core Functions:** CF2, CF3, CF4  
**Primary Roles:** `data_steward`

```
AbstractUI: ReviewDetail
├── ReviewHeader
│   ├── DatasetTitle
│   ├── SubmitterInfo [name, ORCiD, contact]
│   ├── SubmissionDate
│   └── ReviewAssignment
│       ├── AssignedTo [current reviewer]
│       └── ReassignButton → ReviewerSelectorModal
│
├── SplitView
│   ├── LeftPanel: MetadataReadOnly
│   │   └── [Same structure as ViewDatasetDetail]
│   │
│   └── RightPanel: ReviewTools
│       ├── ValidationReport
│       │   ├── SchemaValidation [pass/fail per section]
│       │   ├── FAIRnessScore [F,A,I,R subscores]
│       │   └── QualityChecks [warnings, errors]
│       │
│       ├── ReviewChecklist
│       │   ├── CompletenessCheck [checkbox]
│       │   ├── AccuracyCheck [checkbox]
│       │   ├── StandardsComplianceCheck [checkbox]
│       │   └── NotesField [textarea per item]
│       │
│       ├── CommunicationPanel
│       │   ├── MessageToSubmitter [textarea]
│       │   ├── InternalNotes [private textarea]
│       │   └── PreviousCorrespondence [accordion]
│       │
│       └── DecisionActions
│           ├── ApproveButton → ApproveConfirmationModal
│           ├── RequestRevisionsButton → RevisionRequestModal
│           │   ├── RevisionReason [required textarea]
│           │   ├── SpecificIssues [repeating]
│           │   │   ├── FieldReference [dropdown]
│           │   │   ├── IssueDescription [textarea]
│           │   │   └── SuggestedFix [optional textarea]
│           │   └── DueDate [datepicker]
│           │
│           └── EscalateButton [to senior steward]
│
└── TimelinePanel
    └── ActivityStream [chronological]
        ├── Submitted event
        ├── Assigned event
        ├── ReviewStarted event
        ├── Correspondence events
        └── Decision events
```

---

## Abstract Model Tree 7: Platform Configuration (FAIR Phase: SHARE)

**Supported Core Functions:** CF2, CF4  
**Primary Roles:** `admin`, `data_steward` (limited)

```
AbstractUI: PlatformConfiguration
├── ConfigHeader
│   ├── Title: "Target Platform Management"
│   └── AddPlatformButton → PlatformSelectorModal
│
├── PlatformList
│   └── PlatformCard [repeater]
│       ├── PlatformInfo
│       │   ├── PlatformName
│       │   ├── DomainBadge
│       │   ├── PluginVersion
│       │   └── ConnectionStatus [connected | error | not-configured]
│       │
│       ├── ConfigurationSection [collapsible]
│       │   ├── APIEndpoint [URL input]
│       │   ├── AuthenticationConfig
│       │   │   ├── AuthType [dropdown: OAuth2 | API-Key | Basic]
│       │   │   ├── CredentialsManager → CredentialVaultModal
│       │   │   └── TestConnectionButton
│       │   │
│       │   ├── SchemaMapping
│       │   │   ├── SourceSchema [EDO internal]
│       │   │   ├── TargetSchema [platform-specific]
│       │   │   ├── MappingEditor → MappingMatrixWidget
│       │   │   └── ValidationRules [editable list]
│       │   │
│       │   └── PublicationDefaults
│       │       ├── DefaultLicense [dropdown]
│       │       ├── DefaultAccessType [dropdown]
│       │       └── AutoPublishToggle [checkbox]
│       │
│       └── CardActions
│           ├── EditButton
│           ├── TestPublicationButton → TestPublicationModal
│           ├── DisableButton
│           └── DeleteButton [with confirmation]
│
└── PluginManagement [admin only]
    ├── InstalledPlugins [table]
    ├── AvailablePlugins [catalog browser] → PluginCatalogModal
    └── InstallPluginButton
```

**Role Constraints:**
- `admin`: Full access including plugin installation
- `data_steward`: Can configure existing platforms, cannot install plugins
- `research_fellow`: Can select from configured platforms during metadata creation (see CreateMetadataWizard Step6)
- `guest_viewer`: No access

---

## Abstract Model Tree 8: System Administration (FAIR Phase: Infrastructure)

**Supported Core Functions:** CF1, CF2, CF4  
**Primary Roles:** `admin`

```
AbstractUI: SystemAdministration
├── AdminNav
│   ├── UsersAndRoles
│   ├── InformationSources
│   ├── KnowledgeGraph
│   ├── PluginsAndIntegrations
│   ├── SystemMonitoring
│   └── BackupAndRecovery
│
├── Panel: UsersAndRoles
│   ├── UserTable [searchable, sortable]
│   │   └── UserRow
│   │       ├── Username
│   │       ├── Email
│   │       ├── Role [dropdown: change role]
│   │       ├── Status [active | suspended]
│   │       └── Actions [edit, suspend, delete]
│   │
│   ├── AddUserButton → CreateUserModal
│   └── BulkRoleAssignmentTool
│
├── Panel: InformationSources [CF1 configuration]
│   ├── SourceConnectorList
│   │   └── ConnectorCard [type: maDMP | ELN | SMS | IdentityProvider]
│   │       ├── ConnectorName
│   │       ├── ConnectionStatus
│   │       ├── LastSyncTime
│   │       ├── ConfigurationButton → ConnectorConfigModal
│   │       └── TestConnectionButton
│   │
│   └── SyncScheduleConfig
│       ├── FrequencySelector [hourly | daily | weekly | manual]
│       └── RunNowButton
│
├── Panel: KnowledgeGraph [CF2 infrastructure]
│   ├── KGStats
│   │   ├── EntityCount
│   │   ├── RelationshipCount
│   │   └── LastUpdateTime
│   │
│   ├── OntologyManagement
│   │   ├── LoadedOntologies [list]
│   │   ├── UploadOntologyButton
│   │   └── VocabularyEditor
│   │
│   └── ReasoningConfig
│       ├── InferenceRules [editable list]
│       └── EnableSemanticMatching [toggle]
│
├── Panel: SystemMonitoring
│   ├── HealthDashboard
│   │   ├── ServiceStatus [API | Database | Search | Queue]
│   │   ├── ResourceUsage [CPU, Memory, Disk]
│   │   └── ActiveUsers [real-time count]
│   │
│   ├── LogViewer
│   │   ├── LogLevelFilter
│   │   ├── TimeRangeFilter
│   │   └── LogStream [scrolling]
│   │
│   └── AlertConfiguration
│       ├── AlertRules [list]
│       └── NotificationChannels [email | slack | pagerduty]
│
└── Panel: BackupAndRecovery
    ├── BackupSchedule
    ├── LastBackupInfo
    ├── RestorePointSelector
    └── RunBackupNowButton
```

---

## Workflow Integration: FAIR Lifecycle Navigation

The Abstract UI models are connected through workflow transitions that mirror the FAIR Data Lifecycle:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FAIR WORKFLOW NAVIGATION                         │
│                                                                     │
│  PLAN                        COLLECT/PROCESS                        │
│  ┌──────────────┐            ┌──────────────┐                       │
│  │CreateMetadata│───────────▶│ EditMetadata │                       │
│  │   Wizard     │            │   (ELN/      │                       │
│  └──────────────┘            │    SMS)      │                       │
│                              └──────────────┘                       │
│                                     │                               │
│                                     ▼                               │
│  PRESERVE                      ANALYZE                              │
│  ┌───────────────┐            ┌───────────────┐                     │
│  │ReviewDashboard│◀───────────│EditMetadata   │                     │
│  │   (steward)   │            │(analysis link)│                     │
│  └───────────────┘            └───────────────┘                     │
│         │                                                           │
│         ▼                                                           │
│  SHARE                         REUSE                                │
│  ┌───────────────┐            ┌──────────────┐                      │
│  │PlatformConfig │───────────▶│BrowseCatalog │                      │
│  └───────────────┘            └──────────────┘                      │
│                                     │                               │
│                                     ▼                               │
│                              ┌─────────────────┐                    │
│                              │ViewDatasetDetail│                    │
│                              └─────────────────┘                    │
│                                     │                               │
│                                     └──────────────┐                │
│                                                    ▼                │
│                                             ┌───────────────┐       │
│                                             │CreateMetadata │       │
│                                             │(new iteration)│       │
│                                             └───────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
```

### Transition Rules

| From UI | To UI | Trigger | Role Constraint |
|---------|-------|---------|-----------------|
| CreateMetadataWizard | EditMetadata | Save Draft | research_fellow, data_steward |
| EditMetadata | ReviewDashboard | Submit for Review | research_fellow |
| ReviewDashboard | ReviewDetail | Click Review | data_steward |
| ReviewDetail | EditMetadata | Request Revisions | data_steward → research_fellow |
| ReviewDetail | ViewDatasetDetail | Approve & Publish | data_steward |
| ViewDatasetDetail | CreateMetadataWizard | Create Similar Dataset | research_fellow |
| BrowseCatalog | ViewDatasetDetail | Click Dataset Card | all roles |
| PlatformConfiguration | CreateMetadataWizard | Select during creation | research_fellow (select), admin (configure) |

---

## Accessibility Considerations

All Abstract UI models must satisfy:

- **WCAG 2.1 Level AA** compliance
- Keyboard navigation support
- Screen reader compatibility (ARIA labels)
- Color contrast ratios ≥ 4.5:1
- Focus indicators on all interactive elements
- Error messages linked to form fields

---

## Internationalization Support

All text content in Abstract UI models:

- Externalized in resource bundles
- Support for RTL languages
- Date/time format localization
- Number format localization
- Pluralization rules per locale

---

## Next Steps: Concretization

These Abstract UI models will be transformed into:

1. **Concrete UI Models:** Platform-specific implementations (React web app, iOS app, etc.)
2. **Final UI:** Rendered interfaces with actual styling and branding
3. **Interaction Logic:** Event handlers, state management, API integrations

---

*This document serves as the authoritative Abstract UI model specification for EDO, linking core functions, user roles, and FAIR lifecycle phases to concrete interface designs.*
