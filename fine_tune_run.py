import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import time
def fineTune_audio_generate(text, file_path, speaker_wav, language, voice_actor):
    global current_model
    global tts
    start_time = time.time()  # Record the start time

    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Add here the xtts_config path
    CONFIG_PATH = f"tortoise/voices/{voice_actor}/model/config.json"
    # Add here the vocab file that you have used to train the model
    TOKENIZER_PATH = f"tortoise/voices/{voice_actor}/model/vocab.json_"
    # Add here the checkpoint that you want to do inference with
    XTTS_CHECKPOINT = f"tortoise/voices/{voice_actor}/model/model.pth"
    # Add here the speaker reference
    SPEAKER_REFERENCE = speaker_wav
    # output wav path
    OUTPUT_WAV_PATH = file_path


    if current_model !=  voice_actor:
        print(f"found fine tuned for voice actor: {voice_actor}: loading custom model...")
        config = XttsConfig()
        config.load_json(CONFIG_PATH)
        if 'tts' not in locals():
            tts = Xtts.init_from_config(config)
            tts.load_checkpoint(config, checkpoint_path=XTTS_CHECKPOINT, vocab_path=TOKENIZER_PATH, use_deepspeed=False)
        #make sure it runs on cpu or cuda depending on whats avalible on the machine
        if device == "cuda":
            tts.cuda()
        if device == "cpu":
            tts.cpu()
        current_model = voice_actor
    else:
        print(f"found fine tuned model for voice actor: {voice_actor} but {voice_actor} model is already loaded")

    print("Computing speaker latents...")
    gpt_cond_latent, speaker_embedding = tts.get_conditioning_latents(audio_path=[SPEAKER_REFERENCE])

    print("Inference...")
    out = tts.inference(
        text,
        language,
        gpt_cond_latent,
        speaker_embedding,
        temperature=0.7, # Add custom parameters here
    )
    torchaudio.save(OUTPUT_WAV_PATH, torch.tensor(out["wav"]).unsqueeze(0), 24000)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Time taken for execution: {elapsed_time:.2f} seconds")
current_model = ""
voice_actor = "morgan"
model = None
print("running test...")
fragment = "dang, I got fat fast."
if os.path.exists(f"tortoise/voices/{voice_actor}/model") and os.path.isdir(f"tortoise/voices/{voice_actor}/model"):
    fineTune_audio_generate(text=fragment, file_path=f"test.wav", speaker_wav=f"tortoise/voices/{voice_actor}/Morgan Freeman_00000051.wav", language="en", voice_actor = voice_actor)
    fineTune_audio_generate(text=fragment, file_path=f"test.wav", speaker_wav=f"tortoise/voices/{voice_actor}/Morgan Freeman_00000051.wav", language="en", voice_actor = voice_actor)

#tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=list_reference_files(voice_actor), language=language_code)
