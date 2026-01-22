# 🚀 Quick Start Guide

## Step 1: Get Your API Key
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your key

## Step 2: Configure the Application
1. Open the `.env.example` file
2. Copy it and rename to `.env`
3. Replace `your_api_key_here` with your actual key:
   ```
   GEMINI_API_KEY=AIzaSy...your_key_here
   ```

## Step 3: Run the Application

### Option A: Quick Start (Windows)
Double-click `start.bat` - it will:
- Create virtual environment
- Install dependencies
- Launch the application

### Option B: Manual Start
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run the application
python app.py
```

## Step 4: Generate Your First Audio

### Basic Mode (Recommended for first try)
1. Keep "Basic" mode selected
2. Choose a voice (try "Kore")
3. Type your text: "Hello, this is my first audio!"
4. Click "🎵 Generate Audio"
5. Find your audio in the `outputs/` folder

### Advanced Mode (For professionals)
1. Select "Advanced" mode
2. Fill in the fields:
   - **Audio Profile**: Character description
   - **Scene**: Environment setting
   - **Director's Notes**: Style instructions
   - **Transcript**: Your actual text
3. Click "🎵 Generate Audio"

## 🎤 All 30 Available Voices

- Puck, Charon, Kore (← Try these first!)
- Fenrir, Aoede, Orus, Pegasus
- Vesta, Callisto, Oberon, Proteus
- Janus, Umbriel, Io, Phobos
- Dione, Titan, Thebe, Ceres
- Elara, Helene, Iapetus, Larissa
- Leda, Metis, Nereid, Rhea
- Naiad, Triton, Thalassa

## 🌍 Supported Languages (Auto-detected)
Arabic, Bengali, German, English (US/India), Spanish, French, Hindi, Indonesian, Italian, Japanese, Korean, Marathi, Dutch, Polish, Portuguese, Romanian, Russian, Tamil, Telugu, Thai, Turkish, Ukrainian, Vietnamese

## 💡 Tips

✅ **Start with Flash model** - It's faster and uses less quota  
✅ **Monitor your usage** - Check "API Calls Today" in the status bar  
✅ **Save prompts** - Copy good prompts to reuse later  
✅ **Test different voices** - Each has unique characteristics  

## ⚠️ Free Tier Limits
- ~15 requests/minute
- ~1,500 requests/day estimated
- 32k tokens per request

## 🆘 Troubleshooting

**"API Key Required" error?**
→ Add your API key in Settings or `.env` file

**"Rate Limit Exceeded" error?**
→ Wait 1 minute, you hit the 15/min limit

**No sound in audio file?**
→ Check if API key is valid, try a different voice

## 📚 More Information
See [README.md](README.md) for complete documentation.

---
**Ready to generate amazing audio? Let's go! 🎵**
