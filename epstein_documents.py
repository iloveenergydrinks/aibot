#!/usr/bin/env python3
"""
Epstein Documents Parser - Extracts and searches quotes from court filings
"""
import json
import os
import re
from typing import List, Dict, Optional

# Try to import PDF library
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ PyPDF2 not installed. Run: pip install PyPDF2")

PDF_FILE = "gov.uscourts.nysd.447706.1320.0-combined.pdf"
CACHE_FILE = "epstein_quotes_cache.json"

# Keywords to search for and extract quotes
SEARCH_TOPICS = {
    "clinton": ["clinton", "bill", "president"],
    "andrew": ["andrew", "prince", "royal", "duke"],
    "maxwell": ["ghislaine", "maxwell", "gmax"],
    "island": ["island", "st. james", "little st", "caribbean", "virgin islands"],
    "flights": ["flight", "plane", "jet", "lolita", "aircraft", "passenger"],
    "girls": ["girl", "minor", "young", "massage", "recruit"],
    "money": ["money", "paid", "payment", "financial", "bank"],
    "blackmail": ["blackmail", "kompromat", "video", "camera", "record", "tape"],
    "parties": ["party", "parties", "dinner", "event", "guest"],
    "lawsuit": ["lawsuit", "civil", "suit", "court", "legal", "defamation"],
    "email": ["email", "wrote", "message", "sent"],
    "relationship": ["relationship", "friend", "knew", "met", "introduced"],
}


def extract_quotes_from_pdf() -> List[Dict]:
    """Extract relevant quotes from the Epstein files PDF."""
    if not PDF_AVAILABLE:
        print("❌ PyPDF2 not available")
        return []
    
    if not os.path.exists(PDF_FILE):
        print(f"❌ PDF file not found: {PDF_FILE}")
        return []
    
    print(f"📄 Reading PDF: {PDF_FILE}")
    quotes = []
    
    with open(PDF_FILE, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        print(f"📑 Total pages: {total_pages}")
        
        for page_num in range(total_pages):
            if page_num % 50 == 0:
                print(f"   Processing page {page_num}/{total_pages}...")
            
            try:
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                if not text or len(text) < 50:
                    continue
                
                # Clean up text
                text = text.replace('\n', ' ').replace('  ', ' ')
                
                # Check for each topic
                text_lower = text.lower()
                
                for topic, keywords in SEARCH_TOPICS.items():
                    for keyword in keywords:
                        if keyword in text_lower:
                            # Extract sentences containing the keyword
                            sentences = re.split(r'[.!?]+', text)
                            for sentence in sentences:
                                if keyword in sentence.lower() and len(sentence) > 30:
                                    # Clean the sentence
                                    sentence = sentence.strip()
                                    if len(sentence) > 300:
                                        # Truncate long sentences
                                        sentence = sentence[:300] + "..."
                                    
                                    # Avoid duplicates
                                    if not any(q['quote'] == sentence for q in quotes):
                                        quotes.append({
                                            'topic': topic,
                                            'keyword': keyword,
                                            'quote': sentence,
                                            'page': page_num + 1,
                                            'source': f"Giuffre v. Maxwell, Page {page_num + 1}"
                                        })
            except Exception as e:
                continue
    
    print(f"✅ Extracted {len(quotes)} quotes")
    return quotes


def save_quotes_cache(quotes: List[Dict]):
    """Save extracted quotes to cache file."""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved {len(quotes)} quotes to {CACHE_FILE}")


def load_quotes_cache() -> List[Dict]:
    """Load quotes from cache file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        print(f"📂 Loaded {len(quotes)} quotes from cache")
        return quotes
    return []


def search_quotes(query: str, max_results: int = 5) -> List[Dict]:
    """Search for quotes matching a query."""
    quotes = load_quotes_cache()
    
    if not quotes:
        # Try to extract if cache is empty
        quotes = extract_quotes_from_pdf()
        if quotes:
            save_quotes_cache(quotes)
    
    if not quotes:
        return []
    
    query_lower = query.lower()
    query_words = query_lower.split()
    
    results = []
    
    for quote in quotes:
        quote_lower = quote['quote'].lower()
        topic = quote['topic']
        
        # Score based on matches
        score = 0
        
        # Direct topic match
        if topic in query_lower:
            score += 10
        
        # Word matches
        for word in query_words:
            if len(word) > 3 and word in quote_lower:
                score += 5
            if word in topic:
                score += 3
        
        if score > 0:
            results.append({**quote, 'score': score})
    
    # Sort by score and return top results
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:max_results]


def get_random_quotes(topic: Optional[str] = None, count: int = 3) -> List[Dict]:
    """Get random quotes, optionally filtered by topic."""
    import random
    
    quotes = load_quotes_cache()
    
    if not quotes:
        quotes = extract_quotes_from_pdf()
        if quotes:
            save_quotes_cache(quotes)
    
    if not quotes:
        return []
    
    if topic:
        topic_lower = topic.lower()
        filtered = [q for q in quotes if q['topic'] == topic_lower or topic_lower in q['quote'].lower()]
        if filtered:
            quotes = filtered
    
    return random.sample(quotes, min(count, len(quotes)))


def format_citation(quote_data: Dict) -> str:
    """Format a quote as a citation string."""
    return f'"{quote_data["quote"]}" (Source: {quote_data["source"]})'


def build_cache():
    """Build the quotes cache from the PDF."""
    print("🔨 Building Epstein quotes cache...")
    quotes = extract_quotes_from_pdf()
    if quotes:
        save_quotes_cache(quotes)
        
        # Print summary by topic
        print("\n📊 Quotes by topic:")
        topic_counts = {}
        for q in quotes:
            topic = q['topic']
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        for topic, count in sorted(topic_counts.items(), key=lambda x: -x[1]):
            print(f"   {topic}: {count} quotes")
    else:
        print("❌ No quotes extracted")


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build_cache()
    elif len(sys.argv) > 1 and sys.argv[1] == "search":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "clinton"
        print(f"\n🔍 Searching for: {query}")
        results = search_quotes(query)
        for i, r in enumerate(results, 1):
            print(f"\n{i}. [{r['topic']}] Page {r['page']}")
            print(f"   \"{r['quote']}\"")
    else:
        print("Usage:")
        print("  python epstein_documents.py build   - Extract quotes from PDF")
        print("  python epstein_documents.py search <query> - Search quotes")




