import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from epub2txt import epub2txt
from booknlp.booknlp import BookNLP

def calibre_installed():
    """Check if Calibre's ebook-convert tool is available."""
    try:
        subprocess.run(['ebook-convert', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("""ERROR NO CALIBRE: running epub2txt convert version...
It appears you dont have the calibre commandline tools installed on your,
This will allow you to convert from any ebook file format:
Calibre supports the following input formats: CBZ, CBR, CBC, CHM, EPUB, FB2, HTML, LIT, LRF, MOBI, ODT, PDF, PRC, PDB, PML, RB, RTF, SNB, TCR, TXT.

If you want this feature please follow online instruction for downloading the calibre commandline tool.

For Linux its: 
sudo apt update && sudo apt upgrade
sudo apt install calibre

""")
        return False

def convert_with_calibre(file_path, output_format="txt"):
    """Convert a file using Calibre's ebook-convert tool."""
    output_path = file_path.rsplit('.', 1)[0] + '.' + output_format
    subprocess.run(['ebook-convert', file_path, output_path])
    return output_path

def process_file():
    file_path = filedialog.askopenfilename(
        title='Select File',
        filetypes=[('Supported Files', 
                    ('*.cbz', '*.cbr', '*.cbc', '*.chm', '*.epub', '*.fb2', '*.html', '*.lit', '*.lrf', 
                     '*.mobi', '*.odt', '*.pdf', '*.prc', '*.pdb', '*.pml', '*.rb', '*.rtf', '*.snb', 
                     '*.tcr', '*.txt'))]
    )
    
    if not file_path:
        return

    if file_path.lower().endswith(('.cbz', '.cbr', '.cbc', '.chm', '.epub', '.fb2', '.html', '.lit', '.lrf', 
                                  '.mobi', '.odt', '.pdf', '.prc', '.pdb', '.pml', '.rb', '.rtf', '.snb', '.tcr')) and calibre_installed():
        file_path = convert_with_calibre(file_path)
    elif file_path.lower().endswith('.epub') and not calibre_installed():
        content = epub2txt(file_path)
        if not os.path.exists('Working_files'):
            os.makedirs('Working_files')
        file_path = os.path.join('Working_files', 'Book.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    elif not file_path.lower().endswith('.txt'):
        messagebox.showerror("Error", "Selected file format is not supported or Calibre is not installed.")
        return

    # Now process the TXT file with BookNLP
    book_id = "Book"
    output_directory = os.path.join('Working_files', book_id)

    model_params = {
        "pipeline": "entity,quote,supersense,event,coref",
        "model": "big"
    }

    booknlp = BookNLP("en", model_params)
    booknlp.process(file_path, output_directory, book_id)

    print("Success, File processed successfully!")
    
    # Close the GUI
    root.destroy()

root = tk.Tk()
root.title("BookNLP Processor")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

process_button = tk.Button(frame, text="Process File", command=process_file)
process_button.pack()

root.mainloop()





import pandas as pd

def filter_and_correct_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    corrected_lines = []
    
    # Filter out lines with mismatched quotes
    for line in lines:
        if line.count('"') % 2 == 0:
            corrected_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(corrected_lines)

    print(f"Processed {len(lines)} lines.")
    print(f"Removed {len(lines) - len(corrected_lines)} problematic lines.")
    print(f"Wrote {len(corrected_lines)} lines back to the file.")

if __name__ == "__main__":
    file_path = "Working_files/Book/Book.quotes"
    filter_and_correct_quotes(file_path)





import pandas as pd
import re
import glob
import os

def process_files(quotes_file, tokens_file):
    skip_rows = []
    while True:
        try:
            df_quotes = pd.read_csv(quotes_file, delimiter="\t", skiprows=skip_rows)
            break
        except pd.errors.ParserError as e:
            msg = str(e)
            match = re.search(r'at row (\d+)', msg)
            if match:
                problematic_row = int(match.group(1))
                print(f"Skipping problematic row {problematic_row} in {quotes_file}")
                skip_rows.append(problematic_row)
            else:
                print(f"Error reading {quotes_file}: {e}")
                return

    df_tokens = pd.read_csv(tokens_file, delimiter="\t", error_bad_lines=False, quoting=3)
    
    last_end_id = 0
    nonquotes_data = []

    for index, row in df_quotes.iterrows():
        start_id = row['quote_start']
        end_id = row['quote_end']
        
        filtered_tokens = df_tokens[(df_tokens['token_ID_within_document'] > last_end_id) & 
                                    (df_tokens['token_ID_within_document'] < start_id)]
        
        words_chunk = ' '.join([str(token_row['word']) for index, token_row in filtered_tokens.iterrows()])
        words_chunk = words_chunk.replace(" n't", "n't").replace(" n’", "n’").replace("( ", "(").replace(" ,", ",").replace("gon na", "gonna").replace(" n’t", "n’t")
        words_chunk = re.sub(r' (?=[^a-zA-Z0-9\s])', '', words_chunk)
        
        if words_chunk:
            nonquotes_data.append([words_chunk, last_end_id, start_id, "False", "Narrator"])
        
        last_end_id = end_id

    nonquotes_df = pd.DataFrame(nonquotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])
    output_filename = os.path.join(os.path.dirname(quotes_file), "non_quotes.csv")
    nonquotes_df.to_csv(output_filename, index=False)
    print(f"Saved nonquotes.csv to {output_filename}")

def main():
    quotes_files = glob.glob('Working_files/**/*.quotes', recursive=True)
    tokens_files = glob.glob('Working_files/**/*.tokens', recursive=True)

    for q_file in quotes_files:
        base_name = os.path.splitext(os.path.basename(q_file))[0]
        matching_token_files = [t_file for t_file in tokens_files if os.path.splitext(os.path.basename(t_file))[0] == base_name]

        if matching_token_files:
            process_files(q_file, matching_token_files[0])

    print("All processing complete!")

if __name__ == "__main__":
    main()














import pandas as pd
import re
import glob
import os
import nltk

def process_files(quotes_file, entities_file):
    # Load the files
    df_quotes = pd.read_csv(quotes_file, delimiter="\t")
    df_entities = pd.read_csv(entities_file, delimiter="\t")

    character_info = {}

    def is_pronoun(word):
        tagged_word = nltk.pos_tag([word])
        return 'PRP' in tagged_word[0][1] or 'PRP$' in tagged_word[0][1]

    def get_gender(pronoun):
        male_pronouns = ['he', 'him', 'his']
        female_pronouns = ['she', 'her', 'hers']

        if pronoun in male_pronouns:
            return 'Male'
        elif pronoun in female_pronouns:
            return 'Female'
        return 'Unknown'

    # Process the quotes dataframe
    for index, row in df_quotes.iterrows():
        char_id = row['char_id']
        mention = row['mention_phrase']

        # Initialize character info if not already present
        if char_id not in character_info:
            character_info[char_id] = {"names": {}, "pronouns": {}, "quote_count": 0}

        # Update names or pronouns based on the mention_phrase
        if is_pronoun(mention):
            character_info[char_id]["pronouns"].setdefault(mention.lower(), 0)
            character_info[char_id]["pronouns"][mention.lower()] += 1
        else:
            character_info[char_id]["names"].setdefault(mention, 0)
            character_info[char_id]["names"][mention] += 1

        character_info[char_id]["quote_count"] += 1

    # Process the entities dataframe
    for index, row in df_entities.iterrows():
        coref = row['COREF']
        name = row['text']

        if coref in character_info:
            if is_pronoun(name):
                character_info[coref]["pronouns"].setdefault(name.lower(), 0)
                character_info[coref]["pronouns"][name.lower()] += 1
            else:
                character_info[coref]["names"].setdefault(name, 0)
                character_info[coref]["names"][name] += 1

    # Extract the most likely name and gender for each character
    for char_id, info in character_info.items():
        most_likely_name = max(info["names"].items(), key=lambda x: x[1])[0] if info["names"] else "Unknown"
        most_common_pronoun = max(info["pronouns"].items(), key=lambda x: x[1])[0] if info["pronouns"] else None

        gender = get_gender(most_common_pronoun) if most_common_pronoun else 'Unknown'
        gender_suffix = ".M" if gender == 'Male' else ".F" if gender == 'Female' else ".?"

        info["formatted_speaker"] = f"{char_id}:{most_likely_name}{gender_suffix}"
        info["most_likely_name"] = most_likely_name
        info["gender"] = gender

    # Write the formatted data to quotes.csv
    output_filename = os.path.join(os.path.dirname(quotes_file), "quotes.csv")
    with open(output_filename, 'w', newline='') as outfile:
        fieldnames = ["Text", "Start Location", "End Location", "Is Quote", "Speaker"]
        writer = pd.DataFrame(columns=fieldnames)

        for index, row in df_quotes.iterrows():
            char_id = row['char_id']

            if not re.search('[a-zA-Z0-9]', row['quote']):
                print(f"Removing row with text: {row['quote']}")
                continue

            if character_info[char_id]["quote_count"] == 1:
                formatted_speaker = "Narrator"
            else:
                formatted_speaker = character_info[char_id]["formatted_speaker"] if char_id in character_info else "Unknown"

            new_row = {"Text": row['quote'], "Start Location": row['quote_start'], "End Location": row['quote_end'], "Is Quote": "True", "Speaker": formatted_speaker}
            writer = writer.append(new_row, ignore_index=True)

        writer.to_csv(output_filename, index=False)
        print(f"Saved quotes.csv to {output_filename}")

def main():
    # Use glob to get all .quotes and .entities files within the "Working_files" directory and its subdirectories
    quotes_files = glob.glob('Working_files/**/*.quotes', recursive=True)
    entities_files = glob.glob('Working_files/**/*.entities', recursive=True)

    # Pair and process .quotes and .entities files with matching filenames (excluding the extension)
    for q_file in quotes_files:
        base_name = os.path.splitext(os.path.basename(q_file))[0]
        matching_entities_files = [e_file for e_file in entities_files if os.path.splitext(os.path.basename(e_file))[0] == base_name]

        if matching_entities_files:
            process_files(q_file, matching_entities_files[0])

    print("All processing complete!")

if __name__ == "__main__":
    main()






import pandas as pd
import re
import glob
import os

def process_files(quotes_file, tokens_file):
    # Load the files
    df_quotes = pd.read_csv(quotes_file, delimiter="\t")
    df_tokens = pd.read_csv(tokens_file, delimiter="\t", error_bad_lines=False, quoting=3)

    last_end_id = 0  # Initialize the last_end_id to 0
    nonquotes_data = []  # List to hold data for nonquotes.csv

    # Iterate through the quotes dataframe
    for index, row in df_quotes.iterrows():
        start_id = row['quote_start']
        end_id = row['quote_end']
        
        # Get tokens between the end of the last quote and the start of the current quote
        filtered_tokens = df_tokens[(df_tokens['token_ID_within_document'] > last_end_id) & 
                                    (df_tokens['token_ID_within_document'] < start_id)]
        
        # Build the word chunk
        #words_chunk = ' '.join([token_row['word'] for index, token_row in filtered_tokens.iterrows()])
        words_chunk = ' '.join([str(token_row['word']) for index, token_row in filtered_tokens.iterrows()])
        words_chunk = words_chunk.replace(" n't", "n't").replace(" n’", "n’").replace(" ’", "’").replace(" ,", ",").replace(" .", ".").replace(" n’t", "n’t")
        words_chunk = re.sub(r' (?=[^a-zA-Z0-9\s])', '', words_chunk)
        
        # Append data to nonquotes_data if words_chunk is not empty
        if words_chunk:
            nonquotes_data.append([words_chunk, last_end_id, start_id, "False", "Narrator"])
        
        last_end_id = end_id  # Update the last_end_id to the end_id of the current quote

    # Create a DataFrame for non-quote data
    nonquotes_df = pd.DataFrame(nonquotes_data, columns=["Text", "Start Location", "End Location", "Is Quote", "Speaker"])

    # Write to nonquotes.csv
    output_filename = os.path.join(os.path.dirname(quotes_file), "non_quotes.csv")
    nonquotes_df.to_csv(output_filename, index=False)
    print(f"Saved nonquotes.csv to {output_filename}")

def main():
    # Use glob to get all .quotes and .tokens files within the "Working_files" directory and its subdirectories
    quotes_files = glob.glob('Working_files/**/*.quotes', recursive=True)
    tokens_files = glob.glob('Working_files/**/*.tokens', recursive=True)

    # Pair and process .quotes and .tokens files with matching filenames (excluding the extension)
    for q_file in quotes_files:
        base_name = os.path.splitext(os.path.basename(q_file))[0]
        matching_token_files = [t_file for t_file in tokens_files if os.path.splitext(os.path.basename(t_file))[0] == base_name]

        if matching_token_files:
            process_files(q_file, matching_token_files[0])

    print("All processing complete!")

if __name__ == "__main__":
    main()




import pandas as pd
import numpy as np

# Read the CSV files
quotes_df = pd.read_csv("Working_files/Book/quotes.csv")
non_quotes_df = pd.read_csv("Working_files/Book/non_quotes.csv")

# Concatenate the dataframes
combined_df = pd.concat([quotes_df, non_quotes_df], ignore_index=True)

# Convert 'None' to NaN
combined_df.replace('None', np.nan, inplace=True)

# Drop rows with NaN in 'Start Location'
combined_df.dropna(subset=['Start Location'], inplace=True)

# Convert the 'Start Location' column to integers
combined_df["Start Location"] = combined_df["Start Location"].astype(int)

# Sort by 'Start Location'
sorted_df = combined_df.sort_values(by="Start Location")

# Save to 'book.csv'
sorted_df.to_csv("Working_files/Book/book.csv", index=False)






#this is a clean up script to try to clean up the quotes.csv and non_quotes.csv files of any types formed by booknlp
import pandas as pd
import os
import re

def process_text(text):
    # Apply the rule to remove spaces before punctuation and other non-alphanumeric characters
    text = re.sub(r' (?=[^a-zA-Z0-9\s])', '', text)
    # Replace " n’t" with "n’t"
    text = text.replace(" n’t", "n’t").replace("[", "(").replace("]", ")").replace("gon na", "gonna").replace("—————–", "")
    return text

def process_file(filename):
    # Load the file
    df = pd.read_csv(filename)

    # Check if the "Text" column exists
    if "Text" in df.columns:
        # Apply the rules to the "Text" column
        df['Text'] = df['Text'].apply(lambda x: process_text(str(x)))
        
        # Save the processed data back to the file
        df.to_csv(filename, index=False)
        print(f"Processed and saved {filename}")
    else:
        print(f"Column 'Text' not found in {filename}")

def main():
    folder_path = "Working_files/Book/"
    files = ["non_quotes.csv", "quotes.csv", "book.csv"]

    for filename in files:
        full_path = os.path.join(folder_path, filename)
        if os.path.exists(full_path):
            process_file(full_path)
        else:
            print(f"File {filename} not found in {folder_path}")

if __name__ == "__main__":
    main()








#this will wipe the computer of any current audio clips from a previous session
import os

def wipe_folder(directory_path):
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist!")
        return

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it's a regular file (not a subdirectory)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

print("wiping any fast generated audio clips cache")
folder_path = "Working_files/generated_audio_clips/"
wipe_folder(folder_path)






import torch
from TTS.api import TTS

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import pandas as pd
import random
import os
import time

import os
import pandas as pd
import random
import shutil

import torch
import torchaudio
import time
import pygame
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

# Ensure that nltk punkt is downloaded
nltk.download('punkt', quiet=True)


demo_text = "Imagine a world where endless possibilities await around every corner."

# Load the CSV data
data = pd.read_csv("Working_files/Book/book.csv")

#voice actors folder
voice_actors_folder ="tortoise/voices/"
# Get the list of voice actors
voice_actors = [va for va in os.listdir(voice_actors_folder) if va != "cond_latent_example"]
male_voice_actors = [va for va in voice_actors if va.endswith(".M")]
female_voice_actors = [va for va in voice_actors if va.endswith(".F")]

# Dictionary to hold each character's selected language
character_languages = {}

models = TTS().list_models()
#selected_tts_model = 'tts_models/multilingual/multi-dataset/xtts_v2'
selected_tts_model = models[0]


# Map for speaker to voice actor
speaker_voice_map = {}
CHAPTER_KEYWORD = "CHAPTER"

multi_voice_model1 ="tts_models/en/vctk/vits"
multi_voice_model2 ="tts_models/en/vctk/fast_pitch"
multi_voice_model3 ="tts_models/ca/custom/vits"

multi_voice_model_voice_list1 =speakers_list = TTS(multi_voice_model1).speakers
multi_voice_model_voice_list2 =speakers_list = TTS(multi_voice_model2).speakers
multi_voice_model_voice_list3 =speakers_list = TTS(multi_voice_model3).speakers



def get_random_voice_for_speaker(speaker):
    selected_voice_actors = voice_actors  # default to all voice actors

    if speaker.endswith(".M") and male_voice_actors:    
        selected_voice_actors = male_voice_actors
    elif speaker.endswith(".F") and female_voice_actors:
        selected_voice_actors = female_voice_actors

    if not selected_voice_actors:  # If list is empty, default to all voice actors
        selected_voice_actors = voice_actors
        
    return random.choice(selected_voice_actors)
def ensure_output_folder():
    if not os.path.exists("Working_files/generated_audio_clips"):
        os.mkdir("Working_files/generated_audio_clips")
        
def ensure_temp_folder():
    if not os.path.exists("Working_files/temp"):
        os.mkdir("Working_files/temp")

def select_voices():
    random.seed(int(time.time()))
    ensure_output_folder()
    total_rows = len(data)

    for speaker in data['Speaker'].unique():
        random_voice = get_random_voice_for_speaker(speaker)
        speaker_voice_map[speaker] = random_voice

    for speaker, voice in speaker_voice_map.items():
        print(f"Selected voice for {speaker}: {voice}")
# Pre-select the voices before starting the GUI
select_voices()

# Main application window
root = tk.Tk()
root.title("coqui TTS GUI")
root.geometry("1200x800")

chapter_delimiter_var = tk.StringVar(value="CHAPTER")


# Dictionary to hold the comboboxes references
voice_comboboxes = {}

# Initialize the mixer module
pygame.mixer.init()

# This function is called when a voice actor is selected from the dropdown
def update_voice_actor(speaker):
    selected_voice_actor = voice_comboboxes[speaker].get()
    speaker_voice_map[speaker] = selected_voice_actor
    print(f"Updated voice for {speaker}: {selected_voice_actor}")

    # Get a random reference file for the selected voice actor
    reference_files = list_reference_files(selected_voice_actor)
    if reference_files:  # Check if there are any reference files
        random_file = random.choice(reference_files)
        try:
            # Stop any currently playing music or sound
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            if random_file.endswith('.mp3'):
                # Use the music module for mp3 files
                pygame.mixer.music.load(random_file)
                pygame.mixer.music.play()
            else:
                # Use the Sound class for wav files
                sound = pygame.mixer.Sound(random_file)
                sound.play()
        except Exception as e:
            print(f"Could not play the audio file: {e}")


# Function to split long strings into parts
def split_long_string(text, limit=250):
    if len(text) <= limit:
        return [text]
    
    # Split by commas
    parts = text.split(',')
    new_parts = []
    
    for part in parts:
        while len(part) > limit:
            # Split at the last space before the limit
            break_point = part.rfind(' ', 0, limit)
            if break_point == -1:  # If no space found, split at the limit
                break_point = limit
            new_parts.append(part[:break_point].strip())
            part = part[break_point:].strip()
        new_parts.append(part)
    
    return new_parts


def combine_wav_files(input_directory, output_directory, file_name):
    # Get a list of all .wav files in the specified input directory
    input_file_paths = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.endswith(".wav")]

    # Create an empty list to store the loaded audio tensors
    audio_tensors = []

    # Iterate through the input file paths and load each audio file
    for input_file_path in input_file_paths:
        waveform, sample_rate = torchaudio.load(input_file_path)
        audio_tensors.append(waveform)

    # Concatenate the audio tensors along the time axis (dimension 1)
    combined_audio = torch.cat(audio_tensors, dim=1)

    # Ensure that the output directory exists, create it if necessary
    os.makedirs(output_directory, exist_ok=True)

    # Specify the output file path
    output_file_path = os.path.join(output_directory, file_name)

    # Save the combined audio to the output file path
    torchaudio.save(output_file_path, combined_audio, sample_rate)

    print(f"Combined audio saved to {output_file_path}")

def wipe_folder(directory_path):
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist!")
        return

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it's a regular file (not a subdirectory)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


# List of available TTS models

tts_models = [
    #'tts_models/multilingual/multi-dataset/xtts_v2',
    # Add all other models here...
]
tts_models = TTS().list_models()

# Function to update the selected TTS model
def update_tts_model(event):
    global selected_tts_model
    selected_tts_model = tts_model_combobox.get()
    print(f"Selected TTS model: {selected_tts_model}")

# Frame for TTS Model Selection Dropdown
tts_model_selection_frame = ttk.LabelFrame(root, text="Select TTS Model")
tts_model_selection_frame.pack(fill="x", expand="yes", padx=10, pady=10)

# Create a dropdown for TTS model selection
tts_model_var = tk.StringVar()
tts_model_combobox = ttk.Combobox(tts_model_selection_frame, textvariable=tts_model_var, state="readonly")
multilingual_tts_models = [model for model in tts_models if "multi-dataset" in model]

# modelse to be removed because i found that they are multi speaker and not single speaker
models_to_remove = [multi_voice_model1, multi_voice_model2, multi_voice_model3]

# List comprehension to remove the unwatned models
multilingual_tts_models = [model for model in multilingual_tts_models if model not in models_to_remove]


tts_model_combobox['values'] = multilingual_tts_models
tts_model_combobox.set(selected_tts_model)  # Set default value
tts_model_combobox.bind("<<ComboboxSelected>>", update_tts_model)
tts_model_combobox.pack(side="top", fill="x", expand="yes")



def update_voice_comboboxes():
    if include_single_models_var.get():  # Checkbox is checked
        # your code snippet to include single voice models
        filtered_tts_models = [model for model in tts_models if "multi-dataset" not in model]
        combined_values = voice_actors + filtered_tts_models
        combined_values += multi_voice_model_voice_list1 + multi_voice_model_voice_list2 + multi_voice_model_voice_list3
    else:  # Checkbox is not checked
        # Just use the default voice actors without single voice models
        combined_values = voice_actors

    # Now update each combobox with the new combined_values
    for speaker, combobox in voice_comboboxes.items():
        combobox['values'] = combined_values
        combobox.set(speaker_voice_map[speaker])  # Reset to the currently selected voice actor


# Add this near the top of your script where other variables are defined
include_single_models_var = tk.BooleanVar(value=False)

# Add this in your GUI setup section, after initializing `root`
include_single_models_checkbox = ttk.Checkbutton(
    root,  # or another frame where you want the checkbox to appear
    text="Include fast Voice Models:(fast generate at cost of audio quality)",
    variable=include_single_models_var,
    onvalue=True,
    offvalue=False,
    command=update_voice_comboboxes  # This function will be defined later
)
include_single_models_checkbox.pack()  # Adjust layout options as needed


# Call this function once initially to set the correct values from the start
update_voice_comboboxes()




def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


#i want to gigv ethis the voice actor name and have it turn that into the full directory of the voice actor location, and then use that to grab all the files inside of that voice actoers folder
def list_reference_files(voice_actor):
	
    if voice_actor in multi_voice_model_voice_list1:
    	create_folder_if_not_exists(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}")
    	reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    	if len(reference_files)==0:
    		device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    		tts = TTS(multi_voice_model1, progress_bar=True).to(device)
    		tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}/demo.wav", speaker = voice_actor)
    		reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    		return reference_files
    	else:
    		return reference_files
    		
    		
    elif voice_actor in multi_voice_model_voice_list2:
    	create_folder_if_not_exists(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}")
    	reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    	if len(reference_files)==0:
    		device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    		tts = TTS(multi_voice_model2, progress_bar=True).to("cpu")
    		tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}/demo.wav", speaker = voice_actor)
    		reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    		return reference_files
    	else:
    		return reference_files

    		
    		
    elif voice_actor in multi_voice_model_voice_list3:
    	create_folder_if_not_exists(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}")
    	reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    	if len(reference_files)==0:
    		device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    		tts = TTS(multi_voice_model3, progress_bar=True).to(device)
    		tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}/demo.wav", speaker = voice_actor)
    		reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    		return reference_files
    	else:
    		return reference_files

    		
    		
    elif "tts_models" in voice_actor:
    	create_folder_if_not_exists("tortoise/_model_demo_voices")
    	create_folder_if_not_exists(f"tortoise/_model_demo_voices/{voice_actor}")
    	reference_files = [os.path.join(f"tortoise/_model_demo_voices/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    	if len(reference_files)==0:
    		device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    		tts = TTS(voice_actor, progress_bar=True).to(device)
    		tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{voice_actor}/demo.wav")
    		reference_files = [os.path.join(f"tortoise/_model_demo_voices/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{voice_actor}") if file.endswith((".wav", ".mp3"))]
    		return reference_files
    	else:
    		return reference_files
    		
    	

    single_voice_actor_folder = f"{voice_actors_folder}{voice_actor}/"
    # List all .wav and .mp3 files in the folder
    reference_files = [os.path.join(single_voice_actor_folder, file) for file in os.listdir(single_voice_actor_folder) if file.endswith((".wav", ".mp3"))]
    return reference_files



# List of language codes and their display names
languages = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
    'Italian': 'it', 'Portuguese': 'pt', 'Polish': 'pl', 'Turkish': 'tr',
    'Russian': 'ru', 'Dutch': 'nl', 'Czech': 'cs', 'Arabic': 'ar',
    'Chinese': 'zh-cn', 'Japanese': 'ja', 'Hungarian': 'hu', 'Korean': 'ko'
}

# Variable to hold the current language selection, default to English
current_language = 'en'




# Function to generate audio for the text
def generate_audio():
    # Get device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    ensure_temp_folder()

    # List available TTS models
    #print(TTS().list_models())

    # Initialize the TTS model and set the device
    #tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    # Update the model initialization to use the selected model
    tts = TTS(selected_tts_model, progress_bar=True).to(device)
    fast_tts = TTS(multi_voice_model1, progress_bar=True).to(device)
    
    
    
    
    
    random.seed(int(time.time()))
    ensure_output_folder()
    total_rows = len(data)

    chapter_num = 0
    for index, row in data.iterrows():
        update_progress(index, total_rows)  # Update progress based on the current index and total rows

        speaker = row['Speaker']
        text = row['Text']
        
        language_code = character_languages.get(speaker, current_language)  # Default to 'en' if not found

        if CHAPTER_KEYWORD in text.upper():
            chapter_num += 1
            print(f"chapter num: {chapter_num}")
            print(f"CHAPTER KEYWORD IS: {CHAPTER_KEYWORD}")

        voice_actor = speaker_voice_map[speaker]
        sentences = sent_tokenize(text)
        
        audio_tensors = []
        temp_count =0
        for sentence in sentences:
            fragments = split_long_string(sentence)
            for fragment in fragments:
                # Check if the selected model is multilingual
                if 'multilingual' in selected_tts_model:
                    language_code = character_languages.get(speaker, current_language)
                else:
                    language_code = None  # No language specification for non-multilingual models

                print(f"Voice actor: {voice_actor}, {current_language}")
                temp_count = temp_count +1
                # Use the model and language code to generate the audio
                #tts = TTS(model_name="tts_models/en/ek1/tacotron2", progress_bar=False).to(device)
                #tts.tts_to_file(fragment, speaker_wav=list_reference_files(voice_actor), progress_bar=True, file_path=f"Working_files/temp/{temp_count}.wav")
   
                
                
                #this will make it so that if your selecting a model as a voice actor name then itll initalize the voice actor name as the model
                if voice_actor in multi_voice_model_voice_list1:
                	print(f"{voice_actor} is a fast model voice: {multi_voice_model1}")
                	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                	fast_tts = TTS(multi_voice_model1, progress_bar=True).to(device)
                	fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
                elif voice_actor in multi_voice_model_voice_list2:
                	print(f"{voice_actor} is a fast model voice: {multi_voice_model2}")
                	fast_tts = TTS(multi_voice_model2, progress_bar=True).to("cpu")
                	fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
                elif voice_actor in multi_voice_model_voice_list3:
                	print(f"{voice_actor} is a fast model voice: {multi_voice_model3}")
                	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                	fast_tts = TTS(multi_voice_model3, progress_bar=True).to(device)
                	fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
                elif "tts_models" in voice_actor and "multi-dataset" not in voice_actor:
                	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                	fast_tts = TTS(voice_actor, progress_bar=True).to(device)
                	#selected_tts_model = voice_actor
                	
                	
                	print(f"Model for this character has been switched to: {voice_actor} by user")
                	tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav")
                	#else:
                	#	print(f"{voice_actor} is neither multi-dataset nor multilingual")
                	#	tts.tts_to_file(text=fragment,file_path=f"Working_files/temp/{temp_count}.wav")  # Assuming the tts_to_file function has default arguments for unspecified parameters
                
                # If the model contains both "multilingual" and "multi-dataset"
                if "multilingual" in selected_tts_model and "multi-dataset" in selected_tts_model:
                    try:
                        if "bark" in selected_tts_model:
                            print(f"{selected_tts_model} is bark so multilingual but has no language code")
                            #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                            #tts = TTS(selected_tts_model, progress_bar=True).to(device)
                            tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=list_reference_files(voice_actor))
                        else:
                            print(f"{selected_tts_model} is multi-dataset and multilingual")
                            #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                            #tts = TTS(selected_tts_model, progress_bar=True).to(device)
                            tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=list_reference_files(voice_actor), language=language_code)
                    except ValueError as e:
                        if str(e) == "Model is not multi-lingual but `language` is provided.":
                            print("Caught ValueError: Model is not multi-lingual. Ignoring the language parameter.")
                            #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                            #tts = TTS(selected_tts_model, progress_bar=True).to(device)
                            tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=list_reference_files(voice_actor))

                # If the model only contains "multilingual"
                elif "multilingual" in selected_tts_model:
                	print(f"{selected_tts_model} is multilingual")
                	#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                	#tts = TTS(selected_tts_model, progress_bar=True).to(device)
                	tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", language=language_code)

                # If the model only contains "multi-dataset"
                elif "multi-dataset" in selected_tts_model:
                	print(f"{selected_tts_model} is multi-dataset")
                	#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                	#tts = TTS(selected_tts_model, progress_bar=True).to(device)
                	tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav")

                # If the model contains neither "multilingual" nor "multi-dataset"
                else:
                	print(f"{selected_tts_model} is neither multi-dataset nor multilingual")
                	#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                	#tts = TTS(selected_tts_model, progress_bar=True).to(device)
                	tts.tts_to_file(text=fragment,file_path=f"Working_files/temp/{temp_count}.wav")  # Assuming the tts_to_file function has default arguments for unspecified parameters

                
                
                
        temp_input_directory = "Working_files/temp"  # Replace with the actual input directory path
        output_directory = "Working_files/generated_audio_clips"  # Replace with the desired output directory path
        combine_wav_files(temp_input_directory, output_directory, f"audio_{index}_{chapter_num}.wav")
        wipe_folder("Working_files/temp")
    root.destroy()






