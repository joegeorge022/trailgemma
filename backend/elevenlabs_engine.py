"""
ElevenLabs Audio Narration Engine
Synthesizes immersive, hands-free field audio guides for hikers, runners, and gardeners.
Enables true 'Pocket Mode' / 'Touch Grass' philosophy: screen time under 45 seconds.
"""

import os
import hashlib
import logging
import httpx

logger = logging.getLogger(__name__)

AUDIO_CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'assets', 'audio_cache')
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

class ElevenLabsAudioEngine:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        # Default voice: Warm, soothing naturalist narrator (e.g., 'Adam' or 'George')
        self.default_voice_id = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb") # George / naturalist voice

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    async def generate_speech(self, text: str, voice_id: str = None) -> dict:
        """
        Synthesizes text to speech using ElevenLabs API.
        Caches audio files locally for offline replay.
        """
        clean_text = text.strip()
        text_hash = hashlib.md5(clean_text.encode('utf-8')).hexdigest()
        cache_filename = f"briefing_{text_hash}.mp3"
        cache_filepath = os.path.join(AUDIO_CACHE_DIR, cache_filename)
        public_url = f"/assets/audio_cache/{cache_filename}"

        # If already cached, return existing file
        if os.path.exists(cache_filepath) and os.path.getsize(cache_filepath) > 100:
            logger.info(f"Returning cached ElevenLabs audio: {cache_filepath}")
            return {
                "status": "cached",
                "audio_url": public_url,
                "text": clean_text,
                "provider": "ElevenLabs (Cached Offline)"
            }

        # If API key is available, call ElevenLabs API
        if self.is_configured():
            target_voice = voice_id or self.default_voice_id
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{target_voice}"
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": clean_text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.55,
                    "similarity_boost": 0.75,
                    "style": 0.20,
                    "use_speaker_boost": True
                }
            }
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        with open(cache_filepath, "wb") as f:
                            f.write(resp.content)
                        return {
                            "status": "generated",
                            "audio_url": public_url,
                            "text": clean_text,
                            "provider": "ElevenLabs Turbo v2"
                        }
                    else:
                        logger.error(f"ElevenLabs API error: {resp.status_code} - {resp.text}")
            except Exception as e:
                logger.error(f"Failed to reach ElevenLabs: {e}")

        # Fallback to browser Web Speech API
        return {
            "status": "local_speech_synthesis",
            "audio_url": None,
            "text": clean_text,
            "provider": "Native Offline Web Speech Synthesis (Zero-latency / Offline Trailhead)",
            "tip": "Playing audio through high-fidelity on-device speech synthesis engine."
        }
