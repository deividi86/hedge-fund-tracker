#!/usr/bin/env python3
"""
Hedge Fund Tracker — Track what the biggest funds are buying and selling.

Uses SEC 13F filings via the SEC EDGAR Financial Data API on RapidAPI.
Get your API key at: https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api
"""

import argparse
import json
import os
import sys

import requests

API_BASE = "https://sec-edgar-financial-data-api.p.rapidapi.com"
API_HOST = "sec-edgar-financial-data-api.p.rapidapi.com"

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Well-known fund CIKs for convenience
KNOWN_FUNDS = {
    "berkshire": {"cik": "0001067983", "name": "Berkshire Hathaway (Warren Buffett)"},
    "bridgewater": {"cik": "0001350694", "name": "Bridgewater Associates (Ray Dalio)"},
    "renaissance": {"cik": "0001037389", "name": "Renaissance Technologies (Jim Simons)"},
    "citadel": {"cik": "0001423053", "name": "Citadel Advisors (Ken Griffin)"},
    "soros": {"cik": "0001029160", "name": "Soros Fund Management"},
    "appaloosa": {"cik": "0001656456", "name": "Appaloosa Management (David Tepper)"},
    "pershing": {"cik": "0001336528", "name": "Pershing Square (Bill Ackman)"},
    "third-point": {"cik": "0001040273", "name": "Third Point (Dan Loeb)"},
    "elliott": {"cik": "0001048445", "name": "Elliott Management (Paul Singer)"},
    "two-sigma": {"cik": "0001179392", "name": "Two Sigma Investments"},
    "tiger-global": {"cik": "0001167483", "name": "Tiger Global Management"},
    "dragoneer": {"cik": "0001571052", "name": "Dragoneer Investment Group"},
    "millennium": {"cik": "0001273087", "name": "Millennium Management (Israel Englander)"},
    "point72": {"cik": "0001603466", "name": "Point72 (Steve Cohen)"},
    "de-shaw": {"cik": "0001009207", "name": "D.E. Shaw & Co"},
}


def get_api_key():
    """Retrieve the RapidAPI key from environment or .env file."""
    key = os.environ.get("RAPIDAPI_KEY")
    if key:
        return key
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("RAPIDAPI_KEY="):
                    return line.split("=", 1)[1].strip().strip("\"'\"")
    return None