from functools import partial



# Function to update the progress bar
def update_progress(index, total):
    progress = (index + 1) / total * 100
    progress_var.set(progress)
    progress_label.config(text=f"{progress:.2f}% done ({index+1}/{total} rows)")
    root.update_idletasks()

    

# Function to create a scrollable frame
def create_scrollable_frame(parent):
    # Create a canvas and a scrollbar
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    
    # Create a frame inside the canvas
    scrollable_frame = ttk.Frame(canvas)
    
    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Bind the canvas to configure the scroll region
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    # Create a window inside the canvas for the scrollable frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return scrollable_frame

# Replace your existing voice_selection_frame setup with this
voice_selection_frame = ttk.LabelFrame(root, text="Character Voices")
voice_selection_frame.pack(fill="both", expand="yes", padx=10, pady=10)

# Create the scrollable frame inside the voice_selection_frame
scrollable_voice_selection_frame = create_scrollable_frame(voice_selection_frame)

# Now, instead of packing your comboboxes directly into voice_selection_frame,
# pack them into scrollable_voice_selection_frame.
for speaker in data['Speaker'].unique():
    speaker_label = ttk.Label(scrollable_voice_selection_frame, text=speaker)
    speaker_label.pack(side="top", fill="x", expand="yes")
    
    
    #this is to make it so that the avalibe voice to select from includes the single voice models
    filtered_tts_models = [model for model in tts_models if "multi-dataset" not in model]
    combined_values = voice_actors
    #combined_values = voice_actors + filtered_tts_models
    #combined_values = multi_voice_model_voice_list1 + multi_voice_model_voice_list2 + multi_voice_model_voice_list3
    
    longest_name_length = max(len(name) for name in combined_values)
    voice_combobox = ttk.Combobox(scrollable_voice_selection_frame, values=combined_values, state="readonly", width = longest_name_length )
    voice_combobox.set(speaker_voice_map[speaker])  # Set the current voice actor
    voice_combobox.pack(side="top", fill="x", expand="yes")
    voice_combobox.bind("<<ComboboxSelected>>", lambda event, speaker=speaker: update_voice_actor(speaker))

    voice_comboboxes[speaker] = voice_combobox
    
    # Create a dropdown for language selection for each character
    language_var = tk.StringVar()
    language_combobox = ttk.Combobox(voice_selection_frame, textvariable=language_var, state="readonly")
    language_combobox['values'] = list(languages.keys())  # Use the display names for the user
    language_combobox.set('English')  # Set default value
    language_combobox.pack(side="top", fill="x", expand="yes")
    
    # Update character_languages when a language is selected
    def on_language_selected(event, speaker=speaker, combobox=language_combobox):
        selected_language_key = combobox.get()
        selected_language = languages[selected_language_key]
        character_languages[speaker] = selected_language
        print(f"Language for {speaker} changed to {selected_language}")

    # Use partial to correctly capture the current speaker
    language_combobox.bind("<<ComboboxSelected>>", partial(on_language_selected, speaker=speaker))

    # Initialize each character's language preference to English
    character_languages[speaker] = 'en'
