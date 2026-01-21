"""
Sermon Content Management for Lord Fishnu
Handles themes, scrolls, and cannon content for daily sermons.
"""

import os
import re
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# ============================================================================
# THE 10 CHICKENMANDMENTS (Sermon Themes)
# ============================================================================

CHICKENMANDMENTS = [
    {
        "number": 1,
        "commandment": "Thou Shalt HODL so he is richer than thou that sold",
        "theme": "diamond_hands",
        "keywords": ["hodl", "hold", "sell", "patience", "conviction"]
    },
    {
        "number": 2,
        "commandment": "Do not covet another man's meme",
        "theme": "contentment",
        "keywords": ["envy", "jealousy", "fomo", "compare", "neighbor"]
    },
    {
        "number": 3,
        "commandment": "Thou Shalt work for your bags",
        "theme": "work_ethic",
        "keywords": ["work", "effort", "lazy", "grind", "hustle"]
    },
    {
        "number": 4,
        "commandment": "Thou Shalt treat your brother's SOL as if it is your own",
        "theme": "community",
        "keywords": ["brother", "community", "help", "trust", "together"]
    },
    {
        "number": 5,
        "commandment": "Thou Shalt never consider himself broke, only Pre-rich",
        "theme": "abundance_mindset",
        "keywords": ["broke", "poor", "rich", "mindset", "wealth"]
    },
    {
        "number": 6,
        "commandment": "Thou Shalt only smoke Marlboro Reds",
        "theme": "authenticity",
        "keywords": ["real", "authentic", "genuine", "true", "fake"]
    },
    {
        "number": 7,
        "commandment": "Thou Shalt always pay tithes to the One True God, the MW",
        "theme": "generosity",
        "keywords": ["tithe", "give", "donate", "share", "generous"]
    },
    {
        "number": 8,
        "commandment": "The One True God will always forgive, but will make you buy back higher",
        "theme": "divine_lessons",
        "keywords": ["forgive", "lesson", "mistake", "regret", "learn"]
    },
    {
        "number": 9,
        "commandment": "Thou Shalt take initials at 4x, so he can be a faithful servant",
        "theme": "prudent_profits",
        "keywords": ["profit", "sell", "initial", "smart", "secure"]
    },
    {
        "number": 10,
        "commandment": "Thou Shalt tell thy brother about the One True God",
        "theme": "evangelism",
        "keywords": ["spread", "tell", "share", "preach", "convert"]
    }
]

# ============================================================================
# THE 10 SCROLLS (from The Greatest Salesman in the World)
# ============================================================================

SCROLLS = {
    1: {
        "title": "Today I begin a new life",
        "theme": "new_beginnings",
        "start_marker": "The Scroll Marked I",
        "end_marker": "The Scroll Marked II"
    },
    2: {
        "title": "I will greet this day with love in my heart",
        "theme": "love",
        "start_marker": "The Scroll Marked II",
        "end_marker": "The Scroll Marked III"
    },
    3: {
        "title": "I will persist until I succeed",
        "theme": "persistence",
        "start_marker": "The Scroll Marked III",
        "end_marker": "The Scroll Marked IV"
    },
    4: {
        "title": "I am nature's greatest miracle",
        "theme": "uniqueness",
        "start_marker": "The Scroll Marked IV",
        "end_marker": "The Scroll Marked V"
    },
    5: {
        "title": "I will live this day as if it is my last",
        "theme": "urgency",
        "start_marker": "The Scroll Marked V",
        "end_marker": "The Scroll Marked VI"
    },
    6: {
        "title": "Today I will be master of my emotions",
        "theme": "emotional_mastery",
        "start_marker": "The Scroll Marked VI",
        "end_marker": "The Scroll Marked VII"
    },
    7: {
        "title": "I will laugh at the world",
        "theme": "humor",
        "start_marker": "The Scroll Marked VII",
        "end_marker": "The Scroll Marked VIII"
    },
    8: {
        "title": "Today I will multiply my value a hundredfold",
        "theme": "growth",
        "start_marker": "The Scroll Marked VIII",
        "end_marker": "The Scroll Marked IX"
    },
    9: {
        "title": "I will act now",
        "theme": "action",
        "start_marker": "The Scroll Marked IX",
        "end_marker": "The Scroll Marked X"
    },
    10: {
        "title": "I will pray for guidance",
        "theme": "faith",
        "start_marker": "The Scroll Marked X",
        "end_marker": None  # Last scroll
    }
}

