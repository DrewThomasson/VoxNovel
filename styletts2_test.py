import subprocess
import sys

# Function to install package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import the package
try:
    from styletts2 import tts
except ImportError:
    # If package is not found, install it
    print("styletts2 not found, installing now...")
    install("styletts2")
    # After installation, attempt to import again
    from styletts2 import tts

import time
from styletts2 import tts

# First block of code
start_time1 = time.time()

# No paths provided means default checkpoints/configs will be downloaded/cached.
my_tts = tts.StyleTTS2()
out = my_tts.inference("Hello there, I am now a python package.", output_wav_file="test.wav")

end_time1 = time.time()
elapsed_time1 = end_time1 - start_time1
print(f"The first code block took {elapsed_time1} seconds to run.")

# Second block of code
start_time2 = time.time()

# Specific paths to a checkpoint and config can also be provided.
other_tts = tts.StyleTTS2(model_checkpoint_path='/PATH/TO/epochs_2nd_00020.pth', config_path='/PATH/TO/config.yml')
other_tts.inference("Hello there, I am now a python package.", target_voice_path="/Users/admin/styletts2/test.wav", output_wav_file="another_test.wav")

end_time2 = time.time()
elapsed_time2 = end_time2 - start_time2
print(f"The second code block took {elapsed_time2} seconds to run.")

other_tts.inference("Hello there, I am now a python package.", target_voice_path="/Users/admin/test/VoxNovel/tortoise/voices/angie.F/1.wav", output_wav_file="another_test1.wav")
other_tts.inference("Hello there, I am now a python package.", target_voice_path="/Users/admin/test/VoxNovel/tortoise/voices/daniel.M/1.wav", output_wav_file="another_test2.wav")
other_tts.inference("Hello there, I am now a python package.", target_voice_path="/Users/admin/test/VoxNovel/tortoise/voices/tim_reynolds.M/1.mp3", output_wav_file="another_test3.wav")


