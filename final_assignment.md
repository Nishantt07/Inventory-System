# Inventory Tracking System for Divine Hindu Bangalore Inventory

## 1. Objective

Divine Hindu needs a simple, practical, and scalable inventory tracking system for Bangalore inventory. The system should maintain SKU-wise stock and align it with online sales, store sales, returns, warehouse movement, damaged stock, and dispatch.

The main objective is to answer these questions daily:

- Which product has how much stock?
- How much stock came in?
- How much stock went out through Shopify or store sales?
- How many products were returned?
- How many products are damaged or non-sellable?
- What is the final closing stock?
- Is system stock matching with physical warehouse stock?
- Which products need reorder?

## 2. Business Context

Divine Hindu sells spiritual and devotional products such as Karungali items, Rudraksha malas, gemstone bracelets, idols, daily essentials, puja kits, and gifting combos.

These products need careful inventory control because:

- Some products are fast-moving during festivals and gifting seasons.
- Combo products may include multiple individual items.
- Jewellery, malas, bracelets, and idols can get damaged during storage or dispatch.
- Online Shopify sales and offline Bangalore store sales should be aligned with the same inventory ledger.
- Returned products should be quality checked before adding back to sellable stock.

## 3. Core Stock Formula

The inventory system will use this daily stock formula for every SKU:

```text
Closing Stock =
Opening Stock
+ Inward Stock
+ Good Returns
- Sales / Dispatch
- Damaged Stock
+/- Manual Adjustment
```

Opening stock for today will automatically become the previous day's closing stock.

## 4. Product/SKU-wise Stock Tracking

Every product should have a unique SKU code. Example:

| Category | Example SKU |
|---|---|
| Karungali | KAR-001 |
| Rudraksha | RUD-001 |
| Gemstone/Jewellery | GEM-001 |
| Idols | IDL-001 |
| Daily Essentials | ESS-001 |
| Gifting Combos | GFT-001 |

Each SKU master record should include:

- SKU code
- Product name
- Category
- Location
- Opening stock
- Minimum stock level
- Reorder quantity
- Supplier
- Cost price
- Selling price
- Combo product status
- Active/inactive status

## 5. Inventory Workflow

### Step 1: Opening Stock

At the start of each day, the system takes the previous day's closing stock as today's opening stock.

### Step 2: Inward Stock

Stock is added when:

- New stock is received from suppliers.
- Stock is transferred from head office or another warehouse.
- New gifting combos are assembled.
- Returned products pass quality check and become resellable.

### Step 3: Outward Stock

Stock is reduced when:

- Shopify orders are dispatched.
- Bangalore store sales happen.
- Stock is transferred out.
- Products are used in combo assembly.

### Step 4: Returns Handling

Returned products should not be directly added back to sellable stock. First, they should go through QC.

Return flow:

1. Return received from customer/courier.
2. QC team checks product condition and packaging.
3. If product is good, add it back to sellable stock.
4. If damaged, move it to damaged/write-off stock.
5. Record return reason and return reference ID.

### Step 5: Damaged / Expired Stock Handling

Damaged or expired stock should be recorded separately.

Examples:

- Broken bracelet thread
- Damaged mala
- Cracked idol
- Damaged packaging
- Expired/shelf-life sensitive daily essential product

Damaged stock should not be included in sellable inventory.

### Step 6: Physical Stock Count

Daily or weekly physical count should be done for important SKUs.

The system compares:

```text
Physical Stock vs Calculated Closing Stock
```

If both are different, the system marks it as a mismatch.

### Step 7: Stock Correction

If mismatch is found, the team should check:

- Missed sale entry
- Wrong return entry
- Wrong inward entry
- Damaged item not recorded
- Counting mistake
- Possible shrinkage/loss

After verification, correction should be recorded in an adjustment log with reason and approval.

## 6. Tools and Apps Used

### 1. Google Sheets

Used as the main data entry layer.

Sheets required:

- SKU Master
- Stock Movements
- Physical Count
- Reconciliation Report
- Returns and Damage Log

Google Sheets is practical because warehouse/store teams can use it easily without complex training.

### 2. Python + Pandas

Used for automatic reconciliation:

- Opening stock calculation
- Inward/outward summary
- Good return calculation
- Damaged stock deduction
- Closing stock calculation
- Mismatch detection
- Low-stock flagging
- Reorder recommendation

### 3. Streamlit Dashboard

Used for visual reporting and interview-ready demo.

Dashboard includes:

- Total SKUs
- Closing stock units
- Stock value
- Low-stock items
- Mismatch items
- Category-wise stock
- Returns and damaged stock
- Sales channel summary
- SKU-wise reconciliation table

### 4. Shopify Export / API

In the first version, Shopify order export can be imported into the stock movement sheet.

In the scalable version, Shopify API can directly push order and return data into the inventory system.

### 5. Alerts

Low-stock and mismatch alerts can be sent using:

- Google Apps Script email alerts
- Python email alerts
- WhatsApp Business API in future

## 7. Dashboard Format

The dashboard should have the following sections:

### Top KPI Cards

- Total active SKUs
- Total closing stock
- Low-stock SKUs
- Mismatch SKUs
- Inventory value

### Charts

- Category-wise closing stock
- Stock health summary
- Sales by channel
- Returns and damage summary

