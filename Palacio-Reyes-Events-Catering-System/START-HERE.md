# 🎯 START HERE – Palacio Reyes Events & Catering System

## Welcome to Your Professional Catering Management System

**Provider:** Palacio Reyes Hospitality (“Caterer”)  
**Brand:** Palacio Reyes Events & Catering  
**Status:** ✅ Section 1.1 (Lead Intake System) – COMPLETE & PRODUCTION-READY

---

## 📦 What You Just Received

A complete, professional-grade document management system for your catering and events business. This is not a basic template collection; it is a comprehensive operational system designed for a chef-led, boutique hospitality group.

### What's Included (Section 1.1):

✅ **Interactive Lead Intake Form** – Mobile-responsive web form  
✅ **Event Master Sheet** – Central tracking spreadsheet (Google Sheets/Excel)  
✅ **Auto-Response Emails** – Professional client communication templates  
✅ **JSON Schema** – Data validation for integrations  
✅ **Sample Data** – Real-world examples (corporate gala, wedding)  
✅ **Complete Documentation** – Step-by-step setup and usage guides  
✅ **File Structure** – Professional folder organization (0_SYSTEM through 5_REPORTING)  
✅ **Lookup Tables** – Client and Venue standardization  
✅ **Branding Guide** – Customization template (`BRANDING-CONFIG.md`)

---

## 🪟 Brand Snapshot – Palacio Reyes Hospitality

These are the core brand details this system is designed around. They should also be reflected in `BRANDING-CONFIG.md`.

**Company & Identity**

- **Operating Name:** Palacio Reyes Events & Catering  
- **Legal Business Name:** Palacio Reyes Hospitality  
- **Brand Positioning:** Heritage-meets-contemporary, chef-driven modern hospitality  
- **Tagline/Slogan:**  
  > Palacio Reyes Hospitality is a chef-founded boutique hospitality group that builds and operates distinctive restaurants, food media, and experiential events, all centered on high-integrity cooking, design, and storytelling.

**Contact & Legal**

- **Service Provider:** Palacio Reyes Hospitality (“Caterer”)  
- **Address:** 355 S Grand Ave Ste 2450-100A, Los Angeles, CA 90071  
- **Contact:** Luke Reyes, Chef  
- **Phone:** 310-754-0849  
- **Email:** Luke@ritasdeluxe.com  
- **EIN:** 39-224363  

**Logo & System**

- **Logo System:** Primary wordmark (“Palacio Reyes Hospitality”) + secondary line (“Palacio Reyes Events & Catering”), with a supporting PRH monogram for icons and stamps.
- **Typography:**  
  - Editorial serif: TeX Gyre Pagella  
  - Clean grotesque: TeX Gyre Heros  
- **Color Palette (Core):**  
  - Forest Green `#2C4A3E` – primary brand color  
  - Warm Ivory `#F5F1E8` – background / paper color  
  - Oxblood `#6B2C2C` – accent, rules, emphasis  
  - Charcoal `#3A3A3A` – body text and details  

These values are the defaults assumed across templates. You can refine or extend them in `BRANDING-CONFIG.md`.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Choose Your Starting Point

**Option A: Test Drive (Fastest)**  
1. Open `0_SYSTEM/00_Templates/1.1-Lead-Intake-Form.html` in your web browser  
2. Fill out the form with sample data  
3. Click “Submit” to see the Event ID generation  
4. Click “Export as JSON” to inspect the data format

**Option B: Production Setup (Recommended)**  
1. Read `0_SYSTEM_GUIDE.md` (≈15 minutes)  
2. Fill out `BRANDING-CONFIG.md` with the PRH details above  
3. Import `1_PIPELINE/1.1-Event-Master-Sheet-Template.csv` into Google Sheets  
4. Update the HTML templates with your logo, colors, and contact information  
5. Deploy the Lead Intake Form to your website or staging server

---

## 📚 Essential Documents (Read These First)

### 1. System Overview
- **File:** `README.md`  
- **Read Time:** ≈10 minutes  
- **Purpose:** Understand the entire system architecture and roadmap

### 2. File Organization Guide
- **File:** `0_SYSTEM_GUIDE.md`  
- **Read Time:** ≈20 minutes  
- **Purpose:** Learn the professional file naming and folder structure  
- **Key Topics:**
  - Event ID format: `PRH-YYYYMMDD-CLIENTKEY-VENUEKEY`
  - Document naming: `[EventID]_[DocType]_[ShortLabel]_vX.Y.[ext]`
  - Folder structure: `0_SYSTEM` through `5_REPORTING`
  - Versioning rules

### 3. Lead Intake Form Guide
- **File:** `docs/1.1-Lead-Intake-Form-DOCUMENTATION.md`  
- **Read Time:** ≈15 minutes  
- **Purpose:** Deploy and customize the lead intake form  
- **Key Topics:**
  - How to embed on your website
  - Integration options (Google Sheets, CRM, email)
  - Customization guide
  - Troubleshooting

