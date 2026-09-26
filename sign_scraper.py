import requests

SIGN_MAP = {
    "US:R1-1": "MUTCD_R1-1.svg",
    "US:R2-1": "MUTCD_R2-1.svg",
    "US:W3-3": "MUTCD_W3-3.svg",
    "STOP": "MUTCD_R1-1.svg"
}

def fetch_sign_svg(sign_code):
    filename = SIGN_MAP.get(sign_code, "MUTCD_R1-1.svg")
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.content
    return None
    