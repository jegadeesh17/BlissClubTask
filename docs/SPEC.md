# Functional Specification: BlissClub Last Mile Operations Intelligence

## 1. Executive Summary & Objective
This specification defines the functional requirements, calculation formulas, and acceptance criteria for the Last Mile Operations Intelligence and Decision Support Suite for BlissClub. The system processes 92,707 e-commerce shipments and a multi-partner rate card to answer 6 strategic business questions for the Last Mile Operations Manager evaluation.

---

## 2. Core Data Ingestion & Data Dictionary

### 2.1 Raw Dataset Schema (`Data` sheet)
| Field | Type | Description | Cleaning & Validation Rules |
|---|---|---|---|
| `Order ID` | String | Unique customer order identifier | Strip whitespace, preserve leading zeros. |
| `Order Date` | DateTime | Timestamp when customer placed order | Parse datetime format. |
| `Courier Aggregator` | String | Aggregator identifier (`A1`, `A2`, `A3`) | Normalize whitespace. |
| `Courier` | String | Courier code (`C1` through `C17`) | Normalize whitespace. |
| `AWB` | String | Airway Bill number | Unique parcel identifier for billing. |
| `Status` | String | Final shipment status | Normalize case: `'LOST'` / `'Lost'` $\rightarrow$ `'LOST'`. Valid values: `DELIVERED`, `RTO`, `Not Shipped`, `LOST`. |
| `Shipping pincode` | Integer / String | 6-digit Indian postal code | Validate 6-digit format. |
| `Shipping State` | String | Indian State / UT (35 unique) | Standardize title case. |
| `Pickup Point` | String | Origin fulfillment warehouse / facility | Origin anchor for zone mapping. |
| `Product` | String | Product name / category | Categorize line items. |
| `SKU` | String | Stock keeping unit | Item code. |
| `Quantity` | Integer | Units per line item | $\ge 1$. |
| `Order Type` | String | Payment mode | Normalize: `PrePaid` vs `COD`. |
| `AWB Assignment Time`| DateTime | Timestamp when AWB was generated | WMS pack & manifest completion. |
| `Pickup Date` | DateTime | Timestamp when courier picked up parcel | First-mile scan by carrier fleet. |
| `Delivered Date` | DateTime | Timestamp when parcel reached customer | Last-mile delivery completion scan. |
| `Zone` | String | Delivery Zone (`A`, `B`, `C`, `D`, `E`, `F`) | Normalize case: `'d'` $\rightarrow$ `'D'`. |
| `Shipment weight (in Kg)`| Float | Actual weight in kilograms | Numeric validation. |

### 2.2 Rate Card Rules (`Rate Card` sheet)
Charges apply **per Airway Bill (AWB)**:
- **Weight Slab Rule:** Billable weight is rounded up to the nearest 500g ($0.5$ kg) increment.
  $$\text{Billable Slabs} = \lceil \frac{\text{Weight (kg)}}{0.5} \rceil$$
  - Base Slab: First 500g ($0.5$ kg) rate.
  - Additional Slabs: $(\text{Billable Slabs} - 1) \times \text{Additional 500g rate}$.
- **COD Rule:**
  $$\text{COD Fee} = \text{Flat COD Rate (₹)}$$
  (Since Order Value is not present in the dataset, the flat minimum fee per AWB is the contracted baseline).
- **Total Freight per AWB:**
  $$\text{Total Cost} = \text{Base Rate} + (\text{Additional Slabs} \times \text{Addnl Rate}) + \text{COD Fee (if COD)}$$

---

## 3. Specifications for the 6 Case Study Questions

### Spec 1: Delivery Health & Reliability (Question 1)
- **Primary Signals:**
  - Gross Delivery Rate: $\frac{\text{Delivered Shipments}}{\text{Total Shipped}} \times 100$
  - RTO Rate: $\frac{\text{RTO Shipments}}{\text{Total Shipped}} \times 100$
  - Lost Shipment Rate: $\frac{\text{Lost Shipments}}{\text{Total Shipped}} \times 100$
  - First-Attempt / NDR Rate
