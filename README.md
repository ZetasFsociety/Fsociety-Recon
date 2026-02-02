# FsocietyRecon

Advanced Cybersecurity Reconnaissance Suite

## Features

- **URL to IP Discovery**: Resolve domain names to IP addresses with geolocation info
- **Port Scanner**: Multi-threaded port scanning with banner grabbing
- **Subdomain Finder**: Discover subdomains using common wordlists
- **Vulnerability Scanner**: Basic web vulnerability assessment
- **Full Reconnaissance**: Complete intelligence gathering combining all tools

## Installation

```bash
git clone https://github.com/yourusername/FsocietyRecon.git
cd FsocietyRecon
pip install requests
python fsociety_recon.py
```

## Usage

Run FsocietyRecon:
```bash
python fsociety_recon.py
```

Select from the menu:
1. URL to IP Discovery
2. Port Scanner
3. Subdomain Finder
4. Vulnerability Scanner
5. Full Reconnaissance (All)
0. Exit

## Examples

### URL to IP Discovery
```
Enter URL: google.com
[*] Resolving IP address for google.com...
[+] google.com -> 142.250.191.14
[+] Location: Mountain View, United States
[+] ISP: Google LLC
```

### Port Scanner
```
Enter target: scanme.nmap.org
[*] Starting port scan on scanme.nmap.org...
[+] Port 22/tcp open - SSH
[+] Port 80/tcp open - HTTP
[+] Port 443/tcp open - HTTPS
```

### Subdomain Finder
```
Enter domain: example.com
[*] Starting subdomain scan for example.com...
[+] www.example.com -> 93.184.216.34
[+] mail.example.com -> 93.184.216.35
```

### Full Reconnaissance
```
Enter target: testphp.vulnweb.com
[!] Starting full reconnaissance...
[*] Resolving IP address for testphp.vulnweb.com...
[*] Starting port scan...
[*] Starting subdomain scan...
[*] Vulnerability scan...
```

## Legal Disclaimer

**FsocietyRecon** is for educational and authorized testing purposes only. Users are responsible for complying with applicable laws and regulations. Unauthorized access to computer systems is illegal.

## Requirements

- Python 3.6+
- requests library

## License

MIT License - Use responsibly and ethically.

---

*"We are fsociety. We are everywhere."*