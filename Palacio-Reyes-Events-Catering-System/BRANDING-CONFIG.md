# 🎨 Branding Configuration Template

## Instructions

Fill out this template with your business information. Use these values when customizing all documents and templates in the system.

**TIP:** Keep this file updated and reference it whenever you customize a new template.

---

## Company Information

### Basic Details
```
Company Name:         Palacio Reyes Events & Catering
Legal Business Name:  [Your Legal Entity Name, if different]
Tagline/Slogan:       Exceptional Catering for Memorable Moments
```

### Contact Information
```
Primary Phone:        [Your Phone Number]
        Format:       (555) 555-5555

Primary Email:        [Your Email Address]
        Format:       events@yourcompany.com

Website URL:          [Your Website]
        Format:       https://www.yourwebsite.com

Business Address:     [Your Full Address]
        Format:       123 Main Street, Suite 100
                      City, State ZIP
```

### Social Media
```
Instagram:            [Your Instagram URL]
        Format:       https://instagram.com/yourhandle

Facebook:             [Your Facebook URL]
        Format:       https://facebook.com/yourpage

LinkedIn:             [Your LinkedIn URL]
        Format:       https://linkedin.com/company/yourcompany

Pinterest:            [Your Pinterest URL - Optional]
TikTok:               [Your TikTok URL - Optional]
```

---

## Brand Colors

### Primary Color Palette
```
Primary Color 1:      #1e3c72  (Deep Blue)
Primary Color 2:      #2a5298  (Royal Blue)
Accent Color:         #667eea  (Purple-Blue)
Secondary Accent:     #764ba2  (Purple)

Light Background:     #f8f9ff  (Very Light Blue)
Dark Background:      #1e3c72  (Deep Blue)
```

### Usage Guide
- **Primary Colors** - Headers, navigation, major sections
- **Accent Colors** - Buttons, highlights, call-to-action elements
- **Backgrounds** - Content sections, alternating rows

### How to Update in Templates

**HTML/CSS Files:**
```css
/* Find and replace these color codes */
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);  /* Update both colors */
background-color: #667eea;  /* Accent color */
border-color: #667eea;      /* Accent color */
```

**Color Picker Tools:**
- Adobe Color: https://color.adobe.com
- Coolors: https://coolors.co
- HTML Color Codes: https://htmlcolorcodes.com

---

## Logo & Images

### Logo Files
```
Primary Logo:         [Path or URL to your logo]
        Format:       PNG with transparent background
        Size:         Minimum 800px width for print quality

Secondary Logo:       [Alternative version - white/inverted]
Icon/Favicon:         [Small square icon version]
        Size:         512x512px recommended
```

### How to Add Logo to Templates

**HTML Templates (Lead Intake Form, Emails):**
```html
<!-- Find this section in the header -->
<h1>🍽️ Palacio Reyes Events & Catering</h1>

<!-- Replace with -->
<img src="your-logo.png" alt="Your Company Name" style="max-width: 200px; margin-bottom: 15px;">
<h1>Your Company Name</h1>

<!-- Or use a URL -->
<img src="https://yourwebsite.com/images/logo.png" alt="Your Company Name">
```

### Brand Photography
```
Event Photo Library:  [Link to your photo library]
Food Photography:     [Link to food photos]
Team Photos:          [Link to team headshots]
Venue Photos:         [Link to venue portfolio]
```

---

## Team Information

### Primary Contacts for Templates

**Sales Team Lead:**
```
Name:                 [Name]
Title:                [Title - e.g., "Events Director"]
Email:                [Email]
Phone:                [Phone]
Photo:                [Optional - URL to headshot]
```

**Operations Manager:**
```
Name:                 [Name]
Title:                [Title]
Email:                [Email]
Phone:                [Phone]
```

**Executive Chef:**
```
Name:                 [Name]
Title:                [Title]
Email:                [Email]
Phone:                [Phone]
```

### Email Signature Format
```
[Name]
[Title]
Palacio Reyes Events & Catering
[Phone] | [Email]
[Website]
[Social Media Icons/Links]
```

