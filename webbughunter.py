#!/usr/bin/env python3
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse

# টুলের ব্যানার ডিসপ্লে
def show_banner():
    print("""
    ██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗██████╗ 
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║██╔══██╗
    ██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██████╔╝
    ██╔══██╗██╔══╝  ██╔══██╗██╔═══╝ ██║   ██║██╔═══╝ 
    ██║  ██║███████╗██████╔╝██║     ╚██████╔╝██║     
    ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝      ╚═════╝ ╚═╝     
    WebBugHunter - Website Vulnerability Scanner v1.0
    """)

# XSS ভালনারেবিলিটি চেক
def check_xss(url):
    test_payload = "<script>alert('XSS')</script>"
    try:
        response = requests.get(url, params={"q": test_payload}, timeout=5)
        if test_payload in response.text:
            return True
    except:
        pass
    return False

# SQL Injection চেক
def check_sql_injection(url):
    test_payload = "' OR '1'='1"
    try:
        response = requests.get(url, params={"id": test_payload}, timeout=5)
        if "error in your SQL syntax" in response.text.lower():
            return True
    except:
        pass
    return False

# Broken Link চেক
def check_broken_links(base_url):
    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        broken_links = []
        for link in links:
            absolute_url = urljoin(base_url, link)
            try:
                res = requests.head(absolute_url, timeout=5, allow_redirects=True)
                if res.status_code >= 400:
                    broken_links.append(absolute_url)
            except:
                broken_links.append(absolute_url)
        
        return broken_links
    except:
        return []

# মেইন ফাংশন
def main():
    show_banner()
    parser = argparse.ArgumentParser(description="WebBugHunter - Website Vulnerability Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan")
    args = parser.parse_args()

    target_url = args.url if args.url.startswith(('http://', 'https://')) else f"http://{args.url}"

    print(f"\n[+] Scanning: {target_url}\n")

    # XSS চেক
    if check_xss(target_url):
        print("[!] Possible XSS Vulnerability Found!")
    else:
        print("[✓] No XSS Vulnerability Detected")

    # SQL Injection চেক
    if check_sql_injection(target_url):
        print("[!] Possible SQL Injection Vulnerability Found!")
    else:
        print("[✓] No SQL Injection Vulnerability Detected")

    # Broken Links চেক
    broken_links = check_broken_links(target_url)
    if broken_links:
        print("\n[!] Broken Links Found:")
        for link in broken_links[:5]:  # প্রথম ৫টি লিঙ্ক দেখাবে
            print(f" - {link}")
    else:
        print("\n[✓] No Broken Links Found")

    print("\n[+] Scan completed!")

if __name__ == "__main__":
    main()
