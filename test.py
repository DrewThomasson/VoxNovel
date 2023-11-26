import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from epub2txt import epub2txt
from booknlp.booknlp import BookNLP
import nltk
nltk.download('averaged_perceptron_tagger')

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

    df_tokens = pd.read_csv(tokens_file, delimiter="\t", on_bad_lines='skip', quoting=3)

    
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
            #turn the new_row into a data frame 
            new_row_df = pd.DataFrame([new_row])
            # Concatenate 'writer' with 'new_row_df'
            writer = pd.concat([writer, new_row_df], ignore_index=True)

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
    df_tokens = pd.read_csv(tokens_file, delimiter="\t", on_bad_lines='skip', quoting=3)

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

