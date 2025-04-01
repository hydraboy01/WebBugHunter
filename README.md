# WebBugHunter

A website vulnerability scanner for Kali Linux that detects XSS, SQL Injection and broken links.

## Features
- XSS Vulnerability Detection
- SQL Injection Testing
- Broken Links Finder

## Installation
```bash
git clone https://github.com/hydraboy01/WebBugHunter.git
cd WebBugHunter
chmod +x webbughunter.py
```

## Usage
```bash
./webbughunter.py -u https://example.com
```

## Requirements
- Python 3
- Kali Linux (Recommended)
- Required Python packages:
  ```bash
  pip install requests beautifulsoup4
  ```

## Contribution
Feel free to contribute by opening issues or pull requests.

## Disclaimer
This tool is for educational purposes only. Use only on websites you own or have permission to test.
