"""
Tests for minimax_tts.py – MiniMax Cloud TTS integration for VoxNovel.

Unit tests mock the HTTP layer; integration tests require MINIMAX_API_KEY.
"""

import json
import os
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch, call

# ---------------------------------------------------------------------------
# Minimal stubs for heavy optional dependencies so the module can be imported
# without them being installed in the test environment.
# ---------------------------------------------------------------------------

for mod_name in ["styletts2", "styletts2.tts", "TTS", "TTS.api",
                 "TTS.tts", "TTS.tts.configs", "TTS.tts.configs.xtts_config",
                 "TTS.tts.models", "TTS.tts.models.xtts"]:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = types.ModuleType(mod_name)

# Make sure minimax_tts is importable from the repo root
sys.path.insert(0, os.path.dirname(__file__))

import minimax_tts  # noqa: E402
from minimax_tts import (  # noqa: E402
    MINIMAX_VOICES,
    MINIMAX_VOICE_PREFIX,
    MINIMAX_TTS_MODEL_HD,
    MINIMAX_TTS_MODEL_TURBO,
    MiniMaxTTS,
    get_minimax_voice_actor_ids,
    strip_prefix,
    synthesize_to_file,
    get_client,
)


# ===========================================================================
# Unit tests (no network)
# ===========================================================================

class TestVoiceActorHelpers(unittest.TestCase):
    """Test helper functions for voice-actor ID management."""

    def test_get_minimax_voice_actor_ids_returns_prefixed_list(self):
        ids = get_minimax_voice_actor_ids()
        self.assertEqual(len(ids), len(MINIMAX_VOICES))
        for vid in ids:
            self.assertTrue(
                vid.startswith(MINIMAX_VOICE_PREFIX),
                f"{vid!r} does not start with {MINIMAX_VOICE_PREFIX!r}",
            )

    def test_all_known_voices_present(self):
        ids = get_minimax_voice_actor_ids()
        bare_ids = [strip_prefix(v) for v in ids]
        for v in MINIMAX_VOICES:
            self.assertIn(v, bare_ids)

    def test_strip_prefix_removes_prefix(self):
        self.assertEqual(strip_prefix("minimax:English_Graceful_Lady"), "English_Graceful_Lady")

    def test_strip_prefix_no_prefix_unchanged(self):
        self.assertEqual(strip_prefix("English_Graceful_Lady"), "English_Graceful_Lady")

    def test_strip_prefix_only_removes_once(self):
        self.assertEqual(strip_prefix("minimax:minimax:foo"), "minimax:foo")

    def test_voice_ids_are_unique(self):
        ids = get_minimax_voice_actor_ids()
        self.assertEqual(len(ids), len(set(ids)))


class TestMiniMaxTTSInit(unittest.TestCase):
    """Test MiniMaxTTS constructor / API-key handling."""

    def test_raises_if_no_key(self):
        with patch.dict(os.environ, {}, clear=True):
            # Ensure MINIMAX_API_KEY is not set
            os.environ.pop("MINIMAX_API_KEY", None)
            with self.assertRaises(ValueError):
                MiniMaxTTS()

    def test_uses_env_key(self):
        with patch.dict(os.environ, {"MINIMAX_API_KEY": "test-key"}):
            client = MiniMaxTTS()
            self.assertEqual(client.api_key, "test-key")

    def test_explicit_key_overrides_env(self):
        with patch.dict(os.environ, {"MINIMAX_API_KEY": "env-key"}):
            client = MiniMaxTTS(api_key="explicit-key")
            self.assertEqual(client.api_key, "explicit-key")

    def test_default_model_is_hd(self):
        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            client = MiniMaxTTS()
            self.assertEqual(client.model, MINIMAX_TTS_MODEL_HD)

    def test_custom_model(self):
        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            client = MiniMaxTTS(model=MINIMAX_TTS_MODEL_TURBO)
            self.assertEqual(client.model, MINIMAX_TTS_MODEL_TURBO)


