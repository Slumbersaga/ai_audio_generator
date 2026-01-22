"""
Gemini TTS Audio Generator - Desktop Application
A comprehensive audio generation tool with all Google Gemini TTS capabilities
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
from pathlib import Path
from datetime import datetime

import config
from audio_engine import AudioEngine
from utils import sanitize_filename, validate_text, create_prompt_from_components, save_history

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AudioGeneratorApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Gemini TTS Audio Generator")
        self.geometry("900x800")
        self.minsize(800, 700)
        
        # Application state
        self.api_key = config.API_KEY
        self.output_dir = config.DEFAULT_OUTPUT_DIR
        self.engine = None
        self.generation_count = 0
        
        # Load settings
        self.load_settings()
        
        # Initialize engine if API key exists
        if self.api_key:
            try:
                self.engine = AudioEngine(self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize engine: {e}")
        
        # Build UI
        self.create_widgets()
        
        # Update status
        self.update_status()
    
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎵 Gemini TTS Audio Generator",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Top controls
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # Mode selection
        mode_frame = ctk.CTkFrame(top_frame)
        mode_frame.pack(side="left", padx=5)
        
        ctk.CTkLabel(mode_frame, text="Mode:").pack(side="left", padx=5)
        self.mode_var = ctk.StringVar(value="basic")
        ctk.CTkRadioButton(
            mode_frame, text="Basic", variable=self.mode_var,
            value="basic", command=self.toggle_mode
        ).pack(side="left", padx=5)
        ctk.CTkRadioButton(
            mode_frame, text="Advanced", variable=self.mode_var,
            value="advanced", command=self.toggle_mode
        ).pack(side="left", padx=5)
        
        # Model selection
        model_frame = ctk.CTkFrame(top_frame)
        model_frame.pack(side="left", padx=20)
        
        ctk.CTkLabel(model_frame, text="Model:").pack(side="left", padx=5)
        self.model_var = ctk.StringVar(value=list(config.MODELS.keys())[0])
        model_menu = ctk.CTkOptionMenu(
            model_frame,
            variable=self.model_var,
            values=list(config.MODELS.keys()),
            width=200
        )
        model_menu.pack(side="left", padx=5)
        
        # Voice and Language controls
        voice_frame = ctk.CTkFrame(main_frame)
        voice_frame.pack(fill="x", padx=10, pady=10)
        
        # Voice selection
        voice_left = ctk.CTkFrame(voice_frame)
        voice_left.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(voice_left, text="Voice:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        self.voice_var = ctk.StringVar(value=config.VOICES[2])  # Default: Kore
        voice_menu = ctk.CTkOptionMenu(
            voice_left,
            variable=self.voice_var,
            values=config.VOICES,
            width=250
        )
        voice_menu.pack(fill="x")
        
        # Language selection
        lang_right = ctk.CTkFrame(voice_frame)
        lang_right.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(lang_right, text="Language:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        self.lang_var = ctk.StringVar(value="Auto-detect")
        lang_menu = ctk.CTkOptionMenu(
            lang_right,
            variable=self.lang_var,
            values=list(config.LANGUAGES.keys()),
            width=250
        )
        lang_menu.pack(fill="x")
        
        # Speaker mode
        speaker_frame = ctk.CTkFrame(main_frame)
        speaker_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(speaker_frame, text="Speakers:").pack(side="left", padx=5)
        self.speaker_mode = ctk.StringVar(value="single")
        ctk.CTkRadioButton(
            speaker_frame, text="Single Speaker", variable=self.speaker_mode,
            value="single", command=self.toggle_speaker_mode
        ).pack(side="left", padx=5)
        ctk.CTkRadioButton(
            speaker_frame, text="Multi-Speaker (2)", variable=self.speaker_mode,
            value="multi", command=self.toggle_speaker_mode
        ).pack(side="left", padx=5)
        
        # Multi-speaker configuration (hidden by default)
        self.multi_speaker_frame = ctk.CTkFrame(main_frame)
        self.multi_speaker_frame.pack(fill="x", padx=10, pady=5)
        self.multi_speaker_frame.pack_forget()  # Hide initially
        
        # Speaker 1
        sp1_frame = ctk.CTkFrame(self.multi_speaker_frame)
        sp1_frame.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(sp1_frame, text="Speaker 1:").pack(anchor="w")
        self.speaker1_name = ctk.CTkEntry(sp1_frame, placeholder_text="Name (e.g., Alice)")
        self.speaker1_name.pack(fill="x", pady=2)
        self.speaker1_voice = ctk.CTkOptionMenu(sp1_frame, values=config.VOICES)
        self.speaker1_voice.set(config.VOICES[0])
        self.speaker1_voice.pack(fill="x")
        
        # Speaker 2
        sp2_frame = ctk.CTkFrame(self.multi_speaker_frame)
        sp2_frame.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(sp2_frame, text="Speaker 2:").pack(anchor="w")
        self.speaker2_name = ctk.CTkEntry(sp2_frame, placeholder_text="Name (e.g., Bob)")
        self.speaker2_name.pack(fill="x", pady=2)
        self.speaker2_voice = ctk.CTkOptionMenu(sp2_frame, values=config.VOICES)
        self.speaker2_voice.set(config.VOICES[1])
        self.speaker2_voice.pack(fill="x")
        
        # Content frame (scrollable)
        content_frame = ctk.CTkScrollableFrame(main_frame, height=400)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Basic mode text input
        self.basic_frame = ctk.CTkFrame(content_frame)
        self.basic_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            self.basic_frame,
            text="Enter Text to Convert to Speech:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.text_input = ctk.CTkTextbox(self.basic_frame, height=300, wrap="word")
        self.text_input.pack(fill="both", expand=True)
        self.text_input.insert("1.0", "Welcome to the Gemini TTS Audio Generator!")
        
        # Advanced mode inputs (hidden by default)
        self.advanced_frame = ctk.CTkFrame(content_frame)
        
        # Audio Profile
        ctk.CTkLabel(
            self.advanced_frame,
            text="Audio Profile:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(5, 2))
        self.audio_profile = ctk.CTkTextbox(self.advanced_frame, height=60)
        self.audio_profile.pack(fill="x", pady=(0, 10))
        self.audio_profile.insert("1.0", "Professional narrator, warm and engaging voice")
        
        # Scene
        ctk.CTkLabel(
            self.advanced_frame,
            text="Scene:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 2))
        self.scene = ctk.CTkTextbox(self.advanced_frame, height=60)
        self.scene.pack(fill="x", pady=(0, 10))
        self.scene.insert("1.0", "Cozy recording studio with warm lighting")
        
        # Director's Notes
        ctk.CTkLabel(
            self.advanced_frame,
            text="Director's Notes:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 2))
        self.directors_notes = ctk.CTkTextbox(self.advanced_frame, height=60)
        self.directors_notes.pack(fill="x", pady=(0, 10))
        self.directors_notes.insert("1.0", "Calm pace, clear articulation, friendly tone")
        
        # Transcript
        ctk.CTkLabel(
            self.advanced_frame,
            text="Transcript:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 2))
        self.transcript = ctk.CTkTextbox(self.advanced_frame, height=150)
        self.transcript.pack(fill="both", expand=True)
        self.transcript.insert("1.0", "Welcome to the Gemini TTS Audio Generator!")
        
        # Output controls
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="x", padx=10, pady=10)
        
        # Output directory
        dir_frame = ctk.CTkFrame(output_frame)
        dir_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(dir_frame, text="Output:").pack(side="left", padx=5)
        self.output_label = ctk.CTkLabel(
            dir_frame,
            text=str(self.output_dir),
            anchor="w"
        )
        self.output_label.pack(side="left", fill="x", expand=True, padx=5)
        
        browse_btn = ctk.CTkButton(
            dir_frame,
            text="📁 Browse",
            width=100,
            command=self.browse_output_dir
        )
        browse_btn.pack(side="left", padx=5)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            output_frame,
            text="🎵 Generate Audio",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.generate_audio,
            fg_color="#2B8A3E",
            hover_color="#37A24A"
        )
        self.generate_btn.pack(fill="x", pady=10)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            output_frame,
            text="⚙️ API Settings",
            command=self.show_settings,
            fg_color="#495057",
            hover_color="#5A6268"
        )
        settings_btn.pack(fill="x")
        
        # Status bar
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Status: Ready",
            anchor="w"
        )
        self.status_label.pack(side="left", padx=5)
        
        self.api_usage_label = ctk.CTkLabel(
            status_frame,
            text=f"API Calls Today: {self.generation_count}/~{config.FREE_TIER_DAILY_ESTIMATE}",
            anchor="e"
        )
        self.api_usage_label.pack(side="right", padx=5)
    
    def toggle_mode(self):
        """Toggle between basic and advanced mode"""
        if self.mode_var.get() == "basic":
            self.advanced_frame.pack_forget()
            self.basic_frame.pack(fill="both", expand=True)
        else:
            self.basic_frame.pack_forget()
            self.advanced_frame.pack(fill="both", expand=True)
    
    def toggle_speaker_mode(self):
        """Toggle multi-speaker configuration visibility"""
        if self.speaker_mode.get() == "multi":
            self.multi_speaker_frame.pack(fill="x", padx=10, pady=5)
        else:
            self.multi_speaker_frame.pack_forget()
    
    def browse_output_dir(self):
        """Browse for output directory"""
        dir_path = filedialog.askdirectory(initialdir=self.output_dir)
        if dir_path:
            self.output_dir = Path(dir_path)
            self.output_label.configure(text=str(self.output_dir))
            self.save_settings()
    
    def show_settings(self):
        """Show API settings dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("API Settings")
        dialog.geometry("500x200")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame,
            text="Google Gemini API Key",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            frame,
            text="Get your API key from: https://aistudio.google.com/app/apikey",
            font=("Arial", 10),
            text_color="gray"
        ).pack(pady=(0, 10))
        
        api_entry = ctk.CTkEntry(frame, width=400, show="*")
        api_entry.insert(0, self.api_key)
        api_entry.pack(pady=10)
        
        def save_api_key():
            new_key = api_entry.get().strip()
            if new_key:
                self.api_key = new_key
                # Update .env file
                env_file = Path(__file__).parent / ".env"
                with open(env_file, "w") as f:
                    f.write(f"GEMINI_API_KEY={new_key}\n")
                
                # Reinitialize engine
                try:
                    self.engine = AudioEngine(self.api_key)
                    messagebox.showinfo("Success", "API key saved successfully!")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid API key: {str(e)}")
            else:
                messagebox.showwarning("Warning", "Please enter an API key")
        
        ctk.CTkButton(
            frame,
            text="Save",
            command=save_api_key,
            fg_color="#2B8A3E",
            hover_color="#37A24A"
        ).pack(pady=10)
    
    def generate_audio(self):
        """Generate audio from text"""
        # Validate API key
        if not self.api_key or not self.engine:
            messagebox.showerror(
                "API Key Required",
                "Please set your Google Gemini API key in Settings"
            )
            self.show_settings()
            return
        
        # Get text based on mode
        if self.mode_var.get() == "basic":
            text = self.text_input.get("1.0", "end-1c").strip()
        else:
            # Advanced mode - build prompt
            audio_profile = self.audio_profile.get("1.0", "end-1c").strip()
            scene = self.scene.get("1.0", "end-1c").strip()
            directors_notes = self.directors_notes.get("1.0", "end-1c").strip()
            transcript = self.transcript.get("1.0", "end-1c").strip()
            
            text = create_prompt_from_components(
                audio_profile, scene, directors_notes, transcript
            )
        
        # Validate text
        is_valid, error_msg = validate_text(text)
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Get filename from text
        filename_base = sanitize_filename(text[:100])
        output_path = self.output_dir / f"{filename_base}.wav"
        
        # Get model
        model_name = config.MODELS[self.model_var.get()]
        
        # Disable button during generation
        self.generate_btn.configure(state="disabled", text="⏳ Generating...")
        
        # Run generation in thread
        def generate():
            try:
                if self.speaker_mode.get() == "single":
                    # Single speaker
                    self.engine.generate_single_speaker(
                        text=text,
                        voice=self.voice_var.get(),
                        model=model_name,
                        output_path=output_path,
                        progress_callback=self.update_progress
                    )
                else:
                    # Multi-speaker
                    speaker1 = self.speaker1_name.get() or "Speaker1"
                    speaker2 = self.speaker2_name.get() or "Speaker2"
                    
                    speakers = [
                        {"name": speaker1, "voice": self.speaker1_voice.get()},
                        {"name": speaker2, "voice": self.speaker2_voice.get()}
                    ]
                    
                    self.engine.generate_multi_speaker(
                        text=text,
                        speakers=speakers,
                        model=model_name,
                        output_path=output_path,
                        progress_callback=self.update_progress
                    )
                
                # Save to history
                save_history(text, self.voice_var.get(), output_path)
                
                # Update generation count
                self.generation_count += 1
                self.save_settings()
                
                # Success
                self.after(100, lambda: messagebox.showinfo(
                    "Success",
                    f"Audio generated successfully!\n\nSaved as: {output_path.name}"
                ))
                
            except Exception as e:
                self.after(100, lambda: messagebox.showerror(
                    "Generation Error",
                    f"Failed to generate audio:\n{str(e)}"
                ))
            
            finally:
                # Re-enable button
                self.after(100, lambda: self.generate_btn.configure(
                    state="normal",
                    text="🎵 Generate Audio"
                ))
                self.after(100, self.update_status)
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
    
    def update_progress(self, message: str):
        """Update progress status"""
        self.status_label.configure(text=f"Status: {message}")
    
    def update_status(self):
        """Update status bar"""
        self.status_label.configure(text="Status: Ready")
        self.api_usage_label.configure(
            text=f"API Calls Today: {self.generation_count}/~{config.FREE_TIER_DAILY_ESTIMATE}"
        )
    
    def load_settings(self):
        """Load saved settings"""
        if config.SETTINGS_FILE.exists():
            try:
                with open(config.SETTINGS_FILE, "r") as f:
                    settings = json.load(f)
                    self.generation_count = settings.get("generation_count", 0)
                    last_date = settings.get("last_date", "")
                    
                    # Reset count if new day
                    today = datetime.now().strftime("%Y-%m-%d")
                    if last_date != today:
                        self.generation_count = 0
                    
                    # Load output dir
                    output_dir = settings.get("output_dir")
                    if output_dir:
                        self.output_dir = Path(output_dir)
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save current settings"""
        settings = {
            "generation_count": self.generation_count,
            "last_date": datetime.now().strftime("%Y-%m-%d"),
            "output_dir": str(self.output_dir)
        }
        
        try:
            with open(config.SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")


def main():
    """Main entry point"""
    app = AudioGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()