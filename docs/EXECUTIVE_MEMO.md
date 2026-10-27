# Operations Strategy Report: Last Mile Performance & 90-Day Plan

**To:** Operations Leadership, BlissClub  
**From:** Candidate (Operations Analyst Assessment)  
**Date:** January 2026 Audit (92,707 Shipments Analyzed)  
**Interactive Dashboard:** Hosted live on GitHub Pages (`https://jegadeesh17.github.io/BlissClubTask`)

---

## Executive Summary

An audit of **92,707 shipments** from January 2026 and the 3-partner contracted Rate Card reveals that BlissClub’s last-mile logistics engine maintains a healthy gross delivery rate of **94.94%**. However, underneath this topline success lie two severe operational and financial vulnerabilities:

1. **Massive Partner Overspending:** **73.0% of total volume (67,642 orders)** is routed to **Aggregator A3 (Courier C9)**, despite A3 charging the highest base freight rates across Zones A, B, C, and E. Routing this volume through contracted partners A1 or A2 represents an immediate **₹5.95 Lakhs/month (₹71.4 Lakhs annualized) cost-reduction opportunity**.
2. **First-Mile Handover Bottleneck:** While internal warehouse fulfillment is rapid (median $0.79$ hours), parcels languish on the dispatch dock for an average of **15.98 hours** (median $17.17$ hours, 55.1% breaching 12-hour SLA) awaiting courier pickup scan, adding an artificial 1-day lag to Click-to-Deliver speed.
3. **COD Return Skew:** While prepaid orders achieve a **99.16% delivery rate** (0.80% RTO), Cash-on-Delivery (COD) orders suffer an **RTO rate of 12.23%**, driving **89.9% of all returns in the company**.

Below is the complete analytical diagnosis and operational action plan answering all 6 assignment questions.

---

## 1. Delivery Health & Reliability (Question 1)

### What Signals Matter Most?
In D2C last-mile logistics, tracking only "Gross Delivery %" is dangerous because it hides carrier failure modes. We evaluate operations across 4 core vectors:
- **Net Delivery Success Rate:** Actual customer receipt.
- **RTO Incidence by Payment Mode:** Cash-on-Delivery failure rate vs. Prepaid.
- **Partner Concentration Risk:** Single-point-of-failure exposure.
- **First-Mile Handover Latency:** Time from manifest to carrier pickup scan.

### Performance Breakdown (92,707 Shipments)
| Status Metric | Volume | Percentage | Operational Significance |
|---|---|---|---|
| **DELIVERED** | 88,013 | **94.94%** | Healthy delivery baseline across e-commerce benchmarks (>92%). |
| **RTO (Return to Origin)** | 4,631 | **4.99%** | Moderate aggregate rate, but heavily skewed by payment mode. |
| **LOST** | 21 | **0.02%** | Excellent transit security (loss rate is negligible at $<0.05\%$). |
| **Not Shipped** | 42 | **0.05%** | Minor WMS inventory/order cancellation cancellation artifacts. |

### Where Are We Succeeding?
- **Prepaid Delivery Excellence:** Prepaid shipments achieve a phenomenal **99.16% delivery success rate** (only 468 returns out of 58,666 orders). When customer payment is secured, delivery failure is practically zero.
- **Loss Prevention:** Only 21 shipments were lost across the entire month, indicating disciplined carrier custody and linehaul security.

### Where Are We at Risk?
1. **Severe Single-Partner Concentration Risk:** Courier **C9** (routed via Aggregator A3) handles **57,899 shipments (62.4% of total volume)**. The company is completely dependent on a single carrier. Any regional hub strike, severe weather disruption, or capacity crunch at C9 will halt over 60% of customer orders.
2. **COD Return Hemorrhage:** COD orders have an **RTO rate of 12.23%** (4,163 returns out of 34,041 orders). **COD accounts for 89.9% of all returned products**. Every RTO consumes double freight, damages packaging, locks up inventory, and incurs reverse logistics fees without generating revenue.