---

## Email Template Variables

Use these when customizing email templates:

### Auto-Response Email Placeholders
```
{{CLIENT_NAME}}        → Client's first name
{{EVENT_DESCRIPTION}}  → Brief event description
{{EVENT_DATE}}         → Event date in readable format
{{EVENT_ID}}           → Auto-generated Event ID
{{SCHEDULING_LINK}}    → Your Calendly/scheduling URL
{{SENDER_NAME}}        → Your name or "Events Team"
{{SENDER_TITLE}}       → Your title
{{PHONE_NUMBER}}       → Your business phone
{{EMAIL_ADDRESS}}      → Your business email
{{WEBSITE_URL}}        → Your website
{{CURRENT_YEAR}}       → Current year (auto-update annually)
{{BUSINESS_ADDRESS}}   → Your full address
{{INSTAGRAM_URL}}      → Your Instagram
{{FACEBOOK_URL}}       → Your Facebook
{{LINKEDIN_URL}}       → Your LinkedIn
{{PRIVACY_POLICY_URL}} → Link to your privacy policy
{{UNSUBSCRIBE_URL}}    → Unsubscribe link
```

### Actual Values (Fill In)
```
SCHEDULING_LINK:       [Your Calendly or scheduling tool URL]
PRIVACY_POLICY_URL:    [Link to your privacy policy page]
UNSUBSCRIBE_URL:       [Your email unsubscribe link]
```

---

## Typography

### Font Families
```
Primary Font:         'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
Heading Font:         Same as primary (or specify custom font)
Monospace Font:       'Courier New', monospace (for Event IDs)
```

### Custom Fonts (Optional)
If you want to use custom fonts (e.g., from Google Fonts):

```html
<!-- Add to <head> section of HTML templates -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Your+Font+Name&display=swap" rel="stylesheet">

<!-- Update CSS -->
<style>
body {
    font-family: 'Your Font Name', sans-serif;
}
</style>
```

**Recommended Font Pairings:**
- **Professional/Corporate:** Roboto + Roboto Slab
- **Elegant/Luxury:** Playfair Display + Lato
- **Modern/Clean:** Montserrat + Open Sans
- **Classic/Traditional:** Merriweather + Lato

---

## Legal & Compliance

### Business Registration
```
Business License #:   [Your License Number]
EIN/Tax ID:           [Your Tax ID]
Insurance Provider:   [Your Insurance Company]
Policy Number:        [Policy Number]
Coverage Amount:      [Coverage Amount - e.g., $2M General Liability]
```

### Certifications & Permits
```
Health Department:    [Permit Number & Expiration]
Liquor License:       [If applicable]
Food Handler Certs:   [List certified team members]
ServSafe:             [Certification details]
```

### Legal Disclaimers

**Allergen Disclaimer:**
```
"While we accommodate specified allergies and dietary restrictions, our kitchen
is not an allergen-free facility. Cross-contamination may occur. Clients are
responsible for communicating all guest allergies by [X] days before the event."
```

**Substitution Policy:**
```
"Menus reflect seasonal availability. If key ingredients become unavailable,
we reserve the right to make like-for-like substitutions of equal or greater
value. Significant substitutions will be communicated to the client when possible."
```

**Service Charge Disclosure:**
```
"A [X]% service charge is added to all events. This service charge is not a
gratuity and is used to cover operational costs. Additional gratuity for
exceptional service is at the client's discretion."
```

---

## Pricing Structure

### Deposit Requirements
```
Standard Deposit:     30% of total estimate
High-Risk Clients:    40-50% deposit
Weddings/Personal:    40% deposit + installment plan option
```

### Payment Terms
```
Deposit Due:          Within [X] days of contract signing
Balance Due:          [X] business days before event (typically 5-7 days)
Accepted Methods:     Credit Card, ACH, Check
Late Payment Fee:     [X]% per month (or fixed amount)
```

### Service Charge & Taxes
```
Service Charge:       [X]% (typically 18-22%)
Sales Tax:            [Your Local Tax Rate]
Delivery Fee:         [If applicable - e.g., $50-$150 based on distance]
```