### 4. Event Master Sheet Guide
- **File:** `docs/1.1-Event-Master-Sheet-GUIDE.md`  
- **Read Time:** ≈15 minutes  
- **Purpose:** Set up your central tracking system  
- **Key Topics:**
  - Import to Google Sheets/Excel
  - Conditional formatting
  - Formulas and automation
  - Views and filters

### 5. Branding Configuration
- **File:** `BRANDING-CONFIG.md`  
- **Read Time:** ≈10 minutes  
- **Purpose:** Customize all templates with your business information  

Fill in: company details, legal entity, contact block, colors, typography, social links, and any updated URLs (website, scheduling, email platform).

---

## 🗂️ Folder Structure at a Glance

```text
Palacio-Reyes-Events-Catering-System/
│
├── 0_SYSTEM/                    ← Templates & reference materials
│   ├── 00_Templates/            ← All form and document templates
│   ├── 02_EmailTemplates/       ← Email scripts and auto-responses
│   └── 03_Reference/            ← ClientKey & VenueKey lookup tables
│
├── 1_PIPELINE/                  ← Central tracking (Event Master Sheet)
│
├── 2_EVENTS/                    ← Event-specific documents (organized by year)
│   └── [YYYY]/                  ← Year folders
│       └── [EventID]/           ← Individual event folders
│           ├── 01_Sales/        ← Proposals, contracts, SOWs
│           ├── 02_Finance/      ← Invoices, P&L, insurance
│           ├── 03_Operations/   ← BEOs, prep lists, staffing
│           ├── 04_Logs_&_Incidents/  ← Day-of notes, photos
│           └── 05_PostEvent/    ← Feedback, postmortems
│
├── 3_CLIENTS/                   ← Client relationship management
├── 4_VENDORS/                   ← Vendor documentation
├── 5_REPORTING/                 ← Analytics and insights
│
├── docs/                        ← Usage guides and documentation
├── examples/                    ← Sample filled forms
├── schemas/                     ← JSON validation schemas
│
├── START-HERE.md                ← This file
├── README.md                    ← System overview
├── 0_SYSTEM_GUIDE.md            ← Complete file structure guide
└── BRANDING-CONFIG.md           ← Customization template

```

---

#
🎨 Customization Checklist
Before using the system in production:

Branding
 Fill out BRANDING-CONFIG.md with Palacio Reyes details

 Update company name and legal name in all templates

 Add your logo and monogram to HTML/PDF templates

 Update color scheme in CSS to PRH palette

 Update contact information (phone, email, address)

 Add social media links

Lookup Tables
 Review 0_SYSTEM/03_Reference/ClientKey_Lookup.csv

 Add existing clients with consistent CLIENTKEY values

 Review 0_SYSTEM/03_Reference/VenueKey_Lookup.csv

 Add frequently used venues with VENUEKEY values

Event Master Sheet
 Import 1_PIPELINE/1.1-Event-Master-Sheet-Template.csv to Google Sheets

 Set up conditional formatting (see guide)

 Configure access permissions for your team

 Test with sample data

Lead Intake Form
 Update logo, colors, and PRH-specific copy

 Test on desktop and mobile

 Configure form submission (Sheets, CRM, email)

 Set up auto-response email

Email Templates
 Replace all {{PLACEHOLDER}} values

 Add PRH signature and masthead details

 Configure email platform integration

 Send test emails

🔧 Integration Options
Option 1: Google Sheets (Easiest)
Best for: Small to medium operations (≈1–50 events/month)

Setup:

Import Event Master Sheet CSV to Google Sheets

Use the HTML lead intake form or a Google Form mirroring the same fields

Use Google Apps Script to auto-populate the sheet from form submissions

Use Gmail + templates for auto-response emails

Pros: Free, simple, collaborative
Cons: Limited automation at scale

Option 2: CRM System (Most Powerful)
Best for: Growing operations with more automation

Platforms: Salesforce, HubSpot, Zoho, Pipedrive, etc.

Setup:

Import contacts and deals from Event Master Sheet

Customize fields to align with lead intake form

Set up web-to-lead form or API integration

Configure email templates and workflows

Pros: Automation, reporting, scalability
Cons: Cost and learning curve

Option 3: Hybrid (Recommended)
Best for: Most catering businesses

Setup:

Use Google Sheets for Event Master Sheet

Host HTML form on your site

Use Zapier/Make.com to connect form → Sheets → CRM or email platform

Use Mailchimp, SendGrid, or similar for email automation

Pros: Flexible, cost-efficient, future-proof
Cons: Requires light technical setup

📖 Learning Path
Week 1: Understanding the System
 Read README.md

 Read 0_SYSTEM_GUIDE.md

 Review sample data in examples/

 Test the Lead Intake Form end-to-end

Week 2: Customization
 Complete BRANDING-CONFIG.md with PRH details

 Update all templates with your masthead and colors

 Set up Event Master Sheet in Google Sheets

 Create your first test event

Week 3: Integration
 Deploy Lead Intake Form to your website or a staging URL

 Set up auto-response email workflow

 Connect form → sheet → CRM or email platform

 Test full workflow with a real inquiry