### What Would I Act on First?
- **Immediate Action:** Institute **carrier diversification** in Zone A & B to cap Courier C9's volume at 50%, while deploying an **automated WhatsApp NDR (Non-Delivery Report) intervention engine** after failed attempt #1 to capture customer re-delivery instructions before initiating RTO.

---

## 2. Cost-to-Serve & Financial Leakage (Question 2)

### Cost Structure Overview
Applying the contracted Rate Card schedules per Airway Bill (AWB) with 500g slab rounding and COD surcharges yields the total logistics cost structure:

- **Total Monthly Logistics Spend:** **₹64,81,773.20 (~₹64.82 Lakhs)**
  - Base & Additional Freight: **₹56,16,432.20 (86.6%)**
  - COD Flat Handling Fees: **₹8,65,341.00 (13.4%)**
- **Average Cost per AWB:** **₹69.92**
- **Average Cost per Delivered Order:** **₹73.65**

### Rate Card Pricing Comparison (First 500g Base Rate)
| Zone | A1 Rate | A2 Rate | A3 Rate | A3 Surcharge vs Lowest Partner |
|---|---|---|---|---|
| **Zone A (Intra-City)** | **₹19.0** | ₹20.2 | ₹24.0 | **+₹5.0 (+26.3% higher)** |
| **Zone B (Regional)** | **₹22.0** | ₹23.5 | ₹27.0 | **+₹5.0 (+22.7% higher)** |
| **Zone C (Metro-to-Metro)** | **₹32.0** | ₹32.5 | ₹33.0 | **+₹1.0 (+3.1% higher)** |
| **Zone D (Rest of India)** | **₹38.0** | ₹39.2 | ₹39.0 | **+₹1.0 (+2.6% higher)** |
| **Zone E (Special / NE / J&K)**| **₹41.0** | ₹44.8 | ₹56.0 | **+₹15.0 (+36.6% higher)** |

### Where Are We Overspending? (The ₹71.4 Lakh Leakage)
Aggregator A3 handles **73.0% of all shipments (67,642 orders)**, totaling **₹50.25 Lakhs** in freight spend.
- If these exact same shipments had been routed via **Aggregator A1**, the total spend would have been **₹44.30 Lakhs**.
- **Net Monthly Overpayment:** **₹5,95,193 / month**
- **Annualized Financial Leakage:** **₹71,42,316 (~₹71.4 Lakhs/year)**

Because A3 charges ₹24 vs A1’s ₹19 in Zone A, and ₹56 vs A1’s ₹41 in Zone E, routing 3 out of 4 parcels to A3 is directly bleeding company cash.

### How to Reduce Shipping Cost Without Compromising Speed
1. **Phased Reallocation in Core Zones (Quick Win):** Reallocate **25% to 30% of Zone A and Zone B volume** from A3 to A1 and A2. Zone A/B delivery speeds for A1 (2.4 days) are within 6 hours of A3 (2.2 days), saving **₹55,000 to ₹70,000 monthly** immediately.
2. **Packaging Optimization:** 98.8% of shipments are $\le 0.5$kg. Ensure warehouse teams use standardized poly-mailers to prevent volumetric weight crossing 500g, avoiding accidental multi-slab billing.
3. **Prepayment Conversion:** Every order converted from COD to Prepaid saves **₹25.00 in flat COD fees** plus eliminates the risk of RTO reverse freight.

---

## 3. Order Mix & Geographic Intelligence (Question 3)

### Geographic Pareto Analysis (Top 5 States)
Demand is intensely clustered in 5 states, which generate **65.4% of total order volume**:
1. **Maharashtra:** 24,650 orders (26.6% share) • ₹15.7L spend • 96.0% delivered
2. **Karnataka:** 12,731 orders (13.7% share) • ₹7.5L spend • 96.8% delivered
3. **Delhi:** 9,413 orders (10.2% share) • ₹6.5L spend • 95.4% delivered
4. **Gujarat:** 7,650 orders (8.3% share) • ₹5.6L spend • 96.0% delivered
5. **Uttar Pradesh:** 6,242 orders (6.7% share) • ₹4.8L spend • 91.7% delivered (7.9% RTO)

