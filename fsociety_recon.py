#!/usr/bin/env python3
"""
FsocietyRecon - Advanced Reconnaissance Suite
Professional cybersecurity reconnaissance tools
"""

import socket
import threading
import requests
import subprocess
import sys
import time
from urllib.parse import urlparse
import json

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class FsocietyRecon:
    def __init__(self):
        self.banner()
    
    def banner(self):
        print(f"""
{Colors.CYAN}{Colors.BOLD}
███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗
██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
█████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝ 
██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝  
██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║   
╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝   
                                                              
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
Zetas
{Colors.END}
{Colors.RED}[!] FsocietyRecon v1.0 - Advanced Reconnaissance Suite{Colors.END}
{Colors.YELLOW}[+] URL to IP | Port Scanner | Subdomain Finder | Vuln Scanner{Colors.END}
{Colors.GREEN}[+] Real results, Real reconnaissance tools{Colors.END}
{Colors.PURPLE}[!] Use responsibly - Educational purposes only{Colors.END}
        """)

    def url_to_ip(self, url):
        """Find real IP address from URL"""
        try:
            # Clean URL
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            parsed = urlparse(url)
            hostname = parsed.netloc
            
            print(f"{Colors.YELLOW}[*] Resolving IP address for {hostname}...{Colors.END}")
            
            # DNS resolution
            ip = socket.gethostbyname(hostname)
            print(f"{Colors.GREEN}[+] {hostname} -> {ip}{Colors.END}")
            
            # Additional info
            self.get_ip_info(ip)
            return ip
            
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.END}")
            return None

    def get_ip_info(self, ip):
        """Get detailed information about IP"""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = response.json()
            
            if data['status'] == 'success':
                print(f"{Colors.CYAN}[+] Location: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}{Colors.END}")
                print(f"{Colors.CYAN}[+] ISP: {data.get('isp', 'N/A')}{Colors.END}")
                print(f"{Colors.CYAN}[+] Organization: {data.get('org', 'N/A')}{Colors.END}")
        except:
            pass

    def port_scan(self, target, ports=None):
        """Performs real port scanning"""
        if ports is None:
            # Most common ports
            ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        print(f"{Colors.YELLOW}[*] Starting port scan on {target}...{Colors.END}")
        print(f"{Colors.YELLOW}[*] Scanning {len(ports)} ports{Colors.END}")
        
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    open_ports.append(port)
                    service = self.get_service_name(port)
                    print(f"{Colors.GREEN}[+] Port {port}/tcp open - {service}{Colors.END}")
                    
                    # Banner grabbing
                    banner = self.grab_banner(target, port)
                    if banner:
                        print(f"{Colors.CYAN}    Banner: {banner[:100]}{Colors.END}")
                
                sock.close()
            except:
                pass
        
        # Multi-threaded fast scanning
        threads = []
        for port in ports:
            thread = threading.Thread(target=scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(f"\n{Colors.BOLD}[+] Scan completed: {len(open_ports)} open ports found{Colors.END}")
        return open_ports

    def get_service_name(self, port):
        """Returns service name from port number"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 993: "IMAPS", 995: "POP3S",
            1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt"
        }
        return services.get(port, "Unknown")

    def grab_banner(self, target, port):
        """Grabs banner information from port"""
        try:
            sock = socket.socket()
            sock.settimeout(2)
            sock.connect((target, port))
            
            if port == 80 or port == 8080:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            else:
                sock.send(b"\r\n")
            
            banner = sock.recv(1024).decode().strip()
            sock.close()
            return banner
        except:
            return None

    def subdomain_finder(self, domain):
        """Subdomain discovery - real results"""
        print(f"{Colors.YELLOW}[*] Starting subdomain scan for {domain}...{Colors.END}")
        
        # Common subdomain list
        subdomains = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'api', 'blog',
            'shop', 'forum', 'support', 'help', 'docs', 'cdn', 'static', 'img',
            'images', 'js', 'css', 'assets', 'media', 'upload', 'downloads',
            'secure', 'login', 'auth', 'account', 'user', 'users', 'client',
            'clients', 'customer', 'customers', 'partner', 'partners', 'vendor',
            'vendors', 'supplier', 'suppliers', 'beta', 'alpha', 'demo', 'preview'
        ]
        
        found_subdomains = []
        
        def check_subdomain(sub):
            try:
                full_domain = f"{sub}.{domain}"
                ip = socket.gethostbyname(full_domain)
                found_subdomains.append((full_domain, ip))
                print(f"{Colors.GREEN}[+] {full_domain} -> {ip}{Colors.END}")
            except:
                pass
        
        threads = []
        for sub in subdomains:
            thread = threading.Thread(target=check_subdomain, args=(sub,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(f"\n{Colors.BOLD}[+] {len(found_subdomains)} subdomains found{Colors.END}")
        return found_subdomains

    def vulnerability_scan(self, target):
        """Basic vulnerability scanning"""
        print(f"{Colors.YELLOW}[*] Vulnerability scan for {target}...{Colors.END}")
        
        vulnerabilities = []
        
        # HTTP header check
        try:
            response = requests.get(f"http://{target}", timeout=5)
            headers = response.headers
            
            # Security headers check
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-XSS-Protection': 'XSS protection',
                'X-Content-Type-Options': 'MIME type sniffing protection',
                'Strict-Transport-Security': 'HTTPS enforcement',
                'Content-Security-Policy': 'CSP protection'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    vulnerabilities.append(f"Missing security header: {header} ({description})")
                    print(f"{Colors.RED}[-] Missing: {header}{Colors.END}")
            
            # Server information
            server = headers.get('Server', 'Unknown')
            print(f"{Colors.CYAN}[+] Server: {server}{Colors.END}")
            
            # Powered-by information
            powered_by = headers.get('X-Powered-By', 'Unknown')
            if powered_by != 'Unknown':
                print(f"{Colors.CYAN}[+] Powered by: {powered_by}{Colors.END}")
                vulnerabilities.append(f"Information disclosure: X-Powered-By header ({powered_by})")
            
        except Exception as e:
            print(f"{Colors.RED}[-] HTTP check failed: {str(e)}{Colors.END}")
        
        # Common files check
        common_files = [
            '/robots.txt', '/sitemap.xml', '/.htaccess', '/config.php',
            '/admin', '/admin.php', '/login', '/login.php', '/phpmyadmin',
            '/.git', '/.env', '/backup', '/test', '/debug'
        ]
        
        print(f"{Colors.YELLOW}[*] Common files/directories check...{Colors.END}")
        for file_path in common_files:
            try:
                response = requests.get(f"http://{target}{file_path}", timeout=3)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}[+] Found: {file_path} (Status: {response.status_code}){Colors.END}")
                    vulnerabilities.append(f"Accessible file: {file_path}")
            except:
                pass
        
        print(f"\n{Colors.BOLD}[+] {len(vulnerabilities)} potential security issues found{Colors.END}")
        return vulnerabilities

    def main_menu(self):
        """Main menu"""
        while True:
            print(f"""
{Colors.BOLD}=== FsocietyRecon Main Menu ==={Colors.END}

{Colors.GREEN}1.{Colors.END} URL to IP Discovery
{Colors.GREEN}2.{Colors.END} Port Scanner
{Colors.GREEN}3.{Colors.END} Subdomain Finder
{Colors.GREEN}4.{Colors.END} Vulnerability Scanner
{Colors.GREEN}5.{Colors.END} Full Reconnaissance (All)
{Colors.RED}0.{Colors.END} Exit

            """)
            
            choice = input(f"{Colors.YELLOW}Select your option: {Colors.END}")
            
            if choice == "1":
                url = input(f"{Colors.CYAN}Enter URL (e.g: google.com): {Colors.END}")
                self.url_to_ip(url)
                
            elif choice == "2":
                target = input(f"{Colors.CYAN}Enter target IP/Domain: {Colors.END}")
                ports_input = input(f"{Colors.CYAN}Port list (leave empty for default): {Colors.END}")
                
                if ports_input:
                    ports = [int(p.strip()) for p in ports_input.split(',')]
                else:
                    ports = None
                
                self.port_scan(target, ports)
                
            elif choice == "3":
                domain = input(f"{Colors.CYAN}Enter domain (e.g: example.com): {Colors.END}")
                self.subdomain_finder(domain)
                
            elif choice == "4":
                target = input(f"{Colors.CYAN}Enter target: {Colors.END}")
                self.vulnerability_scan(target)
                
            elif choice == "5":
                target = input(f"{Colors.CYAN}Enter target (full reconnaissance): {Colors.END}")
                print(f"{Colors.RED}[!] Starting full reconnaissance...{Colors.END}")
                
                # IP discovery
                ip = self.url_to_ip(target)
                if ip:
                    # Port scanning
                    open_ports = self.port_scan(ip)
                    # Subdomain discovery
                    self.subdomain_finder(target)
                    # Vulnerability scanning
                    self.vulnerability_scan(target)
                
            elif choice == "0":
                print(f"{Colors.RED}[!] Shutting down FsocietyRecon...{Colors.END}")
                break
                
            else:
                print(f"{Colors.RED}[-] Invalid selection!{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    recon = FsocietyRecon()
    recon.main_menu()