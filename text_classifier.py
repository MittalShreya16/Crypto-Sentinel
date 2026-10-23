"""
Tool 1: Text Classifier
Analyzes crypto messages/posts and classifies as SCAM or LEGITIMATE
using Google Gemini API
"""
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


def classify_crypto_text(text: str) -> dict:
    """
    Analyzes a crypto message and returns scam verdict.
    Returns: {verdict, confidence, reasons, risk_level}
    """
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""You are an expert cryptocurrency scam detector. 
Analyze the following message and determine if it is a SCAM or LEGITIMATE.

Message to analyze:
"{text}"

Common scam patterns to look for:
- Promises of guaranteed high returns (e.g. "10x returns guaranteed")
- Urgency tactics ("Limited time offer!", "Act now!")
- Requests for private keys or seed phrases
- Fake celebrity endorsements
- Pump and dump schemes
- Phishing attempts
- Too-good-to-be-true investment offers
- Requests to send crypto first to receive more
- Impersonation of legitimate projects

Respond in this EXACT format:
VERDICT: [SCAM or LEGITIMATE]
CONFIDENCE: [HIGH, MEDIUM, or LOW]
RISK_LEVEL: [CRITICAL, HIGH, MEDIUM, LOW]
REASONS:
- [reason 1]
- [reason 2]
- [reason 3]
RECOMMENDATION: [one line advice for the user]"""

    try:
        response = model.generate_content(prompt)
        result_text = response.text

        # Parse response
        lines = result_text.strip().split('\n')
        verdict = "UNKNOWN"
        confidence = "LOW"
        risk_level = "UNKNOWN"
        reasons = []
        recommendation = ""

        for i, line in enumerate(lines):
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip()
            elif line.startswith("CONFIDENCE:"):
                confidence = line.replace("CONFIDENCE:", "").strip()
            elif line.startswith("RISK_LEVEL:"):
                risk_level = line.replace("RISK_LEVEL:", "").strip()
            elif line.startswith("- "):
                reasons.append(line.replace("- ", "").strip())
            elif line.startswith("RECOMMENDATION:"):
                recommendation = line.replace("RECOMMENDATION:", "").strip()

        return {
            "verdict": verdict,
            "confidence": confidence,
            "risk_level": risk_level,
            "reasons": reasons,
            "recommendation": recommendation,
            "raw_analysis": result_text
        }

    except Exception as e:
        return {
            "verdict": "ERROR",
            "confidence": "LOW",
            "risk_level": "UNKNOWN",
            "reasons": [f"Analysis failed: {str(e)}"],
            "recommendation": "Please try again",
            "raw_analysis": str(e)
        }


if __name__ == "__main__":
    # Test
    test_message = "🚀 URGENT! Elon Musk is giving away 10,000 BTC! Send 0.1 BTC to this address and receive 1 BTC back! Limited time only! Act NOW before it's too late!"
    result = classify_crypto_text(test_message)
    print(f"Verdict: {result['verdict']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Reasons: {result['reasons']}")