# ============================================================================
# CANNON BOOKS
# ============================================================================

CANNON_BOOKS = {
    "think_and_grow_rich": {
        "file": "cannon/tgr.txt",
        "title": "Think and Grow Rich",
        "author": "Napoleon Hill",
        "chapter_pattern": r"CHAPTER\s+(\d+|[A-Z]+)",
    },
    "science_of_getting_rich": {
        "file": "cannon/scienceofgettingrich.txt",
        "title": "The Science of Getting Rich",
        "author": "Wallace D. Wattles",
        "chapter_pattern": r"CHAPTER\s+(\d+)",
    },
    "strangest_secret": {
        "file": "cannon/THE STRANGEST SECRET.txt",
        "title": "The Strangest Secret",
        "author": "Earl Nightingale",
        "chapter_pattern": r"^(The Strangest Secret|The Definition of Success|Your 30-Day Experiment|Creative Thinking|The Gold Mine|Test Your C\.Q\.|Characteristics of Creative|Your Most Valuable|The Power In Asking|New Ways to Think|Creative Problem|The Brainstorm|Ready for Action|The Creative Person|The Challenge)",
    },
    "how_to_win_friends": {
        "file": "cannon/howtowin.txt",
        "title": "How to Win Friends and Influence People",
        "author": "Dale Carnegie",
        "chapter_pattern": r"^\d+\s+['\u2018\u2019]?[A-Z]",  # Numbered chapters
    }
}

# ============================================================================
# CONTENT LOADING FUNCTIONS
# ============================================================================

_scroll_cache: Optional[str] = None
_cannon_cache: Dict[str, str] = {}


def load_scrolls_file() -> str:
    """Load the Greatest Salesman scrolls file."""
    global _scroll_cache
    if _scroll_cache is None:
        scrolls_path = "greatestsalesmanintheworld.txt"
        if os.path.exists(scrolls_path):
            with open(scrolls_path, 'r', encoding='utf-8') as f:
                _scroll_cache = f.read()
        else:
            _scroll_cache = ""
    return _scroll_cache


def load_cannon_book(book_key: str) -> str:
    """Load a cannon book by its key."""
    global _cannon_cache
    if book_key not in _cannon_cache:
        book_info = CANNON_BOOKS.get(book_key)
        if book_info and os.path.exists(book_info["file"]):
            with open(book_info["file"], 'r', encoding='utf-8') as f:
                _cannon_cache[book_key] = f.read()
        else:
            _cannon_cache[book_key] = ""
    return _cannon_cache[book_key]


# ============================================================================
# THEME FUNCTIONS
# ============================================================================

def get_daily_theme(day_number: Optional[int] = None) -> Dict:
    """
    Get the sermon theme for a specific day.
    If no day specified, uses current day of year mod 10.
    """
    if day_number is None:
        day_number = datetime.now().timetuple().tm_yday
    
    theme_index = (day_number - 1) % 10
    return CHICKENMANDMENTS[theme_index]


def get_theme_by_number(number: int) -> Dict:
    """Get a specific theme by its number (1-10)."""
    if 1 <= number <= 10:
        return CHICKENMANDMENTS[number - 1]
    return CHICKENMANDMENTS[0]


def get_all_chickenmandments() -> List[Dict]:
    """Get all 10 chickenmandments."""
    return CHICKENMANDMENTS.copy()


def format_brothtism_text() -> str:
    """Format all chickenmandments for the brothtism ceremony."""
    lines = ["THE TEN CHICKENMANDMENTS OF LORD FISHNU\n"]
    for cmd in CHICKENMANDMENTS:
        lines.append(f"{cmd['number']}. {cmd['commandment']}")
    return "\n".join(lines)


