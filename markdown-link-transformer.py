#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "markdown-it-py",
#   "urllib3",
# ]
# ///

"""
Transforms a markdown file by replacing link text with just the domain name (TLD).
Reads from stdin and writes to stdout.

Example usage:
    cat input.md | ./markdown-link-transformer.py > output.md
"""

import sys
import re
from urllib.parse import urlparse
import markdown_it


def extract_domain(url):
    """Extract just the domain name from a URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Handle cases where there might be a subdomain
    domain_parts = domain.split('.')
    if len(domain_parts) > 2:
        return '.'.join(domain_parts[-2:])
    return domain


def process_markdown(content):
    """Process markdown content to replace link text with domain names."""
    # Regex for markdown links: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        domain = extract_domain(url)
        if domain:
            return f'[{domain}]({url})'
        # If no domain found, keep original link
        return match.group(0)
    
    return re.sub(link_pattern, replace_link, content)


def main():
    # Read from stdin
    content = sys.stdin.read()
    
    # Process the markdown
    processed_content = process_markdown(content)
    
    # Write to stdout
    sys.stdout.write(processed_content)


if __name__ == "__main__":
    main()