class TestMiniMaxTTSSynthesize(unittest.TestCase):
    """Test MiniMaxTTS.synthesize() with mocked HTTP and ffmpeg."""

    def _make_mock_response(self, audio_hex="68656c6c6f"):
        """Return a mock requests.Response with valid JSON body."""
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {
            "base_resp": {"status_code": 0, "status_msg": "success"},
            "data": {"audio": audio_hex},
        }
        return resp

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_calls_api_with_correct_payload(self, mock_post, mock_convert):
        mock_post.return_value = self._make_mock_response()
        mock_convert.return_value = None

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "test-key"}):
            client = MiniMaxTTS()
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            client.synthesize("Hello world", "English_Graceful_Lady", out)

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], minimax_tts.MINIMAX_API_URL)
        payload = kwargs["json"]
        self.assertEqual(payload["text"], "Hello world")
        self.assertEqual(payload["voice_setting"]["voice_id"], "English_Graceful_Lady")
        self.assertEqual(payload["audio_setting"]["format"], "mp3")

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_strips_minimax_prefix(self, mock_post, mock_convert):
        mock_post.return_value = self._make_mock_response()
        mock_convert.return_value = None

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            client = MiniMaxTTS()
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            client.synthesize("Hi", "minimax:English_Persuasive_Man", out)

        payload = mock_post.call_args[1]["json"]
        self.assertEqual(payload["voice_setting"]["voice_id"], "English_Persuasive_Man")

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_writes_mp3_bytes(self, mock_post, mock_convert):
        audio_hex = "68656c6c6f"  # b"hello"
        mock_post.return_value = self._make_mock_response(audio_hex)
        # Raise so the MP3 is NOT deleted by the cleanup code
        mock_convert.side_effect = RuntimeError("skip conversion")

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            client = MiniMaxTTS()
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            mp3 = out.replace(".wav", ".mp3")
            with self.assertRaises(RuntimeError):
                client.synthesize("Test", "Wise_Woman", out)
            # The MP3 should have been written before the convert call failed
            self.assertTrue(os.path.exists(mp3), "MP3 temp file was not written")
            with open(mp3, "rb") as f:
                self.assertEqual(f.read(), bytes.fromhex(audio_hex))

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_raises_on_api_error(self, mock_post, mock_convert):
        mock_post.return_value = MagicMock(
            raise_for_status=MagicMock(),
            json=MagicMock(return_value={
                "base_resp": {"status_code": 1000, "status_msg": "Invalid voice"},
                "data": {},
            }),
        )
        mock_convert.return_value = None

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            client = MiniMaxTTS()
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            with self.assertRaises(RuntimeError):
                client.synthesize("Hi", "bad_voice", out)

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_raises_on_empty_audio(self, mock_post, mock_convert):
        mock_post.return_value = MagicMock(
            raise_for_status=MagicMock(),
            json=MagicMock(return_value={
                "base_resp": {"status_code": 0, "status_msg": "success"},
                "data": {"audio": ""},
            }),
        )
        mock_convert.return_value = None

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            client = MiniMaxTTS()
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            with self.assertRaises(RuntimeError):
                client.synthesize("Hi", "Wise_Woman", out)

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_uses_bearer_auth(self, mock_post, mock_convert):
        mock_post.return_value = self._make_mock_response()
        mock_convert.return_value = None

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "my-secret"}):
            client = MiniMaxTTS()
        with tempfile.TemporaryDirectory() as td:
            client.synthesize("Hi", "cute_boy", os.path.join(td, "o.wav"))

        headers = mock_post.call_args[1]["headers"]
        self.assertEqual(headers["Authorization"], "Bearer my-secret")


class TestGetClient(unittest.TestCase):
    """Test the module-level get_client() singleton."""

    def setUp(self):
        # Reset the module-level singleton before each test
        minimax_tts._client = None

    def test_get_client_creates_instance(self):
        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            c = get_client()
        self.assertIsInstance(c, MiniMaxTTS)

    def test_get_client_same_model_returns_same_instance(self):
        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            c1 = get_client()
            c2 = get_client()
        self.assertIs(c1, c2)

    def test_get_client_different_model_creates_new_instance(self):
        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            c1 = get_client(MINIMAX_TTS_MODEL_HD)
            c2 = get_client(MINIMAX_TTS_MODEL_TURBO)
        self.assertIsNot(c1, c2)
        self.assertEqual(c2.model, MINIMAX_TTS_MODEL_TURBO)


