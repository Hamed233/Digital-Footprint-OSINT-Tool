# Digital Footprint OSINT Tool 🔍

A powerful Open Source Intelligence (OSINT) tool for analyzing digital footprints across multiple platforms. This tool helps researchers and security professionals map an individual's online presence while respecting privacy and platform policies.

## ⚠️ Disclaimer

This tool is provided for educational and research purposes only. Users must:

- Obtain proper authorization before investigating any individual
- Comply with all applicable laws and regulations
- Respect privacy rights and platform terms of service
- Not use this tool for stalking, harassment, or malicious purposes
- Understand that the tool provides no guarantees about data accuracy

The authors assume no liability for misuse or any damages arising from the use of this tool.

## ✨ Features

- 🌐 Multi-platform social media presence detection
- 🔄 Smart username variation analysis
- 📧 Contact information discovery
- 🌍 Domain registration intelligence
- 🚀 Multi-threaded scanning for efficiency
- 🛡️ Rate limiting and user agent rotation
- 📊 Progress tracking with detailed output
- 🎨 Colorized console interface

### Supported Platforms

- GitHub
- Instagram
- Twitter/X
- LinkedIn
- Medium
- Reddit
- TikTok
- Pinterest
- Twitch
- DeviantArt
- Behance
- Steam
- Spotify
- SoundCloud
- Vimeo
- Facebook
- YouTube
- Telegram

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/digital-footprint.git
cd digital-footprint
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💡 Usage

Basic usage:
```bash
python digital_footprint.py username
```

Example with real output:
```bash
$ python digital_footprint.py johndoe

[*] Starting Digital Footprint Analysis for: johndoe

[*] Checking domain registrations...
[+] Found registered domains:
    Domain: johndoe.com
        registrar: GoDaddy.com, LLC
        creation_date: 2010-05-15
        expiration_date: 2025-05-15

[*] Checking social media presence...
[+] GitHub profile found: https://github.com/johndoe
    name: John Doe
    bio: Software Developer
    location: San Francisco
    public_repos: 45
    followers: 128
[+] Twitter profile found: https://twitter.com/johndoe
[+] LinkedIn profile found: https://linkedin.com/in/johndoe
[+] Medium profile found: https://medium.com/@johndoe

[*] Searching for contact information...
[+] Found potential email addresses:
    john.doe@example.com
    contact@johndoe.com
[+] Found potential phone numbers:
    +1 (555) 123-4567
```

## 🛠️ Advanced Features

### Name Variations
The tool automatically checks multiple username variations:
- Original: johndoe
- Dotted: john.doe
- Underscored: john_doe
- Hyphenated: john-doe

### Domain Intelligence
Checks multiple TLDs:
- .com
- .net
- .org
- .io
- .me
- .dev

### Contact Discovery
- Email pattern recognition
- Phone number validation
- Social media bio parsing
- Domain WHOIS contact extraction

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Privacy & Security

- No data is stored or transmitted to external servers
- All scanning is done locally
- Rate limiting is implemented to respect platform policies
- User agent rotation prevents IP blocking

## ⚡ Performance Tips

- Use specific usernames for better results
- Expect some false positives with common usernames
- Platform response times may vary
- Some platforms may block automated scanning

## 🐛 Known Issues

- Rate limiting on some platforms may affect results
- False positives with common usernames
- Some platforms actively block automated scanning
- WHOIS data may be incomplete for privacy-protected domains

## 📚 References

- [OSINT Framework](https://osintframework.com/)
- [Python WHOIS Documentation](https://pypi.org/project/python-whois/)
- [Requests Library](https://docs.python-requests.org/)

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by various OSINT tools and frameworks
- Built with respect for privacy and security

## 👨‍💻 Author

**Hamed Esam**

- Twitter: [@hamedesam_dev](https://x.com/hamedesam_dev)
- Website: [albashmoparmeg.com](https://albashmoparmeg.com)
- GitHub: [@Hamed233](https://github.com/Hamed233)

---

**Note**: This tool is part of a broader OSINT toolkit. Use responsibly and ethically.
