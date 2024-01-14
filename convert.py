import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

multi_voice_model1 ="tts_models/en/vctk/vits"

multi_voice_model_voice_list1 = TTS(multi_voice_model1).speakers

print(multi_voice_model_voice_list1)

# List available 🐸TTS models
print(TTS().list_models())

tts = TTS("tts_models/en/vctk/vits")
tts.tts_with_vc_to_file(
    "Imagine a world where endless poop is found around every corner.",
    speaker_wav="tortoise/voices/mol.F/1.wav",
    file_path="output.wav",
    speaker = "p363"
)