### Tables

- SKU-wise reconciliation
- Low-stock alert table
- Mismatch report
- Returns and damaged stock log

## 8. Daily, Weekly, and Monthly Reporting

### Daily Report

Purpose: Daily operations tracking.

Includes:

- SKU-wise opening stock
- Inward stock
- Sales/dispatch
- Good returns
- Damaged stock
- Closing stock
- Physical stock
- Mismatch status
- Low-stock alerts

### Weekly Report

Purpose: Inventory health review.

Includes:

- Low-stock SKUs
- Mismatch SKUs
- Returned products
- Damaged products
- Fast-moving products
- Slow-moving products
- Reorder suggestions

### Monthly Report

Purpose: Management-level decision making.

Includes:

- Opening vs closing inventory value
- Category-wise stock value
- Fast-moving products
- Slow-moving products
- Return and damage trend
- Stock mismatch summary
- Reorder plan for next month
- Festival/gifting season preparation

## 9. Minimum Stock Alerts

Each SKU will have a minimum stock level.

Example:

```text
If current stock <= minimum stock,
mark item as Low Stock and recommend reorder quantity.
```

Example:

| SKU | Product | Current Stock | Minimum Stock | Action |
|---|---|---:|---:|---|
| GFT-002 | Festive Puja Gift Hamper | 5 | 6 | Reorder |
| IDL-002 | Shivling Brass Idol | 4 | 5 | Reorder |

This helps avoid stockouts during high-demand periods.

## 10. Stock Mismatch Checking

Mismatch formula:

```text
Mismatch Qty = Physical Stock - Calculated Closing Stock
```

If mismatch quantity is not zero, the item is flagged for review.

Correction process:

1. Recount physical stock.
2. Check Shopify sales entries.
3. Check Bangalore store sale entries.
4. Check inward entries.
5. Check return/damage logs.
6. Add approved adjustment if required.

## 11. Handling Combo Products

Divine Hindu has gifting and combo products. For combo SKUs, a Bill of Materials approach can be used.

Example:

```text
Protection Gift Combo =
1 Karungali Bracelet
+ 1 Rudraksha Bracelet
+ 1 Puja Kit
+ Packaging Box
```

When one combo is sold, the system should reduce the stock of its components or the finished combo SKU, depending on how inventory is maintained.

For the first version, finished combo SKUs can be tracked directly. In the scalable version, component-level deduction can be added.

## 12. Implementation Approach

### Phase 1: Set up SKU Master

Create complete SKU master with category, opening stock, minimum stock, supplier, and price.

### Phase 2: Set up Stock Movement Log

Create a single transaction log for inward, sales, returns, damage, and adjustments.

### Phase 3: Add Daily Physical Count

Warehouse/store team updates physical count for key SKUs.

### Phase 4: Build Reconciliation Logic

Use Python to calculate closing stock, low-stock items, and mismatch items.

### Phase 5: Build Dashboard

Use Streamlit dashboard for management and operations visibility.

### Phase 6: Add Alerts

Set up email/WhatsApp alerts for low stock and mismatch.

### Phase 7: Scale with Integrations

Connect Shopify sales, return data, barcode scanning, and warehouse app integration.

## 13. Challenges and Solutions

| Challenge | Solution |
|---|---|
| Shopify and store sales are tracked separately | Use one common stock movement ledger |
| Returned products may be damaged | Add QC step before restocking |
| Physical stock may not match system stock | Daily/weekly mismatch report |
| Fast-moving SKUs may go out of stock | Minimum stock alerts and reorder quantity |
| Damaged products affect sellable stock | Maintain separate damaged/write-off log |
| Combo SKUs are harder to track | Use BOM/component mapping in scalable version |
| Manual entries may cause errors | Use dropdowns, validation, and barcode scanning |
| Festival demand spikes | Maintain buffer stock for fast-moving categories |

## 14. Scalability Plan

The system can start with Google Sheets and Python because it is simple and quick to deploy.

Later, it can be scaled by adding:

- Shopify API integration
- Barcode scanner
- Role-based access
- Automated email/WhatsApp alerts
- Zoho Inventory or ERP integration
- Multi-location inventory tracking
- Batch/expiry tracking for daily essentials
- Supplier reorder automation
- AI-based demand forecasting for festival seasons

## 15. Why This Solution Is Practical

This solution is practical because:

- It can be started quickly with Google Sheets.
- It does not require expensive ERP setup in the first phase.
- Warehouse and store teams can easily understand it.
- Python automation reduces manual calculation errors.
- Dashboard gives clear visibility to operations and management.
- It supports Divine Hindu's D2C model with Shopify, store sales, returns, dispatch, and gifting combos.
- It can later scale into a full inventory management system.

## 16. Final Outcome

The final system will help Divine Hindu maintain accurate Bangalore inventory by tracking:

- SKU-wise stock
- Opening and closing stock
- Inward and outward movement
- Shopify and store sales
- Returns
- Damaged stock
- Low-stock alerts
- Physical mismatch
- Reorder planning
- Daily, weekly, and monthly reports

This will make inventory operations more simple, sorted, scalable, and ready to deploy.

I have also prepared a working prototype using CSV/Google Sheets-style data, Python reconciliation logic, and a Streamlit dashboard to demonstrate this workflow practically during the interview.