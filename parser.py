import re
from .entropy import is_high_entropy
# الگوهای شناسایی Endpointها و روت‌های داخلی
ENDPOINT_REGEX = re.compile(
    r"""(?:"|')((?:/[a-zA-Z0-9_.~-]+)+|\b(?:https?://[a-zA-Z0-9_.~-]+(?:/[a-zA-Z0-9_.~-]*)*))(?:"|')"""
)
# الگو برای پیدا کردن توکن‌ها و کلیدهای متنی داخل رشته‌های کوتیشن‌دار
GENERIC_STRING_REGEX = re.compile(r"""(?:"|')([a-zA-Z0-9_\-+/=]{16,128})(?:"|')""")

# الگوهای سکرت‌های با ساختار معین (مانند کلیدهای رایج کلود یا درگاه)
KNOWN_KEY_PATTERNS = {
    "AWS Access Key": re.compile(r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
    "Google API Key": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    "JSON Web Token (JWT)": re.compile(r"eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*"),
}
def extract_endpoints(content: str) -> set[str]:
    """استخراج روت‌ها و اندپوینت‌های پنهان درون کدهای جاوااسکریپت."""
    raw_matches = ENDPOINT_REGEX.findall(content)
    cleaned_endpoints = set()
    # This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries. Please try rephrasing your prompt. You can [send feedback](https://ai.google.dev/gemini-api/docs/troubleshooting#file-bug) or read more about [our policies here](https://policies.google.com/terms/generative-ai/use-policy).