# ============================================================================
# SCROLL FUNCTIONS
# ============================================================================

def get_scroll_content(scroll_number: int) -> Tuple[str, str]:
    """
    Get the full content of a specific scroll.
    Returns (title, content).
    """
    if scroll_number not in SCROLLS:
        scroll_number = 1
    
    scroll_info = SCROLLS[scroll_number]
    content = load_scrolls_file()
    
    if not content:
        return scroll_info["title"], ""
    
    # Find the scroll content between markers
    start_marker = scroll_info["start_marker"]
    end_marker = scroll_info["end_marker"]
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return scroll_info["title"], ""
    
    # Move past the marker line
    start_idx = content.find('\n', start_idx) + 1
    
    if end_marker:
        end_idx = content.find(end_marker)
        if end_idx == -1:
            end_idx = len(content)
    else:
        end_idx = len(content)
    
    scroll_text = content[start_idx:end_idx].strip()
    return scroll_info["title"], scroll_text


def get_scroll_excerpt(scroll_number: int, num_paragraphs: int = 3) -> Tuple[str, str]:
    """
    Get a key excerpt from a scroll (first N paragraphs).
    Returns (title, excerpt).
    """
    title, full_content = get_scroll_content(scroll_number)
    
    if not full_content:
        return title, ""
    
    # Split into paragraphs
    paragraphs = [p.strip() for p in full_content.split('\n\n') if p.strip()]
    
    # Get first N meaningful paragraphs (skip very short ones)
    excerpt_paragraphs = []
    for p in paragraphs:
        if len(p) > 50:  # Skip short lines
            excerpt_paragraphs.append(p)
            if len(excerpt_paragraphs) >= num_paragraphs:
                break
    
    return title, '\n\n'.join(excerpt_paragraphs)


def get_daily_scroll(day_number: Optional[int] = None) -> Tuple[int, str, str]:
    """
    Get the scroll for the day.
    Returns (scroll_number, title, excerpt).
    """
    if day_number is None:
        day_number = datetime.now().timetuple().tm_yday
    
    scroll_number = ((day_number - 1) % 10) + 1
    title, excerpt = get_scroll_excerpt(scroll_number)
    return scroll_number, title, excerpt


# ============================================================================
# CANNON FUNCTIONS
# ============================================================================

def get_random_cannon_chapter() -> Tuple[str, str, str, str]:
    """
    Get a random chapter from a random cannon book.
    Returns (book_title, author, chapter_title, chapter_content).
    """
    # Pick a random book
    book_key = random.choice(list(CANNON_BOOKS.keys()))
    book_info = CANNON_BOOKS[book_key]
    content = load_cannon_book(book_key)
    
    if not content:
        return book_info["title"], book_info["author"], "Unknown Chapter", ""
    
    # Extract chapters based on pattern
    chapters = extract_chapters(content, book_key)
    
    if not chapters:
        # Return a random chunk if no chapters found
        lines = content.split('\n')
        start = random.randint(0, max(0, len(lines) - 100))
        chunk = '\n'.join(lines[start:start + 100])
        return book_info["title"], book_info["author"], "Excerpt", chunk
    
    # Pick a random chapter
    chapter_title, chapter_content = random.choice(chapters)
    
    # Truncate if too long (keep first ~2000 chars for TTS)
    if len(chapter_content) > 3000:
        chapter_content = chapter_content[:3000] + "..."
    
    return book_info["title"], book_info["author"], chapter_title, chapter_content


