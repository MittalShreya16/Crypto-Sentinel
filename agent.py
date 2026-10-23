"""
Main AI Agent — Crypto Scam Detection
Uses LangChain ReAct framework to orchestrate all 3 tools
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
from text_classifier import classify_crypto_text
from wallet_checker import check_wallet
from url_analyzer import analyze_url
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def detect_input_type(user_input: str) -> str:
    """Automatically detect if input is a message, wallet address, or URL."""
    user_input = user_input.strip()

    # URL detection
    if user_input.startswith('http') or user_input.startswith('www.') or '.' in user_input and '/' in user_input:
        return "url"

    # Wallet address detection
    if re.match(r'^(bc1|1|3)[a-zA-HJ-NP-Z0-9]{25,62}$', user_input):
        return "wallet_btc"
    if re.match(r'^0x[a-fA-F0-9]{40}$', user_input):
        return "wallet_eth"
    if re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', user_input) and len(user_input) > 30:
        return "wallet_sol"
    if re.match(r'^T[A-Za-z1-9]{33}$', user_input):
        return "wallet_tron"

    # Default: treat as text message
    return "text"

def run_agent(user_input: str) -> dict:
    """
    Main agent function — automatically detects input type
    and routes to the appropriate tool.
    """
    input_type = detect_input_type(user_input)

    if input_type == "url":
        result = analyze_url(user_input)
        result["input_type"] = "URL"
        result["tool_used"] = "URL Analyzer"

    elif input_type.startswith("wallet"):
        result = check_wallet(user_input)
        result["input_type"] = "Wallet Address"
        result["tool_used"] = "Wallet Checker"

    else:
        result = classify_crypto_text(user_input)
        result["input_type"] = "Text Message"
        result["tool_used"] = "Text Classifier"

    return result

def get_verdict_emoji(verdict: str) -> str:
    """Returns emoji for verdict."""
    verdict = verdict.upper()
    if "SCAM" in verdict or "SUSPICIOUS" in verdict or "CRITICAL" in verdict:
        return "🚨"
    elif "SAFE" in verdict or "LEGITIMATE" in verdict:
        return "✅"
    else:
        return "⚠️"

def get_risk_color(risk_level: str) -> str:
    """Returns color for risk level."""
    risk_level = risk_level.upper()
    if risk_level == "CRITICAL":
        return "#dc2626"
    elif risk_level == "HIGH":
        return "#f97316"
    elif risk_level == "MEDIUM":
        return "#eab308"
    else:
        return "#16a34a"


if __name__ == "__main__":
    print("🕵️ Crypto Scam Detection Agent")
    print("=" * 50)

    # Test examples
    tests = [
        "Send 1 ETH to get 10 ETH back! Elon Musk approved crypto giveaway!",
        "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "http://bitcoin-giveaway-elon2024.com/claim"
    ]

    for test in tests:
        print(f"\nInput: {test[:50]}...")
        result = run_agent(test)
        print(f"Tool Used: {result.get('tool_used')}")
        print(f"Verdict: {result.get('verdict')}")
        print(f"Risk Level: {result.get('risk_level')}")
        print("-" * 30)
