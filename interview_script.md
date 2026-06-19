# Divine Hindu Inventory System - Interview Demo Script

## 1. Opening Introduction

Hello, thank you for giving me this assignment.

I understood the problem as an inventory operations challenge for Divine Hindu's Bangalore inventory, where stock needs to stay aligned across Shopify orders, store sales, returns, warehouse movement, damaged items, and dispatch.

So I designed a simple but scalable inventory tracking system that starts with Google Sheets or CSV for easy data entry, uses Python for reconciliation logic, and uses a Streamlit dashboard for reporting and visibility.

The goal is to help the team answer one core question daily:

```text
For every SKU, how much stock came in, how much went out, what came back, what got damaged, and what is the accurate closing stock?
```

## 2. Business Understanding

Before designing the system, I considered Divine Hindu's product type.

The product categories include:

- Karungali products
- Rudraksha malas and bracelets
- Gemstone bracelets
- Idols
- Puja essentials
- Gifting combos

These products need careful inventory control because:

- Festival and gifting seasons can create sudden demand.
- Bracelets, malas, idols, and packaging can get damaged.
- Returned products cannot directly go back into sellable stock.
- Shopify sales and Bangalore store sales need to reduce stock from the same inventory ledger.
- Combo products need special tracking because they may include multiple component SKUs.

## 3. Core Logic

The complete system is based on one simple formula:

```text
Closing Stock =
Opening Stock
+ Inward Stock
+ Good Returns
- Sales / Dispatch
- Damaged Stock
+/- Adjustment
```

This formula runs SKU-wise.

For example, if Karungali Mala has:

```text
Opening stock = 45
Inward stock = 20
Sales = 7
Returns = 0
Damage = 0
```

Then:

```text
Closing stock = 45 + 20 - 7 = 58
```

After that, the system compares calculated closing stock with physical stock.

```text
Mismatch = Physical Stock - Calculated Closing Stock
```

If mismatch is not zero, the SKU is flagged for checking.

## 4. Tools Used

I used a simple and practical stack:

### Google Sheets / CSV

For easy data entry by warehouse or store team.

Sheets used:

- SKU Master
- Stock Movements
- Physical Count

### Python + Pandas

For calculation and automation:

- Closing stock calculation
- Inward and outward summary
- Return handling
- Damaged stock deduction
- Physical mismatch checking
- Low-stock alerts
- Reorder recommendation

### Streamlit

For dashboard and reporting:

- KPI view
- Stock charts
- Low-stock table
- Mismatch report
- Returns and damage log
- SKU-wise reconciliation

### Shopify Integration Scope

For first deployment, Shopify order export can be imported daily.

For scalable deployment, Shopify API can directly push sales and return data into the system.

## 5. Data Structure Explanation

The system uses three main data files.

### 1. SKU Master

This is the product database.

It stores:

- SKU
- Product name
- Category
- Opening stock
- Minimum stock
- Reorder quantity
- Supplier
- Cost price
- Selling price
- Combo status

### 2. Stock Movements

This is the transaction ledger.

It records:

- Date
- SKU
- Movement type
- Channel
- Quantity
- Condition
- Reference ID
- Remarks

Movement types include:

- INWARD
- SALE
- RETURN
- DAMAGE
- ADJUSTMENT

### 3. Physical Count

This stores the actual counted stock from warehouse or store.

It includes:

- Date
- SKU
- Physical stock
- Counted by
- Remarks

## 6. Dashboard Walkthrough

When I open the dashboard, the top section shows five important KPIs:

- Total SKUs
- Closing units
- Low-stock items
- Mismatch items
- Stock value

Then there are visual charts:

- Category-wise closing stock
- Stock health summary
- Sales/dispatch by channel

The dashboard also has action tables:

- Low Stock Alerts
- Mismatch Report
- SKU-wise Reconciliation
- Returns and Damage Log

So an operations manager can quickly see:

```text
Which product needs reorder?
Which product has mismatch?
Which product got damaged?
Which channel sold how many units?
What is today's closing stock?
```

## 7. Return Handling Explanation

I have not directly added all returns back to stock.

The return process is:

1. Return is received from customer/courier.
2. QC checks product and packaging.
3. If product is good, it is added back to sellable stock.
4. If damaged, it goes to damaged/write-off stock.
5. Return ID and reason are recorded.

This is important because spiritual jewellery, idols, and gifting products may get damaged in transit or during handling.

## 8. Damaged Stock Explanation

Damaged stock is kept separate from sellable stock.

Examples:

- Broken bracelet thread
- Damaged mala
- Cracked idol
- Damaged packaging
- Expired/shelf-life sensitive daily essentials

This avoids showing damaged products as available for sale.

## 9. Low Stock Alert Explanation

