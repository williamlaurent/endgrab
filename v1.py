import requests
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + "\n🔎 JS Recon Bot - Smart API Endpoint Scanner")
    print(Fore.YELLOW + "   by indonesiancodeparty | Input: domain or full URL\n")

def normalize_url(raw_url):
    if not raw_url.startswith("http"):
        raw_url = "https://" + raw_url
    return raw_url.strip("/")

def get_js_urls(base_url):
    try:
        resp = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        js_files = [
            urljoin(base_url, tag['src'])
            for tag in soup.find_all("script", src=True)
            if tag['src'].endswith('.js')
        ]
        return js_files
    except Exception as e:
        print(Fore.RED + f"❌ Failed to fetch page: {e}")
        return []

def fetch_and_scan_js(js_url):
    print(Fore.CYAN + f"\n📥 Scanning JS: {js_url}")
    try:
        r = requests.get(js_url, timeout=10)
        js = r.text

        # 🔍 Endpoint detection (smart regex)
        endpoints = sorted(set(
            re.findall(r'\/(?:api|v1|v2|auth|svc|user|merchant)[a-zA-Z0-9\/_\-]{3,}', js)
        ))

        if endpoints:
            print(Fore.GREEN + f"🔗 Found {len(endpoints)} endpoint(s):")
            for ep in endpoints:
                print(Fore.GREEN + f"  - {ep}")
        else:
            print(Fore.YELLOW + "⚠️  No common API endpoints found.")

        # 🕵️‍♂️ Keyword-based sensitive detection
        keywords = ['token', 'auth', 'upload', 'delete', 'password', 'jwt', 'profile', 'image', 'admin']
        found = [k for k in keywords if k in js]

        if found:
            print(Fore.MAGENTA + "\n🔑 Suspicious keywords:")
            for k in found:
                print(Fore.MAGENTA + f"  ✅ {k}")
        else:
            print(Fore.BLUE + "ℹ️  No suspicious keywords found.")

    except Exception as e:
        print(Fore.RED + f"❌ Error reading JS: {e}")

def main():
    banner()
    try:
        url = input(Fore.WHITE + Style.BRIGHT + "🌐 Target (e.g. domain.com or https://...): ").strip()
        full_url = normalize_url(url)

        print(Fore.BLUE + f"\n🔗 Normalized URL: {full_url}")
        js_files = get_js_urls(full_url)

        if not js_files:
            print(Fore.RED + "❌ No JavaScript files found on this page.")
            sys.exit(1)

        for js in js_files:
            fetch_and_scan_js(js)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n🛑 Stopped by user (Ctrl+C). Exiting cleanly.")
        sys.exit(0)

if __name__ == "__main__":
    main()
