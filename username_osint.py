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

init(autoreset=True)

class UsernameOSINT:
    def __init__(self, username):
        self.username = username
        self.results = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.phone_pattern = re.compile(r'\+?[1-9][0-9]{7,14}')

    def check_github(self):
        """Check GitHub profile"""
        try:
            response = requests.get(f"https://api.github.com/users/{self.username}", headers=self.headers)
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
                    "profile_url": data.get("html_url"),
                    "email": data.get("email")
                }
        except Exception as e:
            print(f"Error checking GitHub: {e}")
        return {"exists": False}

    def check_instagram(self):
        """Check Instagram profile"""
        try:
            response = requests.get(f"https://www.instagram.com/{self.username}/", headers=self.headers)
            return {"exists": response.status_code == 200}
        except Exception as e:
            print(f"Error checking Instagram: {e}")
            return {"exists": False}

    def check_twitter(self):
        """Check Twitter/X profile"""
        try:
            response = requests.get(f"https://twitter.com/{self.username}", headers=self.headers)
            return {"exists": response.status_code == 200}
        except Exception as e:
            print(f"Error checking Twitter: {e}")
            return {"exists": False}

    def check_linkedin(self):
        """Check LinkedIn profile"""
        try:
            response = requests.get(f"https://www.linkedin.com/in/{self.username}/", headers=self.headers)
            return {"exists": response.status_code == 200}
        except Exception as e:
            print(f"Error checking LinkedIn: {e}")
            return {"exists": False}

    def check_medium(self):
        """Check Medium profile"""
        try:
            response = requests.get(f"https://medium.com/@{self.username}", headers=self.headers)
            return {"exists": response.status_code == 200}
        except Exception as e:
            print(f"Error checking Medium: {e}")
            return {"exists": False}

    def search_whatsapp(self):
        """Search for potential WhatsApp numbers"""
        found_numbers = set()
        search_query = f"{self.username} whatsapp contact"
        
        try:
            # Search for potential pages containing WhatsApp numbers
            search_results = search(search_query, num_results=10)
            
            for url in search_results:
                try:
                    response = requests.get(url, headers=self.headers, timeout=5)
                    if response.status_code == 200:
                        # Find potential phone numbers
                        numbers = self.phone_pattern.findall(response.text)
                        for number in numbers:
                            try:
                                parsed_number = phonenumbers.parse(number)
                                if phonenumbers.is_valid_number(parsed_number):
                                    formatted_number = phonenumbers.format_number(
                                        parsed_number, 
                                        phonenumbers.PhoneNumberFormat.INTERNATIONAL
                                    )
                                    found_numbers.add(formatted_number)
                            except:
                                continue
                except:
                    continue
                
        except Exception as e:
            print(f"Error searching WhatsApp: {e}")
        
        return list(found_numbers)

    def search_emails(self):
        """Search for email addresses"""
        found_emails = set()
        search_query = f"{self.username} email contact"
        
        try:
            # Search for potential pages containing email addresses
            search_results = search(search_query, num_results=10)
            
            for url in search_results:
                try:
                    response = requests.get(url, headers=self.headers, timeout=5)
                    if response.status_code == 200:
                        # Find email addresses
                        emails = self.email_pattern.findall(response.text)
                        found_emails.update(emails)
                except:
                    continue
                
        except Exception as e:
            print(f"Error searching emails: {e}")
        
        return list(found_emails)

    def run_search(self):
        """Run all searches"""
        print(f"\n{Fore.CYAN}[*] Searching for username: {self.username}{Style.RESET_ALL}\n")

        # Check social media platforms
        platforms = {
            "GitHub": self.check_github,
            "Instagram": self.check_instagram,
            "Twitter": self.check_twitter,
            "LinkedIn": self.check_linkedin,
            "Medium": self.check_medium
        }

        for platform_name, check_function in platforms.items():
            print(f"{Fore.CYAN}[*] Checking {platform_name}...{Style.RESET_ALL}")
            result = check_function()
            
            if platform_name == "GitHub" and result["exists"]:
                print(f"{Fore.GREEN}[+] GitHub profile found:{Style.RESET_ALL}")
                for key, value in result.items():
                    if key != "exists" and value:
                        print(f"    {key}: {value}")
            elif result["exists"]:
                print(f"{Fore.GREEN}[+] {platform_name} profile found: {self.username}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] No {platform_name} profile found{Style.RESET_ALL}")
            
            time.sleep(1)

        # Search for WhatsApp numbers
        print(f"\n{Fore.CYAN}[*] Searching for potential WhatsApp numbers...{Style.RESET_ALL}")
        whatsapp_numbers = self.search_whatsapp()
        if whatsapp_numbers:
            print(f"{Fore.GREEN}[+] Found potential WhatsApp numbers:{Style.RESET_ALL}")
            for number in whatsapp_numbers:
                print(f"    {number}")
        else:
            print(f"{Fore.RED}[-] No WhatsApp numbers found{Style.RESET_ALL}")

        # Search for email addresses
        print(f"\n{Fore.CYAN}[*] Searching for email addresses...{Style.RESET_ALL}")
        emails = self.search_emails()
        if emails:
            print(f"{Fore.GREEN}[+] Found potential email addresses:{Style.RESET_ALL}")
            for email in emails:
                print(f"    {email}")
        else:
            print(f"{Fore.RED}[-] No email addresses found{Style.RESET_ALL}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <username>")
        sys.exit(1)

    username = sys.argv[1]
    osint = UsernameOSINT(username)
    osint.run_search()

if __name__ == "__main__":
    main()