# ... the rest of your GUI setup ...


# Create a label for the entry
chapter_delimiter_label = ttk.Label(root, text="Chapter Delimiter:")
chapter_delimiter_label.pack()  # Adjust layout options as needed

# Create the Entry widget for chapter delimiter
chapter_delimiter_entry = ttk.Entry(root, textvariable=chapter_delimiter_var)
chapter_delimiter_entry.pack()  # Adjust layout options as needed

def update_chapter_keyword(*args):
    global CHAPTER_KEYWORD
    CHAPTER_KEYWORD = chapter_delimiter_var.get()

# Add a trace to call update_chapter_keyword whenever the value changes
chapter_delimiter_var.trace_add("write", update_chapter_keyword)


# Frame for Language Selection Dropdown
language_selection_frame = ttk.LabelFrame(root, text="Select TTS Language")
language_selection_frame.pack(fill="x", expand="yes", padx=10, pady=10)

# Create a dropdown for language selection
language_var = tk.StringVar()
language_combobox = ttk.Combobox(language_selection_frame, textvariable=language_var, state="readonly")
language_combobox['values'] = list(languages.keys())  # Use the display names for the user
language_combobox.set('English')  # Set default value

def on_language_selected(event):
    global current_language
    # Update the current_language variable based on selection
    current_language = languages[language_combobox.get()]
    print(f"current language updated to: {current_language}")

