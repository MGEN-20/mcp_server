import re
import requests
from typing import Optional


def fetch_swagger_from_github(url: str) -> Optional[str]:
    """
    Fetch YAML/JSON content from GitHub
    Supports both raw GitHub URLs and regular GitHub file URLs
    """
    try:
        # Convert regular GitHub URLs to raw URLs if needed
        if "github.com" in url and "/blob/" in url:
            url = (url.replace("github.com", "raw.githubusercontent.com")
                      .replace("/blob/", "/"))
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        return response.text.strip()
        
    except Exception as e:
        print(f"❌ Error fetching from {url}: {str(e)}")
        return None


def fetch_swagger_from_url(url: str) -> Optional[str]:
    """
    Fetch swagger content from any URL
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        return response.text.strip()
        
    except Exception as e:
        print(f"❌ Error fetching from {url}: {str(e)}")
        return None


def is_url(text: str) -> bool:
    """Check if the given text is a URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(text) is not None


def get_swagger_content(source: str) -> str:
    """
    Get swagger content from either a file path or URL
    
    Args:
        source: Either a file path or URL
        
    Returns:
        The swagger content as a string
    """
    if is_url(source):
        print(f"🌐 Fetching swagger from URL: {source}")
        
        if "github.com" in source:
            content = fetch_swagger_from_github(source)
        else:
            content = fetch_swagger_from_url(source)
            
        if content:
            print(f"✅ Successfully fetched {len(content)} characters")
            return content
        else:
            raise ValueError(f"Failed to fetch content from URL: {source}")
    else:
        print(f"📁 Loading swagger from file: {source}")
        try:
            with open(source, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"✅ Successfully loaded {len(content)} characters")
            return content
        except FileNotFoundError:
            raise ValueError(f"File not found: {source}")
        except Exception as e:
            raise ValueError(f"Error reading file {source}: {str(e)}")


def sync_get_swagger_content(source: str) -> str:
    """Synchronous wrapper for get_swagger_content"""
    return get_swagger_content(source) 