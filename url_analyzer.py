"""
Tool 3: URL Analyzer
Analyzes URLs for crypto scam indicators using:
- Pattern matching
- Suspicious keyword detection
- LLM analysis
"""
import re
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

import streamlit as st
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        pass
genai.configure(api_key=api_key)

# Suspicious patterns in URLs
SUSPICIOUS_KEYWORDS = [
    'giveaway', 'airdrop', 'free-crypto', 'double-bitcoin',
    'elon-musk', 'binance-giveaway', 'eth-giveaway', 'btc-giveaway',
    'claim-reward', 'free-btc', 'crypto-gift', 'win-crypto',
    'investment-guaranteed', 'crypto-profit'
]

LEGITIMATE_DOMAINS = [
    'coinbase.com', 'binance.com', 'kraken.com', 'etherscan.io',
    'bitcoin.org', 'ethereum.org', 'coingecko.com', 'coinmarketcap.com'
]

def extract_url_features(url: str) -> dict:
    """Extract features from URL for analysis."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        full_url = url.lower()

        # Check features
        features = {
            "domain": domain,
            "has_https": url.startswith('https'),
            "suspicious_keywords": [kw for kw in SUSPICIOUS_KEYWORDS if kw in full_url],
            "is_known_legitimate": any(legit in domain for legit in LEGITIMATE_DOMAINS),
            "has_numbers_in_domain": bool(re.search(r'\d', domain)),
            "domain_length": len(domain),
            "has_hyphens": '-' in domain,
            "subdomain_count": len(domain.split('.')) - 2,
            "path": path
        }
        return features
    except:
        return {"error": "Invalid URL format"}

def analyze_url_with_llm(url: str, features: dict) -> dict:
    """Use Gemini to analyze URL for scam indicators."""
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""You are a cybersecurity expert specializing in cryptocurrency scam detection.
Analyze this URL for potential scam indicators:

URL: {url}
Features detected:
- Has HTTPS: {features.get('has_https')}
- Suspicious keywords found: {features.get('suspicious_keywords')}
- Known legitimate domain: {features.get('is_known_legitimate')}
- Domain has numbers: {features.get('has_numbers_in_domain')}
- Domain length: {features.get('domain_length')} characters
- Number of hyphens in domain: {features.get('has_hyphens')}

Common crypto scam URL patterns:
- Fake versions of legitimate sites (binance-pro.com, eth-reward.net)
- Giveaway sites (bitcoin-giveaway2024.com)
- Phishing sites mimicking exchanges
- Sites with suspicious keywords like "free", "reward", "giveaway"
- Newly registered domains with crypto themes
- URLs with excessive numbers or hyphens

Respond in EXACT format:
VERDICT: [SCAM or SUSPICIOUS or SAFE]
RISK_LEVEL: [CRITICAL, HIGH, MEDIUM, LOW]
REASONS:
- [reason 1]
- [reason 2]
- [reason 3]
RECOMMENDATION: [one line advice]"""

    try:
        response = model.generate_content(prompt)
        result_text = response.text
        lines = result_text.strip().split('\n')

        verdict = "UNKNOWN"
        risk_level = "MEDIUM"
        reasons = []
        recommendation = ""

        for line in lines:
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip()
            elif line.startswith("RISK_LEVEL:"):
                risk_level = line.replace("RISK_LEVEL:", "").strip()
            elif line.startswith("- "):
                reasons.append(line.replace("- ", "").strip())
            elif line.startswith("RECOMMENDATION:"):
                recommendation = line.replace("RECOMMENDATION:", "").strip()

        return {
            "verdict": verdict,
            "risk_level": risk_level,
            "reasons": reasons,
            "recommendation": recommendation
        }
    except Exception as e:
        return {
            "verdict": "ERROR",
            "risk_level": "UNKNOWN",
            "reasons": [str(e)],
            "recommendation": "Unable to analyze"
        }

def analyze_url(url: str) -> dict:
    """
    Main URL analyzer function.
    Returns comprehensive URL analysis.
    """
    # Quick check for known legitimate domains
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if any(legit in domain for legit in LEGITIMATE_DOMAINS):
        return {
            "url": url,
            "verdict": "SAFE",
            "risk_level": "LOW",
            "reasons": ["Known legitimate cryptocurrency platform"],
            "recommendation": "This appears to be a legitimate domain",
            "features": extract_url_features(url)
        }

    features = extract_url_features(url)
    llm_result = analyze_url_with_llm(url, features)

    return {
        "url": url,
        "verdict": llm_result["verdict"],
        "risk_level": llm_result["risk_level"],
        "reasons": llm_result["reasons"],
        "recommendation": llm_result["recommendation"],
        "features": features
    }


if __name__ == "__main__":
    test_url = "http://bitcoin-giveaway-elon2024.com/claim-reward"
    result = analyze_url(test_url)
    print(f"Verdict: {result['verdict']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Reasons: {result['reasons']}")
