"""
Utility functions for the audio generator
"""
import re
from datetime import datetime
from pathlib import Path


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    Create a safe filename from text content
    
    Args:
        text: Input text to convert to filename
        max_length: Maximum length of the filename (default: 50)
    
    Returns:
        Sanitized filename string
    """
    # Remove special characters and replace spaces with underscores
    filename = re.sub(r'[^\w\s-]', '', text.lower())
    filename = re.sub(r'[\s_-]+', '_', filename)
    filename = filename.strip('_')
    
    # Truncate if too long
    if len(filename) > max_length:
        filename = filename[:max_length]
    
    # Add timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # If filename is empty or too short, use a generic name
    if not filename or len(filename) < 3:
        filename = "audio"
    
    return f"{filename}_{timestamp}"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def estimate_audio_duration(text: str, words_per_minute: int = 150) -> float:
    """
    Estimate audio duration based on text length
    
    Args:
        text: Input text
        words_per_minute: Average speaking rate (default: 150 WPM)
    
    Returns:
        Estimated duration in seconds
    """
    word_count = len(text.split())
    duration_minutes = word_count / words_per_minute
    return duration_minutes * 60


def validate_text(text: str, max_tokens: int = 32000) -> tuple[bool, str]:
    """
    Validate input text for TTS generation
    
    Args:
        text: Input text to validate
        max_tokens: Maximum allowed tokens (default: 32000)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Text cannot be empty"
    
    # Rough token estimation (1 token ≈ 4 characters)
    estimated_tokens = len(text) / 4
    
    if estimated_tokens > max_tokens:
        return False, f"Text is too long (estimated {int(estimated_tokens)} tokens, max {max_tokens})"
    
    return True, ""


def create_prompt_from_components(audio_profile: str = "", scene: str = "", 
                                  directors_notes: str = "", transcript: str = "") -> str:
    """
    Create a formatted prompt from components for advanced mode
    
    Args:
        audio_profile: Audio profile description
        scene: Scene description
        directors_notes: Director's notes
        transcript: The actual text to speak
    
    Returns:
        Formatted prompt string
    """
    parts = []
    
    if audio_profile:
        parts.append(f"# AUDIO PROFILE\n{audio_profile}")
    
    if scene:
        parts.append(f"## THE SCENE\n{scene}")
    
    if directors_notes:
        parts.append(f"### DIRECTOR'S NOTES\n{directors_notes}")
    
    if transcript:
        parts.append(f"#### TRANSCRIPT\n{transcript}")
    
    return "\n\n".join(parts) if parts else transcript


def save_history(text: str, voice: str, output_path: Path, history_file: Path = None):
    """
    Save generation history to a log file
    
    Args:
        text: Generated text
        voice: Voice used
        output_path: Output file path
        history_file: History file path (optional)
    """
    if history_file is None:
        history_file = Path(__file__).parent / "generation_history.txt"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Voice: {voice}\n")
        f.write(f"Output: {output_path}\n")
        f.write(f"Text: {text[:100]}{'...' if len(text) > 100 else ''}\n")
