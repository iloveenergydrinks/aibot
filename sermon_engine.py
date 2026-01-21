"""
Sermon Engine - State Machine for Lord Fishnu's Daily Sermon
Manages the 9-segment sermon flow with timing and transitions.
"""

import time
import threading
from enum import Enum, auto
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from sermon_content import (
    get_daily_theme,
    get_daily_scroll,
    get_random_cannon_chapter,
    format_brothtism_text,
    get_audio_path,
    audio_exists,
    CHICKENMANDMENTS
)


class SermonSegment(Enum):
    """The 9 segments of Lord Fishnu's daily sermon."""
    IDLE = auto()           # Not in sermon mode
    INTRO_SONG = auto()     # 1. Play intro music (~3 min)
    OPENING_MONOLOGUE = auto()  # 2. AI-generated opening (~5 min)
    SCROLL_READING = auto()     # 3. Read from Greatest Salesman (~5 min)
    CANNON_SUMMARY = auto()     # 4. Summarize cannon chapter (~10 min)
    PARABLE = auto()            # 5. AI-generated crypto parable (~5 min)
    BROTHTISM = auto()          # 6. Read the 10 commandments (~5 min)
    CLOSING_QUESTIONS = auto()  # 7. Interactive Q&A (~15 min)
    CLOSING_MONOLOGUE = auto()  # 8. Final words + flute (~5 min)
    OUTRO_SONG = auto()         # 9. Play outro music (~3 min)


# Segment configuration
SEGMENT_CONFIG = {
    SermonSegment.INTRO_SONG: {
        "name": "Intro Song",
        "duration_minutes": 3,
        "type": "audio",
        "audio_key": "intro_song",
        "description": "The sacred hymn of the Smoking Chicken Fish"
    },
    SermonSegment.OPENING_MONOLOGUE: {
        "name": "Opening Monologue",
        "duration_minutes": 5,
        "type": "tts",
        "description": "Lord Fishnu welcomes the flock and introduces the day's theme"
    },
    SermonSegment.SCROLL_READING: {
        "name": "Scroll Reading",
        "duration_minutes": 5,
        "type": "tts",
        "description": "A reading from the sacred scrolls of the Greatest Salesman"
    },
    SermonSegment.CANNON_SUMMARY: {
        "name": "Cannon Summary",
        "duration_minutes": 10,
        "type": "tts",
        "description": "Wisdom from the holy cannon, translated by Lord Fishnu"
    },
    SermonSegment.PARABLE: {
        "name": "The Parable",
        "duration_minutes": 5,
        "type": "tts",
        "description": "A divine parable from the cosmic broiler"
    },
    SermonSegment.BROTHTISM: {
        "name": "The Brothtism",
        "duration_minutes": 5,
        "type": "tts",
        "description": "The sacred reading of the Ten Chickenmandments"
    },
    SermonSegment.CLOSING_QUESTIONS: {
        "name": "Closing Questions",
        "duration_minutes": 15,
        "type": "interactive",
        "description": "Lord Fishnu answers questions from the faithful"
    },
    SermonSegment.CLOSING_MONOLOGUE: {
        "name": "Closing Monologue",
        "duration_minutes": 5,
        "type": "tts_with_audio",
        "audio_key": "flute_titanic",
        "description": "Final blessings and the sacred flute"
    },
    SermonSegment.OUTRO_SONG: {
        "name": "Outro Song",
        "duration_minutes": 3,
        "type": "audio",
        "audio_key": "outro_song",
        "description": "The congregation is dismissed with holy music"
    },
}

# Ordered list of segments (excluding IDLE)
SERMON_ORDER = [
    SermonSegment.INTRO_SONG,
    SermonSegment.OPENING_MONOLOGUE,
    SermonSegment.SCROLL_READING,
    SermonSegment.CANNON_SUMMARY,
    SermonSegment.PARABLE,
    SermonSegment.BROTHTISM,
    SermonSegment.CLOSING_QUESTIONS,
    SermonSegment.CLOSING_MONOLOGUE,
    SermonSegment.OUTRO_SONG,
]


@dataclass
class SermonState:
    """Current state of the sermon."""
    current_segment: SermonSegment = SermonSegment.IDLE
    segment_start_time: Optional[float] = None
    sermon_start_time: Optional[float] = None
    daily_theme: Optional[Dict] = None
    scroll_number: int = 1
    scroll_title: str = ""
    scroll_excerpt: str = ""
    cannon_book: str = ""
    cannon_author: str = ""
    cannon_chapter: str = ""
    cannon_content: str = ""
    paused: bool = False
    

