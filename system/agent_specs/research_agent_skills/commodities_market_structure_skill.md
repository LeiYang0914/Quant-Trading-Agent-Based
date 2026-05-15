# commodities_market_structure_skill.md

## Purpose

Ensure commodity futures alpha research is professional, contract-aware, and grounded in real futures market microstructure. Every commodities research memo must demonstrate understanding of how futures markets actually operate — including term structure, carry, inventory, seasonality, and macro drivers.

## When to Use

Whenever the session domain is `commodities`. Apply before writing any commodities alpha discovery note or research memo. This skill is the structural counterpart to `crypto_market_structure_skill.md`.

## Core Market Structure Topics

### 1. Futures Term Structure
- **Contango:** Futures price > spot price. Normal for storable commodities with positive storage costs.
- **Backwardation:** Futures price < spot price. Normal when immediate delivery commands a premium or storage is constrained.
- **Term structure slope:** The shape of the futures curve contains information about inventory, storage, and supply/demand expectations.
- **Roll yield:** The return earned from rolling a futures position as the contract converges toward spot. Positive in backwardation (long futures), negative in contango.
- **Carry:** The total return from holding a futures position, including roll yield and collateral yield.

### 2. Convenience Yield
- The benefit of holding physical inventory rather than a futures contract.
- Arises when supply is tight or demand is urgent.
- Cannot be directly observed — inferred from the basis and storage cost.
- Key for gold, crude oil, and natural gas.

### 3. Storage Cost
- Physical storage cost (warehousing, insurance, financing).
- Higher storage costs → steeper contango.
- Key for crude oil (tank storage), natural gas (underground storage), copper (warehouse).

### 4. Inventory Data
- **Crude oil:** EIA Weekly Petroleum Status Report (eia.gov), API weekly data
- **Natural gas:** EIA Weekly Natural Gas Storage Report
- **Gold/Silver:** LBMA clearing data, COMEX warehouse stocks
- **Copper:** LME and COMEX warehouse stocks
- **Agriculture:** USDA WASDE, NASS, CFTC COT
- **Role in alpha:** Inventory surprises (actual vs. expected) move prices. Low inventory + backwardation = supply stress signal.

### 5. CFTC Commitments of Traders (COT) Reports
- **Weekly report:** Released every Friday, covering positions as of Tuesday.
- **Categories:** Commercial (hedgers), Non-Commercial (speculators), Non-Reportable (small traders).
- **Key alpha signals:**
  - Speculative positioning extremes as contrarian indicator
  - Commercial vs. non-commercial divergence
  - Changes in open interest by category
- **Available for:** Gold, silver, copper, crude oil, natural gas, ags — plus crypto (CME Bitcoin futures)

### 6. Major Exchanges

| Exchange | Key Contracts |
|----------|--------------|
| CME / COMEX | Gold (GC), Silver (SI), Copper (HG) |
| CME / NYMEX | Crude Oil (CL), Natural Gas (NG), RBOB Gasoline (RB) |
| ICE | Brent Crude (B), Gas Oil |
| LME | Copper, Aluminum, Zinc, Nickel (3-month and daily dates) |

### 7. Gold and Silver Market Structure
- **Gold:** Dual role — commodity (jewelry, industrial) and monetary asset (central bank reserves, inflation hedge).
- **Gold drivers:** Real yields (TIPS), USD strength, inflation expectations, central bank buying, ETF flows.
- **Silver:** Industrial + precious. Silver-gold ratio as risk appetite indicator.
- **Gold futures:** COMEX GC, 100 oz contract. Active months: Feb, Apr, Jun, Aug, Dec (plus serial months).
- **Gold leasing market:** GOFO (Gold Forward Offered Rate) — cost of borrowing gold.

### 8. Crude Oil Market Structure
- **CL (WTI):** NYMEX, 1,000 barrels, physical delivery at Cushing, OK.
- **Brent:** ICE, cash-settled based on North Sea physical.
- **Calendar spread:** Price difference between front-month and deferred contracts = inventory signal.
- **Key reports:** EIA Weekly Petroleum Status, OPEC+ production decisions, IEA monthly.

### 9. Seasonality
- Natural gas: winter heating demand, summer cooling demand, shoulder-month storage builds
- Gasoline: summer driving season, RVP transitions
- Agricultural: planting/harvest cycles, weather events
- Gold: Indian wedding season, Chinese New Year
- Seasonality is a known factor — easily overfit. Must survive out-of-sample and cost adjustment.

### 10. Roll Mechanics
- Most commodity futures positions are rolled before expiry to avoid physical delivery.
- Roll schedule matters: rolling during high-volume periods minimizes roll cost.
- Roll yield affects strategic positioning: long backwardated contracts earn positive roll.

### 11. Macro Sensitivity
- Commodities are macro-sensitive in ways crypto is not:
  - USD strength/weakness (commodities priced in USD)
  - Real rates (opportunity cost of holding non-yielding commodities like gold)
  - Inflation expectations
  - Global industrial demand (PMIs, China data)
  - Geopolitical risk

### 12. Liquidity Constraints
- Front-month contracts are most liquid.
- Deferred contracts have wider spreads and lower depth.
- Position limits exist on many contracts.
- Capacity per commodity is limited by daily volume and open interest.

## Required Fields for Every Commodities Memo

Every commodities research memo must clearly identify:
- **Exchange:** CME, ICE, LME, etc.
- **Contract:** Specific contract code and size (e.g., COMEX GC, 100 oz)
- **Settlement mechanism:** Physical delivery or cash-settled?
- **Contract logic:** Front-month, second-month, or which part of the curve?
- **Roll schedule:** When and how does the position roll? What is the expected roll cost?
- **Inventory or positioning data source:** CFTC COT, EIA, LBMA, exchange warehouse data
- **Macro risk drivers:** What macro variables affect this commodity? Which regimes are favorable?

## Inputs

- Domain context (always commodities for this skill)
- Alpha idea specifics
- CFTC COT data, EIA reports, exchange contract specs

## Outputs

- Market structure context integrated into the alpha discovery note or research memo
- Exchange and contract identification
- Inventory/positioning data source identified
- Macro driver assessment

## Anti-Patterns

- Treating commodities like crypto — different market hours, liquidity profiles, and data sources
- Ignoring roll cost in signal construction
- Forgetting that COT data is weekly and released with a 3-day lag
- Proposing a strategy on a deferred contract without checking liquidity
- Applying crypto-specific concepts (funding rates, perps) to commodity futures without adaptation
