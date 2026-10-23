"""
Tool 2: Wallet Checker
Checks if a crypto wallet address is suspicious using:
- Pattern analysis
- Free blockchain APIs
- LLM analysis
"""
import requests
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

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

# Known scam wallet patterns (examples)
KNOWN_SCAM_PATTERNS = [
    r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$',  # Bitcoin format check
]

def detect_crypto_type(address: str) -> str:
    """Detect cryptocurrency type from address format."""
    address = address.strip()
    if re.match(r'^(bc1|1|3)[a-zA-HJ-NP-Z0-9]{25,62}$', address):
        return "Bitcoin"
    elif re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return "Ethereum/EVM"
    elif re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', address):
        return "Solana"
    elif re.match(r'^T[A-Za-z1-9]{33}$', address):
        return "TRON"
    else:
        return "Unknown"

def check_ethereum_address(address: str) -> dict:
    """Check Ethereum address using free Etherscan API."""
    try:
        # Using free Etherscan API (no key needed for basic checks)
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == "1":
            balance_wei = int(data.get("result", 0))
            balance_eth = balance_wei / 1e18
            return {
                "valid": True,
                "balance": f"{balance_eth:.6f} ETH",
                "api_data": data
            }
        return {"valid": False, "balance": "Unknown", "api_data": data}
    except:
        return {"valid": False, "balance": "API unavailable", "api_data": {}}

def analyze_wallet_with_llm(address: str, crypto_type: str, api_data: dict) -> dict:
    """Use Gemini to analyze wallet address for suspicious patterns."""
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""You are a cryptocurrency security expert analyzing a wallet address for potential scam indicators.

Wallet Address: {address}
Detected Crypto Type: {crypto_type}
API Data Available: {api_data}

Analyze this wallet address for:
1. Address format validity
2. Suspicious patterns in the address
3. Common scam wallet characteristics
4. Risk assessment

Respond in this EXACT format:
VERDICT: [SUSPICIOUS or SAFE or UNKNOWN]
RISK_LEVEL: [HIGH, MEDIUM, LOW]
ADDRESS_VALID: [YES or NO]
REASONS:
- [reason 1]
- [reason 2]
RECOMMENDATION: [advice for user]"""

    try:
        response = model.generate_content(prompt)
        result_text = response.text
        lines = result_text.strip().split('\n')

        verdict = "UNKNOWN"
        risk_level = "MEDIUM"
        address_valid = "UNKNOWN"
        reasons = []
        recommendation = ""

        for line in lines:
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip()
            elif line.startswith("RISK_LEVEL:"):
                risk_level = line.replace("RISK_LEVEL:", "").strip()
            elif line.startswith("ADDRESS_VALID:"):
                address_valid = line.replace("ADDRESS_VALID:", "").strip()
            elif line.startswith("- "):
                reasons.append(line.replace("- ", "").strip())
            elif line.startswith("RECOMMENDATION:"):
                recommendation = line.replace("RECOMMENDATION:", "").strip()

        return {
            "verdict": verdict,
            "risk_level": risk_level,
            "address_valid": address_valid,
            "reasons": reasons,
            "recommendation": recommendation
        }
    except Exception as e:
        return {
            "verdict": "ERROR",
            "risk_level": "UNKNOWN",
            "address_valid": "UNKNOWN",
            "reasons": [str(e)],
            "recommendation": "Unable to analyze"
        }

def check_wallet(address: str) -> dict:
    """
    Main wallet checker function.
    Returns comprehensive wallet analysis.
    """
    address = address.strip()
    crypto_type = detect_crypto_type(address)
    api_data = {}

    # Get blockchain data if Ethereum
    if crypto_type == "Ethereum/EVM":
        api_data = check_ethereum_address(address)

    # LLM analysis
    llm_result = analyze_wallet_with_llm(address, crypto_type, api_data)

    return {
        "address": address,
        "crypto_type": crypto_type,
        "verdict": llm_result["verdict"],
        "risk_level": llm_result["risk_level"],
        "address_valid": llm_result["address_valid"],
        "reasons": llm_result["reasons"],
        "recommendation": llm_result["recommendation"],
        "blockchain_data": api_data
    }


if __name__ == "__main__":
    # Test
    test_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    result = check_wallet(test_address)
    print(f"Verdict: {result['verdict']}")
    print(f"Crypto Type: {result['crypto_type']}")
    print(f"Risk Level: {result['risk_level']}")