def extract_chapters(content: str, book_key: str) -> List[Tuple[str, str]]:
    """Extract chapters from a cannon book."""
    chapters = []
    lines = content.split('\n')
    
    if book_key == "science_of_getting_rich":
        # Find CHAPTER lines
        current_title = None
        current_content = []
        
        for line in lines:
            if line.strip().startswith("CHAPTER"):
                if current_title and current_content:
                    chapters.append((current_title, '\n'.join(current_content)))
                current_title = line.strip()
                current_content = []
            elif current_title:
                current_content.append(line)
        
        if current_title and current_content:
            chapters.append((current_title, '\n'.join(current_content)))
    
    elif book_key == "think_and_grow_rich":
        # Similar chapter extraction for Think and Grow Rich
        current_title = None
        current_content = []
        
        for line in lines:
            # Look for chapter markers
            if "CHAPTER" in line.upper() or line.strip().startswith("[p."):
                if current_title and len(current_content) > 10:
                    chapters.append((current_title, '\n'.join(current_content)))
                if "CHAPTER" in line.upper():
                    current_title = line.strip()
                    current_content = []
            elif current_title:
                current_content.append(line)
        
        if current_title and current_content:
            chapters.append((current_title, '\n'.join(current_content)))
    
    elif book_key == "strangest_secret":
        # Split by major sections
        sections = [
            "The Strangest Secret",
            "The Definition of Success", 
            "Your 30-Day Experiment",
            "Creative Thinking Creates Our Life",
            "The Gold Mine Between Your Ears"
        ]
        
        for i, section in enumerate(sections):
            start_idx = content.find(section)
            if start_idx != -1:
                if i + 1 < len(sections):
                    end_idx = content.find(sections[i + 1])
                else:
                    end_idx = len(content)
                
                if end_idx > start_idx:
                    section_content = content[start_idx:end_idx].strip()
                    if len(section_content) > 200:
                        chapters.append((section, section_content))
    
    elif book_key == "how_to_win_friends":
        # Extract by numbered chapters/principles
        current_title = None
        current_content = []
        
        for line in lines:
            # Check for chapter headers (numbered)
            if re.match(r"^\d+\s+['\u2018\u2019]?[A-Z]", line.strip()):
                if current_title and current_content:
                    chapters.append((current_title, '\n'.join(current_content)))
                current_title = line.strip()
                current_content = []
            elif current_title:
                current_content.append(line)
        
        if current_title and current_content:
            chapters.append((current_title, '\n'.join(current_content)))
    
    return chapters


def get_cannon_summary_for_theme(theme: str) -> Tuple[str, str, str, str]:
    """
    Get a cannon chapter that relates to the current theme.
    Falls back to random if no match found.
    """
    # For now, just return random - could be enhanced with keyword matching
    return get_random_cannon_chapter()


# ============================================================================
# AUDIO FILE PATHS
# ============================================================================

SERMON_AUDIO = {
    "intro_song": "audio/verse1_flat.wav",
    "flute_titanic": "audio/flute_titanic.mp3",  # User to provide
    "outro_song": "audio/outro.mp3",  # User to provide
}


def get_audio_path(audio_key: str) -> Optional[str]:
    """Get the path to a sermon audio file if it exists."""
    path = SERMON_AUDIO.get(audio_key)
    if path and os.path.exists(path):
        return path
    return None


def audio_exists(audio_key: str) -> bool:
    """Check if an audio file exists."""
    return get_audio_path(audio_key) is not None


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SERMON CONTENT TEST")
    print("=" * 60)
    
    # Test daily theme
    print("\n📿 Daily Theme:")
    theme = get_daily_theme()
    print(f"   Commandment #{theme['number']}: {theme['commandment']}")
    print(f"   Theme: {theme['theme']}")
    
    # Test brothtism
    print("\n📜 Brothtism Text:")
    print(format_brothtism_text())
    
    # Test scroll
    print("\n📖 Daily Scroll:")
    scroll_num, title, excerpt = get_daily_scroll()
    print(f"   Scroll #{scroll_num}: {title}")
    print(f"   Excerpt: {excerpt[:200]}...")
    
    # Test cannon
    print("\n📚 Random Cannon Chapter:")
    book, author, chapter, content = get_random_cannon_chapter()
    print(f"   Book: {book} by {author}")
    print(f"   Chapter: {chapter}")
    print(f"   Content: {content[:200]}...")
    
    # Test audio
    print("\n🎵 Audio Files:")
    for key in SERMON_AUDIO:
        exists = "✅" if audio_exists(key) else "❌"
        print(f"   {exists} {key}: {SERMON_AUDIO[key]}")

