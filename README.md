# Hedge Fund Tracker — Monitor Institutional 13F Holdings

\![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
\![License: MIT](https://img.shields.io/badge/license-MIT-green)

Track what the world's biggest hedge funds are buying and selling by pulling their 13F filings directly from the SEC — powered by the [SEC EDGAR Financial Data API](https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api) on RapidAPI.

## Quick Demo

```
$ python tracker.py berkshire

============================================================
  13F Holdings | 42 positions | $348,291,520,000 total
============================================================

   1. Apple Inc                       $156,234,000,000  ████████████████████ 44.9%
   2. Bank of America Corp            $ 34,821,000,000  █████░░░░░░░░░░░░░░░ 10.0%
   3. American Express Co             $ 28,456,000,000  ████░░░░░░░░░░░░░░░░  8.2%
   4. Coca-Cola Co                    $ 24,132,000,000  ███░░░░░░░░░░░░░░░░░  6.9%
   5. Chevron Corp                    $ 18,987,000,000  ██░░░░░░░░░░░░░░░░░░  5.5%

  ... and 27 more positions
```

## Installation

```bash
git clone https://github.com/deividi86/hedge-fund-tracker.git
cd hedge-fund-tracker
pip install -r requirements.txt
```

## Usage

1. Get your free API key from [RapidAPI — SEC EDGAR Financial Data API](https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api)
2. Set your key:

```bash
export RAPIDAPI_KEY="your-key-here"
```

3. Track holdings:

```bash
# Use built-in shortcuts
python tracker.py berkshire
python tracker.py citadel
python tracker.py renaissance
python tracker.py bridgewater

# Search by name
python tracker.py "Soros Fund Management"

# Use CIK directly
python tracker.py 0001067983

# Show top N holdings
python tracker.py berkshire --top 25

# Raw JSON output
python tracker.py berkshire --json
```

## Built-in Fund Shortcuts

| Shortcut      | Fund                          | CIK         |
|---------------|-------------------------------|-------------|
| `berkshire`   | Berkshire Hathaway            | 0001067983  |
| `bridgewater` | Bridgewater Associates        | 0001350694  |
| `citadel`     | Citadel Advisors              | 0001423053  |
| `renaissance` | Renaissance Technologies      | 0001037389  |

## Use Cases

- **Track What Billionaires Buy/Sell** — Follow the moves of Buffett, Dalio, and Griffin
- **Find Consensus Picks** — Identify stocks that multiple top funds are accumulating
- **Sector Rotation Analysis** — Spot where institutional money is flowing
- **Portfolio Inspiration** — Build conviction from the smartest money in the room

## API

Powered by the [SEC EDGAR Financial Data API on RapidAPI](https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api).

## License

MIT — see [LICENSE](LICENSE)