Every SKU has a minimum stock level.

If calculated closing stock is less than or equal to minimum stock, the system marks it as Low Stock and suggests reorder quantity.

Example:

```text
If Rudraksha Bracelet current stock is 12
and minimum stock is 15,
then it becomes Low Stock.
```

This helps avoid stockout, especially during festival or gifting seasons.

## 10. Mismatch Handling Explanation

Mismatch means system stock and physical stock are different.

If mismatch happens, the process should be:

1. Recount physical stock.
2. Check Shopify sales.
3. Check Bangalore store sales.
4. Check inward entries.
5. Check return and damage logs.
6. Record approved adjustment if required.

This creates an audit trail and avoids silent manual corrections.

## 11. Combo Product Handling

For gifting combos, there are two ways to manage stock.

### Version 1: Finished Combo Tracking

Track combo as a separate SKU.

Example:

```text
GFT-001 = Protection Gift Combo
```

This is simple and suitable for first deployment.

### Version 2: BOM / Component Tracking

Track the components inside each combo.

Example:

```text
Protection Gift Combo =
1 Karungali Bracelet
+ 1 Rudraksha Bracelet
+ 1 Puja Kit
+ Packaging Box
```

When combo is sold, the system deducts component stock automatically.

For initial deployment, I would start with finished combo SKU tracking and then move to BOM-based tracking when process is stable.

## 12. Deployment Plan

I would deploy this in phases.

### Phase 1: Data Setup

Create clean SKU master and import current Bangalore stock.

### Phase 2: Daily Movement Tracking

Start recording inward, sales, returns, damage, and adjustments.

### Phase 3: Reconciliation Automation

Run Python reconciliation daily to generate closing stock and mismatch report.

### Phase 4: Dashboard

Give operations manager a dashboard for daily visibility.

### Phase 5: Alerts

Add email or WhatsApp alerts for low stock and mismatches.

### Phase 6: Integrations

Connect Shopify API, barcode scanning, and eventually tools like Zoho Inventory if required.

## 13. Why I Chose This Approach

I chose this approach because it is:

- Simple for ground-level team
- Fast to deploy
- Low cost
- Easy to understand
- Easy to audit
- Scalable later
- Suitable for D2C/ecommerce operations

Instead of directly suggesting a heavy ERP, I designed a practical system that can start with Sheets and automation, then scale with APIs and dedicated tools.

## 14. Possible Interview Questions and Answers

### Q1. Why did you choose Google Sheets instead of ERP?

Because the first version should be easy for the warehouse/store team to adopt. Google Sheets is simple, low-cost, and fast to deploy. Once the process is stable, the same logic can be moved to Zoho Inventory, ERP, or Shopify API integration.

### Q2. How will you avoid manual entry errors?

I would use dropdowns for movement type, SKU, channel, and condition. I would also add required fields, validation rules, barcode scanning, and daily reconciliation checks.

### Q3. How will Shopify sales reduce stock?

Initially, Shopify order export can be imported daily into the stock movement log as SALE entries. Later, Shopify API can automatically push order data to the inventory system.

### Q4. How will you handle returned products?

Returned products will go through QC first. Only good-condition returns will be added back to sellable stock. Damaged returns will be moved to damaged/write-off stock.

### Q5. How will you detect mismatch?

The system calculates closing stock from stock movements and compares it with physical stock count.

```text
Mismatch = Physical Stock - Calculated Closing Stock
```

If mismatch is not zero, the SKU is flagged.

### Q6. How will you make it scalable?

By adding Shopify API integration, barcode scanning, role-based access, multi-location tracking, BOM for combos, automated alerts, and demand forecasting.

### Q7. How will you handle combo products?

First, I will track finished combo SKUs. Later, I will add BOM/component-level tracking so that selling one combo deducts its individual components.

### Q8. What are the biggest challenges?

The biggest challenges are manual entry errors, return condition tracking, stock mismatch, and festival demand spikes. I solve these through validation, QC flow, mismatch reports, and reorder thresholds.

### Q9. How can AI be added later?

AI can be added for:

- Demand forecasting
- Festival season stock planning
- Fast-moving and slow-moving SKU detection
- Return reason analysis
- Smart reorder recommendation
- Anomaly detection for unusual mismatch

### Q10. What would you implement first if you joined tomorrow?

First, I would clean the SKU master and current Bangalore stock. Then I would start daily stock movement tracking and build a simple daily closing report. After that, I would automate reconciliation and alerts.

## 15. Closing Statement

My approach is to keep the first version simple and practical so the team can actually use it daily. Once the process is stable, the same system can scale into Shopify API integration, barcode scanning, automated alerts, and AI-based demand forecasting.

The final goal is to make Divine Hindu's Bangalore inventory more accurate, organized, and ready for growth.