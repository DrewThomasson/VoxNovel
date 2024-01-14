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


'''thsi is way better make a dictionary of all of the modesl hat are fast in coqio to select from for the speaker value, for them
and the spaeker value will be None if it isnt a ulti voice one, whihc is most of them
BUT if it does then you can set it to seom voice within the three that do so that w=should make the if statment a lot shorter

so then you can just amke it 

make a disctonary of the speakers to set for each model witht eh rtules above

fast_voice_cloning_models= "get mdoels command"
fast_voice_cloning_models_dict= {}

if the model selected for voice cloning is one fo the fast ones then:

tts = TTS(model_selected)

target_speaker_wav = "drew.wav"

# First text to speech conversion
tts.tts_with_vc_to_file(
    "An adventure begins at the break of dawn.",
    speaker_wav=target_speaker_wav,
    file_path="output.wav",
    speaker = fast_voice_cloning_models_dict[model_selected] #this will make it select a specific voice in the dict assosicated witht hat model or just None 
    #speaker="p363"
)
'''