Week 4: Team Training
 Train sales/front-of-house on lead intake process

 Train operations on Event Master Sheet and folder usage

 Document PRH-specific workflows and policies

 Gather feedback and adjust

💡 Pro Tips
Event ID Best Practices
Event ID: PRH-YYYYMMDD-CLIENTKEY-VENUEKEY

Example: PRH-20251108-ASCEND-BHH

Always check lookup tables before creating new keys

Keep CLIENTKEY and VENUEKEY short and consistent

Update lookup tables as soon as you add new clients or venues

Use the same key consistently for repeat clients

Document Versioning
All drafts end at v0.9

Client-approved documents become v1.0

Do not delete old versions; keep a clear audit trail

Use descriptive ShortLabels (e.g., _Main, _Reception, _AddDessert)

Folder Organization
Keep all event documents inside the event’s folder in 2_EVENTS/[Year]/[EventID]/

Use subfolders (01_Sales, 02_Finance, 03_Operations, etc.) consistently

Link critical documents from the Event Master Sheet

Archive completed events annually

Data Security
Set appropriate folder permissions by role

Avoid sending sensitive data in unsecured channels

Back up the Event Master Sheet regularly

Keep payment processing in PCI-compliant tools

🆘 Common Questions
Q: Where do I start if I have existing clients?
A:

Add them to ClientKey_Lookup.csv with new CLIENTKEY values

Create folders in 3_CLIENTS/[CLIENTKEY]/

Add historical events to Event Master Sheet

Archive old event documents in 2_EVENTS/[Year]/[EventID]/

Q: Can I change the Event ID format?
A: Yes, but do it before production use. If you change it, update:

Lead Intake Form JavaScript (Event ID generator)

All documentation references

Lookup table examples

Any formulas that parse EventID components

Q: What if I don’t use Google Sheets?
A: The CSV templates work with Excel, Airtable, Notion, or similar. Import, then replicate views and formulas based on your tool.

Q: How do I integrate with my website?
A:

Embed the HTML form directly (upload 1.1-Lead-Intake-Form.html to your host), or

Recreate the form in your website builder (Squarespace, Wix, WordPress) using the same fields, or

Use an API-based approach that posts JSON conforming to schemas/lead-intake-schema.json.

Q: What comes after Section 1.1?
A: Planned sections include:

1.2–1.9: Sales & Contracting (quotes, contracts, invoices)

2.1–2.6: Operations & Kitchen (BEOs, prep lists, staffing)

3.1–3.3: Finance & Compliance (P&L, insurance, vendors)

4.1–4.3: Post-Event & Client Experience (feedback, postmortems)

🎯 Success Metrics
Track these KPIs to measure effectiveness:

Lead Management
Response Time: < 24 hours from submission to first contact

Qualification Rate: > 60% of leads become qualified opportunities

Conversion Rate: > 30% of quotes convert to contracts

Operational Efficiency
Time to BEO: < 7 days from contract signing to final BEO

Document Accuracy: > 95% error-free finals

Adoption: 100% of active events appear in the Event Master Sheet

Client Experience
Satisfaction Score: > 9/10

Repeat Client Rate: > 40% year-over-year

Referral Rate: > 25% of new business from referrals

📞 Support Resources
Documentation
README.md – System overview

0_SYSTEM_GUIDE.md – File organization

docs/1.1-Lead-Intake-Form-DOCUMENTATION.md – Form setup

docs/1.1-Event-Master-Sheet-GUIDE.md – Tracking setup

BRANDING-CONFIG.md – Brand customization guide

Examples
examples/lead-intake-sample-01-corporate-gala.json

examples/lead-intake-sample-02-wedding-reception.json

Technical References
schemas/lead-intake-schema.json – Data validation rules

Lookup tables in 0_SYSTEM/03_Reference/

🚀 Next Steps
Today: Read this document and 0_SYSTEM_GUIDE.md

This Week: Complete BRANDING-CONFIG.md and update templates with PRH branding

Next Week: Set up Event Master Sheet and test a full workflow

This Month: Deploy lead intake form and train your team

✅ System Checklist
Initial Setup
 Read START-HERE.md

 Read 0_SYSTEM_GUIDE.md

 Review sample data

 Test Lead Intake Form

 Complete BRANDING-CONFIG.md with PRH information

 Update templates with masthead, colors, and contact details

 Set up Event Master Sheet

 Configure team permissions

First Event
 Receive lead inquiry

 Capture via Lead Intake Form

 Generate Event ID

 Add to Event Master Sheet

 Send auto-response email

 Create event folder in 2_EVENTS/

 Link documents in Event Master Sheet

Production Launch
 Deploy form to website

 Train sales and ops teams

 Set up backups

 Configure automation (optional)

 Monitor adoption and performance

📌 Versioning
Version: 1.0.1
Last Updated: November 2025
Created For: Palacio Reyes Hospitality (Palacio Reyes Events & Catering)
