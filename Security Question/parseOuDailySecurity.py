"""
===========================================================
 OU TRIVIA PROJECT – SECURITY REVIEW & CWE-200 MAPPING
============================================================

This document contains:

1. Security concerns related to the scraping and parsing logic
2. Potential risks when interacting with external websites
3. Full code of parseOUDaily.py with embedded security comments
4. Tying to CWE-200: Exposure of Sensitive Information

============================================================
 SECTION 1 — SECURITY CONCERNS & RECOMMENDATIONS
============================================================

1. **Lack of Input Validation**
   The scraper accepts any URL from `URLS` without validating:
   - Scheme (http/https)
   - Domain (could be replaced maliciously)
   - Redirects
   MITIGATION: Validate all URLs before requesting content.

2. **No Timeout or Retry Handling**
   A remote server could hang indefinitely.
   MITIGATION: Use: requests.get(url, timeout=5)

3. **Untrusted HTML Parsing**
   HTML from OU Daily is not guaranteed safe.
   Risks:
   - JavaScript injection
   - Embedded malicious code
   MITIGATION: Treat all scraped text as untrusted.

4. **No Rate-Limit Handling**
   Many servers will block scraping if done too aggressively.
   MITIGATION:
   - Add randomized delays
   - Implement exponential backoff

5. **Fingerprintable User-Agent**
   Using a static `"Mozilla/5.0"` header makes scraping detectable.
   MITIGATION: Rotate user-agents.

6. **Regex & Large Input Processing**
   Large HTML inputs could cause:
   - ReDoS (catastrophic regex backtracking)
   - Excessive memory usage
   MITIGATION: Use safer regex patterns or limits.

7. **Error Output Leakage**
   Exceptions print raw HTML or URL data to logs.
   MITIGATION: Sanitize log output.

8. **HTML Structure Dependency**
   If OU Daily changes page layout, the scraper breaks silently.
   MITIGATION: Add fallbacks and structure detection.
"""

"""
============================================================
 SECTION 2 — FULL CODE WITH SECURITY COMMENTARY
============================================================

FILE: parseOUDaily.py
------------------------------------------------------------
(Original code with added security analysis comments)
------------------------------------------------------------
"""

import requests  # request website
from bs4 import BeautifulSoup  # html scrape
import re  # for text formatting
from urls import urls as URLS

class ArticleScraper:
    def __init__(self):
        # SECURITY NOTE:
        # A static User-Agent increases fingerprintability.
        # Consider rotating user-agents to reduce detection.
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def scrape(self, url):
        # SECURITY ISSUE:
        # No URL validation. A malicious URL in URLS could execute unexpected behavior.
        # Mitigation: Validate that URL starts with https:// and belongs to allowed domains.

        # SECURITY ISSUE:
        # No timeout. A hanging server could freeze the system.
        # Use timeout=5 to fail gracefully.
        response = requests.get(url, headers=self.headers)

        # SECURITY NOTE:
        # If OU Daily returns a 500 or 403, this will raise an exception.
        # Caller must handle exceptions so the application does not crash.
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # TITLE EXTRACTION
        title = soup.select_one("h1")
        title_text = title.get_text(strip=True) if title else "No title found"

        # BODY EXTRACTION
        article = soup.find("div", {"id": "article-body"})
        content_text = article.get_text("\n", strip=True) if article else "No content found"

        # SECURITY NOTE:
        # This content is untrusted HTML to treat as unsafe input.
        # Never send raw text to SQL or file writes without sanitization.

        # REMOVE NEWSLETTER PROMPTS
        newsletter_markers = [
            "NEWSLETTERS",
            "A few times a week",
            "FREE SIGN UP",
            "Subscribing",
            "NEWSLETTERS\n* required",
            "Subscribing...",
            "Thank you for subscribing!"
        ]
        for marker in newsletter_markers:
            if marker in content_text:
                # SECURITY NOTE: split() may cut off unintended content if marker is partial.
                content_text = content_text.split(marker)[0].strip()

        # REMOVE FOOTERS
        footer_markers = [
            "This story was edited by",
            "Commenting policy:",
            "MAKE US A GOOGLE PREFERRED SOURCE",
            "COMPLETE ONE-STEP PROCESS"
        ]
        for marker in footer_markers:
            if marker in content_text:
                content_text = content_text.split(marker)[0].strip()
                break

        # SECURITY ISSUE:
        # Regex on unbounded input can lead to ReDoS if pattern is too complex.
        content_text = re.sub(r"\n{2,}", "\n\n", content_text)

        return title_text, content_text


if __name__ == "__main__":
    scraper = ArticleScraper()

    for url in URLS:
        # SECURITY NOTE:
        # No exception handling here; one failed URL will crash entire loop.
        title_text, content_text = scraper.scrape(url)

        print("\n--- URL ---")
        print(url)
        print("\n--- Article Title ---\n", title_text)
        print("\n--- Article Content ---\n", content_text)
        print("\n")

"""
============================================================
 SECTION 3 — CWE-200: EXPOSURE OF SENSITIVE INFORMATION
============================================================

CWE Reference:
https://cwe.mitre.org/data/definitions/200.html

CWE-200 occurs when a system unintentionally exposes sensitive
information to unauthorized parties. In the current implementation,
there are several relevant exposure points:

1. Verbose Console Logging
   - Raw article text, URLs, and exception traces may be printed.
   - If logs are shared or stored, they may reveal internal data.
   - CWE-200 explicitly notes that excessive debug output can leak
     information not intended for the user.

   Mitigations:
   - Limit console output to short status messages.
   - Store detailed logs separately and protect access to them.

2. Forwarding Data to Third-Party APIs
   - Scraped website content is forwarded to OpenAI for processing.
   - Today, only public OU Daily content is used.
   - However, future additions (user input, private sources) could lead
     to unintentional exposure of sensitive information, matching CWE-200.

   Mitigations:
   - Clearly define allowable data types.
   - Audit outbound API traffic for unintended content.

3. Detailed Error Messages
   - Unhandled exceptions may disclose:
     * URLs
     * Response metadata
     * Server behavior
     * Internal logic
   - CWE-200 warns against exposing technical information via errors.

   Mitigations:
   - Wrap scraper calls in try/except blocks.
   - Provide generic user-facing error notifications.
   - Log detailed error messages only in protected debug logs.
"""
"""
------------------------------------------------------------
 SUMMARY OF CWE-200 RISK LEVEL
------------------------------------------------------------

Current Risk Level: LOW–MODERATE

Reason:
- Data comes from publicly available journalism sources.
- No user personal data is collected or stored.
- No credentials, tokens, or system internals are exposed.

Risk could increase if:
- Additional data sources are added
- Logging becomes persistent or publicly available
- Data is forwarded to more external services

------------------------------------------------------------
 RECOMMENDED BEST PRACTICES
------------------------------------------------------------

1. Sanitize log output
2. Implement structured logging with access controls
3. Add URL allowlists and validation
4. Add request timeouts and exception handling
5. Document all outbound data flows
"""