- **Partner Concentration Risk:**
  - Concentration ratio: Share of shipments handled by top courier (`C9`) and top aggregator (`A3`).
- **Acceptance Criteria (G/W/T):**
  - **Given** 92,707 raw shipment rows, **When** processed, **Then** total `DELIVERED`, `RTO`, `Not Shipped`, and `LOST` reconcile exactly to 100% of the dataset.

### Spec 2: Cost-to-Serve Modeling (Question 2)
- **Financial Metrics:**
  - Total Shipping Cost (₹)
  - Cost per Order & Cost per Delivered Order (₹)
  - Cost Breakdown by Zone (A to F), Aggregator (A1, A2, A3), and Payment Type (Prepaid vs COD)
  - Cost Leakage Identification: Quantifying the overpayment of assigning Zone A/B/C/E shipments to A3 instead of A1/A2.
- **Acceptance Criteria (G/W/T):**
  - **Given** rate card schedules for A1, A2, and A3, **When** applied to each AWB based on weight, zone, and order type, **Then** calculated freight matches contract formulas with zero NaN or null values.

### Spec 3: Order Mix & Geographic Intelligence (Question 3)
- **Analyses Required:**
  - Geographic Pareto: Top 5 states vs. long-tail (35 states).
  - Zone mix: Intra-city (A) vs Regional (B) vs Metro-to-Metro (C) vs Rest of India (D) vs Special (E/F).
  - Weight profile: Percentage of volume $\le 0.5$kg vs $> 0.5$kg.
  - Payment profile: COD share vs Prepaid share across states and zones.
  - Temporal trend: Daily order volume progression across January 2026.
- **Acceptance Criteria (G/W/T):**
  - **Given** customer pincodes and states, **When** aggregated, **Then** regional volume distributions and RTO correlations are clearly isolated.

### Spec 4: Courier & Aggregator Evaluation & Simulator (Question 4)
- **Evaluation Matrix:**
  - Scorecard per aggregator and courier: Cost per AWB vs Delivery Speed (TAT) vs Delivery Success Rate vs RTO %.
- **Volume Reallocation Simulator:**
  - Interactive parameters: Percentage shift of volume from A3 to A1 and A2 across specific zones.
  - Output: Net monthly financial savings (₹) and projected delivery risk.
- **Acceptance Criteria (G/W/T):**
  - **Given** user slider adjusting volume allocation by $X\%$, **When** simulated, **Then** cost deltas update dynamically in real time.

### Spec 5: Process Efficiency & SLA Design (Question 5)
- **Funnel Stage Breakdown:**
  1. Stage 1: Warehouse Fulfillment TAT = `AWB Assignment Time - Order Date`
  2. Stage 2: Handover / Dispatch Lag = `Pickup Date - AWB Assignment Time`
  3. Stage 3: In-Transit / Last Mile TAT = `Delivered Date - Pickup Date`
  4. Total Click-to-Deliver TAT = `Delivered Date - Order Date`
- **SLA Breach Thresholds:**
  - Warehouse SLA: $\le 12$ hours
  - Handover SLA: $\le 12$ hours
  - Courier Transit SLA: Zone A: 24h, Zone B: 48h, Zone C/D: 72–96h, Zone E: 120h
- **Acceptance Criteria (G/W/T):**
  - **Given** timestamped records, **When** evaluated, **Then** mean, median, P90 TAT, and breach percentages are computed per stage.

### Spec 6: 90-Day Execution Roadmap (Question 6)
- **Deliverables:**
  - Structured 30-60-90 day agenda with explicit milestones, operational owners, and target KPIs.
  - Executive Defense Memo (`docs/EXECUTIVE_MEMO.md`).
  - Interactive decision dashboard deployed on GitHub Pages.
