import re
import requests
from urllib.parse import urlparse
import ssl
import socket
import whois
from datetime import datetime

class SourceChecker:
    def __init__(self):
        # List of known credible news domains
        self.credible_domains = {
            'reuters.com', 'apnews.com', 'npr.org', 'bbc.com', 'bbc.co.uk',
            'nytimes.com', 'wsj.com', 'washingtonpost.com', 'theguardian.com',
            'bloomberg.com', 'economist.com', 'forbes.com', 'time.com'
        }
        
        # List of known fake news domains
        self.fake_domains = {
            'newsexaminer.net', 'worldnewsdailyreport.com', 'nationalreport.net',
            'empirenews.net', 'huzlers.com', 'theonion.com'  # Note: theonion.com is satire
        }

    def check_source_credibility(self, url):
        """Main method to check source credibility"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            if not domain:
                return {
                    'credibility_score': 0,
                    'factors': {
                        'is_known_credible': False,
                        'is_known_fake': False,
                        'has_ssl': False,
                        'domain_age': 0,
                        'suspicious_patterns': True
                    },
                    'details': "Invalid URL format"
                }

            # Initialize credibility checks
            is_known_credible = domain in self.credible_domains
            is_known_fake = domain in self.fake_domains
            has_ssl = self._check_ssl(url)
            domain_age = self._check_domain_age(domain)
            suspicious_patterns = self._check_suspicious_patterns(url, domain)

            # Calculate credibility score (0-100)
            base_score = 50
            if is_known_credible:
                base_score += 30
            if is_known_fake:
                base_score -= 30
            if has_ssl:
                base_score += 10
            if domain_age > 5:  # More than 5 years old
                base_score += 10
            if suspicious_patterns:
                base_score -= 20

            # Ensure score stays within 0-100 range
            credibility_score = max(0, min(100, base_score))

            return {
                'credibility_score': credibility_score,
                'factors': {
                    'is_known_credible': is_known_credible,
                    'is_known_fake': is_known_fake,
                    'has_ssl': has_ssl,
                    'domain_age': domain_age,
                    'suspicious_patterns': suspicious_patterns
                },
                'details': self._generate_details(credibility_score, is_known_credible, 
                                                is_known_fake, has_ssl, domain_age, 
                                                suspicious_patterns)
            }
        except Exception as e:
            return {
                'credibility_score': 0,
                'factors': {
                    'is_known_credible': False,
                    'is_known_fake': False,
                    'has_ssl': False,
                    'domain_age': 0,
                    'suspicious_patterns': True
                },
                'details': f"Error checking credibility: {str(e)}"
            }

    def _check_ssl(self, url):
        """Check if the website has SSL certificate"""
        try:
            response = requests.get(url, verify=True)
            return response.url.startswith('https://')
        except:
            return False

    def _check_domain_age(self, domain):
        """Check domain age in years"""
        try:
            w = whois.whois(domain)
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    creation_date = w.creation_date[0]
                else:
                    creation_date = w.creation_date
                age = (datetime.now() - creation_date).days / 365
                return round(age)
        except:
            pass
        return 0

    def _check_suspicious_patterns(self, url, domain):
        """Check for suspicious patterns in URL and domain"""
        suspicious_patterns = [
            r'\d+(?=\.)',  # Numbers before TLD
            r'[0-9]{4,}',  # Long number sequences
            r'news\d',     # news followed by number
            r'([a-z0-9])\1{4,}',  # Character repetition
        ]
        
        return any(re.search(pattern, domain.lower()) for pattern in suspicious_patterns)

    def _generate_details(self, score, is_known_credible, is_known_fake, has_ssl, 
                         domain_age, suspicious_patterns):
        """Generate detailed explanation of credibility assessment"""
        details = []
        
        if score >= 80:
            details.append("✅ This appears to be a highly credible source.")
        elif score >= 60:
            details.append("✓ This source shows some indicators of credibility.")
        elif score >= 40:
            details.append("⚠️ Exercise caution with this source.")
        else:
            details.append("❌ This source has multiple credibility concerns.")

        if is_known_credible:
            details.append("✅ Recognized as a credible news source")
        if is_known_fake:
            details.append("❌ Known for publishing fake or satirical news")
        if has_ssl:
            details.append("✓ Secure website connection (HTTPS)")
        else:
            details.append("⚠️ Insecure website connection")
        if domain_age > 5:
            details.append(f"✓ Established domain ({domain_age} years old)")
        elif domain_age > 0:
            details.append(f"⚠️ Relatively new domain ({domain_age} years old)")
        if suspicious_patterns:
            details.append("❌ URL contains suspicious patterns")

        return "\n".join(details)