def api_request(endpoint: str, params: dict, api_key: str) -> dict:
    """Make a request to the SEC EDGAR API."""
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": API_HOST,
    }
    resp = requests.get(f"{API_BASE}{endpoint}", params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_13f_filings(cik: str, api_key: str) -> list:
    """Fetch recent 13F filing summaries for a given CIK."""
    data = api_request("/api/v1/filings", {"cik": cik, "formType": "13F-HR", "limit": "4"}, api_key)
    return data if isinstance(data, list) else data.get("filings", data.get("results", []))


def get_13f_holdings(cik: str, api_key: str, filing_date: str = None) -> list:
    """Fetch 13F holdings for a given CIK."""
    params = {"cik": cik}
    if filing_date:
        params["filingDate"] = filing_date
    data = api_request("/api/v1/holdings/13f", params, api_key)
    return data if isinstance(data, list) else data.get("holdings", data.get("results", []))


def format_value(val) -> str:
    """Format a dollar value with abbreviations."""
    if val is None:
        return "-"
    try:
        val = float(val)
    except (ValueError, TypeError):
        return str(val)
    if abs(val) >= 1_000_000_000:
        return f"${val / 1_000_000_000:.2f}B"
    if abs(val) >= 1_000_000:
        return f"${val / 1_000_000:.1f}M"
    if abs(val) >= 1_000:
        return f"${val / 1_000:.0f}K"
    return f"${val:,.0f}"


def format_shares(val) -> str:
    """Format share count."""
    if val is None:
        return "-"
    try:
        val = int(val)
    except (ValueError, TypeError):
        return str(val)
    if abs(val) >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    if abs(val) >= 1_000:
        return f"{val / 1_000:.1f}K"
    return f"{val:,}"


# ---------------------------------------------------------------------------
# Rich output
# ---------------------------------------------------------------------------

def print_holdings_rich(fund_name: str, holdings: list, top_n: int = 20):
    console = Console()
    console.print()
    console.print(
        Panel(
            Text("Hedge Fund Tracker", style="bold cyan", justify="center"),
            subtitle="Powered by SEC EDGAR Financial Data API",
            box=box.DOUBLE,
        )
    )
    console.print()
    console.print(f"  [bold]{fund_name}[/bold]  —  [dim]Top {min(top_n, len(holdings))} Holdings from Latest 13F Filing[/dim]")
    console.print()

    if not holdings:
        console.print("  [dim]No holdings data available.[/dim]\n")
        return

    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold magenta", pad_edge=False)
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Company", style="cyan", min_width=28)
    table.add_column("Shares", justify="right", style="white", min_width=12)
    table.add_column("Value", justify="right", style="green", min_width=12)
    table.add_column("% of Portfolio", justify="right", style="yellow", min_width=14)

    # Sort by value descending
    sorted_holdings = sorted(
        holdings,
        key=lambda h: float(h.get("value", 0) or 0),
        reverse=True,
    )[:top_n]

    total_value = sum(float(h.get("value", 0) or 0) for h in holdings)

    for i, h in enumerate(sorted_holdings, 1):
        name = h.get("nameOfIssuer") or h.get("name") or h.get("company", "Unknown")
        shares = h.get("shrsOrPrnAmt", {}).get("sshPrnamt") if isinstance(h.get("shrsOrPrnAmt"), dict) else h.get("shares")
        value = h.get("value")
        pct = ""
        if total_value > 0 and value:
            try:
                pct = f"{float(value) / total_value * 100:.1f}%"
            except (ValueError, TypeError):
                pct = "-"
        table.add_row(str(i), name, format_shares(shares), format_value(value), pct)

    console.print(table)
    console.print()
    if total_value > 0:
        console.print(f"  [dim]Total portfolio value: {format_value(total_value)}[/dim]")
        console.print()


# ---------------------------------------------------------------------------
# Plain-text output
# ---------------------------------------------------------------------------

def print_holdings_plain(fund_name: str, holdings: list, top_n: int = 20):
    print()
    print("=" * 70)
    print("  Hedge Fund Tracker")
    print("  Powered by SEC EDGAR Financial Data API")
    print("=" * 70)
    print()
    print(f"  {fund_name}  —  Top {min(top_n, len(holdings))} Holdings from Latest 13F Filing")
    print("-" * 70)

    if not holdings:
        print("  No holdings data available.\n")
        return

    sorted_holdings = sorted(
        holdings,
        key=lambda h: float(h.get("value", 0) or 0),
        reverse=True,
    )[:top_n]

    total_value = sum(float(h.get("value", 0) or 0) for h in holdings)

    header = "  {:>3}  {:<30} {:>12} {:>12} {:>12}".format("#", "Company", "Shares", "Value", "% Portfolio")
    print(header)
    print("  " + "-" * 66)

    for i, h in enumerate(sorted_holdings, 1):
        name = h.get("nameOfIssuer") or h.get("name") or h.get("company", "Unknown")
        shares = h.get("shrsOrPrnAmt", {}).get("sshPrnamt") if isinstance(h.get("shrsOrPrnAmt"), dict) else h.get("shares")
        value = h.get("value")
        pct = ""
        if total_value > 0 and value:
            try:
                pct = f"{float(value) / total_value * 100:.1f}%"
            except (ValueError, TypeError):
                pct = "-"
        name_trunc = (name[:28] + "..") if len(name) > 30 else name
        print(f"  {i:>3}  {name_trunc:<30} {format_shares(shares):>12} {format_value(value):>12} {pct:>12}")

    print()
    if total_value > 0:
        print(f"  Total portfolio value: {format_value(total_value)}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_list_funds(args):
    """List well-known funds."""
    print("\nAvailable fund aliases:\n")
    for alias, info in sorted(KNOWN_FUNDS.items()):
        print(f"  {alias:<18} {info[name]:<45} CIK: {info[cik]}")
    print(f"\nUsage: python tracker.py holdings {list(KNOWN_FUNDS.keys())[0]}\n")


def cmd_holdings(args):
    """Show top holdings for a fund."""
    api_key = args.key or get_api_key()
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Set RAPIDAPI_KEY env var, create a .env file, or use --key.", file=sys.stderr)
        print("Get your key at https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api", file=sys.stderr)
        sys.exit(1)

    fund_input = args.fund.lower()
    if fund_input in KNOWN_FUNDS:
        cik = KNOWN_FUNDS[fund_input]["cik"]
        fund_name = KNOWN_FUNDS[fund_input]["name"]
    else:
        cik = fund_input
        fund_name = f"CIK {cik}"

    try:
        holdings = get_13f_holdings(cik, api_key)
    except requests.exceptions.HTTPError as exc:
        print(f"Error: HTTP {exc.response.status_code}: {exc.response.text[:300]}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    top_n = args.top

    if args.output == "json":
        print(json.dumps(holdings[:top_n] if top_n else holdings, indent=2))
    elif RICH_AVAILABLE:
        print_holdings_rich(fund_name, holdings, top_n)
    else:
        print_holdings_plain(fund_name, holdings, top_n)


def main():
    parser = argparse.ArgumentParser(
        description="Track hedge fund portfolios using SEC 13F filings.",
        epilog="Get your API key at https://rapidapi.com/dapdev-dapdev-default/api/sec-edgar-financial-data-api",
    )
    parser.add_argument("-k", "--key", help="RapidAPI key (or set RAPIDAPI_KEY env var)")
    parser.add_argument("-o", "--output", choices=["table", "json"], default="table", help="Output format")
    sub = parser.add_subparsers(dest="command")

    # list-funds
    p_list = sub.add_parser("list-funds", help="Show available fund aliases")
    p_list.set_defaults(func=cmd_list_funds)

    # holdings
    p_hold = sub.add_parser("holdings", help="Show top holdings for a fund")
    p_hold.add_argument("fund", help="Fund alias (e.g. berkshire) or CIK number")
    p_hold.add_argument("-n", "--top", type=int, default=20, help="Number of top holdings to show (default: 20)")
    p_hold.set_defaults(func=cmd_holdings)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\nQuick start:")
        print("  python tracker.py list-funds          # See available funds")
        print("  python tracker.py holdings berkshire   # Buffett's latest holdings")
        print()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