### Key Patterns & Operational Priorities
1. **Western Corridor Dominance (Maharashtra + Gujarat = 34.8% of National Volume):**
   - *Operational Priority:* If the central warehouse is in Southern India (e.g. Bangalore), shipping 32,000+ parcels to MH and GJ incurs Zone C/D rates (₹32–₹39/parcel). Establishing a **Western Regional Fulfillment Center (RFC)** in Mumbai/Bhiwandi converts these to Zone A/B shipments (₹19–₹22/parcel), saving **₹10–₹15 per parcel** (~₹3.5–₹4.5 Lakhs/month).
2. **Weight Profile Uniformity:**
   - **98.8% (91,595 orders)** weigh $\le 0.5$ kg. Only 1.2% are multi-item packages $>0.5$ kg.
   - *Priority:* Contracting should focus 100% on negotiating the **base 500g slab rate**, rather than additional slab pricing.
3. **High-Risk COD Geographies:**
   - In Uttar Pradesh, RTO reaches **7.9%** (vs. 3.2% in Karnataka). Tier 2/3 COD orders experience higher buyer remorse and delivery refusal.
   - *Priority:* Implement targeted OTP verification on COD orders in Tier 2/3 pin codes in UP, Bihar, and Rajasthan.

---

## 4. Courier & Aggregator Strategy (Question 4)

### Partner Benchmark Scorecard
| Partner | Total Shipments | Volume Share | Delivery Rate | RTO Rate | Avg Transit TAT | Avg Cost / AWB |
|---|---|---|---|---|---|---|
| **Aggregator A3** | 67,642 | **73.0%** | **95.0%** | 5.0% | **2.18 days** | ₹74.29 (Highest) |
| **Aggregator A1** | 12,989 | **14.0%** | 94.7% | 5.3% | 2.43 days | **₹53.11 (Lowest)** |
| **Aggregator A2** | 12,076 | **13.0%** | **95.0%** | 4.9% | 2.44 days | ₹63.50 (Balanced) |

