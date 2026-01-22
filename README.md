# 🎵 Gemini TTS Audio Generator

A comprehensive desktop application that leverages all Google Gemini TTS capabilities to generate high-quality audio from text.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## ✨ Features

### 🎤 30 Voice Options
Access all 30 prebuilt voices from Google Gemini TTS:
- Puck, Charon, Kore, Fenrir, Aoede, Orus, Pegasus, Vesta, Callisto, Oberon
- Proteus, Janus, Umbriel, Io, Phobos, Dione, Titan, Thebe, Ceres, Elara
- Helene, Iapetus, Larissa, Leda, Metis, Nereid, Rhea, Naiad, Triton, Thalassa

### 🌍 24 Language Support
Automatic language detection with support for:
- **Americas**: English (US), Spanish (US), Portuguese (Brazil)
- **Europe**: German, French, Italian, Dutch, Polish, Romanian, Russian, Ukrainian
- **Asia**: Arabic, Bengali, Hindi, Indonesian, Japanese, Korean, Marathi, Tamil, Telugu, Thai, Turkish, Vietnamese
- **Variants**: English (India)

### 🎭 Two Generation Modes

#### Basic Mode
Simple text-to-speech conversion:
- Enter your text
- Select a voice
- Generate audio instantly

#### Advanced Mode
Full control with professional prompting:
- **Audio Profile**: Define character identity and persona
- **Scene**: Set the environment and emotional context
- **Director's Notes**: Specify style, accent, pace, and breathing
- **Transcript**: The actual text to convert

### 👥 Speaker Options
- **Single Speaker**: One voice narration
- **Multi-Speaker**: Up to 2 speakers for dialogues and conversations

### 🤖 Two Models
- **Gemini 2.5 Flash TTS**: Fast generation, ideal for testing
- **Gemini 2.5 Pro TTS**: Higher quality for production use

### 💾 Smart File Management
- Automatic filename generation based on text content
- Timestamp-based naming for uniqueness
- Custom output directory selection
- Generation history logging

### 📊 API Usage Tracking
- Real-time request counting
- Daily usage monitoring
- Free tier limit warnings

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Setup

1. **Clone or download this repository**
```bash
cd audio_generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API key**

Create a `.env` file in the project directory:
```bash
copy .env.example .env
```

Edit `.env` and add your API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Alternatively, you can set the API key through the application's Settings dialog.

4. **Run the application**
```bash
python app.py
```

## 📖 Usage Guide

### Basic Workflow

1. **Launch the application**
   ```bash
   python app.py
   ```

2. **Choose your mode**
   - **Basic**: For simple text-to-speech
   - **Advanced**: For professional-grade audio with detailed prompts

3. **Select a voice**
   - Browse through 30 available voices
   - Each voice has unique characteristics

4. **Configure speakers**
   - **Single**: Standard narration
   - **Multi-Speaker**: For dialogues (define speaker names and voices)

5. **Enter your text**
   - Basic mode: Direct text input
   - Advanced mode: Fill Audio Profile, Scene, Director's Notes, and Transcript

6. **Generate audio**
   - Click "Generate Audio"
   - Audio saves automatically with smart naming

### Advanced Prompting Example

**Audio Profile:**
```
Sarah - A professional documentary narrator with 15 years of experience. 
Warm, authoritative, and engaging. Age: 40s. Background: BBC trained.
```

**Scene:**
```
A professional recording studio in London. Late afternoon, warm lighting. 
The atmosphere is focused and calm.
```

**Director's Notes:**
```
Style: Documentary narration
Pace: Moderate, clear articulation
Accent: Received Pronunciation (British English)
Tone: Authoritative but warm
Breathing: Natural pauses at punctuation
```

**Transcript:**
```
The Amazon rainforest spans over 5.5 million square kilometers, 
making it the largest tropical rainforest in the world.
```

### Multi-Speaker Example

**Setup:**
- Speaker 1: "Alice" - Voice: Kore
- Speaker 2: "Bob" - Voice: Fenrir

**Text:**
```
Alice: Good morning! How are you today?
Bob: I'm doing great, thanks for asking!
Alice: That's wonderful to hear.
```

## ⚠️ API Limits (Free Tier)

When using the **AI Studio Free API**, be aware of these limitations:

### Rate Limits
- **~15 requests per minute** for Gemini 2.5 Flash
- **Lower limits** for Gemini 2.5 Pro

### Quotas
- **Daily limits** may apply (approximately 1,500 requests/day)
- Limits may vary based on Google's policies

### Context Window
- **32,000 tokens maximum** per request
- Roughly 24,000-30,000 words depending on complexity

### Recommendations for Free Tier

✅ **Best Practices:**
- Use **Gemini 2.5 Flash TTS** for development and testing
- Monitor usage through the built-in tracker
- Save frequently used prompts as templates
- Batch your generation needs
- Keep individual requests under 10,000 words

⚡ **For Production Use:**
Consider upgrading to a paid plan for:
- Higher rate limits (60+ RPM)
- No daily quotas
- Priority access
- Better reliability
- Extended support

## 📂 Project Structure

```
audio_generator/
├── app.py                  # Main GUI application
├── audio_engine.py         # Audio generation engine
├── config.py              # Configuration and constants
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Your API key (create this)
├── README.md             # This file
├── outputs/              # Generated audio files
└── generation_history.txt # Generation log
```

## 🎯 Output Files

Generated audio files are saved as:
- **Format**: WAV (Waveform Audio File)
- **Sample Rate**: 24,000 Hz
- **Channels**: Mono (1 channel)
- **Bit Depth**: 16-bit PCM
- **Naming**: `{text_preview}_{timestamp}.wav`

Example: `welcome_to_gemini_20260122_225959.wav`

## 🛠️ Troubleshooting

### "API Key Required" Error
- Ensure you've created a `.env` file with your API key
- Or set the API key through Settings → API Settings
- Verify your key at [AI Studio](https://aistudio.google.com/app/apikey)

### "Rate Limit Exceeded" Error
- You've hit the free tier limit (15 RPM)
- Wait 1 minute before trying again
- Consider upgrading to a paid plan

### "Text Too Long" Error
- Your text exceeds 32,000 tokens
- Split into smaller chunks
- Each chunk should be under ~25,000 words

### No Sound in Generated Audio
- Check if the file size is > 0 bytes
- Verify your API key is valid
- Try a different voice or model

### Application Won't Start
- Ensure Python 3.8+ is installed
- Install dependencies: `pip install -r requirements.txt`
- Check for error messages in the console

## 🔒 Privacy & Security

- API keys are stored locally in `.env` file
- Never commit `.env` to version control
- Generated audio is saved locally only
- No data is uploaded except API requests to Google

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/gemini-api/docs/speech-generation)
- UI powered by [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Developed for educational and productivity purposes

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues related to:
- **This application**: Open an issue in the repository
- **Gemini API**: Check [Google's documentation](https://ai.google.dev/gemini-api/docs)
- **API limits**: Visit [AI Studio](https://aistudio.google.com/)

---

**Made with ❤️ using Google Gemini TTS**

*Generate amazing audio with the power of AI!*
