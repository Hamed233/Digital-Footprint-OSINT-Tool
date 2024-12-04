#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import time
import json
import re
from googlesearch import search
import phonenumbers
import whois
from datetime import datetime
from tqdm import tqdm
import pwnedpasswords
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import argparse
import socket
from urllib.parse import urlparse, quote
import hashlib

init(autoreset=True)

class DigitalFootprint:
    def __init__(self, username):
        self.username = username
        self.name_variations = self._generate_name_variations(username)
        self.ua = UserAgent()
        self.results = {}
        self.headers = {'User-Agent': self.ua.random}
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.phone_pattern = re.compile(r'\+?[1-9][0-9]{7,14}')
        
        # Platform URLs with format strings
        self.social_platforms = {
            'GitHub': {
                'api_url': 'https://api.github.com/users/{username}',
                'profile_url': 'https://github.com/{username}'
            },
            'Instagram': {
                'url': 'https://www.instagram.com/{username}/',
                'api_url': None
            },
            'Twitter': {
                'url': 'https://twitter.com/{username}',
                'api_url': None
            },
            'LinkedIn': {
                'url': 'https://www.linkedin.com/in/{username}/',
                'api_url': None
            },
            'Medium': {
                'url': 'https://medium.com/@{username}',
                'api_url': None
            },
            'Reddit': {
                'url': 'https://www.reddit.com/user/{username}',
                'api_url': None
            },
            'TikTok': {
                'url': 'https://www.tiktok.com/@{username}',
                'api_url': None
            },
            'Pinterest': {
                'url': 'https://www.pinterest.com/{username}',
                'api_url': None
            },
            'Twitch': {
                'url': 'https://www.twitch.tv/{username}',
                'api_url': None
            },
            'DeviantArt': {
                'url': 'https://www.deviantart.com/{username}',
                'api_url': None
            },
            'Behance': {
                'url': 'https://www.behance.net/{username}',
                'api_url': None
            },
            'Steam': {
                'url': 'https://steamcommunity.com/id/{username}',
                'api_url': None
            },
            'Spotify': {
                'url': 'https://open.spotify.com/user/{username}',
                'api_url': None
            },
            'SoundCloud': {
                'url': 'https://soundcloud.com/{username}',
                'api_url': None
            },
            'Vimeo': {
                'url': 'https://vimeo.com/{username}',
                'api_url': None
            },
            'Facebook': {
                'url': 'https://www.facebook.com/{username}',
                'api_url': None
            },
            'YouTube': {
                'url': 'https://www.youtube.com/@{username}',
                'api_url': None
            },
            'Telegram': {
                'url': 'https://t.me/{username}',
                'api_url': None
            }
        }

    def _generate_name_variations(self, username):
        """Generate variations of the username"""
        variations = {username}
        
        # Remove special characters
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', username)
        if clean_name != username:
            variations.add(clean_name)
        
        # Add dot between words if there isn't one
        if ' ' in username:
            variations.add(username.replace(' ', '.'))
            variations.add(username.replace(' ', '_'))
            variations.add(username.replace(' ', '-'))
            variations.add(username.replace(' ', ''))
        
        # Remove dots if present
        if '.' in username:
            variations.add(username.replace('.', ''))
            variations.add(username.replace('.', '_'))
            variations.add(username.replace('.', '-'))
            variations.add(username.replace('.', ' '))
        
        # Lowercase variations
        variations.update([v.lower() for v in variations])
        
        return list(variations)

    def check_domain(self, username):
        """Check domain information"""
        potential_domains = [
            f"{username}.com",
            f"{username}.net",
            f"{username}.org",
            f"{username}.io",
            f"{username}.me",
            f"{username}.dev"
        ]
        
        domain_info = {}
        for domain in potential_domains:
            try:
                w = whois.whois(domain)
                if w.domain_name:
                    domain_info[domain] = {
                        "registrar": w.registrar,
                        "creation_date": w.creation_date,
                        "expiration_date": w.expiration_date,
                        "email": w.emails,
                        "url": f"http://{domain}"
                    }
            except Exception:
                continue
        return domain_info

    def check_social_media(self, username):
        """Check social media profiles"""
        results = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_platform = {
                executor.submit(self._check_platform, platform, urls, username): platform
                for platform, urls in self.social_platforms.items()
            }
            
            for future in tqdm(future_to_platform, desc="Checking social media", unit="platform"):
                platform = future_to_platform[future]
                try:
                    result = future.result()
                    if result["exists"]:
                        results[platform] = result
                except Exception as e:
                    print(f"Error checking {platform}: {e}")
        return results

    def _check_platform(self, platform, urls, username):
        """Check individual platform"""
        try:
            self.headers['User-Agent'] = self.ua.random
            
            if platform == "GitHub":
                response = requests.get(urls['api_url'].format(username=username), headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "exists": True,
                        "name": data.get("name"),
                        "bio": data.get("bio"),
                        "location": data.get("location"),
                        "public_repos": data.get("public_repos"),
                        "followers": data.get("followers"),
                        "following": data.get("following"),
                        "profile_url": urls['profile_url'].format(username=username),
                        "email": data.get("email")
                    }
            else:
                url = urls['url'].format(username=username)
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    return {
                        "exists": True,
                        "profile_url": url
                    }
            
            return {"exists": False}
        except Exception:
            return {"exists": False}

    def search_digital_footprint(self):
        """Search for all digital footprints"""
        all_results = {}
        
        print(f"\n{Fore.CYAN}[*] Starting Digital Footprint Analysis for variations of: {self.username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Checking variations: {', '.join(self.name_variations)}{Style.RESET_ALL}\n")

        for variation in self.name_variations:
            print(f"\n{Fore.YELLOW}[*] Analyzing variation: {variation}{Style.RESET_ALL}")
            
            # Check domains
            print(f"\n{Fore.CYAN}[*] Checking domain registrations...{Style.RESET_ALL}")
            domains = self.check_domain(variation)
            if domains:
                print(f"{Fore.GREEN}[+] Found registered domains:{Style.RESET_ALL}")
                for domain, info in domains.items():
                    print(f"    Domain: {domain}")
                    print(f"    URL: {info['url']}")
                    for key, value in info.items():
                        if key not in ['url']:
                            print(f"        {key}: {value}")
            
            # Check social media
            print(f"\n{Fore.CYAN}[*] Checking social media presence...{Style.RESET_ALL}")
            social_results = self.check_social_media(variation)
            
            if social_results:
                for platform, result in social_results.items():
                    if platform == "GitHub" and len(result) > 1:
                        print(f"{Fore.GREEN}[+] {platform} profile found:{Style.RESET_ALL}")
                        for key, value in result.items():
                            if key != "exists" and value:
                                print(f"    {key}: {value}")
                    else:
                        print(f"{Fore.GREEN}[+] {platform} profile found: {result['profile_url']}{Style.RESET_ALL}")
            
            # Search for contact information
            print(f"\n{Fore.CYAN}[*] Searching for contact information...{Style.RESET_ALL}")
            self._search_contact_info(variation)

    def _search_contact_info(self, username):
        """Search for contact information"""
        search_queries = [
            f"{username} contact information",
            f"{username} email address",
            f"{username} contact details",
            f"contact {username}"
        ]
        
        found_emails = set()
        found_numbers = set()
        
        for query in search_queries:
            try:
                search_results = list(search(query, num_results=5))
                
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = [
                        executor.submit(self._scrape_contact_info, url)
                        for url in search_results
                    ]
                    
                    for future in tqdm(futures, desc=f"Scanning websites for {query}", unit="site"):
                        try:
                            emails, numbers = future.result()
                            found_emails.update(emails)
                            found_numbers.update(numbers)
                        except Exception:
                            continue

            except Exception as e:
                print(f"Error searching contact info: {e}")

        if found_emails:
            print(f"{Fore.GREEN}[+] Found potential email addresses:{Style.RESET_ALL}")
            for email in found_emails:
                print(f"    {email}")
        
        if found_numbers:
            print(f"{Fore.GREEN}[+] Found potential phone numbers:{Style.RESET_ALL}")
            for number in found_numbers:
                print(f"    {number}")

    def _scrape_contact_info(self, url):
        """Scrape contact information from a URL"""
        emails = set()
        numbers = set()
        
        try:
            response = requests.get(url, headers={'User-Agent': self.ua.random}, timeout=10)
            if response.status_code == 200:
                # Find email addresses
                emails.update(self.email_pattern.findall(response.text))
                
                # Find and validate phone numbers
                potential_numbers = self.phone_pattern.findall(response.text)
                for number in potential_numbers:
                    try:
                        parsed_number = phonenumbers.parse(number)
                        if phonenumbers.is_valid_number(parsed_number):
                            formatted_number = phonenumbers.format_number(
                                parsed_number,
                                phonenumbers.PhoneNumberFormat.INTERNATIONAL
                            )
                            numbers.add(formatted_number)
                    except:
                        continue
        except:
            pass
            
        return emails, numbers

def main():
    parser = argparse.ArgumentParser(description='Digital Footprint Analyzer')
    parser.add_argument('username', help='Username to analyze')
    args = parser.parse_args()

    analyzer = DigitalFootprint(args.username)
    analyzer.search_digital_footprint()

if __name__ == "__main__":
    main()
