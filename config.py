"""
Configuration and constants for the Gemini TTS Audio Generator
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv("GEMINI_API_KEY", "")

# All 30 available voices in Gemini TTS
VOICES = [
    "Puck", "Charon", "Kore", "Fenrir", "Aoede", "Orus", "Pegasus", "Vesta",
    "Callisto", "Oberon", "Proteus", "Janus", "Umbriel", "Io", "Phobos", "Dione",
    "Titan", "Thebe", "Ceres", "Elara", "Helene", "Iapetus", "Larissa", "Leda",
    "Metis", "Nereid", "Rhea", "Naiad", "Triton", "Thalassa"
]

# All 24 supported languages with their codes and display names
LANGUAGES = {
    "Auto-detect": None,
    "Arabic (Egypt)": "ar-EG",
    "Bengali (Bangladesh)": "bn-BD",
    "German (Germany)": "de-DE",
    "English (US)": "en-US",
    "English (India)": "en-IN",
    "Spanish (US)": "es-US",
    "French (France)": "fr-FR",
    "Hindi (India)": "hi-IN",
    "Indonesian (Indonesia)": "id-ID",
    "Italian (Italy)": "it-IT",
    "Japanese (Japan)": "ja-JP",
    "Korean (South Korea)": "ko-KR",
    "Marathi (India)": "mr-IN",
    "Dutch (Netherlands)": "nl-NL",
    "Polish (Poland)": "pl-PL",
    "Portuguese (Brazil)": "pt-BR",
    "Romanian (Romania)": "ro-RO",
    "Russian (Russia)": "ru-RU",
    "Tamil (India)": "ta-IN",
    "Telugu (India)": "te-IN",
    "Thai (Thailand)": "th-TH",
    "Turkish (Turkey)": "tr-TR",
    "Ukrainian (Ukraine)": "uk-UA",
    "Vietnamese (Vietnam)": "vi-VN",
}

# Available models
MODELS = {
    "Gemini 2.5 Flash TTS (Fast)": "gemini-2.5-flash-preview-tts",
    "Gemini 2.5 Pro TTS (Quality)": "gemini-2.5-pro-preview-tts"
}

# Audio settings
AUDIO_SAMPLE_RATE = 24000
AUDIO_CHANNELS = 1
AUDIO_SAMPLE_WIDTH = 2  # 16-bit

# Application settings
DEFAULT_OUTPUT_DIR = Path(__file__).parent / "outputs"
DEFAULT_OUTPUT_DIR.mkdir(exist_ok=True)

# API Rate limits (Free tier estimates)
FREE_TIER_RPM = 15  # Requests per minute
FREE_TIER_DAILY_ESTIMATE = 1500  # Estimated daily requests

# Settings file
SETTINGS_FILE = Path(__file__).parent / ".settings.json"
