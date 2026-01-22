"""
Core audio generation engine using Google Gemini TTS API
"""
import wave
from pathlib import Path
from typing import Callable, Optional
from google import genai
from google.genai import types
import config


class AudioEngine:
    """Audio generation engine for Gemini TTS"""
    
    def __init__(self, api_key: str):
        """
        Initialize the audio engine
        
        Args:
            api_key: Google Gemini API key
        """
        self.client = genai.Client(api_key=api_key)
        self.request_count = 0
    
    def generate_single_speaker(
        self,
        text: str,
        voice: str,
        model: str = "gemini-2.5-flash-preview-tts",
        output_path: Optional[Path] = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Path:
        """
        Generate single-speaker audio
        
        Args:
            text: Text to convert to speech
            voice: Voice name (from config.VOICES)
            model: Model to use
            output_path: Output file path (optional)
            progress_callback: Callback function for progress updates
        
        Returns:
            Path to the generated audio file
        """
        try:
            if progress_callback:
                progress_callback("Generating audio with Gemini TTS...")
            
            # Generate content with audio modality
            response = self.client.models.generate_content(
                model=model,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice,
                            )
                        )
                    ),
                )
            )
            
            # Extract audio data
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            
            if progress_callback:
                progress_callback("Saving audio file...")
            
            # Save to WAV file
            if output_path is None:
                output_path = config.DEFAULT_OUTPUT_DIR / "output.wav"
            
            self._save_wave_file(output_path, audio_data)
            
            self.request_count += 1
            
            if progress_callback:
                progress_callback(f"Audio saved successfully: {output_path.name}")
            
            return output_path
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            raise
    
    def generate_multi_speaker(
        self,
        text: str,
        speakers: list[dict],
        model: str = "gemini-2.5-flash-preview-tts",
        output_path: Optional[Path] = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Path:
        """
        Generate multi-speaker audio (up to 2 speakers)
        
        Args:
            text: Text to convert with speaker annotations
            speakers: List of speaker configs [{"name": "Speaker1", "voice": "Kore"}, ...]
            model: Model to use
            output_path: Output file path (optional)
            progress_callback: Callback function for progress updates
        
        Returns:
            Path to the generated audio file
        """
        try:
            if progress_callback:
                progress_callback("Generating multi-speaker audio...")
            
            # Create speaker voice configs
            speaker_configs = []
            for speaker in speakers[:2]:  # Max 2 speakers
                speaker_configs.append(
                    types.SpeakerVoiceConfig(
                        speaker=speaker["name"],
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=speaker["voice"]
                            )
                        )
                    )
                )
            
            # Generate content
            response = self.client.models.generate_content(
                model=model,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                                speakers=speaker_configs
                            )
                        )
                    ),
                )
            )
            
            # Extract audio data
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            
            if progress_callback:
                progress_callback("Saving audio file...")
            
            # Save to WAV file
            if output_path is None:
                output_path = config.DEFAULT_OUTPUT_DIR / "output.wav"
            
            self._save_wave_file(output_path, audio_data)
            
            self.request_count += 1
            
            if progress_callback:
                progress_callback(f"Audio saved successfully: {output_path.name}")
            
            return output_path
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            raise
    
    def _save_wave_file(
        self,
        filename: Path,
        pcm_data: bytes,
        channels: int = config.AUDIO_CHANNELS,
        rate: int = config.AUDIO_SAMPLE_RATE,
        sample_width: int = config.AUDIO_SAMPLE_WIDTH
    ):
        """
        Save PCM data to a WAV file
        
        Args:
            filename: Output filename
            pcm_data: PCM audio data
            channels: Number of audio channels
            rate: Sample rate
            sample_width: Sample width in bytes
        """
        with wave.open(str(filename), "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
