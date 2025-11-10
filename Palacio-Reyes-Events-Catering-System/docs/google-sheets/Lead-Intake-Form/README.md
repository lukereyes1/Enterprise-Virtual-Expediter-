# Lead Intake Form – Google Sheets Package

This folder provides CSV exports that mirror the Google Sheets workbook structure for the Lead Intake Form (Documentation 1.1). Import each CSV as a separate tab to recreate the recommended sheet.

## Tabs Included

1. **Form-Fields** – Complete field inventory with types, requirements, and option lists.
2. **Validation-Rules** – Data validation logic to enforce quality.
3. **Workflow** – Step-by-step guidance for sales teams and clients.
4. **Integration-Options** – Available submission and automation pathways.
5. **Auto-Response-Email** – Ready-to-use confirmation template.
6. **Performance-Metrics** – KPIs to monitor lead funnel health.

### Suggested Import Steps

1. Create a new Google Sheet.
2. Use **File → Import → Upload** for each CSV and choose *Insert new sheet(s)*.
3. Rename the tabs to match the file names for clarity.
4. Apply column widths, formatting, and protected ranges as needed.
5. Link the sheet to the Event Master Sheet or automation scripts per your integration plan.

## Notes

- All option lists are semi-colon delimited to simplify conversion into Google Sheets data validation lists.
- Internal-only fields (risk assessment, assignment, qualification score) should reside on protected tabs when sharing externally.
- The Auto-Response Email tab can feed directly into Apps Script templates or CRM automations.

For more detail on usage and business context, reference `docs/1.1-Lead-Intake-Form-DOCUMENTATION.md`.