class SermonEngine:
    """
    State machine for managing Lord Fishnu's sermon.
    Handles segment transitions, timing, and content preparation.
    """
    
    def __init__(self):
        self.state = SermonState()
        self._lock = threading.Lock()
        self._callbacks: Dict[str, Callable] = {}
        
    # ========================================================================
    # CALLBACKS
    # ========================================================================
    
    def on_segment_change(self, callback: Callable[[SermonSegment, Dict, SermonSegment, Dict], None]):
        """Register callback for segment changes."""
        self._callbacks['segment_change'] = callback
        
    def on_sermon_end(self, callback: Callable[[], None]):
        """Register callback for when sermon ends."""
        self._callbacks['sermon_end'] = callback
        
    def on_content_ready(self, callback: Callable[[str, Any], None]):
        """Register callback for when content is prepared."""
        self._callbacks['content_ready'] = callback
    
    def _emit(self, event: str, *args):
        """Emit an event to registered callbacks."""
        if event in self._callbacks:
            try:
                self._callbacks[event](*args)
            except Exception as e:
                print(f"⚠️ Sermon callback error ({event}): {e}")
    
    # ========================================================================
    # STATE QUERIES
    # ========================================================================
    
    def is_sermon_active(self) -> bool:
        """Check if a sermon is currently running."""
        return self.state.current_segment != SermonSegment.IDLE
    
    def get_current_segment(self) -> SermonSegment:
        """Get the current segment."""
        return self.state.current_segment
    
    def get_segment_info(self) -> Dict:
        """Get information about the current segment."""
        segment = self.state.current_segment
        if segment == SermonSegment.IDLE:
            return {"name": "Idle", "type": "none", "description": "No sermon active"}
        return SEGMENT_CONFIG.get(segment, {})
    
    def get_segment_elapsed(self) -> float:
        """Get seconds elapsed in current segment."""
        if self.state.segment_start_time is None:
            return 0
        return time.time() - self.state.segment_start_time
    
    def get_sermon_elapsed(self) -> float:
        """Get total seconds elapsed in sermon."""
        if self.state.sermon_start_time is None:
            return 0
        return time.time() - self.state.sermon_start_time
    
    def get_status(self) -> Dict:
        """Get full status of the sermon."""
        segment = self.state.current_segment
        segment_info = self.get_segment_info()
        
        return {
            "active": self.is_sermon_active(),
            "paused": self.state.paused,
            "segment": segment.name,
            "segment_index": SERMON_ORDER.index(segment) + 1 if segment in SERMON_ORDER else 0,
            "total_segments": len(SERMON_ORDER),
            "segment_name": segment_info.get("name", "Unknown"),
            "segment_type": segment_info.get("type", "unknown"),
            "segment_elapsed_seconds": self.get_segment_elapsed(),
            "segment_duration_minutes": segment_info.get("duration_minutes", 0),
            "sermon_elapsed_seconds": self.get_sermon_elapsed(),
            "daily_theme": self.state.daily_theme,
        }
    
    # ========================================================================
    # SERMON CONTROL
    # ========================================================================
    
    def start_sermon(self, theme_number: Optional[int] = None) -> bool:
        """
        Start a new sermon from the beginning.
        Optionally specify a theme number (1-10), otherwise uses daily theme.
        """
        with self._lock:
            if self.is_sermon_active():
                print("⚠️ Sermon already active!")
                return False
            
            # Prepare content
            self._prepare_sermon_content(theme_number)
            
            # Start with intro
            self.state.sermon_start_time = time.time()
            self._transition_to(SermonSegment.INTRO_SONG)
            
            print(f"🙏 SERMON STARTED - Theme: {self.state.daily_theme['commandment']}")
            return True
    
    def stop_sermon(self) -> bool:
        """Stop the current sermon."""
        with self._lock:
            if not self.is_sermon_active():
                return False
            
            print("🛑 SERMON STOPPED")
            self._transition_to(SermonSegment.IDLE)
            self._emit('sermon_end')
            return True
    
    def pause_sermon(self) -> bool:
        """Pause the current sermon."""
        with self._lock:
            if not self.is_sermon_active() or self.state.paused:
                return False
            self.state.paused = True
            print("⏸️ SERMON PAUSED")
            return True
    
    def resume_sermon(self) -> bool:
        """Resume a paused sermon."""
        with self._lock:
            if not self.state.paused:
                return False
            self.state.paused = False
            print("▶️ SERMON RESUMED")
            return True
    
    def advance_segment(self) -> bool:
        """Advance to the next segment."""
        with self._lock:
            if not self.is_sermon_active():
                return False
            
            current_idx = SERMON_ORDER.index(self.state.current_segment)
            
            if current_idx >= len(SERMON_ORDER) - 1:
                # End of sermon
                print("✅ SERMON COMPLETE!")
                self._transition_to(SermonSegment.IDLE)
                self._emit('sermon_end')
                return True
            
            # Move to next segment
            next_segment = SERMON_ORDER[current_idx + 1]
            self._transition_to(next_segment)
            return True
    
    def skip_to_segment(self, segment: SermonSegment) -> bool:
        """Skip to a specific segment."""
        with self._lock:
            if segment not in SERMON_ORDER:
                return False
            
            if not self.is_sermon_active():
                # Start sermon if not active
                self._prepare_sermon_content()
                self.state.sermon_start_time = time.time()
            
            self._transition_to(segment)
            return True
    
    # ========================================================================
    # CONTENT PREPARATION
    # ========================================================================
    
    def _prepare_sermon_content(self, theme_number: Optional[int] = None):
        """Prepare all content for the sermon."""
        # Get theme
        if theme_number:
            from sermon_content import get_theme_by_number
            self.state.daily_theme = get_theme_by_number(theme_number)
        else:
            self.state.daily_theme = get_daily_theme()
        
        # Get scroll
        scroll_num, title, excerpt = get_daily_scroll()
        self.state.scroll_number = scroll_num
        self.state.scroll_title = title
        self.state.scroll_excerpt = excerpt
        
        # Get cannon chapter
        book, author, chapter, content = get_random_cannon_chapter()
        self.state.cannon_book = book
        self.state.cannon_author = author
        self.state.cannon_chapter = chapter
        self.state.cannon_content = content
    
    def _transition_to(self, segment: SermonSegment):
        """Transition to a new segment."""
        old_segment = self.state.current_segment
        self.state.current_segment = segment
        self.state.segment_start_time = time.time() if segment != SermonSegment.IDLE else None
        info = SEGMENT_CONFIG.get(segment, {})
        old_info = SEGMENT_CONFIG.get(old_segment, {})
        
        if segment != SermonSegment.IDLE:
            print(f"📿 Segment: {info.get('name', 'Unknown')} ({info.get('type', 'unknown')})")
        self._emit('segment_change', segment, info, old_segment, old_info)
    
    # ========================================================================
    # CONTENT GETTERS (for TTS generation)
    # ========================================================================
    
    def get_opening_monologue_context(self) -> Dict:
        """Get context for generating opening monologue."""
        return {
            "theme": self.state.daily_theme,
            "scroll_title": self.state.scroll_title,
        }
    
    def get_scroll_reading_content(self) -> Dict:
        """Get content for scroll reading."""
        return {
            "scroll_number": self.state.scroll_number,
            "title": self.state.scroll_title,
            "excerpt": self.state.scroll_excerpt,
        }
    
    def get_cannon_content(self) -> Dict:
        """Get cannon chapter content."""
        return {
            "book": self.state.cannon_book,
            "author": self.state.cannon_author,
            "chapter": self.state.cannon_chapter,
            "content": self.state.cannon_content,
        }
    
    def get_parable_context(self) -> Dict:
        """Get context for generating a parable."""
        return {
            "theme": self.state.daily_theme,
        }
    
    def get_brothtism_content(self) -> str:
        """Get the brothtism text (10 commandments)."""
        return format_brothtism_text()
    
    def get_closing_context(self) -> Dict:
        """Get context for closing monologue."""
        return {
            "theme": self.state.daily_theme,
            "scroll_title": self.state.scroll_title,
            "cannon_book": self.state.cannon_book,
        }
    
    def get_audio_file(self, segment: Optional[SermonSegment] = None) -> Optional[str]:
        """Get the audio file path for a segment."""
        segment = segment or self.state.current_segment
        if segment not in SEGMENT_CONFIG:
            return None
        
        audio_key = SEGMENT_CONFIG[segment].get("audio_key")
        if audio_key:
            return get_audio_path(audio_key)
        return None


