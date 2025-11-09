# 📁 Palacio Reyes Hospitality - System Guide

## Complete File Organization & Naming Convention

**Version:** 2.0.0 (Professional Structure)
**Last Updated:** November 2025
**System Owner:** Palacio Reyes Hospitality Operations

---

## 🎯 Quick Reference

### Event ID Format
```
PRH-YYYYMMDD-CLIENTKEY-VENUEKEY

Example: PRH-20251108-ASCEND-BHH
```

### Document Naming Convention
```
[EventID]_[DocType]_[ShortLabel]_vX.Y.[ext]

Example: PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx
```

---

## 📋 Table of Contents

1. [System Philosophy](#system-philosophy)
2. [Event ID Structure](#event-id-structure)
3. [Document Type Codes](#document-type-codes)
4. [Folder Structure](#folder-structure)
5. [Versioning Rules](#versioning-rules)
6. [Workflow Examples](#workflow-examples)
7. [Lookup Tables](#lookup-tables)
8. [Best Practices](#best-practices)

---

## System Philosophy

### Why This System Works

**Single Source of Truth:** Everything hangs off one canonical Event ID. No confusion, no duplicates, no lost files.

**Scannable Names:** You can see what a document is without opening it:
- `PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx` instantly tells you:
  - Event: November 8, 2025
  - Client: Ascend
  - Venue: Bob Hope Hall
  - Doc Type: Banquet Event Order
  - Label: Main event
  - Version: 1.0 (finalized)

**Structured Access:** Different teams access different folders:
- Sales → 0_SYSTEM templates + 1_PIPELINE tracking
- Operations → 2_EVENTS/[Year]/[EventID]/03_Operations
- Finance → 2_EVENTS/[Year]/[EventID]/02_Finance
- Management → 5_REPORTING analytics

**Scale-Ready:** Works equally well for 10 events/year or 500 events/year.

---

## Event ID Structure

### Format Breakdown

```
PRH - YYYYMMDD - CLIENTKEY - VENUEKEY
 │      │          │           │
 │      │          │           └─ Venue code (3-6 chars)
 │      │          └───────────── Client code (6-10 chars)
 │      └──────────────────────── Date of event (8 digits)
 └─────────────────────────────── Company prefix (PRH = Palacio Reyes Hospitality)
```

### Examples

| Event ID | Breakdown |
|----------|-----------|
| `PRH-20251108-ASCEND-BHH` | Nov 8, 2025 • Ascend Technologies • Bob Hope Hall |
| `PRH-20250312-GOOGLE-DTLA` | Mar 12, 2025 • Google • Downtown LA Convention Center |
| `PRH-20250914-WEDDCHEN-RIVGDN` | Sep 14, 2025 • Chen & Stevens Wedding • Riverside Gardens |
| `PRH-20250522-TECHVIS-MERID` | May 22, 2025 • TechVision Inc. • The Meridian Hotel |

### Key Rules

1. **Company Prefix**
   - `PRH` = Palacio Reyes Hospitality
   - Fixed 3-letter code for your company
   - Update globally if company name changes

2. **Date Format**
   - Always `YYYYMMDD` (ISO 8601 sortable)
   - Use EVENT DATE, not submission date
   - Example: November 8, 2025 = `20251108`

3. **CLIENTKEY**
   - 6-10 characters, uppercase, no spaces
   - Meaningful abbreviation of client name
   - Check `ClientKey_Lookup.csv` before creating new
   - Examples: `ASCEND`, `GOOGLE`, `WEDDCHEN`, `TECHVIS`

4. **VENUEKEY**
   - 3-6 characters, uppercase
   - Short memorable code for venue
   - Check `VenueKey_Lookup.csv` before creating new
   - Examples: `BHH`, `SIG`, `MERID`, `RIVGDN`, `DTLA`

### Creating New Keys

**New Client:**
1. Check `0_SYSTEM/03_Reference/ClientKey_Lookup.csv`
2. If client not found, create meaningful key:
   - Use company acronym or short name
   - 6-10 characters max
   - Must be unique
3. Add row to ClientKey_Lookup.csv
4. Use consistently for all future events

**New Venue:**
1. Check `0_SYSTEM/03_Reference/VenueKey_Lookup.csv`
2. If venue not found, create code:
   - Abbreviation of venue name
   - 3-6 characters
   - Easy to remember
3. Add row to VenueKey_Lookup.csv
4. Document utilities, access, complexity

---

## Document Type Codes

### Core DocType Codes

| Code | Document Type | Description | Typical Extension |
|------|--------------|-------------|-------------------|
| **LEAD** | Lead Intake Summary | Initial inquiry capture | `.pdf` `.json` |
| **PROP** | Quote / Proposal | Pricing and menu options | `.pdf` `.docx` |
| **AGR** | Master Service Agreement | Legal contract governing relationship | `.pdf` `.docx` |
| **SOW** | Statement of Work | Event-specific scope & deliverables | `.pdf` `.docx` |
| **INV-DEP** | Deposit Invoice | Initial payment invoice | `.pdf` `.xlsx` |
| **INV-BAL** | Balance Invoice | Final payment invoice | `.pdf` `.xlsx` |
| **INV-CO** | Change Order Invoice | Invoice for scope changes | `.pdf` `.xlsx` |
| **PAY-AUTH** | Payment Authorization Form | Card-on-file authorization | `.pdf` |
| **BEO** | Banquet Event Order | Comprehensive event execution document | `.xlsx` `.pdf` |
| **PACK** | Event Packet | Combined PDF of all key documents | `.pdf` |
| **PREP** | Prep List | Kitchen production task list | `.xlsx` |
| **PO** | Purchase Order | Purchasing/ordering guide | `.xlsx` `.pdf` |
| **STAFF** | Staffing Plan & Timesheets | Labor planning and tracking | `.xlsx` |
| **LOAD** | Load-Out / Pack-Out Checklist | Equipment and supply tracking | `.xlsx` `.pdf` |
| **INC** | Incident / Exception Report | Issue documentation | `.docx` `.pdf` |
| **P&L** | Event P&L | Profit & loss statement | `.xlsx` |
| **COI** | Certificate of Insurance | Insurance documentation | `.pdf` |
| **FBK** | Client Feedback Export | Post-event satisfaction survey | `.pdf` `.xlsx` |
| **PM** | Internal Postmortem | Lessons learned / retrospective | `.docx` `.pdf` |

### Document Naming Examples

```
PRH-20251108-ASCEND-BHH_PROP_CorporateTraining_v1.0.pdf
PRH-20251108-ASCEND-BHH_SOW_MainEvent_v1.0.pdf
PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx
PRH-20251108-ASCEND-BHH_INV-DEP_50pct_v1.0.pdf
PRH-20251108-ASCEND-BHH_P&L_Final_v1.0.xlsx
PRH-20251108-ASCEND-BHH_INC_GasShutdown_v1.0.docx
PRH-20251108-ASCEND-BHH_PM_Internal_v1.0.docx
```

### ShortLabel Guidelines

The `[ShortLabel]` segment provides context:

**For Proposals:**
- `_CorporateTraining`
- `_HolidayParty`
- `_AnnualGala`

**For Invoices:**
- `_50pct` (deposit amount)
- `_Final`
- `_AddDessert` (change order description)

**For BEOs:**
- `_Main` (primary event)
- `_Reception` (if separate from main)
- `_Breakfast` (for multi-meal events)

**For Purchase Orders:**
- `_Food`
- `_Rentals`
- `_Bar`

**For Incident Reports:**
- `_GasShutdown`
- `_LateDelivery`
- `_ClientComplaint`

---

## Folder Structure

### Top-Level Hierarchy

```
Palacio-Reyes-Events-Catering-System/
│
├── 0_SYSTEM/              ← Templates, reference, OS
├── 1_PIPELINE/            ← Live tracking & dashboards
├── 2_EVENTS/              ← Event-centric filing
├── 3_CLIENTS/             ← Client-centric view
├── 4_VENDORS/             ← Vendor management
├── 5_REPORTING/           ← Analytics & insights
│
├── 0_SYSTEM_GUIDE.md      ← This document
├── README.md              ← System overview
└── BRANDING-CONFIG.md     ← Customization reference
```

---

### 0_SYSTEM - Your Operating System

**Purpose:** All templates, rate cards, email scripts, and reference lookups.

```
0_SYSTEM/
│
├── 00_Templates/
│   ├── AGR_MasterServiceAgreement_Template.docx
│   ├── SOW_Template.docx
│   ├── BEO_Template.xlsx
│   ├── Proposal_Template_Corp.pdf
│   ├── Proposal_Template_NonProfit.pdf
│   ├── Invoice_Template.xlsx
│   ├── ChangeOrder_Template.docx
│   ├── PrepList_Template.xlsx
│   ├── StaffingPlan_Template.xlsx
│   ├── EventP&L_Template.xlsx
│   ├── IncidentReport_Template.docx
│   ├── Postmortem_Template.docx
│   ├── ClientFeedback_Form_Template.docx
│   ├── 1.1-Lead-Intake-Form.html
│   └── 1.1-Auto-Response-Email-Template.html
│
├── 01_RateCards/
│   ├── RateCard_Standard_2025.xlsx
│   ├── RateCard_NonProfit_2025.xlsx
│   └── RateCard_Archive/
│       ├── RateCard_Standard_2024.xlsx
│       └── RateCard_NonProfit_2024.xlsx
│
├── 02_EmailTemplates/
│   ├── Email_NewInquiry.txt
│   ├── Email_ProposalSent.txt
│   ├── Email_ContractAndDeposit.txt
│   ├── Email_FinalConfirmation_BEO.txt
│   ├── Email_DayBefore_Logistics.txt
│   ├── Email_PostEvent_ThankYou.txt
│   ├── Email_FeedbackRequest.txt
│   └── Email_Dispute_Response.txt
│
└── 03_Reference/
    ├── ClientKey_Lookup.csv
    ├── VenueKey_Lookup.csv
    └── Vendor_Cutoff_Times.csv
```

**Access:** All team members (read); Operations Manager (write)

---

### 1_PIPELINE - Live Tracking

**Purpose:** Global view of all active work and historical data.

```
1_PIPELINE/
│
├── EventMasterSheet.xlsx          ← Central tracking spreadsheet
├── Leads_Log.xlsx                  ← All inquiries (even declined)
├── ActiveEvents_Dashboard.xlsx     ← This month + next month view
└── Archive/
    ├── EventMasterSheet_2024.xlsx
    └── EventMasterSheet_2023.xlsx
```

**EventMasterSheet.xlsx Columns:**
- Event ID
- Client (linked to 3_CLIENTS)
- Venue
- Event Date
- Status (Lead / Proposal / Contract / Pre-Prod / Completed / Archived)
- Value (estimated revenue)
- Assigned To
- Key Doc Links:
  - Proposal URL
  - SOW URL
  - BEO URL
  - P&L URL
- Event Folder URL (link to 2_EVENTS/YYYY/EventID)

**Access:** All team members (read); Sales & Ops Managers (write)

---

### 2_EVENTS - Event-Centric Filing

**Purpose:** Complete lifecycle documentation per event.

```
2_EVENTS/
│
├── 2025/
│   ├── PRH-20251108-ASCEND-BHH/
│   │   ├── 01_Sales/
│   │   │   ├── PRH-20251108-ASCEND-BHH_LEAD_Intake_v1.0.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_PROP_CorpTraining_v0.9.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_PROP_CorpTraining_v1.0.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_AGR_Signed_v1.0.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_SOW_MainEvent_v1.0.pdf
│   │   │   └── PRH-20251108-ASCEND-BHH_PAY-AUTH_Signed_v1.0.pdf
│   │   │
│   │   ├── 02_Finance/
│   │   │   ├── PRH-20251108-ASCEND-BHH_INV-DEP_50pct_v1.0.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_INV-BAL_Final_v1.0.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_INV-CO_AddDessert_v1.0.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_P&L_Final_v1.0.xlsx
│   │   │   └── PRH-20251108-ASCEND-BHH_COI_Venue_v1.0.pdf
│   │   │
│   │   ├── 03_Operations/
│   │   │   ├── PRH-20251108-ASCEND-BHH_BEO_Main_v0.9.xlsx
│   │   │   ├── PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx
│   │   │   ├── PRH-20251108-ASCEND-BHH_PACK_EventPacket_v1.0.pdf
│   │   │   ├── PRH-20251108-ASCEND-BHH_PREP_Kitchen_v1.0.xlsx
│   │   │   ├── PRH-20251108-ASCEND-BHH_PO_Food_v1.0.xlsx
│   │   │   ├── PRH-20251108-ASCEND-BHH_PO_Rentals_v1.0.xlsx
│   │   │   ├── PRH-20251108-ASCEND-BHH_STAFF_Plan_v1.0.xlsx
│   │   │   ├── PRH-20251108-ASCEND-BHH_STAFF_Timesheets_v1.0.xlsx
│   │   │   └── PRH-20251108-ASCEND-BHH_LOAD_TruckChecklist_v1.0.xlsx
│   │   │
│   │   ├── 04_Logs_&_Incidents/
│   │   │   ├── PRH-20251108-ASCEND-BHH_LOG_EventDayNotes_v1.0.docx
│   │   │   ├── PRH-20251108-ASCEND-BHH_INC_GasShutdown_v1.0.docx
│   │   │   └── Photos/
│   │   │       ├── setup_001.jpg
│   │   │       ├── buffet_presentation_002.jpg
│   │   │       └── incident_gas_meter_003.jpg
│   │   │
│   │   └── 05_PostEvent/
│   │       ├── PRH-20251108-ASCEND-BHH_FBK_ClientExport_v1.0.pdf
│   │       └── PRH-20251108-ASCEND-BHH_PM_Internal_v1.0.docx
│   │
│   ├── PRH-20250312-GOOGLE-DTLA/
│   └── PRH-20250914-WEDDCHEN-RIVGDN/
│
├── 2024/
└── 2023/
```

**Subfolder Guide:**

| Folder | Purpose | Key Documents |
|--------|---------|--------------|
| **01_Sales** | Client acquisition & contracts | LEAD, PROP, AGR, SOW, PAY-AUTH |
| **02_Finance** | Payments & profitability | INV-DEP, INV-BAL, INV-CO, P&L, COI |
| **03_Operations** | Event execution | BEO, PACK, PREP, PO, STAFF, LOAD |
| **04_Logs_&_Incidents** | Day-of documentation | LOG, INC, Photos |
| **05_PostEvent** | Feedback & lessons | FBK, PM |

**Access:**
- Entire folder: Operations Manager
- 01_Sales: Sales Team
- 02_Finance: Finance Team
- 03_Operations: Kitchen & Event Staff
- 04_Logs: All staff (write); Management (review)
- 05_PostEvent: Management

---

### 3_CLIENTS - Client-Centric View

**Purpose:** Relationship management and client history.

```
3_CLIENTS/
│
├── ASCEND/
│   ├── ASCEND_MasterAgreement_AGR_v1.0.pdf
│   ├── ASCEND_Profile_Notes.docx
│   ├── ASCEND_PastEvents_List.xlsx
│   └── Communications/
│       ├── 2025-03-15_Email_NewContract.pdf
│       └── 2024-11-20_Email_PostEventFollowUp.pdf
│
├── GOOGLE/
├── TECHVIS/
└── WEDDCHEN/
```

**ASCEND_PastEvents_List.xlsx:**
| Event ID | Event Date | Event Type | Venue | Revenue | Satisfaction | Notes |
|----------|------------|------------|-------|---------|--------------|-------|
| PRH-20251108-ASCEND-BHH | 2025-11-08 | Corporate Training | Bob Hope Hall | $15,750 | 9/10 | Excellent execution |
| PRH-20231215-ASCEND-MERID | 2023-12-15 | Holiday Party | Meridian Hotel | $12,200 | 10/10 | Repeat client |

**Access:** Sales Team, Operations Manager

---

### 4_VENDORS - Vendor Management

**Purpose:** Supplier relationships, rate sheets, past orders.

```
4_VENDORS/
│
├── CommunityProvisions/
│   ├── CommunityProvisions_Agreement_2025.pdf
│   ├── CommunityProvisions_RateSheet_2025.xlsx
│   ├── CommunityProvisions_ContactInfo.docx
│   └── Past_POs/
│       ├── 2025_Orders_Summary.xlsx
│       └── Individual_POs/
│           ├── PRH-20251108-ASCEND-BHH_PO_Food_v1.0.xlsx
│           └── PRH-20250312-GOOGLE-DTLA_PO_Food_v1.0.xlsx
│
├── WorldwideProduce/
├── PartyRentalsInc/
└── LinenServiceCo/
```

**Access:** Operations Manager, Kitchen Manager

---

### 5_REPORTING - Analytics & Insights

**Purpose:** Aggregate data, trends, performance tracking.

```
5_REPORTING/
│
├── SalesByClient_2025.xlsx
├── SalesByVenue_2025.xlsx
├── MarginsByEventType_2025.xlsx
├── NonProfit_vs_Corp_Performance_2025.xlsx
├── IssueLog_Summary_2025.xlsx
├── StaffUtilization_2025.xlsx
├── VendorPerformance_2025.xlsx
└── Archive/
    ├── Annual_Report_2024.pdf
    └── Annual_Report_2023.pdf
```

**Key Reports:**

**SalesByClient_2025.xlsx:**
- Aggregates all events per client
- Total revenue, average deal size, frequency
- Identifies top clients for retention focus

**MarginsByEventType_2025.xlsx:**
- Corporate vs. Non-Profit vs. Private
- Average margin, high/low performers
- Pricing optimization insights

**IssueLog_Summary_2025.xlsx:**
- Rollup of all INC reports
- Categorization (Utilities, Venue, Client, Vendor, Staff)
- Trend analysis for systemic improvements

**Access:** Management, Finance Team

---

## Versioning Rules

### Version Number Format

```
vX.Y

X = Major version (0 or 1)
Y = Minor revision (0-9+)
```

### Version Progression

| Version | Status | Description | Example |
|---------|--------|-------------|---------|
| **v0.1** | Draft | Initial creation | First draft of BEO |
| **v0.2** | Draft | Internal revision | Updated after kitchen review |
| **v0.3** | Draft | Internal revision | Incorporated pricing changes |
| **v0.9** | Final Draft | Ready for client review | Sent to client for approval |
| **v1.0** | Approved | Client-approved / Executed | Signed contract or final BEO |
| **v1.1** | Post-Approval | Minor corrections (typos) | Fix spelling error in signed doc |

### Critical Rules

✅ **DO:**
- All drafts end at v0.9 maximum
- Client-approved documents become v1.0
- Stop reusing filename after v1.0 (create new doc for substantive changes)
- Keep all versions in folder for audit trail

❌ **DON'T:**
- Never delete old versions
- Don't skip version numbers
- Don't use v1.0 for drafts
- Don't exceed v1.9 (create new document instead)

### Examples

**BEO Workflow:**
```
PRH-20251108-ASCEND-BHH_BEO_Main_v0.1.xlsx  ← First draft
PRH-20251108-ASCEND-BHH_BEO_Main_v0.2.xlsx  ← Kitchen review incorporated
PRH-20251108-ASCEND-BHH_BEO_Main_v0.9.xlsx  ← Sent to client
PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx  ← Client approved (FINAL)
```

**Contract Workflow:**
```
PRH-20251108-ASCEND-BHH_SOW_MainEvent_v0.9.pdf  ← Sent for signature
PRH-20251108-ASCEND-BHH_SOW_MainEvent_v1.0.pdf  ← Executed/Signed (FINAL)
```

**Change Order:**
If client requests changes after v1.0 BEO:
```
PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx       ← Original
PRH-20251108-ASCEND-BHH_INV-CO_AddDessert_v1.0.pdf  ← Change order invoice
PRH-20251108-ASCEND-BHH_BEO_Main_v2.0.xlsx       ← Revised BEO (new major version)
```

---

## Workflow Examples

### Complete Event Lifecycle

#### 1. Lead Capture
```
Action: Client submits lead intake form
Creates:
  - Event ID: PRH-20251108-ASCEND-BHH
  - Row in 1_PIPELINE/EventMasterSheet.xlsx
  - File: 2_EVENTS/2025/PRH-20251108-ASCEND-BHH/01_Sales/PRH-20251108-ASCEND-BHH_LEAD_Intake_v1.0.pdf
```

#### 2. Qualification & Proposal
```
Action: Sales team qualifies lead, creates proposal
Creates:
  - 2_EVENTS/2025/PRH-20251108-ASCEND-BHH/01_Sales/PRH-20251108-ASCEND-BHH_PROP_CorpTraining_v0.9.pdf
  - Email sent using template: 0_SYSTEM/02_EmailTemplates/Email_ProposalSent.txt
Updates:
  - EventMasterSheet.xlsx: Status = "Proposal"
```

#### 3. Contract & Deposit
```
Action: Client approves proposal; signs contract
Creates:
  - PRH-20251108-ASCEND-BHH_AGR_Signed_v1.0.pdf
  - PRH-20251108-ASCEND-BHH_SOW_MainEvent_v1.0.pdf
  - PRH-20251108-ASCEND-BHH_PAY-AUTH_Signed_v1.0.pdf
  - PRH-20251108-ASCEND-BHH_INV-DEP_50pct_v1.0.pdf
Updates:
  - EventMasterSheet.xlsx: Status = "Contract"
  - 3_CLIENTS/ASCEND/ASCEND_PastEvents_List.xlsx: Add new row
```

#### 4. Event Planning & BEO
```
Action: Operations creates BEO, client reviews
Creates:
  - PRH-20251108-ASCEND-BHH_BEO_Main_v0.1.xlsx (draft)
  - PRH-20251108-ASCEND-BHH_BEO_Main_v0.9.xlsx (sent to client)
  - PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx (client approved)
  - PRH-20251108-ASCEND-BHH_INV-BAL_Final_v1.0.pdf
Updates:
  - EventMasterSheet.xlsx: Status = "Pre-Prod"
```

#### 5. Production
```
Action: Kitchen generates prep lists, purchasing
Creates:
  - PRH-20251108-ASCEND-BHH_PREP_Kitchen_v1.0.xlsx
  - PRH-20251108-ASCEND-BHH_PO_Food_v1.0.xlsx
  - PRH-20251108-ASCEND-BHH_PO_Rentals_v1.0.xlsx
  - PRH-20251108-ASCEND-BHH_STAFF_Plan_v1.0.xlsx
  - PRH-20251108-ASCEND-BHH_LOAD_TruckChecklist_v1.0.xlsx
Copies to:
  - 4_VENDORS/CommunityProvisions/Past_POs/Individual_POs/PRH-20251108-ASCEND-BHH_PO_Food_v1.0.xlsx
```

#### 6. Event Execution
```
Action: Event day service
Creates:
  - PRH-20251108-ASCEND-BHH_LOG_EventDayNotes_v1.0.docx
  - PRH-20251108-ASCEND-BHH_INC_GasShutdown_v1.0.docx (if issue occurred)
  - Photos/ folder with images
  - PRH-20251108-ASCEND-BHH_STAFF_Timesheets_v1.0.xlsx (actual hours)
```

#### 7. Post-Event
```
Action: Financial close-out, feedback, lessons learned
Creates:
  - PRH-20251108-ASCEND-BHH_P&L_Final_v1.0.xlsx
  - PRH-20251108-ASCEND-BHH_FBK_ClientExport_v1.0.pdf
  - PRH-20251108-ASCEND-BHH_PM_Internal_v1.0.docx
Updates:
  - EventMasterSheet.xlsx: Status = "Completed"
  - 3_CLIENTS/ASCEND/ASCEND_PastEvents_List.xlsx: Update satisfaction score
  - 5_REPORTING/IssueLog_Summary_2025.xlsx: Add incident row (if applicable)
```

#### 8. Archive (30 days post-event)
```
Action: Move to archive, maintain links
Updates:
  - EventMasterSheet.xlsx: Status = "Archived"
Optional:
  - Move entire event folder to: 2_EVENTS/2025_ARCHIVE/PRH-20251108-ASCEND-BHH/
  - Maintain URL links in EventMasterSheet for retrieval
```

---

## Lookup Tables

### ClientKey_Lookup.csv

**Location:** `0_SYSTEM/03_Reference/ClientKey_Lookup.csv`

**Purpose:** Standardize client keys; prevent duplicates; maintain metadata.

**Columns:**
- Client Key (unique)
- Legal Client Name
- Short Display Name
- Client Type (Corporate / Non-Profit / Private)
- Primary Contact
- Email
- Phone
- Billing Entity
- Active Status
- Notes

**Workflow:**
1. New inquiry arrives
2. Search client name in lookup table
3. If found → use existing CLIENTKEY
4. If not found → create new key, add row to table
5. Use key in Event ID

### VenueKey_Lookup.csv

**Location:** `0_SYSTEM/03_Reference/VenueKey_Lookup.csv`

**Purpose:** Standardize venue codes; document venue logistics.

**Columns:**
- Venue Key (unique)
- Venue Full Name
- Address, City, State, ZIP
- Venue Type
- Venue Contact Name & Phone
- Utilities Available (Power, Gas, Water)
- Kitchen Access (Full, Prep Only, None)
- Loading Dock (Yes, Loading Area, None)
- Parking (Ample, Limited, Valet, Street)
- Max Capacity
- Complexity Rating (Low, Medium, High)
- Notes

**Workflow:**
1. Client specifies venue
2. Search venue name in lookup table
3. If found → use existing VENUEKEY; review logistics notes
4. If not found → create code, add row, document utilities/access
5. Use key in Event ID

**Complexity Ratings:**
- **Low:** Established venue, full utilities, easy access, past experience
- **Medium:** Some limitations (utilities, parking, access); manageable
- **High:** Significant challenges (no kitchen, limited power, remote, permitting)

---

## Best Practices

### File Naming

✅ **DO:**
- Always use full Event ID
- Use standard DocType codes
- Include version numbers
- Use underscores `_` to separate segments
- Use descriptive ShortLabels

❌ **DON'T:**
- Use spaces in filenames
- Abbreviate Event ID
- Omit version numbers
- Use special characters (except `_` and `-`)
- Create ambiguous names like "Final Final v2"

### Folder Organization

✅ **DO:**
- Keep all event docs in one event folder
- Maintain subfolder structure (01_Sales, 02_Finance, etc.)
- Store templates in 0_SYSTEM only
- Link to docs from EventMasterSheet
- Archive old years annually

❌ **DON'T:**
- Scatter event docs across multiple locations
- Save working drafts to desktop/downloads
- Edit templates directly (make copies)
- Delete old versions
- Mix personal files with business docs

### Version Control

✅ **DO:**
- Increment version with each substantive change
- Keep all versions in folder
- Mark client-approved docs as v1.0
- Document what changed in version notes

❌ **DON'T:**
- Overwrite previous versions
- Skip version numbers
- Use v1.0 for drafts
- Create confusing version labels

### Collaboration

✅ **DO:**
- Use cloud storage (Google Drive, Dropbox, OneDrive)
- Set appropriate folder permissions
- Communicate document locations via EventMasterSheet
- Use version history features

❌ **DON'T:**
- Email documents without context
- Create duplicate "my version" files
- Work offline without syncing
- Share sensitive docs insecurely

### Maintenance

✅ **DO:**
- Update lookup tables promptly
- Review EventMasterSheet weekly
- Archive completed events monthly
- Backup system monthly
- Audit folder structure quarterly

❌ **DON'T:**
- Let lookup tables get stale
- Ignore orphaned files
- Delay archiving indefinitely
- Skip backups

---

## Troubleshooting

### Problem: Can't find a document

**Solution:**
1. Check EventMasterSheet.xlsx for direct links
2. Navigate to 2_EVENTS/[Year]/[EventID]/
3. Look in appropriate subfolder (01_Sales, 02_Finance, etc.)
4. Search by Event ID if using cloud storage search

### Problem: Duplicate Event IDs

**Cause:** Two events on same date with same client and venue

**Solution:**
- Add suffix to second event: `PRH-20251108-ASCEND-BHH-B`
- Or use different VENUEKEY if different venue
- Document in EventMasterSheet notes

### Problem: Client or venue not in lookup table

**Solution:**
1. Create meaningful key (check for similar existing keys)
2. Add row to appropriate lookup CSV
3. Document all required fields
4. Use new key going forward

### Problem: Version confusion

**Solution:**
- Highest version number in folder is latest
- v1.0 is always the approved version
- Check file modified date if uncertain
- Reference EventMasterSheet links for definitive versions

---

## Migration from Old System

If you have existing events in a different file structure:

### Step 1: Create Event IDs
1. Open existing event list
2. For each event, generate Event ID using format:
   - `PRH-YYYYMMDD-CLIENTKEY-VENUEKEY`
3. Add to EventMasterSheet.xlsx

### Step 2: Populate Lookup Tables
1. Extract unique client names → create ClientKey_Lookup.csv
2. Extract unique venues → create VenueKey_Lookup.csv

### Step 3: Create Event Folders
1. For each event, create: `2_EVENTS/[Year]/[EventID]/`
2. Create subfolders: 01_Sales, 02_Finance, 03_Operations, etc.

### Step 4: Rename & Move Documents
1. Locate existing event documents
2. Rename to standard format: `[EventID]_[DocType]_[ShortLabel]_vX.Y.[ext]`
3. Move to appropriate subfolder

### Step 5: Update Links
1. In EventMasterSheet, add URLs to key documents
2. Verify all links work

### Step 6: Archive
1. Move old file structure to `_ARCHIVE_OldSystem/`
2. Keep for reference for 90 days
3. Delete after verifying new system is complete

---

## System Checklist

Use this checklist to ensure system compliance:

### Setup (One-Time)
- [ ] Created top-level folder structure (0-5)
- [ ] Populated ClientKey_Lookup.csv
- [ ] Populated VenueKey_Lookup.csv
- [ ] Moved templates to 0_SYSTEM/00_Templates/
- [ ] Set up EventMasterSheet.xlsx in 1_PIPELINE/
- [ ] Configured folder permissions by team role

### Per Event (Recurring)
- [ ] Generated Event ID using proper format
- [ ] Checked/updated ClientKey_Lookup.csv
- [ ] Checked/updated VenueKey_Lookup.csv
- [ ] Created event folder: 2_EVENTS/[Year]/[EventID]/
- [ ] Created subfolders: 01_Sales through 05_PostEvent
- [ ] Added row to EventMasterSheet.xlsx
- [ ] Named all documents using standard convention
- [ ] Versioned all documents correctly
- [ ] Linked key docs in EventMasterSheet
- [ ] Archived event 30 days post-completion

### Monthly Maintenance
- [ ] Reviewed EventMasterSheet for stale leads
- [ ] Archived completed events
- [ ] Updated lookup tables with new clients/venues
- [ ] Backed up entire system
- [ ] Generated 5_REPORTING analytics

### Quarterly Review
- [ ] Audited folder structure for orphaned files
- [ ] Reviewed and updated templates
- [ ] Verified lookup tables are accurate
- [ ] Updated rate cards (if needed)
- [ ] Trained team on any system changes

---

## Quick Reference Card

**📌 PRINT THIS PAGE**

### Event ID Format
```
PRH-YYYYMMDD-CLIENTKEY-VENUEKEY
Example: PRH-20251108-ASCEND-BHH
```

### Document Naming
```
[EventID]_[DocType]_[ShortLabel]_vX.Y.[ext]
Example: PRH-20251108-ASCEND-BHH_BEO_Main_v1.0.xlsx
```

### Common DocType Codes
| Code | Document |
|------|----------|
| LEAD | Lead Intake |
| PROP | Proposal |
| AGR | Master Agreement |
| SOW | Statement of Work |
| BEO | Banquet Event Order |
| INV-DEP | Deposit Invoice |
| INV-BAL | Balance Invoice |
| P&L | Event P&L |

### Versioning
- v0.1 - v0.9 = Drafts
- v1.0 = Client Approved
- v1.1+ = Post-approval revisions

### Lookup Tables
- `0_SYSTEM/03_Reference/ClientKey_Lookup.csv`
- `0_SYSTEM/03_Reference/VenueKey_Lookup.csv`

### Event Master Sheet
- `1_PIPELINE/EventMasterSheet.xlsx`

---

**Document Version:** 2.0.0
**Last Updated:** November 2025
**Owner:** Palacio Reyes Hospitality Operations Team
**Next Review:** February 2026

For questions about this system, contact your Operations Manager.