class TestSynthesizeToFile(unittest.TestCase):
    """Test the top-level synthesize_to_file() helper."""

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_to_file_delegates(self, mock_post, mock_convert):
        minimax_tts._client = None
        mock_post.return_value = MagicMock(
            raise_for_status=MagicMock(),
            json=MagicMock(return_value={
                "base_resp": {"status_code": 0, "status_msg": "success"},
                "data": {"audio": "68656c6c6f"},
            }),
        )
        mock_convert.return_value = None

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            with tempfile.TemporaryDirectory() as td:
                out = os.path.join(td, "out.wav")
                synthesize_to_file("Hello", "minimax:lovely_girl", out)

        payload = mock_post.call_args[1]["json"]
        self.assertEqual(payload["voice_setting"]["voice_id"], "lovely_girl")

    @patch("minimax_tts._convert_mp3_to_wav")
    @patch("minimax_tts.requests.post")
    def test_synthesize_to_file_turbo_model(self, mock_post, mock_convert):
        minimax_tts._client = None
        mock_post.return_value = MagicMock(
            raise_for_status=MagicMock(),
            json=MagicMock(return_value={
                "base_resp": {"status_code": 0, "status_msg": "success"},
                "data": {"audio": "68656c6c6f"},
            }),
        )
        mock_convert.return_value = None

        with patch.dict(os.environ, {"MINIMAX_API_KEY": "k"}):
            with tempfile.TemporaryDirectory() as td:
                out = os.path.join(td, "out.wav")
                synthesize_to_file("Hello", "Deep_Voice_Man", out, model=MINIMAX_TTS_MODEL_TURBO)

        payload = mock_post.call_args[1]["json"]
        self.assertEqual(payload["model"], MINIMAX_TTS_MODEL_TURBO)


class TestConvertMp3ToWav(unittest.TestCase):
    """Test _convert_mp3_to_wav error handling."""

    @patch("minimax_tts.subprocess.run")
    def test_raises_on_nonzero_returncode(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr=b"error msg")
        with self.assertRaises(RuntimeError):
            minimax_tts._convert_mp3_to_wav("/tmp/in.mp3", "/tmp/out.wav")

    @patch("minimax_tts.subprocess.run")
    def test_no_raise_on_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr=b"")
        # Should not raise
        minimax_tts._convert_mp3_to_wav("/tmp/in.mp3", "/tmp/out.wav")


# ===========================================================================
# Integration tests – skipped unless MINIMAX_API_KEY is set
# ===========================================================================

@unittest.skipUnless(os.environ.get("MINIMAX_API_KEY"), "MINIMAX_API_KEY not set")
class TestMiniMaxTTSIntegration(unittest.TestCase):
    """Live API integration tests (require MINIMAX_API_KEY)."""

    def test_synthesize_english_graceful_lady(self):
        """HD model with a verified English voice should produce a non-empty WAV."""
        client = MiniMaxTTS()
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            client.synthesize("Hello, this is a test of the MiniMax TTS engine.", "English_Graceful_Lady", out)
            self.assertTrue(os.path.exists(out))
            self.assertGreater(os.path.getsize(out), 1000)

    def test_synthesize_turbo_model(self):
        """Turbo model should also work."""
        client = MiniMaxTTS(model=MINIMAX_TTS_MODEL_TURBO)
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            client.synthesize("Quick test.", "English_Persuasive_Man", out)
            self.assertTrue(os.path.exists(out))
            self.assertGreater(os.path.getsize(out), 1000)

    def test_synthesize_to_file_top_level(self):
        """synthesize_to_file() top-level helper works end-to-end."""
        minimax_tts._client = None
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out.wav")
            synthesize_to_file("VoxNovel integration test.", "minimax:Friendly_Person", out)
            self.assertTrue(os.path.exists(out))
            self.assertGreater(os.path.getsize(out), 1000)


if __name__ == "__main__":
    unittest.main()
