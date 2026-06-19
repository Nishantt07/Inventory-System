# Divine Hindu Inventory Reporting Format

## 1. Daily Closing Stock Report

### Purpose
Daily report ka purpose hai har SKU ka opening stock, inward, sales, returns, damage, aur closing stock track karna.

### Frequency
Daily, end of day.

### Prepared By
Warehouse Executive / Inventory Executive.

### Reviewed By
Operations Manager.

### Columns
| Field | Meaning |
|---|---|
| Date | Report date |
| SKU | Unique product code |
| Product Name | Product name |
| Category | Karungali, Rudraksha, Jewellery, Gifting, Idols, Daily Essentials |
| Opening Stock | Previous day closing stock |
| Inward Stock | New stock received |
| Sales / Dispatch | Shopify + store sales |
| Good Returns | Returned products approved by QC |
| Damaged Stock | Broken, expired, packaging damaged, non-resellable stock |
| Closing Stock | Opening + Inward + Good Returns - Sales - Damage |
| Physical Stock | Actual counted stock |
| Mismatch Qty | Physical stock - calculated closing stock |
| Status | Matched / Mismatch |
| Action Required | Recount, correct entry, reorder, or write-off |

### Daily Report Example
| SKU | Product | Opening | Inward | Sales | Returns | Damage | Closing | Physical | Mismatch | Action |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| KAR-001 | Karungali Mala | 45 | 20 | 7 | 0 | 0 | 58 | 58 | 0 | No action |
| RUD-002 | Rudraksha Bracelet | 52 | 0 | 0 | 2 | 1 | 53 | 53 | 0 | Damaged return recorded |
| GEM-002 | Amethyst Bracelet | 28 | 0 | 6 | 0 | 0 | 22 | 22 | 0 | Monitor stock |

## 2. Low Stock Alert Report

### Purpose
Minimum stock threshold ke neeche jaane wale products ko identify karna.

### Frequency
Daily automated alert, plus weekly review.

### Columns
| Field | Meaning |
|---|---|
| SKU | Product SKU |
| Product Name | Product name |
| Category | Product category |
| Current Stock | Calculated closing stock |
| Minimum Stock | Reorder threshold |
| Reorder Qty | Suggested reorder quantity |
| Supplier | Supplier name |
| Priority | High / Medium / Low |

### Alert Logic
If current stock is less than or equal to minimum stock, item should be marked as Low Stock.

### Example Alert Message
Subject: Low Stock Alert - Divine Hindu Bangalore Inventory

The following SKUs need reorder action:
- GFT-002 Festive Puja Gift Hamper: Current stock below reorder level
- IDL-002 Shivling Brass Idol: Close to minimum threshold

## 3. Returns and Damage Report

### Purpose
Returned, damaged, expired, or non-resellable products ka separate tracking.

### Frequency
Weekly.

### Return QC Flow
1. Return received from courier or customer.
2. Product is checked by QC team.
3. If product is good, add back to sellable stock.
4. If damaged, move to damaged/write-off stock.
5. Record return reason and reference ID.

### Columns
| Field | Meaning |
|---|---|
| Date | Return/damage date |
| SKU | Product SKU |
| Product Name | Product name |
| Movement Type | Return / Damage |
| Condition | Good / Damaged |
| Quantity | Units |
| Channel | Shopify / Store / Warehouse |
| Reference ID | Order ID / Return ID / Damage ID |
| Action | Restock / Repair / Write-off |
| Remarks | Reason or QC notes |

## 4. Weekly Inventory Health Report

### Purpose
Operations manager ko weekly view dena ki inventory system healthy hai ya nahi.

### Frequency
Weekly.

### Metrics
| Metric | Meaning |
|---|---|
| Total SKUs | Active product count |
| Total Closing Stock | Total available units |
| Low Stock SKUs | Products needing reorder |
| Mismatch SKUs | Products needing recount/investigation |
| Damaged Units | Total non-sellable units |
| Return Rate | Returns compared to sales |
| Fast-moving SKUs | Highest sales products |
| Slow-moving SKUs | Low/no sales products |

### Weekly Actions
- Low stock items reorder karna.
- Mismatch items recount karna.
- Damaged stock write-off approval lena.
- Fast-moving products ke liye buffer stock maintain karna.
- Slow-moving products ko combo/gifting bundles mein use karna.

## 5. Monthly Management Report

### Purpose
Founder/management ko monthly inventory performance view dena.

### Frequency
Monthly.

### Sections
1. Opening vs closing inventory value.
2. Category-wise stock value.
3. Fast-moving products.
4. Slow-moving products.
5. Return and damaged stock value.
6. Stock mismatch summary.
7. Reorder planning for next month.
8. Festival/gifting season demand preparation.

### Management Insights
- Rudraksha, Karungali, and gifting products ke fast-moving SKUs identify karna.
- Festival months mein gifting combos aur puja kits ke liye higher buffer stock maintain karna.
- Fragile idol products ke liye packaging damage tracking karna.
- Agarbatti/daily essentials ke liye expiry/shelf-life monitoring add karna.
- Shopify online sales aur Bangalore store sales ko same stock ledger se connect karna.

## 6. Dashboard Reporting Layout

### Top KPIs
- Total SKUs
- Closing Stock Units
- Low Stock Items
- Mismatch Items
- Stock Value

### Charts
- Category-wise closing stock
- Stock health summary
- Sales channel summary
- Returns and damage summary

### Tables
- SKU-wise reconciliation
- Low-stock alert list
- Mismatch report
- Return/damage log