---

## Document Naming Conventions

### Event ID Format
```
Format:               PR-YYYYMMDD-XXXXXX
Example:              PR-20250322-A7B9C2

PR = Palacio Reyes (replace with your initials)
YYYYMMDD = Date of submission
XXXXXX = Random alphanumeric code
```

### File Naming for Client Documents
```
Format:               EventID_DocumentType_Version_Date

Examples:
PR-20250322-A7B9C2_Quote_v1.0_2025-03-22.pdf
PR-20250322-A7B9C2_Contract_FINAL_2025-03-25.pdf
PR-20250322-A7B9C2_BEO_v2.1_2025-04-15.pdf
PR-20250322-A7B9C2_Invoice_Deposit_2025-03-25.pdf
```

---

## Platform Integration Details

### Email Marketing Platform
```
Platform Name:        [e.g., Mailchimp, SendGrid, Constant Contact]
API Key:              [Store securely - not in this document]
From Name:            Palacio Reyes Events Team
From Email:           events@yourcompany.com
Reply-To Email:       events@yourcompany.com
```

### CRM System
```
CRM Platform:         [e.g., Salesforce, HubSpot, Zoho]
Lead Source Field:    [Field name for tracking marketing source]
Custom Fields:        [List any custom fields you've created]
```

### Accounting Software
```
Accounting Platform:  [e.g., QuickBooks, Xero, FreshBooks]
Chart of Accounts:    [How you categorize catering revenue/expenses]
```

### Scheduling Tool
```
Platform:             [e.g., Calendly, Acuity, Square Appointments]
Booking URL:          [Your scheduling link]
Default Meeting:      20-minute Discovery Call
```

---

## Customization Checklist

Use this checklist when setting up a new template:

### For HTML Templates
- [ ] Replace company name
- [ ] Add/update logo
- [ ] Update color scheme (CSS)
- [ ] Update contact information (phone, email, address)
- [ ] Update social media links
- [ ] Test on desktop browser
- [ ] Test on mobile browser
- [ ] Test print layout
- [ ] Verify all links work
- [ ] Check spelling and grammar

### For Email Templates
- [ ] Replace all {{PLACEHOLDER}} values
- [ ] Add logo and branding
- [ ] Update signature block
- [ ] Configure email platform integration
- [ ] Send test email to yourself
- [ ] Verify mobile rendering
- [ ] Check spam score
- [ ] Set up automated trigger (if applicable)

### For CSV/Spreadsheet Templates
- [ ] Import to Google Sheets or Excel
- [ ] Configure conditional formatting
- [ ] Set up data validation
- [ ] Create necessary formulas
- [ ] Set up sharing/permissions
- [ ] Configure automated backups
- [ ] Test import/export functions

### For Markdown Documentation
- [ ] Update company name throughout
- [ ] Update team contact information
- [ ] Customize examples to your business
- [ ] Add your specific policies/procedures
- [ ] Review and update terminology
- [ ] Check all internal links

---

## Version Control

Keep track of when you update your branding:

| Date | Change Description | Updated By |
|------|-------------------|------------|
| 2025-03-XX | Initial branding setup | [Your Name] |
| | | |
| | | |

---

## Quick Reference

**🎨 Design Tools:**
- Canva: https://www.canva.com (logo design, graphics)
- Adobe Color: https://color.adobe.com (color palettes)
- Unsplash: https://unsplash.com (free stock photos)
- Pexels: https://www.pexels.com (free stock photos)

**📧 Email Testing:**
- Litmus: https://www.litmus.com (email previews)
- Mail Tester: https://www.mail-tester.com (spam score)

**🔧 Technical Resources:**
- HTML Color Codes: https://htmlcolorcodes.com
- Google Fonts: https://fonts.google.com
- Font Awesome Icons: https://fontawesome.com

---

**Last Updated:** [Date]
**Updated By:** [Your Name]
**Next Review:** [3-6 months from last update]

---

*Keep this document secure and up-to-date. Review quarterly or whenever business information changes.*