language_combobox.bind("<<ComboboxSelected>>", on_language_selected)
language_combobox.pack(side="top", fill="x", expand="yes")

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack()
progress_label = ttk.Label(root, text="0% done")
progress_label.pack()





# Display Text Section
text_display_frame = ttk.Frame(root)
text_display_frame.pack(expand=True, fill='both')

text_display = scrolledtext.ScrolledText(text_display_frame, height=10)
text_display.pack(expand=True, fill='both')

# Load and display the book content with colored speakers
def load_book():
    # Clear the current text
    text_display.delete('1.0', tk.END)

    # Generate a random color for each unique speaker and store it in a dictionary
    speakers = data['Speaker'].unique()
    speaker_colors = {speaker: "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for speaker in speakers}

    # Insert the text with tags for each speaker
    for index, row in data.iterrows():
        speaker = row['Speaker']
        text = row['Text']

        # Check if the speaker has an associated color
        speaker_color = speaker_colors[speaker]

        # Insert the speaker's name with the associated color
        text_display.insert(tk.END, f"{speaker}: ", speaker)
        
        # Insert the text
        text_display.insert(tk.END, f"{text}\n\n")

        # Configure the tag to change the foreground color
        text_display.tag_configure(speaker, foreground=speaker_color)


# Create a frame to contain the buttons
buttons_frame = ttk.Frame(root)
buttons_frame.pack(pady=10)

# Load Book Button
load_book_button = ttk.Button(buttons_frame, text="Load Book", command=load_book)
load_book_button.pack(side=tk.LEFT, padx=5)

# Generate Audio Button
generate_button = ttk.Button(buttons_frame, text="Generate Audio", command=lambda: threading.Thread(target=generate_audio).start())
generate_button.pack(side=tk.LEFT, padx=5)

root.mainloop()



import os
import pandas as pd
import torch
import torchaudio
import pygame

colors = ['#FFB6C1', '#ADD8E6', '#FFDAB9', '#98FB98', '#D8BFD8']
speaker_colors = {}
currently_playing = None
pygame.mixer.init()
INPUT_FOLDER = "Working_files/generated_audio_clips"
OUTPUT_FOLDER = "Final_combined_output_audio"
SILENCE_DURATION_MS = 780

def combine_audio_files(silence_duration_ms):
    folder_path = os.path.join(os.getcwd(), INPUT_FOLDER)
    files = sorted([f for f in os.listdir(folder_path) if f.startswith("audio_") and f.endswith(".wav")], 
                   key=lambda f: (int(f.split('_')[2].split('.')[0]), int(f.split('_')[1].split('.')[0])))
    
    chapter_files = {}
    for file in files:
        chapter_num = int(file.split('_')[2].split('.')[0])
        if chapter_num not in chapter_files:
            chapter_files[chapter_num] = []
        chapter_files[chapter_num].append(file)
    
    for chapter_num, chapter_file_list in chapter_files.items():
        combined_tensor = torch.Tensor()
        for index, file in enumerate(chapter_file_list):
            waveform, sample_rate = torchaudio.load(os.path.join(folder_path, file))
            channels = waveform.shape[0]
            silence_tensor = torch.zeros(channels, int(silence_duration_ms * sample_rate / 1000))
            combined_tensor = torch.cat([combined_tensor, waveform, silence_tensor], dim=1)
            print(f"Processing Chapter {chapter_num} - File {index + 1}/{len(chapter_file_list)}: {file}")

        if not os.path.exists(os.path.join(os.getcwd(), OUTPUT_FOLDER)):
            os.makedirs(os.path.join(os.getcwd(), OUTPUT_FOLDER))

        output_path = os.path.join(os.getcwd(), OUTPUT_FOLDER, f"combined_chapter_{chapter_num}.wav")
        torchaudio.save(output_path, combined_tensor, sample_rate)

    print("Combining audio files complete!")

combine_audio_files(SILENCE_DURATION_MS)




from moviepy.editor import *

def convert_wav_to_mp4(wav_filename, mp4_filename):
    audio = AudioFileClip(wav_filename)
    audio.write_audiofile(mp4_filename, codec='aac')

def convert_all_wav_to_mp4():
    output_dir = "Final_combined_output_audio"
    wav_files = [f for f in os.listdir(output_dir) if f.endswith('.wav')]

    for wav_file in wav_files:
        wav_filename = os.path.join(output_dir, wav_file)
        mp4_filename = os.path.join(output_dir, wav_file.replace('.wav', '.mp4'))
        convert_wav_to_mp4(wav_filename, mp4_filename)
        print(f"{wav_filename} has been converted to {mp4_filename}.")

convert_all_wav_to_mp4()




#this will clean up some space by deleting the wav files copys in the final generation folder
import os

# Define the path to the folder from which you want to remove .wav files
folder_path = 'Final_combined_output_audio'  # You need to replace this with the actual folder path

# Function to remove all .wav files from the given folder
def remove_wav_files(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.wav'):
            os.remove(os.path.join(folder, filename))
            print(f'Removed: {filename}')

# Run the function
remove_wav_files(folder_path)



