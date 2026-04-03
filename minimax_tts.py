"""
MiniMax Cloud TTS engine for VoxNovel.

Supports MiniMax speech-2.8-hd and speech-2.8-turbo models via the
MiniMax T2A v2 API (https://api.minimax.io/v1/t2a_v2).

Set MINIMAX_API_KEY environment variable or pass api_key to MiniMaxTTS().

Verified English voice IDs:
    English_Graceful_Lady, English_Insightful_Speaker, English_radiant_girl,
    English_Persuasive_Man, English_Lucky_Robot, Wise_Woman, cute_boy,
    lovely_girl, Friendly_Person, Inspirational_girl, Deep_Voice_Man,
    sweet_girl
"""

import os
import binascii
import subprocess
import requests


MINIMAX_API_URL = "https://api.minimax.io/v1/t2a_v2"

MINIMAX_TTS_MODEL_HD = "speech-2.8-hd"
MINIMAX_TTS_MODEL_TURBO = "speech-2.8-turbo"

MINIMAX_VOICES = [
    "English_Graceful_Lady",
    "English_Insightful_Speaker",
    "English_radiant_girl",
    "English_Persuasive_Man",
    "English_Lucky_Robot",
    "Wise_Woman",
    "cute_boy",
    "lovely_girl",
    "Friendly_Person",
    "Inspirational_girl",
    "Deep_Voice_Man",
    "sweet_girl",
]

# Prefix used to identify MiniMax voice IDs in the voice-actor dropdown so
# they can be distinguished from local voice-actor folder names.
MINIMAX_VOICE_PREFIX = "minimax:"


def get_minimax_voice_actor_ids():
    """Return the list of voice-actor IDs as shown in the GUI combobox."""
    return [MINIMAX_VOICE_PREFIX + v for v in MINIMAX_VOICES]


def strip_prefix(voice_actor_id: str) -> str:
    """Remove the 'minimax:' prefix from a voice-actor ID."""
    if voice_actor_id.startswith(MINIMAX_VOICE_PREFIX):
        return voice_actor_id[len(MINIMAX_VOICE_PREFIX):]
    return voice_actor_id


class MiniMaxTTS:
    """Lightweight client for the MiniMax T2A v2 API."""

    def __init__(self, api_key: str | None = None, model: str = MINIMAX_TTS_MODEL_HD):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "MiniMax API key not found. "
                "Set the MINIMAX_API_KEY environment variable or pass api_key."
            )
        self.model = model

    def synthesize(self, text: str, voice_id: str, output_path: str) -> None:
        """
        Synthesize *text* with *voice_id* and write the result to *output_path*.

        The MiniMax T2A v2 API returns hex-encoded MP3 audio in the JSON
        response field ``data.audio``.  We decode it and write it directly;
        ffmpeg (already a VoxNovel dependency) handles the MP3 → WAV conversion
        that the rest of the pipeline expects.
        """
        voice_id = strip_prefix(voice_id)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "text": text,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": 1.0,
                "vol": 1.0,
                "pitch": 0,
            },
            "audio_setting": {
                "format": "mp3",
            },
        }

        resp = requests.post(MINIMAX_API_URL, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        if data.get("base_resp", {}).get("status_code", 0) != 0:
            msg = data.get("base_resp", {}).get("status_msg", "unknown error")
            raise RuntimeError(f"MiniMax TTS API error: {msg}")

        audio_hex = data.get("data", {}).get("audio", "")
        if not audio_hex:
            raise RuntimeError("MiniMax TTS API returned empty audio data.")

        audio_bytes = binascii.unhexlify(audio_hex)

        # Write MP3 bytes; VoxNovel converts to WAV via ffmpeg elsewhere if needed.
        # We write a .mp3 extension so pydub/ffmpeg can auto-detect the codec.
        mp3_path = output_path.replace(".wav", ".mp3")
        with open(mp3_path, "wb") as f:
            f.write(audio_bytes)

        # Convert MP3 → WAV so the rest of the pipeline (pydub / torchaudio) works.
        _convert_mp3_to_wav(mp3_path, output_path)
        if mp3_path != output_path and os.path.exists(mp3_path):
            os.remove(mp3_path)


def _convert_mp3_to_wav(mp3_path: str, wav_path: str) -> None:
    """Convert an MP3 file to WAV using ffmpeg (already a project dependency)."""
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", mp3_path, wav_path],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg conversion failed: {result.stderr.decode(errors='replace')}"
        )


# ---------------------------------------------------------------------------
# Module-level singleton – reused across calls so API key is read once.
# ---------------------------------------------------------------------------
_client: MiniMaxTTS | None = None


def get_client(model: str = MINIMAX_TTS_MODEL_HD) -> MiniMaxTTS:
    """Return (creating if necessary) a module-level MiniMaxTTS instance."""
    global _client
    if _client is None or _client.model != model:
        _client = MiniMaxTTS(model=model)
    return _client


def synthesize_to_file(text: str, voice_actor: str, output_path: str,
                       model: str = MINIMAX_TTS_MODEL_HD) -> None:
    """
    Top-level helper called from the VoxNovel generate_audio() loop.

    Parameters
    ----------
    text:        The text fragment to synthesise.
    voice_actor: Either a bare MiniMax voice ID or the 'minimax:<id>' form.
    output_path: Destination WAV file path.
    model:       MiniMax TTS model name.
    """
    client = get_client(model=model)
    client.synthesize(text, voice_actor, output_path)