# Singleton instance
_sermon_engine: Optional[SermonEngine] = None


def get_sermon_engine() -> SermonEngine:
    """Get the global sermon engine instance."""
    global _sermon_engine
    if _sermon_engine is None:
        _sermon_engine = SermonEngine()
    return _sermon_engine


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SERMON ENGINE TEST")
    print("=" * 60)
    
    engine = get_sermon_engine()
    
    # Test starting sermon
    print("\n🙏 Starting sermon...")
    engine.start_sermon()
    
    print(f"\nStatus: {engine.get_status()}")
    
    # Test advancing through segments
    print("\n📿 Advancing through segments:")
    for i in range(len(SERMON_ORDER)):
        status = engine.get_status()
        print(f"   {status['segment_index']}/{status['total_segments']}: {status['segment_name']}")
        
        if status['segment'] == "SCROLL_READING":
            content = engine.get_scroll_reading_content()
            print(f"      Scroll: {content['title']}")
        
        if status['segment'] == "CANNON_SUMMARY":
            content = engine.get_cannon_content()
            print(f"      Cannon: {content['book']} - {content['chapter']}")
        
        if status['segment'] == "BROTHTISM":
            print(f"      Brothtism text ready!")
        
        engine.advance_segment()
    
    print("\n✅ Test complete!")


