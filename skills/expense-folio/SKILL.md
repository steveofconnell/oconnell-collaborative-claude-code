# Expense Folio Builder

Build a travel expense summary spreadsheet from receipts, email, and JPMC card statements. This is a recurring task (~monthly) for Emory University business travel reimbursement.

## Input
Optional arguments: trip location, dates, purpose. If not provided, ask.

## Reference
- Card -9890 = Emory corporate card (JPMC). Reimbursement to: "to JPMC"
- Card -7503 = personal Visa. Reimbursement to: "reimbursement"
- Past folios are in `~/Dropbox/Quickdrop/Chicago2025/` (multiple monthly subfolders with `Expense summary *.xlsx` files)
- GSA per diem rates: fetch from `https://www.gsa.gov/travel/plan-book/per-diem-rates/per-diem-rates-results` for the trip destination. Use fiscal year matching the travel dates. Full day rate and travel day rate (75% of full).

## Step 1: Gather Trip Details
Confirm or ask for:
1. **Trip dates** (departure and return)
2. **Location** (city, state)
3. **Purpose** (e.g., "Professional development and leave")
4. **Position/role** at destination (e.g., "Visiting faculty, Yale University")
5. **Appointment period** if applicable

## Step 2: Set Up Folder
Create folder structure at `~/Dropbox/Quickdrop/<Location><Year>/<period>receipts/pdfs/` if it doesn't already exist. Also create a `jpmdownloads/` sibling folder for JPMC statement files.

## Step 3: Collect Receipts

### Email receipts
Search Gmail for Uber, Lyft, and airline receipts matching the trip date range:
- `from:(uber OR lyft) subject:(receipt OR trip OR ride) after:YYYY/MM/DD before:YYYY/MM/DD`
- `from:<airline> newer_than:<N>d`
- Extract: date, amount, description, driver name

Note: Uber/Lyft receipt emails are massive HTML. Use `grep` on the saved tool result files to extract dollar amounts and card info rather than reading the full HTML.

### JPMC card statement
Look for JPMC transaction downloads in the `jpmdownloads/` folder (`.txt` files with space-separated characters). Parse these to extract:
- Transaction amount, date, merchant name, card number
- Categorize each transaction as: trip-related, subscription, RA payment (Upwork), other purchase, or payment received

The JPMC statement is authoritative for amounts charged to the corp card. Email receipts may differ slightly (e.g., tips added after).

### Flight receipts
User will place flight confirmation PDFs in the `pdfs/` folder. Read these to extract:
- Confirmation number, route, dates, fare breakdown, payment card
- For flights with date changes, track the full payment history across all change documents

### CTM (Corporate Travel Management) invoices
Emory books some flights through CTM. These appear as `eInvoice` PDFs and show:
- Flight details, ticket number, agent fees
- Billed to card number
- Record locator and airline reservation code

## Step 4: Look Up Per Diem
Fetch GSA per diem MI&E rate for the trip destination and fiscal year. Calculate:
- Full days = days between first and last travel day, exclusive of travel days
- Travel days = first and last day (at 75% rate)
- Formula in Excel: `=<full_rate>*<N_full>+<travel_rate>*<N_travel>`

## Step 5: Build the Excel Spreadsheet

### Header block (rows 1-7 or 1-8)
| Field | Example |
|-------|---------|
| Person | O'Connell, Stephen |
| Department | Economics |
| Location | New Haven, CT USA |
| Purpose | Professional development and leave |
| Position | Visiting faculty, Yale University |
| Appointment period | (if applicable) |
| Expense period | March 1 2026 - April 4 2026 |
| Expense period name | O'Connell Yale Professional Development - March/April 2026 |

### Column headers
Date | Amount | Expense category | Description | Payment by | Reimbursement to | Notes | File 1 | File 2

### Expense categories
Use these standard categories (matching prior folios):
- **Airfare** — flight tickets
- **Airfare add-on** — checked bags, carry-on bags, seat upgrades
- **Agent fee** — CTM or other booking agent fees
- **Airport transport** — rides to/from airports (Uber, Lyft, taxi)
- **Within-city transport** — rides within the trip city
- **Per diem** — MI&E per diem (GSA rates)
- **Accommodation** — hotel, rental
- **Utilities** — if applicable (long-term stays)

### Payment by values
- `Corp card -9890` — Emory JPMC corporate card
- `Personal card -7503` — personal Visa
- `personal cash transfer` — bank transfer for accommodation
- `n/a` — per diem (no receipt)

### Reimbursement to values
- `to JPMC` — corp card charges (Emory pays JPMC directly)
- `reimbursement` — personal card/cash charges (reimbursed to paycheck)

### File references
Column H (File 1) and I (File 2) reference PDF filenames in the `pdfs/` folder. Use the filename without extension. Put `n/a` for per diem rows.

### Summary block (after last expense row, skip one row)
```
Total costs     =SUM(B<start>:B<end>)
to JPMC         =SUMIFS(B<start>:B<end>,F<start>:F<end>,A<row>)
reimbursement   =SUMIFS(B<start>:B<end>,F<start>:F<end>,A<row>)
Validate        =SUM(B<jpmc>:B<reimb>)=B<total>
```

### Formatting
- Bold header labels and column headers
- Currency format (#,##0.00) on Amount column
- Date format (M/D/YY) on date cells
- Per diem amounts as formulas (e.g., `=80*6+60*2`) so rate changes are transparent

## Step 6: Identify Non-Trip Charges
From the JPMC statement, list charges that are NOT trip-related but may need handling via web form:
- **Subscriptions**: Claude.AI, OpenAI, Anthropic, Slack, etc.
- **RA payments**: Upwork charges
- **Purchases**: Amazon, etc.
- **Future trip charges**: flights for upcoming trips (note these for future folios)

Present these separately so the user knows what still needs to be handled outside the folio.

## Step 7: Flag Gaps
After building the spreadsheet, explicitly list:
- Expenses that may be missing (e.g., return-trip ground transport not yet incurred)
- Amounts that need verification against card statements
- PDF receipts that still need to be collected and placed in the `pdfs/` folder
- Per diem rates that should be verified

## Step 8: Open the File
Open the completed Excel file with `open <path>` so the user can review immediately.
