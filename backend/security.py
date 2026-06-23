import re
import requests
import base64

BRAND_BLOCKLIST = [
    'google', 'paypal', 'amazon', 'netflix', 'facebook', 'instagram', 'twitter', 'microsoft', 'apple', 'linkedin',
    'sbi', 'hdfc', 'paytm', 
]

def is_brand_impersonation(custom_code):
    if not custom_code:
        return False
    custom_code_clean = custom_code.lower().strip()
    for brand in BRAND_BLOCKLIST:
        if re.search(brand, custom_code_clean):
            return True
    return False

GOOGLE_API_KEY = "AIzaSyBRbb_ixN98FCeyneVToXoymxOIPBNP_as"
VT_API_KEY = "11ea9da27d730ecb634a6d90befd2cd3b70fb2344df792a820c784deac3fb407"

SAFE_BROWSING_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"

def check_google_safe_browsing(target_url):
    payload = {
        "client": {"clientId": "secure-shortener", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": target_url}]
        }
    }
    try:
        response = requests.post(SAFE_BROWSING_URL, json=payload, timeout=4)
        if response.status_code == 200:
            result = response.json()
            if "matches" in result:
                print(f"⚠️ [SECURITY] Google flagged URL: {target_url}")
                return True
        return False
    except Exception as e:
        print(f"Google API Error: {e}")
        return False
    
def check_virustotal(target_url):
    try:
        # Encode URL to base64 without padding for VT API specification
        url_bytes = target_url.encode('utf-8')
        url_b64 = base64.urlsafe_b64encode(url_bytes).decode('utf-8').strip("=")
        
        endpoint = f"https://www.virustotal.com/api/v3/urls/{url_b64}"
        headers = {"accept": "application/json", "x-apikey": VT_API_KEY}
        
        response = requests.get(endpoint, headers=headers, timeout=4)
        if response.status_code == 200:
            result = response.json()
            stats = result['data']['attributes']['last_analysis_stats']
            
            if stats.get('malicious', 0) > 0 or stats.get('phishing', 0) > 0:
                print(f"⚠️ [SECURITY] VirusTotal flagged URL: {target_url}")
                return True
        return False
    except Exception as e:
        print(f"VirusTotal API Error: {e}")
        return False
    
def is_url_malicious(target_url):
    """
    Evaluates safety via sequential verification tiers.
    Fails-open (returns False) on network timeouts to maintain availability.
    """
    if check_google_safe_browsing(target_url):
        return True
        
    if check_virustotal(target_url):
        return True
        
    return False