### Volume Allocation Strategy: Dynamic Balancing
- **The Trade-off:** A1 is ₹21 cheaper per AWB on average than A3, but A3 is ~6 hours faster in transit and currently absorbs 73% of scale.
- **The Flawed Approach:** Shifting 100% volume to A1 overnight would trigger pickup truck shortages, local hub congestion, and SLA collapse.
- **The Senior Operational Recommendation (Phased Reallocation):**
  - **Zone A & B:** Shift **25% to 30% of volume** from A3 to A1 and A2 immediately. Both A1 and A2 have excellent local delivery infrastructure.
  - **Zone C & D:** Maintain a **50/30/20 split** between A3, A1, and A2 to maintain carrier competition and safeguard delivery speeds.
  - **Zone E (Northeast / J&K):** Route primarily to A1 (₹41 base vs. A3's ₹56 base), saving ₹15 per parcel.

### Simulator Results (Tested on 92,707 Rows):
- **A 25% Zone A/B Shift** moves **7,951 orders** from A3 to A1/A2.
- **Immediate Monthly Net Savings:** **₹55,864 / month**
- **Annualized Bottom-Line Contribution:** **₹6.70 Lakhs**
- **Operational Risk:** **LOW** (A1 volume expands from 13.0k to 17.0k, well within safe courier scaling limits).

### Long-Term Aggregator Strategy: The Hybrid Contract Model
At **~1.1 Million shipments/year**, BlissClub should not rely 100% on aggregators. We recommend a **Hybrid Sourcing Architecture**:
1. **Direct Carrier Contracts** (e.g. Delhivery, BlueDart) for top 3 metro states (MH, KA, DL = 50%+ volume) to capture **10–15% lower direct rates**.
2. **Aggregators (A1, A2)** retained for long-tail Tier 3/4 and Zone E/F coverage where automated failover and broad postal reach are critical.

---

## 5. Process Efficiency & SLA Design (Question 5)

### The Click-to-Deliver Lifecycle Waterfall
Using the 4 event timestamps, we map the exact order journey for delivered shipments:

```
[Order Placed] ──► [AWB Assigned] ──► [Courier Pickup Scan] ──► [Delivered to Doorstep]
       │                   │                         │                           │
       └───── Stage 1 ─────┴──────── Stage 2 ────────┴────────── Stage 3 ────────┘
          Warehouse Pack         Dock Handover Lag           Courier In-Transit
            (5.95 hrs)              (15.98 hrs)                 (2.25 days)
```

| Lifecycle Stage | Mean Time | Median Time | P90 Time | SLA Target | Breach Rate | Root Cause / Diagnosis |
|---|---|---|---|---|---|---|
| **Stage 1: Warehouse Fulfillment** (`Order` $\rightarrow$ `AWB`) | 5.95 hrs | **0.79 hrs** | 16.25 hrs | $\le 12$ hrs | 18.26% | **Healthy.** Orders placed before 14:00 are manifested in under 1 hour. P90 driven by late-night orders. |
| **Stage 2: Courier Handover Lag** (`AWB` $\rightarrow$ `Pickup`) | **15.98 hrs** | **17.17 hrs** | **27.83 hrs** | $\le 12$ hrs | **55.05%** | **CRITICAL BOTTLENECK.** Manifested parcels sit on warehouse docks overnight awaiting carrier scan. |
| **Stage 3: Courier Transit** (`Pickup` $\rightarrow$ `Delivered`) | 2.25 days | 1.94 days | 3.83 days | $\le 4$ days | 6.20% | **Healthy.** Couriers execute linehaul efficiently once packages are in their network. |
| **Total Click-to-Deliver** (`Order` $\rightarrow$ `Delivered`) | 3.17 days | 2.90 days | 4.94 days | $\le 5$ days | 9.17% | 75% of total lead time is transit, but 20% is lost before carrier pickup. |

### Process Gap Identified
The single largest point of failure is **Stage 2 (Handover Lag)**. Over **55% of parcels breach the 12-hour handover SLA**. Couriers arrive late for daily pickups or perform consolidation scans off-site the next morning. Eliminating this dock lag immediately shaves **12 to 18 hours off customer Click-to-Deliver TAT**.

### Enforceable SLAs & Accountability Framework
1. **Internal Warehouse SLA (Order to Manifest):**
   - *Target:* $\le 12$ hours (95% adherence).
   - *Operational Cutoff:* Orders placed before **14:00** must be picked, packed, and manifested by **16:00**.
2. **Courier Pickup Window SLA (Manifest to Scan):**
   - *Target:* $\le 4$ hours from manifest window.
   - *Requirement:* Courier pickup vans must arrive between **17:00 and 19:00** for physical cage handover.
   - *Contract Penalty:* **₹10 per parcel billing credit** for any batch not scanned on the designated pickup date.
3. **Linehaul Transit SLA by Zone:**
   - *Targets:* Zone A: $\le 24$h | Zone B: $\le 48$h | Zone C/D: $\le 72$–$96$h | Zone E: $\le 120$h.
   - *Contract Penalty:* **25% freight refund** on any parcel exceeding the agreed transit SLA by $>24$ hours.

---

## 6. Your 90-Day Operational Action Agenda (Question 6)

### Strategic Risk Assessment: Pitfalls & Failure Modes to Avoid
- **Pitfall 1 (Uncalibrated Volume Shifts):** Moving 100% volume to A1 overnight. *Failure Mode:* Carrier pickup capacity collapse and severe transit delays. *Mitigation:* Phased 25% reallocation in Zone A/B with daily pickup caps.
- **Pitfall 2 (Premature Over-Engineering):** Attempting to build a bespoke in-house routing engine from scratch. *Failure Mode:* 6–9 months of engineering backlog delivering zero near-term ROI. *Mitigation:* Exploit immediate contractual and cutoff levers first.
- **Pitfall 3 (Indiscriminate COD Restrictions):** Disabling COD completely. *Failure Mode:* Eliminates 36.7% of total sales volume (34,000 orders), damaging customer acquisition. *Mitigation:* Address root cause through checkout UPI discounts and high-risk pincode verification.

---

### The Phased Execution Roadmap

```
DAYS 1 – 30: QUICK WINS           DAYS 31 – 60: RTO & SLAS          DAYS 61 – 90: SCALE & RFQ
• 25% Zone A/B shift to A1/A2     • WhatsApp NDR verification       • Direct Carrier RFP (MH, KA, DL)
• 14:00 Dock handover cutoff      • Checkout UPI discount nudge     • Dynamic pincode-level routing
• Cap Courier C9 volume at 50%    • Enforce SLA penalty clawbacks   • Western RFC feasibility model
Target: ₹55k/mo savings; TAT -12h  Target: COD RTO 12.2% ➔ 10.0%    Target: 10% lower cost; RTO < 4%
```

#### Days 1 – 30: Immediate Financial Relief & Dock Accountability
- **Action 1 (Routing Quick Win):** Shift 25% of Zone A and Zone B volume from A3 to A1 and A2.
  - *Metric:* Unlocks **₹55,000+ monthly savings** in Month 1 with zero capital expenditure.
- **Action 2 (Dock Cutoff Enforcement):** Establish mandatory 18:30 daily courier pickup cutoff. All orders manifested before 16:00 must be scanned into carrier vans by 19:00.
  - *Metric:* Reduces Stage 2 handover lag from 16.0 hours to $<8.0$ hours.
- **Action 3 (De-risk Courier C9):** Cap C9 allocation at 50% max volume share by onboarding secondary couriers for Zone C/D.

#### Days 31 – 60: RTO Mitigation & Contractual Rigor
- **Action 1 (Automated WhatsApp NDR Engine):** Implement automated WhatsApp messaging triggered instantly upon a failed first delivery attempt. Customers confirm address, pin location, and reschedule delivery time before parcel is returned.
  - *Metric:* Expect to recover **20% to 25% of potential returns**, dropping overall RTO from 5.0% to 4.2%.
- **Action 2 (Checkout Prepayment Incentives):** Partner with Product/Growth to offer ₹30–₹50 instant discounts for UPI prepayment at checkout.
  - *Metric:* Reduce COD order mix from 36.7% down to $<30\%$, permanently eliminating high-risk returns.
- **Action 3 (Carrier Scorecards & Penalties):** Deploy weekly courier scorecards with financial clawbacks for transit SLA breaches.

#### Days 61 – 90: Structural Scaling & Direct Contracting
- **Action 1 (Direct Carrier RFQ):** Issue direct carrier tenders for the top 3 corridors (Maharashtra, Karnataka, Delhi = 50%+ volume), bypassing aggregator margins.
  - *Metric:* Captures **10% to 15% rate reductions** (~₹30–₹45 Lakhs annualized).
- **Action 2 (Dynamic Pincode-Level Routing):** Implement automated routing rules that assign orders based on historical 3-digit pincode delivery success and carrier hub congestion.
- **Action 3 (Western RFC Business Case):** Complete financial modeling for a warehouse node in Mumbai/Bhiwandi to convert MH/GJ shipments to local delivery.

---

### What Success Looks Like at Day 90 (Target OKRs)

| Operational Dimension | Baseline (Day 0) | Day 90 Target | Business Value Delivered |
|---|---|---|---|
| **Average Cost per Delivered Order** | ₹73.65 | **₹65.50** | **11.0% cost reduction** (~₹5.5L monthly savings). |
| **Gross Return to Origin (RTO)** | 5.00% | **$\le 3.90\%$** | ~1,000 fewer returns/month; inventory protected. |
| **COD Return Rate** | 12.23% | **$\le 9.50\%$** | Massive recovery of otherwise lost COD revenue. |
| **Click-to-Deliver Speed** | 3.17 days (76h) | **2.40 days (58h)** | **18-hour reduction** in customer delivery lead time. |
| **Courier C9 Volume Share** | 62.4% | **$\le 40.0\%$** | Healthy, multi-carrier network redundancy. |
| **Prepaid Order Share** | 63.3% | **$\ge 72.0\%$** | Improved cash flow and reduced return exposure. |

---

*This document, backed by the interactive decision dashboard at `docs/index.html` and verified Python analytics engine in `src/`, provides the complete strategic and analytical framework to optimize BlissClub’s last-mile operations.*

