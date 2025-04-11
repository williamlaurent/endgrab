import requests
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + "\n🔎 JS Recon Bot - Full Endpoint & Env Scanner")
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

        # 🔍 Endpoint detection
        endpoints = sorted(set(
            re.findall(r'\/(?:api|v1|v2|auth|svc|user|merchant)[a-zA-Z0-9\/_\-]{3,}', js)
        ))

        if endpoints:
            print(Fore.GREEN + f"🔗 Found {len(endpoints)} endpoint(s):")
            for ep in endpoints:
                print(Fore.GREEN + f"  - {ep}")
        else:
            print(Fore.YELLOW + "⚠️  No common API endpoints found.")

        # 🔐 Suspicious keywords
        keywords = ['token', 'auth', 'upload', 'delete', 'password', 'jwt', 'profile', 'image', 'admin', 'secret', 'apikey']
        found = [k for k in keywords if k.lower() in js.lower()]
        if found:
            print(Fore.MAGENTA + "\n🔑 Suspicious keywords:")
            for k in found:
                print(Fore.MAGENTA + f"  ✅ {k}")
        else:
            print(Fore.BLUE + "ℹ️  No suspicious keywords found.")

        # 🧬 Nuxt env block
        env_blocks = re.findall(r'env\s*:\s*{(.*?)}', js, re.DOTALL)
        if env_blocks:
            print(Fore.YELLOW + "\n🧬 Found env blocks:")
            for block in env_blocks:
                lines = block.split(',')
                for line in lines:
                    pair = line.strip().split(":", 1)
                    if len(pair) == 2:
                        key, value = pair
                        key = key.strip().strip('"').strip("'")
                        value = value.strip().strip('"').strip("'")
                        if key and value:
                            print(Fore.YELLOW + f"  {key}: {Fore.WHITE}{value}")

        # ⚙️ Nuxt config block
        config_blocks = re.findall(r'config\s*:\s*{(.*?)}', js, re.DOTALL)
        if config_blocks:
            print(Fore.LIGHTBLUE_EX + "\n⚙️  Found config blocks:")
            for block in config_blocks:
                lines = block.split(',')
                for line in lines:
                    pair = line.strip().split(":", 1)
                    if len(pair) == 2:
                        key, value = pair
                        key = key.strip().strip('"').strip("'")
                        value = value.strip().strip('"').strip("'")
                        if key and value:
                            print(Fore.LIGHTBLUE_EX + f"  {key}: {Fore.WHITE}{value}")

        # 🔎 NUXT_ env vars
        nuxt_envs = re.findall(r'["\'](NUXT_[A-Z0-9_]+)["\']\s*:\s*["\']([^"\']+)["\']', js)
        if nuxt_envs:
            print(Fore.LIGHTMAGENTA_EX + "\n🧬 Found NUXT_ env variables:")
            for key, val in nuxt_envs:
                print(Fore.LIGHTMAGENTA_EX + f"  {key}: {Fore.WHITE}{val}")

        # 🧨 AWS Access Key
        aws_keys = re.findall(r'AKIA[0-9A-Z]{16}', js)
        if aws_keys:
            print(Fore.RED + "\n🔥 AWS Access Keys Found:")
            for key in aws_keys:
                print(Fore.RED + f"  🛑 {key}")

        # 📍 Google Maps API Key
        gmap_keys = re.findall(r'AIza[0-9A-Za-z\-_]{35}', js)
        if gmap_keys:
            print(Fore.RED + "\n📍 Google Maps API Keys Found:")
            for key in gmap_keys:
                print(Fore.RED + f"  🛑 {key}")

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
