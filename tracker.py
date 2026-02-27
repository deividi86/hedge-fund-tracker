#\!/usr/bin/env python3
"""Hedge Fund Tracker - Monitor institutional 13F holdings from SEC filings."""
import argparse
import os
import sys
import requests

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")
API_HOST = "sec-edgar-financial-data-api.p.rapidapi.com"
BASE = f"https://{API_HOST}"
HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": RAPIDAPI_KEY,
}

POPULAR_FUNDS = {
    "berkshire": "0001067983",
    "bridgewater": "0001350694",
    "citadel": "0001423053",
    "renaissance": "0001037389",
}

def search_company(query):
    resp = requests.get(f"{BASE}/companies/search", params={"query": query}, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def get_holdings(cik):
    resp = requests.get(f"{BASE}/holdings/13f/{cik}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def main():
    if not RAPIDAPI_KEY:
        print("Error: Set RAPIDAPI_KEY environment variable")
        print("Get your key at: https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Track hedge fund 13F holdings")
    parser.add_argument("fund", help="Fund name or CIK (e.g. 'Berkshire Hathaway' or 0001067983)")
    parser.add_argument("--top", type=int, default=15, help="Number of top holdings to show")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    
    # Check if it's a known shorthand
    fund_lower = args.fund.lower()
    cik = POPULAR_FUNDS.get(fund_lower)
    
    if not cik:
        if args.fund.startswith("000"):
            cik = args.fund
        else:
            print(f"Searching for '{ args.fund}'...")
            results = search_company(args.fund)
            companies = results.get("companies", [])
            if not companies:
                print("No companies found.")
                sys.exit(1)
            cik = companies[0]["cik"]
            print(f"Found: {companies[0]['name']} (CIK: {cik})")
    
    data = get_holdings(cik)
    
    if args.json:
        import json
        print(json.dumps(data, indent=2))
        return
    
    holdings = data.get("holdings", [])
    holdings_sorted = sorted(holdings, key=lambda x: x.get("value", 0), reverse=True)
    total_value = sum(h.get("value", 0) for h in holdings)
    
    print(f"\n{'='*60}")
    print(f"  13F Holdings | {len(holdings)} positions | ${total_value:,.0f} total")
    print(f"{'='*60}\n")
    
    for i, pos in enumerate(holdings_sorted[:args.top], 1):
        name = pos.get("name", "Unknown")
        value = pos.get("value", 0)
        shares = pos.get("shares", 0)
        pct = (value / total_value * 100) if total_value else 0
        bar = "\u2588" * int(pct / 2) + "\u2591" * max(0, 20 - int(pct / 2))
        print(f"  {i:>2}. {name:<30s} ${value:>14,.0f}  {bar} {pct:.1f}%")
    
    if len(holdings) > args.top:
        print(f"\n  ... and {len(holdings) - args.top} more positions")

if __name__ == "__main__":
    main()
