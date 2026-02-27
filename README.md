# Hedge Fund Tracker

**See what Buffett, Dalio, and Griffin are buying before everyone else.**

Hedge Fund Tracker is a command-line tool that pulls SEC 13F filings — the quarterly reports that institutional investment managers are required to file — and shows you exactly what the biggest hedge funds are holding, buying, and selling.

Track 15+ major funds including Berkshire Hathaway, Bridgewater, Renaissance Technologies, Citadel, and more.

---

## Example Output

```
╔══════════════════════════════════════════════════════════════════════╗
║                        Hedge Fund Tracker                           ║
║              Powered by SEC EDGAR Financial Data API                 ║
╚══════════════════════════════════════════════════════════════════════╝

  Berkshire Hathaway (Warren Buffett)  —  Top 10 Holdings from Latest 13F Filing

    #  Company                         Shares         Value    % of Portfolio
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1  Apple Inc                       915.56M     $174.3B          28.9%
    2  Bank of America Corp            680.23M      $30.4B           5.0%
    3  American Express Co             151.61M      $44.2B           7.3%
    4  Coca-Cola Co                    400.00M      $28.7B           4.8%
    5  Chevron Corp                    118.61M      $18.8B           3.1%
    6  Occidental Petroleum            255.28M      $16.7B           2.8%
    7  Kraft Heinz Co                  325.63M      $11.5B           1.9%
    8  Moody's Corp                    24.67M      $11.2B           1.9%
    9  DaVita Inc                       36.10M       $5.2B           0.9%
   10  Citigroup Inc                    55.24M       $3.8B           0.6%

  Total portfolio value: $602.4B
```

## Get Started

### 1. Get your API key

This tool uses the [SEC EDGAR Financial Data API](https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api) to pull structured 13F filing data directly from SEC EDGAR.

Sign up on RapidAPI and subscribe to get your API key (free tier available).

### 2. Install

```bash
git clone https://github.com/deividi86/hedge-fund-tracker.git
cd hedge-fund-tracker
pip install -r requirements.txt
```

### 3. Set your API key

```bash
export RAPIDAPI_KEY="your-key-here"
```

Or create a `.env` file in the project directory:

```
RAPIDAPI_KEY=your-key-here
```

### 4. Track

**List available funds:**

```bash
python tracker.py list-funds
```

```
Available fund aliases:

  berkshire          Berkshire Hathaway (Warren Buffett)       CIK: 0001067983
  bridgewater        Bridgewater Associates (Ray Dalio)        CIK: 0001350694
  renaissance        Renaissance Technologies (Jim Simons)     CIK: 0001037389
  citadel            Citadel Advisors (Ken Griffin)            CIK: 0001423053
  soros              Soros Fund Management                     CIK: 0001029160
  pershing           Pershing Square (Bill Ackman)             CIK: 0001336528
  point72            Point72 (Steve Cohen)                     CIK: 0001603466
  de-shaw            D.E. Shaw & Co                            CIK: 0001009207
  ...
```

**View a fund's top holdings:**

```bash
python tracker.py holdings berkshire
```

**Top 5 only:**

```bash
python tracker.py holdings citadel -n 5
```

**JSON output:**

```bash
python tracker.py -o json holdings renaissance | jq .
```

**Use any CIK number directly:**

```bash
python tracker.py holdings 0001067983
```

## Built-in Funds

| Alias | Fund | Manager |
|-------|------|---------|
| `berkshire` | Berkshire Hathaway | Warren Buffett |
| `bridgewater` | Bridgewater Associates | Ray Dalio |
| `renaissance` | Renaissance Technologies | Jim Simons |
| `citadel` | Citadel Advisors | Ken Griffin |
| `soros` | Soros Fund Management | George Soros |
| `pershing` | Pershing Square | Bill Ackman |
| `point72` | Point72 Asset Management | Steve Cohen |
| `de-shaw` | D.E. Shaw & Co | David Shaw |
| `two-sigma` | Two Sigma Investments | John Overdeck |
| `elliott` | Elliott Management | Paul Singer |
| `millennium` | Millennium Management | Israel Englander |
| `tiger-global` | Tiger Global | Chase Coleman |
| `third-point` | Third Point | Dan Loeb |
| `appaloosa` | Appaloosa Management | David Tepper |

## How It Works

Every quarter, hedge funds managing over $100M are required to disclose their equity holdings via [SEC Form 13F](https://www.sec.gov/divisions/investment/13ffaq). This tool pulls that data through the [SEC EDGAR Financial Data API](https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api) and presents it in a readable format.

The data comes directly from SEC EDGAR, so it is as official as it gets.

## Use Cases

- **Follow the Smart Money** — See exactly what positions the top funds are building.
- **Idea Generation** — Discover stocks that multiple top funds are converging on.
- **Due Diligence** — Check if institutional investors are backing (or dumping) a stock you're researching.
- **Quarterly Analysis** — Track how fund allocations shift over time.

## License

MIT License — see [LICENSE](LICENSE) for details.
