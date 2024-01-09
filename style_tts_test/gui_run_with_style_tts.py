#this is code that will be used to turn numbers like 1,000 and in a txt file into 1000 go then booknlp doesnt make it weird and then when the numbers are generated it comes out fine
import re

def process_large_numbers_in_txt(file_path):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression to match numbers with commas
    pattern = r'\b\d{1,3}(,\d{3})+\b'

    # Remove commas in numerical sequences
    modified_content = re.sub(pattern, lambda m: m.group().replace(',', ''), content)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)

# Usage example
#file_path = 'test_1.txt'  # Replace with your actual file path
#process_large_numbers_in_txt(file_path)


#this code here will remove any blank text rows from the csv file
import pandas as pd

def remove_empty_text_rows(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Remove rows where the 'Text' column is empty or NaN
    data = data[data['Text'].notna() & (data['Text'] != '')]

    # Write the modified DataFrame back to the CSV file
    data.to_csv(csv_file, index=False)

    print(f"Rows with empty 'Text' column have been removed from {csv_file}")

# Example usage
#csv_file = 'path_to_your_csv_file.csv'  # Replace with your CSV file path
#remove_empty_text_rows(csv_file)



#this code here will split book.csv file by the custom weird chapter deliminator for amachines to see
import pandas as pd

def process_and_split_csv(file_path, split_string):
    def split_text(text, split_string, original_row):
        # Split the text at the specified string and find the index of the split
        split_index = text.find(split_string)
        parts = text.split(split_string)
        new_rows = []
        start_location = original_row['Start Location']

        for index, part in enumerate(parts):
            new_row = original_row.copy()
            if index == 0:
                new_row['Text'] = part
                new_row['End Location'] = start_location + split_index
            else:
                new_row['Text'] = split_string + part
                new_row['Start Location'] = start_location + split_index
                new_row['End Location'] = start_location + split_index + len(split_string) + len(part)
                split_index += len(split_string) + len(part)  # Update for the next part

            new_rows.append(new_row)

        return new_rows

    def process_csv(df, split_string):
        new_rows = []
        for _, row in df.iterrows():
            text = row['Text']
            if isinstance(text, str) and split_string in text:
                new_rows.extend(split_text(text, split_string, row))
            else:
                new_rows.append(row)
        return pd.DataFrame(new_rows)

    # Read the CSV file
    df = pd.read_csv(file_path)

    # Process the DataFrame
    new_df = process_csv(df, split_string)

    # Write the modified DataFrame back to the CSV file
    new_df.to_csv(file_path, index=False)

# Example usage
#file_path = 'Working_files/Book/book.csv'
#split_string = 'NEWCHAPTERABC'
#process_and_split_csv(file_path, split_string)





#this code right here isnt the book grabbing thing but its before to refrence in ordero to create the sepecial chapter labeled book thing with calibre idk some systems cant seem to get it so just in case but the next bit of code after this is the book grabbing code with booknlp 
import os
import subprocess
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import csv
import nltk

# Only run the main script if Value is True
def create_chapter_labeled_book(ebook_file_path):
    # Function to ensure the existence of a directory
    def ensure_directory(directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")

    ensure_directory('Working_files/Book')

    def convert_to_epub(input_path, output_path):
        # Convert the ebook to EPUB format using Calibre's ebook-convert
        try:
            subprocess.run(['ebook-convert', input_path, output_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while converting the eBook: {e}")
            return False
        return True

    def save_chapters_as_text(epub_path):
        # Create the directory if it doesn't exist
        directory = "Working_files/temp_ebook"
        ensure_directory(directory)

        # Open the EPUB file
        book = epub.read_epub(epub_path)

        previous_chapter_text = ''
        previous_filename = ''
        chapter_counter = 0

        # Iterate through the items in the EPUB file
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Use BeautifulSoup to parse HTML content
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text()

                # Check if the text is not empty
                if text.strip():
                    if len(text) < 2300 and previous_filename:
                        # Append text to the previous chapter if it's short
                        with open(previous_filename, 'a', encoding='utf-8') as file:
                            file.write('\n' + text)
                    else:
                        # Create a new chapter file and increment the counter
                        previous_filename = os.path.join(directory, f"chapter_{chapter_counter}.txt")
                        chapter_counter += 1
                        with open(previous_filename, 'w', encoding='utf-8') as file:
                            file.write(text)
                            print(f"Saved chapter: {previous_filename}")

    # Example usage
    input_ebook = ebook_file_path  # Replace with your eBook file path
    output_epub = 'Working_files/temp.epub'

    if os.path.exists(output_epub):
        os.remove(output_epub)
        print(f"File {output_epub} has been removed.")
    else:
        print(f"The file {output_epub} does not exist.")

    if convert_to_epub(input_ebook, output_epub):
        save_chapters_as_text(output_epub)

    # Download the necessary NLTK data (if not already present)
    nltk.download('punkt')
    """
    def process_chapter_files(folder_path, output_csv):
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['Text', 'Start Location', 'End Location', 'Is Quote', 'Speaker', 'Chapter'])

            # Process each chapter file
            chapter_files = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1].split('.')[0]))
            for filename in chapter_files:
                if filename.startswith('chapter_') and filename.endswith('.txt'):
                    chapter_number = int(filename.split('_')[1].split('.')[0])
                    file_path = os.path.join(folder_path, filename)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()
                            sentences = nltk.tokenize.sent_tokenize(text)
                            for sentence in sentences:
                                start_location = text.find(sentence)
                                end_location = start_location + len(sentence)
                                writer.writerow([sentence, start_location, end_location, 'True', 'Narrator', chapter_number])
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
    """

    
    def process_chapter_files(folder_path, output_csv):
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['Text', 'Start Location', 'End Location', 'Is Quote', 'Speaker', 'Chapter'])

            # Process each chapter file
            chapter_files = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1].split('.')[0]))
            for filename in chapter_files:
                if filename.startswith('chapter_') and filename.endswith('.txt'):
                    chapter_number = int(filename.split('_')[1].split('.')[0])
                    file_path = os.path.join(folder_path, filename)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()
                            # Insert "NEWCHAPTERABC" at the beginning of each chapter's text
                            if text:
                                text = "NEWCHAPTERABC" + text
                            sentences = nltk.tokenize.sent_tokenize(text)
                            for sentence in sentences:
                                start_location = text.find(sentence)
                                end_location = start_location + len(sentence)
                                writer.writerow([sentence, start_location, end_location, 'True', 'Narrator', chapter_number])
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")

    # Example usage
    folder_path = "Working_files/temp_ebook"  # Replace with your folder path
    output_csv = 'Working_files/Book/Other_book.csv'
    process_chapter_files(folder_path, output_csv)

    def wipe_folder(folder_path):
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder {folder_path} does not exist.")
            return

        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if it's a file and not a directory
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}. Reason: {e}")
            else:
                print(f"Skipping directory: {file_path}")

    # Example usage
    # folder_to_wipe = 'Working_files/temp_ebook'  # Replace with the path to your folder
    # wipe_folder(folder_to_wipe)

    def sort_key(filename):
        """Extract chapter number for sorting."""
        match = re.search(r'chapter_(\d+)\.txt', filename)
        return int(match.group(1)) if match else 0

    def combine_chapters(input_folder, output_file):
        # Create the output folder if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # List all txt files and sort them by chapter number
        files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
        sorted_files = sorted(files, key=sort_key)

        with open(output_file, 'w') as outfile:
            for i, filename in enumerate(sorted_files):
                with open(os.path.join(input_folder, filename), 'r') as infile:
                    outfile.write(infile.read())
                    # Add the marker unless it's the last file
                    if i < len(sorted_files) - 1:
                        outfile.write("\nNEWCHAPTERABC\n")

    # Paths
    input_folder = 'Working_files/temp_ebook'
    output_file = 'Working_files/Book/Chapter_Book.txt'

    # Combine the chapters
    combine_chapters(input_folder, output_file)

    ensure_directory('Working_files/Book')

#create_chapter_labeled_book()
























#this is the Booknlp book grabber code
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from epub2txt import epub2txt
from booknlp.booknlp import BookNLP
import nltk
import re
nltk.download('averaged_perceptron_tagger')

epub_file_path = ""
chapters = []
ebook_file_path = ""
input_file_is_txt = False
def convert_epub_and_extract_chapters(epub_path):
    # Regular expression to match the chapter lines in the output
    chapter_pattern = re.compile(r'Detected chapter: \* (.*)')

    # List to store the extracted chapter names
    chapter_names = []

    # Start the conversion process and capture the output
    process = subprocess.Popen(['ebook-convert', epub_path, '/dev/null'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)

    # Read the output line by line
    for line in iter(process.stdout.readline, ''):
        print(line, end='')  # You can comment this out if you don't want to see the output
        match = chapter_pattern.search(line)
        if match:
            chapter_names.append(match.group(1))

    # Wait for the process to finish
    process.stdout.close()
    process.wait()

    return chapter_names

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
    global epub_file_path
    global ebook_file_path
    global input_file_is_txt
    file_path = filedialog.askopenfilename(
        title='Select File',
        filetypes=[('Supported Files', 
                    ('*.cbz', '*.cbr', '*.cbc', '*.chm', '*.epub', '*.fb2', '*.html', '*.lit', '*.lrf', 
                     '*.mobi', '*.odt', '*.pdf', '*.prc', '*.pdb', '*.pml', '*.rb', '*.rtf', '*.snb', 
                     '*.tcr', '*.txt'))]
    )
    ebook_file_path = file_path
    if ".epub" in file_path.lower():
        epub_file_path = file_path
    if ".txt" in file_path.lower():
        input_file_is_txt = True
    
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




    #this will turn stuff like 1,000 and 18,000 into 1000 and 18000 so booknlp doesnt mess them up with tokenization
    process_large_numbers_in_txt(file_path)
    booknlp = BookNLP("en", model_params)
    

    if calibre_installed():
        global filepath
        create_chapter_labeled_book(file_path)
        booknlp.process('Working_files/Book/Chapter_Book.txt', output_directory, book_id)
        #only delete the txt file if the input file isnt a txt file else then youll be deleting the original input file
        if input_file_is_txt != True:
            os.remove(file_path)
            print(f"deleted file: {file_path} because its not needed anymore after the ebook convertsion to txt")
    else:
        booknlp.process(file_path, output_directory, book_id)
        #os.remove(file_path)
        #print(f"deleted file: {file_path}")
    global chapters
    if epub_file_path == "":
        chapters = convert_epub_and_extract_chapters(epub_file_path)
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






#if booknlp came up with nothing then just use the other_book.csv file thank god i still have that code
import os
import tkinter as tk
from tkinter import messagebox

def is_single_line_file(filename):
    with open(filename, 'r') as file:
        return len(file.readlines()) <= 1

def copy_if_single_line(source_file, destination_file):
    if not os.path.isfile(source_file):
        return f"The source file '{source_file}' does not exist."
    elif is_single_line_file(destination_file):
        with open(source_file, 'r') as source:
            content = source.read()

        with open(destination_file, 'w') as dest:
            dest.write(content)

        # Popup message
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Notification", "The 'book.csv' file was found to be empty, so all lines in the book will be said by the narrator.")
        root.destroy()

        return f"File '{destination_file}' had only one line or was empty and has been filled with the contents of '{source_file}'."
    else:
        return f"File '{destination_file}' had more than one line, and no action was taken."

source_file = 'Working_files/Book/Other_book.csv'
destination_file = 'Working_files/Book/book.csv'

result = copy_if_single_line(source_file, destination_file)
print(result)







#this is a clean up script to try to clean up the quotes.csv and non_quotes.csv files of any types formed by booknlp
import pandas as pd
import os
import re

def process_text(text):
    # Apply the rule to remove spaces before punctuation and other non-alphanumeric characters
    text = re.sub(r' (?=[^a-zA-Z0-9\s])', '', text)
    # Replace " n’t" with "n’t"
    text = text.replace(" n’t", "n’t").replace("[", "(").replace("]", ")").replace("gon na", "gonna").replace("—————–", "").replace(" n't", "n't")
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

#this code here will split the bookcsv file by the calibre chapter deliminators such if calibre is installed
if calibre_installed():
    process_and_split_csv("Working_files/Book/book.csv", 'NEWCHAPTERABC')
remove_empty_text_rows("Working_files/Book/book.csv")




#this will wipe the computer of any current audio clips from a previous session
#but itll ask the user first
import os
import tkinter as tk
from tkinter import messagebox

def check_and_wipe_folder(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist!")
        return

    # Check for .wav files in the directory
    wav_files = [f for f in os.listdir(directory_path) if f.endswith('.wav')]

    if wav_files:  # If there are .wav files
        # Initialize tkinter
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Ask the user if they want to delete the files
        response = messagebox.askyesno("Confirm Deletion", "Audio clips from a previous session have been found. Do you want to wipe them?")
        root.destroy()  # Destroy the tkinter instance

        if response:  # If the user clicks 'Yes'
            # Iterate through files and delete them
            for filename in wav_files:
                file_path = os.path.join(directory_path, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
        else:
            print("Wipe operation cancelled by the user.")
    else:
        print("No audio clips from a previous session were found.")

# Usage
check_and_wipe_folder("Working_files/generated_audio_clips/")



from TTS.api import TTS

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog, filedialog
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
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
nltk.download('punkt')

# Ensure that nltk punkt is downloaded
nltk.download('punkt', quiet=True)


demo_text = "Imagine a world where endless possibilities await around every corner."

# Load the CSV data
csv_file="Working_files/Book/book.csv"
data = pd.read_csv(csv_file)

#voice actors folder
voice_actors_folder ="tortoise/voices/"
# Get the list of voice actors
voice_actors = [va for va in os.listdir(voice_actors_folder) if va != "cond_latent_example"]
male_voice_actors = [va for va in voice_actors if va.endswith(".M")]
female_voice_actors = [va for va in voice_actors if va.endswith(".F")]
SILENCE_DURATION_MS = 750
# Dictionary to hold each character's selected language
character_languages = {}

models = TTS().list_models()
#selected_tts_model = 'tts_models/multilingual/multi-dataset/xtts_v2'

#I have to do this right now cause they made a weird change to coqui idk super weird the list models isnt working right now
#so this will chekc if its a list isk man and if not then the bug is still there and itll apply the fix

if isinstance(models, list):
    print("good it's a list I can apply normal code for model list")
    selected_tts_model = models[0]
else:
    tts_manager = TTS().list_models()
    all_models = tts_manager.list_models()
    models = all_models
    selected_tts_model = models[0]


# Map for speaker to voice actor
speaker_voice_map = {}
CHAPTER_KEYWORD = "CHAPTER"

multi_voice_model1 ="tts_models/en/vctk/vits"
multi_voice_model2 ="tts_models/en/vctk/fast_pitch"
multi_voice_model3 ="tts_models/ca/custom/vits"

#multi_voice_model_voice_list1 =speakers_list = TTS(multi_voice_model1).speakers
#multi_voice_model_voice_list2 =speakers_list = TTS(multi_voice_model2).speakers
#multi_voice_model_voice_list3 =speakers_list = TTS(multi_voice_model3).speakers
multi_voice_model_voice_list1 = []
multi_voice_model_voice_list2 = []
multi_voice_model_voice_list3 = []

# Dictionary to hold the comboboxes references
voice_comboboxes = {}



def on_silence_duration_change(*args):
    """
    Update the SILENCE_DURATION_MS based on the entry value.
    """
    global SILENCE_DURATION_MS
    try:
        new_duration = int(silence_duration_var.get())
        if new_duration >= 0:
            SILENCE_DURATION_MS = new_duration
            print(f"SILENCE_DURATION_MS changed to: {SILENCE_DURATION_MS}")
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid non-negative integer.")

def validate_integer(P):
    """
    Validate if the entry is an integer.
    """
    if P.isdigit() or P == "":
        return True
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid integer.")
        return False

def update_silence_duration():
    """
    Update the SILENCE_DURATION_MS based on the entry value.
    """
    global SILENCE_DURATION_MS
    try:
        SILENCE_DURATION_MS = int(silence_duration_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer.")



def add_languages_to_csv():
    df = pd.read_csv('Working_files/Book/book.csv')  # Make sure to use your actual CSV file path
    if 'language' not in df.columns:
        # Map the 'Speaker' column to the 'language' column using the character_languages dictionary
        # The get method returns 'en' as a default value if the speaker is not found in the dictionary
        df['language'] = df['Speaker'].apply(lambda speaker: character_languages.get(speaker, 'en'))
    df.to_csv('Working_files/Book/book.csv', index=False)  # Save the changes back to the CSV file
    print("Added language data to the CSV file.")



def add_voice_actors_to_csv():
    df = pd.read_csv(csv_file)
    if 'voice_actor' not in df.columns:
        df['voice_actor'] = df['Speaker'].map(speaker_voice_map)
    df.to_csv(csv_file, index=False)
    print(f"Added voice actor data to {csv_file}")

def get_random_voice_for_speaker(speaker):
    selected_voice_actors = voice_actors  # default to all voice actors

    if speaker.endswith(".M") and male_voice_actors:    
        selected_voice_actors = male_voice_actors
    elif speaker.endswith(".F") and female_voice_actors:
        selected_voice_actors = female_voice_actors

    if not selected_voice_actors:  # If list is empty, default to all voice actors
        selected_voice_actors = voice_actors
        
    return random.choice(selected_voice_actors)
    
def get_random_voice_for_speaker_fast(speaker):
    selected_voice_actors = voice_actors  # default to all voice actors
    male_voice_actors = {"p226", "p228","p229","p230","p231","p232","p233","p234","p236","p238","p239","p241","p251","p252","p253","p254","p255","p256","p258","p262","p264","p265","p266","p267","p269","p272","p279","p281","p282","p285","p286","p287","p292","p298","p299","p301","p302","p307","p312","p313","p317","p318","p326","p340"}
    female_voice_actors = {"p225","p227","p237","p240","p243","p244","p245","p246","p247","p248","p249","p250","p257","p259","p260","p261","p263","p268","p270","p271","p273","p274","p275","p276","p277","p280","p283","p284","p288","p293","p294","p295","p297","p300","p303","p304","p305","p306","p308","p310","p311","p314","p316","p323","p329","p341","p343","p345","p347","p351","p360","p361","p362","p363","p364","p374"}

    if speaker.endswith(".M") and male_voice_actors: 
        selected_voice_actors = male_voice_actors
    elif speaker.endswith(".F") and female_voice_actors:
        selected_voice_actors = female_voice_actors
    elif speaker.endswith(".?") and female_voice_actors:
        selected_voice_actors = male_voice_actors.union(female_voice_actors)
    if not selected_voice_actors:  # If list is empty, default to all voice actors
        selected_voice_actors = male_voice_actors.union(female_voice_actors)
    
    # Convert the set to a list before using random.choice
    return random.choice(list(selected_voice_actors))

    
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
        # Update the comboboxes if they exist
        if speaker in voice_comboboxes:
            random_voice = get_random_voice_for_speaker(speaker)
            voice_comboboxes[speaker].set(random_voice)
    print("Voices have been selected randomly.")
 
def select_voices_fast():
    random.seed(int(time.time()))
    ensure_output_folder()
    total_rows = len(data)

    for speaker in data['Speaker'].unique():
        random_voice = get_random_voice_for_speaker_fast(speaker)
        speaker_voice_map[speaker] = random_voice

    for speaker, voice in speaker_voice_map.items():
        print(f"Selected voice for {speaker}: {voice}")
        # Update the comboboxes if they exist
        if speaker in voice_comboboxes:
            random_voice = get_random_voice_for_speaker_fast(speaker)
            voice_comboboxes[speaker].set(random_voice)
    print("Voices have been selected randomly.")
 
 
# Pre-select the voices before starting the GUI
select_voices()

# Main application window
root = tk.Tk()
root.title("coqui TTS GUI")
root.geometry("1200x800")
if calibre_installed():
    chapter_delimiter_var = tk.StringVar(value="NEWCHAPTERABC")
else:
    chapter_delimiter_var = tk.StringVar(value="CHAPTER")

def disable_chapter_delimiter_entry():
    chapter_delimiter_entry.config(state='disabled')

def enable_chapter_delimiter_entry():
    chapter_delimiter_entry.config(state='normal')

# Initialize the mixer module
try:
    pygame.mixer.init()
    print("mixer modual initialized successfully.")
except pygame.error:
    print("mixer modual initialization failed")
    print(pygame.error)

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

    # Sort the file paths to ensure numerical order
    input_file_paths.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    # Create an empty list to store the loaded audio tensors
    audio_tensors = []

    # Iterate through the sorted input file paths and load each audio file
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


#This is another coqui bug fix i have to apply for the bug idk why but nwo there this lol it started in coqui V0.22.0
#this will make the models list actually work tho
if isinstance(tts_models, list):
    print("good it's a list I can apply normal code for model list")
    selected_tts_model = models[0]
else:
    tts_manager = TTS().list_models()
    all_models = tts_manager.list_models()
    tts_models = all_models



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
multilingual_tts_models.append('StyleTTS2')

# modelse to be removed because i found that they are multi speaker and not single speaker
models_to_remove = [multi_voice_model1, multi_voice_model2, multi_voice_model3]

# List comprehension to remove the unwatned models
multilingual_tts_models = [model for model in multilingual_tts_models if model not in models_to_remove]


tts_model_combobox['values'] = multilingual_tts_models
tts_model_combobox.set(selected_tts_model)  # Set default value
tts_model_combobox.bind("<<ComboboxSelected>>", update_tts_model)
tts_model_combobox.pack(side="top", fill="x", expand="yes")

# Declare the button as global to access it in other functions
global select_voices_button

def update_voice_comboboxes():
    global multi_voice_model_voice_list1
    global multi_voice_model_voice_list2
    global multi_voice_model_voice_list3
    global voice_actors
    global female_voice_actors
    global male_voice_actors
    #updating the values of the avalible voice actors too
    voice_actors = [va for va in os.listdir(voice_actors_folder) if va != "cond_latent_example"]
    male_voice_actors = [va for va in voice_actors if va.endswith(".M")]
    female_voice_actors = [va for va in voice_actors if va.endswith(".F")]

    if include_single_models_var.get():  # Checkbox is checked
        # your code snippet to include single voice models
        filtered_tts_models = [model for model in tts_models if "multi-dataset" not in model]
        if not multi_voice_model_voice_list1:  # This is True if the list is empty
            print(f"{multi_voice_model_voice_list1} is empty populating it...")
            multi_voice_model_voice_list1 = TTS(multi_voice_model1).speakers
        if not multi_voice_model_voice_list2:  # This is True if the list is empty
            print(f"{multi_voice_model_voice_list2} is empty populating it...")
            multi_voice_model_voice_list2 = TTS(multi_voice_model2).speakers
        if not multi_voice_model_voice_list3:  # This is True if the list is empty
            print(f"{multi_voice_model_voice_list3} is empty populating it...")
            multi_voice_model_voice_list3 = TTS(multi_voice_model3).speakers
            

        combined_values = voice_actors + filtered_tts_models
        combined_values += multi_voice_model_voice_list1 + multi_voice_model_voice_list2 + multi_voice_model_voice_list3
        #this will remove unwatned models from the model list, thats cause these three are multi-speaker so im already including them as their voices
        combined_values.remove(multi_voice_model1)
        combined_values.remove(multi_voice_model2)
        combined_values.remove(multi_voice_model3)
    else:  # Checkbox is not checked
        # Just use the default voice actors without single voice models
        combined_values = voice_actors

    # Now update each combobox with the new combined_values
    for speaker, combobox in voice_comboboxes.items():
        combobox['values'] = combined_values
        combobox.set(speaker_voice_map[speaker])  # Reset to the currently selected voice actor
        longest_string_length = max((len(str(value)) for value in combobox['values']), default=0)
        combobox.config(width=longest_string_length)
        
    # Check the state of the checkbox and manage the visibility of the button
    if include_single_models_var.get():  # Checkbox is checked
        # Create the button if it doesn't exist
        if 'select_voices_button' not in globals():
            global select_voices_button
            select_voices_button = ttk.Button(buttons_frame, text="Select Random Voices", command=select_voices_fast)
            select_voices_button.pack(side=tk.LEFT, padx=5)
        else:
            select_voices_button.pack(side=tk.LEFT, padx=5)
    else:
            # Hide the button if the checkbox is unchecked
            if 'select_voices_button' in globals():
                select_voices_button.pack_forget()


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


#single voice checkbox var
single_voice_checkbox_var = tk.BooleanVar(value=False)  # Initially set to False


single_voice_checkbox = ttk.Checkbutton(
    root,  # Assuming 'root' is your main Tk window
    text="Make all audio generate with Narrerator voice",
    variable=single_voice_checkbox_var,
    onvalue=True,
    offvalue=False
)
single_voice_checkbox.pack()  # Adjust layout options as needed



# Call this function once initially to set the correct values from the start
update_voice_comboboxes()


# Function to clone a new voice
def clone_voice():
    # Prompt the user to enter the name of the new voice actor
    voice_actor_name = simpledialog.askstring("Input", "Enter the name of the voice actor:", parent=root)
    
    # If a name was entered, proceed to ask for gender
    if voice_actor_name:
        # Create a small popup window for gender selection
        gender_window = tk.Toplevel(root)
        gender_window.title("Select Gender")
        
        # Dropdown for gender selection
        gender_var = tk.StringVar(gender_window)
        gender_options = ['M', 'F', '?']
        gender_dropdown = ttk.Combobox(gender_window, textvariable=gender_var, values=gender_options, state='readonly')
        gender_dropdown.pack()


        # Function to be called when 'OK' button is pressed
        def on_gender_select():
            voice_actor_gender = gender_var.get()
            gender_window.destroy()  # Close the popup window
            
            # Now proceed to file selection
            file_path = filedialog.askopenfilename(
                title="Select Voice Sample File",
                filetypes=[("Audio Files", "*.mp3 *.wav *.mp4")],
                parent=root
            )
            
            # Check if the file is selected and is of the correct format
            if file_path and (file_path.lower().endswith('.mp3') or file_path.lower().endswith('.wav') or file_path.lower().endswith('.mp4')):
                # Create the directory path for the new voice actor
                new_voice_path = f"tortoise/voices/{voice_actor_name}.{voice_actor_gender}"
                
                # Check if the directory already exists
                if not os.path.exists(new_voice_path):
                    # Create the directory
                    os.makedirs(new_voice_path)
                    # Copy the selected file to the new directory
                    shutil.copy(file_path, new_voice_path)
                    messagebox.showinfo("Success", f"New voice actor folder created with sample file: {new_voice_path}")
                    update_voice_comboboxes()
                else:
                    messagebox.showerror("Error", "Voice actor folder already exists.")
            else:
                messagebox.showerror("Error", "No file selected or selected file is not an MP3, WAV, or MP4.")

        # OK button for gender selection
        ok_button = ttk.Button(gender_window, text="OK", command=on_gender_select)
        ok_button.pack()

        # Set the focus on the dropdown and wait for the user to make a selection
        gender_dropdown.focus_set()
        root.wait_window(gender_window)
    else:
        messagebox.showerror("Error", "No name entered for the voice actor.")

# Add this near the top of your script where other variables are defined
clone_voice_button = ttk.Button(
    root,
    text="Clone new voice",
    command=clone_voice  # The function to execute when the button is clicked
)

# Add the new button to the GUI
clone_voice_button.pack(padx=5)


#this will add a button that will let you give a voice actor a specific fine tuned model for xtts which you already fine tuned of course
import os
import shutil
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox

def list_folders(directory):
    """List all folders in the given directory."""
    return [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

def copy_files_to_model(source_folder, model_path):
    """Copy files from the selected folder to the model folder."""
    for file in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file)
        destination_file = os.path.join(model_path, file)
        shutil.copy2(source_file, destination_file)  # copy2 to preserve metadata

def start_process():
    base_directory = "tortoise/voices/"
    folders = list_folders(base_directory)

    def on_select(evt):
        selected_folder = folder_listbox.get(folder_listbox.curselection())

        # Create "model" folder if it doesn't exist
        model_path = os.path.join(base_directory, selected_folder, "model")
        if not os.path.exists(model_path):
            os.makedirs(model_path)

        # Select folder to copy files from
        source_folder = filedialog.askdirectory(title="Select folder containing fine tuned xtts model files to copy from:")
        if source_folder:
            copy_files_to_model(source_folder, model_path)
            messagebox.showinfo("Success", f"Files copied successfully to {model_path}")
        selection_window.destroy()

    # Create a new window for folder selection
    selection_window = tk.Toplevel(root)
    selection_window.title("Select a voice actor to add fine tuned model to:")

    folder_listbox = Listbox(selection_window)
    folder_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for folder in folders:
        folder_listbox.insert(tk.END, folder)

    folder_listbox.bind('<<ListboxSelect>>', on_select)

# Assuming 'root' is your existing Tkinter root window
# Add a start button to your existing GUI
start_button = tk.Button(root, text="Add Fine Tuned Xtts model to voice actor", command=start_process)
start_button.pack(pady=20)







def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


#i want to gigv ethis the voice actor name and have it turn that into the full directory of the voice actor location, and then use that to grab all the files inside of that voice actoers folder
def list_reference_files(voice_actor):
    global multi_voice_model_voice_list1
    global multi_voice_model_voice_list2
    global multi_voice_model_voice_list3
    if voice_actor in multi_voice_model_voice_list1:
        create_folder_if_not_exists(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}")
        reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
        if len(reference_files)==0:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            fast_tts = TTS(multi_voice_model1, progress_bar=True).to(device)
            fast_tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}/demo.wav", speaker = voice_actor)
            reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model1}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
            return reference_files
        else:
            return reference_files
            
            
    elif voice_actor in multi_voice_model_voice_list2:
        create_folder_if_not_exists(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}")
        reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
        if len(reference_files)==0:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            fast_tts = TTS(multi_voice_model2, progress_bar=True).to("cpu")
            fast_tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}/demo.wav", speaker = voice_actor)
            reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model2}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
            return reference_files
        else:
            return reference_files

            
            
    elif voice_actor in multi_voice_model_voice_list3:
        create_folder_if_not_exists(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}")
        reference_files = [os.path.join(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}", file) for file in os.listdir(f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}") if file.endswith((".wav", ".mp3"))]
        if len(reference_files)==0:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            fast_tts = TTS(multi_voice_model3, progress_bar=True).to(device)
            fast_tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{multi_voice_model3}/{voice_actor}/demo.wav", speaker = voice_actor)
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
            fast_tts = TTS(voice_actor, progress_bar=True).to(device)
            fast_tts.tts_to_file(text=demo_text , file_path=f"tortoise/_model_demo_voices/{voice_actor}/demo.wav")
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


current_model =""


tts = None
STTS = None



def generate_file_ids(csv_file, chapter_delimiter):

    data = pd.read_csv(csv_file)
    
    if 'audio_id' not in data.columns:
        data['audio_id'] = [''] * len(data)
    
    chapter_num = 0
    
    for index, row in data.iterrows():
        text = row['Text']  # Adjust to the correct column name, e.g., 'Text' if it's uppercase in the CSV
        print(f"{text}")
        if chapter_delimiter in text:  # Ensure both are uppercase for case-insensitive matching/edit: nah 
            chapter_num = chapter_num +1
        
        data.at[index, 'audio_id'] = f"audio_{index}_{chapter_num}"
    
    data.to_csv(csv_file, index=False)
    print(f"'audio_id' column has been updated in {csv_file}")
#delim = chapter_delimiter_var.get()
generate_file_ids(csv_file, chapter_delimiter_var.get())


#function to generate audio for fine tuned speakers in xtts
import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import time
import sys
#this code will install styletts2 if it isnt already pip installed 
# Function to install package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import the package
try:
    from styletts2 import tts as stts
except ImportError:
    # If package is not found, install it
    print("styletts2 not found, installing now...")
    install("styletts2")
    # After installation, attempt to import again
    from styletts2 import tts as stts

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

# Function to generate audio for the text
def generate_audio():
    # Get device
    global multi_voice_model_voice_list1
    global multi_voice_model_voice_list2
    global multi_voice_model_voice_list3
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    global current_model
    global STTS

    #this will make it so that I can't modify the chapter delminator after I click generate
    disable_chapter_delimiter_entry()
    
    ensure_temp_folder()

    # List available TTS models
    #print(TTS().list_models())

    # Initialize the TTS model and set the device
    #tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    # Update the model initialization to use the selected model
    #tts = TTS(selected_tts_model, progress_bar=True).to(device)
    #fast_tts = TTS(multi_voice_model1, progress_bar=True).to(device)
    
    
    
    
    
    random.seed(int(time.time()))
    ensure_output_folder()
    total_rows = len(data)

    chapter_num = 0

    add_voice_actors_to_csv()
    add_languages_to_csv()
    for index, row in data.iterrows():
        #update_progress(index, total_rows)  # Update progress based on the current index and total rows

        speaker = row['Speaker']
        text = row['Text']
        update_progress(index, total_rows, text)  # Update progress based on the current index and total rows and text 

        language_code = character_languages.get(speaker, current_language)  # Default to 'en' if not found
        if calibre_installed:
            if "NEWCHAPTERABC" in text:
                chapter_num += 1
                print(f"chapter num: {chapter_num}")
                print(f"CHAPTER KEYWORD IS: NEWCHAPTERABC")
                text = text.replace("NEWCHAPTERABC", "")
        elif CHAPTER_KEYWORD in text.upper():
            chapter_num += 1
            print(f"chapter num: {chapter_num}")
            print(f"CHAPTER KEYWORD IS: {CHAPTER_KEYWORD}")
            
            
        #This is the code for grabbing the current voice actor    
        #This will make it so that if the button for single voice is checked in the gui then the voice actor is always the narrerators:
        if single_voice_checkbox_var.get():
            print(f"single voice actor checkbox is activated setting to voice actor to Narrator...")
            voice_actor = speaker_voice_map.get("Narrator")
        else:
            voice_actor = speaker_voice_map[speaker]


        #voice_actor = speaker_voice_map[speaker]
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
                    if current_model !=  multi_voice_model1:
                        fast_tts = TTS(multi_voice_model1, progress_bar=True).to("cpu")
                        current_model = multi_voice_model1
                        print(f"The model used in fast_tts has been changed to {current_model}")
                    fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
                elif voice_actor in multi_voice_model_voice_list2:
                    print(f"{voice_actor} is a fast model voice: {multi_voice_model2}")
                    if current_model !=  multi_voice_model2:
                        fast_tts = TTS(multi_voice_model2, progress_bar=True).to("cpu")
                        current_model = multi_voice_model2
                        print(f"The model used in fast_tts has been changed to {current_model}")
                    fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
                elif voice_actor in multi_voice_model_voice_list3:
                    print(f"{voice_actor} is a fast model voice: {multi_voice_model3}")
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    if current_model !=  multi_voice_model3:
                        fast_tts = TTS(multi_voice_model3, progress_bar=True).to("cpu")
                        current_model = multi_voice_model3
                        print(f"The model used in fast_tts has been changed to {current_model}")
                    fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
                elif "tts_models" in voice_actor and "multi-dataset" not in voice_actor:
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    if current_model !=  voice_actor:
                        fast_tts = TTS(voice_actor, progress_bar=True).to(device)
                        current_model = voice_actor
                        print(f"The model used in fast_tts has been changed to {current_model}")
                    #selected_tts_model = voice_actor
                    #"Model is multi-lingual but no `language` is provided."
                    
                    print(f"Model for this character has been switched to: {voice_actor} by user")
                    try:
                        fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav")
                    except ValueError as e:
                        if str(e) == "Model is multi-lingual but no `language` is provided.":
                            print("attempting to correct....")
                            fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav",language=language_code)
                            print("Successfully Corrected!")
                            
                    
                    #else:
                    #   print(f"{voice_actor} is neither multi-dataset nor multilingual")
                    #   tts.tts_to_file(text=fragment,file_path=f"Working_files/temp/{temp_count}.wav")  # Assuming the tts_to_file function has default arguments for unspecified parameters
                
                #If the voice actor has a custom fine tuned xtts model in its refrence folder ie if it has the model folder containing it
                elif os.path.exists(f"tortoise/voices/{voice_actor}/model") and os.path.isdir(f"tortoise/voices/{voice_actor}/model") and 'xtts' in selected_tts_model:
                    speaker_wavz=list_reference_files(voice_actor)
                    fineTune_audio_generate(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=speaker_wavz[0], language=language_code, voice_actor=voice_actor)


                # If the model contains both "multilingual" and "multi-dataset"
                elif "multilingual" in selected_tts_model and "multi-dataset" in selected_tts_model:
                    if 'tts' not in locals():
                            tts = TTS(selected_tts_model, progress_bar=True).to(device)

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
                    if 'tts' not in locals():
                        tts = TTS(selected_tts_model, progress_bar=True).to(device)
                    tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", language=language_code)

                # If the model only contains "multi-dataset"
                elif "multi-dataset" in selected_tts_model:
                    print(f"{selected_tts_model} is multi-dataset")
                    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    #tts = TTS(selected_tts_model, progress_bar=True).to(device)
                    if 'tts' not in locals():
                        tts = TTS(selected_tts_model, progress_bar=True).to(device)
                    tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav")
                elif 'StyleTTS2' in selected_tts_model:
                    print(f'{selected_tts_model} model is selected for voice cloning')
                    if 'STTS' not in locals():
                        STTS = stts.StyleTTS2()
                    STTS.inference(fragment, target_voice_path=list_reference_files(voice_actor)[0], output_wav_file=f"Working_files/temp/{temp_count}.wav")

                # If the model contains neither "multilingual" nor "multi-dataset"
                else:
                    print(f"{selected_tts_model} is neither multi-dataset nor multilingual")
                    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    #tts = TTS(selected_tts_model, progress_bar=True).to(device)
                    if 'tts' not in locals():
                        tts = TTS(selected_tts_model, progress_bar=True).to(device)
                    tts.tts_to_file(text=fragment,file_path=f"Working_files/temp/{temp_count}.wav")  # Assuming the tts_to_file function has default arguments for unspecified parameters

                
                
                
        temp_input_directory = "Working_files/temp"  # Replace with the actual input directory path
        output_directory = "Working_files/generated_audio_clips"  # Replace with the desired output directory path
        combine_wav_files(temp_input_directory, output_directory, f"audio_{index}_{chapter_num}.wav")
        wipe_folder("Working_files/temp")
    root.destroy()






from functools import partial

def format_time(seconds):
    """
    Formats time in seconds to a more readable string with minutes, hours, days, and years if applicable.
    """
    minute = 60
    hour = minute * 60
    day = hour * 24
    year = day * 365

    years = seconds // year
    seconds %= year
    days = seconds // day
    seconds %= day
    hours = seconds // hour
    seconds %= hour
    minutes = seconds // minute
    seconds %= minute

    time_string = ""
    if years > 0:
        time_string += f"{years:.0f} year{'s' if years > 1 else ''} "
    if days > 0:
        time_string += f"{days:.0f} day{'s' if days > 1 else ''} "
    if hours > 0:
        time_string += f"{hours:.0f} hour{'s' if hours > 1 else ''} "
    if minutes > 0:
        time_string += f"{minutes:.0f} min "
    time_string += f"{seconds:.0f} sec"

    return time_string.strip()

"""
# Function to update the progress bar
def update_progress(index, total):
    current_time = time.time()
    
    # Calculate elapsed time
    elapsed_time = current_time - start_time
    
    # Calculate progress
    progress = (index + 1) / total * 100
    progress_var.set(progress)
    
    # Estimate remaining time
    if index > 0:  # Avoid division by zero
        average_time_per_item = elapsed_time / index
        estimated_time_remaining = average_time_per_item * (total - index - 1)
        remaining_time_string = format_time(estimated_time_remaining)
    else:
        remaining_time_string = "Calculating..."
    
    # Update progress label with estimated time
    progress_label.config(text=f"{progress:.2f}% done ({index+1}/{total} rows) - {remaining_time_string}")
    root.update_idletasks()

# Start time capture
start_time = time.time()
    """

def update_progress(index, total, row_text):
    current_time = time.time()
    
    # Calculate elapsed time
    elapsed_time = current_time - start_time

    # Update total characters processed and count of processed rows
    global total_chars_processed, processed_rows_count
    total_chars_processed += len(row_text)
    processed_rows_count += 1
    
    # Calculate progress
    progress = (index + 1) / total * 100

    # Estimate remaining time
    if processed_rows_count > 0:  # Avoid division by zero
        average_chars_per_row = total_chars_processed / processed_rows_count
        estimated_chars_remaining = average_chars_per_row * (total - processed_rows_count)
        average_time_per_char = elapsed_time / total_chars_processed
        estimated_time_remaining = average_time_per_char * estimated_chars_remaining
        remaining_time_string = format_time(estimated_time_remaining)
    else:
        remaining_time_string = "Calculating..."
    
    # Update progress label with estimated time
    progress_label.config(text=f"{progress:.2f}% done ({index+1}/{total} rows) - {remaining_time_string}")
    root.update_idletasks()

# Start time capture and initialize counters
start_time = time.time()
total_chars_processed = 0
processed_rows_count = 0


def create_scrollable_frame(parent, height):
    # Create a canvas with a specific height
    canvas = tk.Canvas(parent, height=height)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    
    scrollable_frame = ttk.Frame(canvas)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame



# Set the maximum height for the frame
max_height = 150  # Maximum height in pixels

# Create a LabelFrame for Character Voices
voice_selection_frame = ttk.LabelFrame(root, text="Character Voices")
voice_selection_frame.pack(fill="x", expand=False, padx=10, pady=5)

# Create a Canvas within the LabelFrame
canvas = tk.Canvas(voice_selection_frame, borderwidth=0)
canvas.config(height=max_height)  # Set the height of the canvas
scrollbar = ttk.Scrollbar(voice_selection_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)

def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind('<Configure>', configure_scroll_region)

# Add the scrollable frame to the canvas and configure the scrollbar
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Now, add comboboxes into the scrollable_frame
for speaker in data['Speaker'].unique():
    speaker_label = ttk.Label(scrollable_frame, text=speaker)
    speaker_label.pack(side="top", fill="x", expand=False)  # Changed to expand=False
    
    voice_combobox = ttk.Combobox(scrollable_frame, values=voice_actors, state="readonly")
    voice_combobox.set(speaker_voice_map[speaker])
    voice_combobox.pack(side="top", fill="x", expand=False)  # Changed to expand=False
    voice_combobox.bind("<<ComboboxSelected>>", lambda event, speaker=speaker: update_voice_actor(speaker))
    
    voice_comboboxes[speaker] = voice_combobox
    
    # Here is a mistake in your code. The language_combobox should be packed into scrollable_frame, not voice_selection_frame.
    language_var = tk.StringVar()
    language_combobox = ttk.Combobox(scrollable_frame, textvariable=language_var, state="readonly")
    language_combobox['values'] = list(languages.keys())
    language_combobox.set('English')
    language_combobox.pack(side="top", fill="x", expand=False)  # Changed to expand=False and should be in scrollable_frame
    
    # Update character_languages when a language is selected
    def on_language_selected(event, speaker=speaker, combobox=language_combobox):
        selected_language_key = combobox.get()
        selected_language = languages[selected_language_key]
        character_languages[speaker] = selected_language
        print(f"Language for {speaker} changed to {selected_language}")

    language_combobox.bind("<<ComboboxSelected>>", partial(on_language_selected, speaker=speaker))
    character_languages[speaker] = 'en'


# Create a label for the entry
chapter_delimiter_label = ttk.Label(root, text="Chapter Delimiter:(Press enter in field to submit change)")
chapter_delimiter_label.pack()  # Adjust layout options as needed

# Create the Entry widget for chapter delimiter and bind the Enter key
chapter_delimiter_entry = ttk.Entry(root, textvariable=chapter_delimiter_var)
chapter_delimiter_entry.pack()

# Label for Silence Duration Entry
silence_duration_label = tk.Label(root, text="Enter Silence Duration in milliseconds (ms):")
silence_duration_label.pack()

# Silence Duration Entry
silence_duration_var = tk.StringVar(value="750")
silence_duration_var.trace("w", on_silence_duration_change)
validate_cmd = root.register(validate_integer)
silence_duration_entry = tk.Entry(root, textvariable=silence_duration_var, validate='key', validatecommand=(validate_cmd, '%P'))
silence_duration_entry.pack()



def on_enter_pressed(event):
    # Path to your CSV file
    csv_file = "Working_files/Book/book.csv"  # Replace with the actual path to your CSV file
    chapter_delimiter = chapter_delimiter_var.get()
    generate_file_ids(csv_file, chapter_delimiter)

# Bind the Enter key to the on_enter_pressed function for chapter_delimiter_entry
chapter_delimiter_entry.bind('<Return>', on_enter_pressed)

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

# Initialize Pygame mixer
#pygame.mixer.init()

import itertools
import random

# Load and display the book content with colored speakers
# Function to play the audio when a tag associated with text is clicked
def on_text_click(event):
    text_widget = event.widget
    text_index = text_widget.index(f"@{event.x},{event.y}")
    tags = text_widget.tag_names(text_index)
    
    # Extract the CSV index from the tags
    csv_index_tag = next((tag for tag in tags if tag.isdigit()), None)
    if csv_index_tag is not None:
        # Here you have the CSV row index
        csv_index = int(csv_index_tag)
        print(f"CSV Index: {csv_index}")

    #use the csv_index to retrive the updated tags value from the csv file
    data = pd.read_csv('Working_files/Book/book.csv')
    audio_id = data.at[csv_index, 'audio_id']
    print(audio_id)
    
    if audio_id.startswith("audio_"):
        audio_file = f"Working_files/generated_audio_clips/{audio_id}.wav"
        print(f"Playing {audio_file}")
        try:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            sound = pygame.mixer.Sound(audio_file)
            sound.play()
        except Exception as e:
            print(f"Could not play the audio file: {e}")

# Function to load the book content and associate each text block with an audio tag
def load_book():
    data = pd.read_csv(csv_file)

    # Clear the current text
    text_display.delete('1.0', tk.END)

    # Define and shuffle colors
    sublime_colors = ['#66D9EF', '#A6E22E', '#F92672', '#FD971F', '#E6DB74', '#AE81FF']
    random.shuffle(sublime_colors)
    color_cycle = itertools.cycle(sublime_colors)

    # Generate a color for each speaker
    speakers = data['Speaker'].unique()
    speaker_colors = {speaker: next(color_cycle) for speaker in speakers}

    for index, row in data.iterrows():
        speaker = row['Speaker']
        text = row['Text']
        audio_id = row['audio_id']
        csv_index = str(index)  # Convert the index to string to use as a tag

        text_display.tag_configure(speaker, foreground="black", background=speaker_colors[speaker])
        text_display.insert(tk.END, f"{speaker}: ", speaker)
        text_display.insert(tk.END, f"{text}\n\n", (audio_id, speaker, csv_index))
        text_display.tag_bind(audio_id, "<Button-1>", on_text_click)

    text_display.yview_moveto(0)





# Load the book content into the Text widget
try:
    load_book()
except Exception as e:
    print(f"An error occured showing error but not stopping program: {e}")


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







































import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
import itertools
import random
import pygame


#add_voice_actors_to_csv()
#add_languages_to_csv()

# Initialize pygame mixer
pygame.mixer.init()

# Load the book data from CSV
csv_file = 'Working_files/Book/book.csv'  # Replace with your actual CSV file path
book_data = pd.read_csv(csv_file)
speakers = book_data['Speaker'].unique()  # List of unique speakers

fast_tts = ""

voice_actor_dropdown_active = False

# Initialize the main window
root = tk.Tk()
root.title("Book Viewer")

# Define and shuffle colors
sublime_colors = ['#66D9EF', '#A6E22E', '#F92672', '#FD971F', '#E6DB74', '#AE81FF']
random.shuffle(sublime_colors)
color_cycle = itertools.cycle(sublime_colors)
speaker_colors = {speaker: next(color_cycle) for speaker in speakers}

# 'Select All' Checkbox variable
select_all_var = tk.BooleanVar(value=False)

# Dropdown frame
dropdown_frame = ttk.Frame(root)
dropdown_frame.pack(fill='x', expand=False)



# Dropdown for actions
actions = ["Print Selected Audio IDs","Regenerate Selected Audio","Select Voice Actor"]
action_var = tk.StringVar(value=actions[0])
action_dropdown = ttk.Combobox(dropdown_frame, textvariable=action_var, values=actions, state="readonly")
action_dropdown.pack(side='left', padx=5, pady=5)

# Listbox for character filter
listbox_frame = ttk.Frame(root)
listbox_frame.pack(fill='x', expand=False)
character_listbox = tk.Listbox(listbox_frame, selectmode='multiple', exportselection=False)
character_listbox.pack(side='left', padx=5, pady=5)
for speaker in speakers:
    character_listbox.insert(tk.END, speaker)

# Function to toggle all checkboxes based on 'Select All' state
def toggle_all_checkboxes():
    # Set all checkbox variables to the value of the 'select all' variable
    for chk_var in checkbox_vars:
        chk_var.set(select_all_var.get())
    # Refresh the display if necessary, for instance to update the view
    # This may not be necessary if the checkbuttons update automatically
    root.update_idletasks()


# 'Select All' Checkbox
select_all_checkbox = ttk.Checkbutton(listbox_frame, text="Select All", variable=select_all_var, command=toggle_all_checkboxes)
select_all_checkbox.pack(side='top')

# Scrollable text widget with disabled editing
text_display_frame = ttk.Frame(root)
text_display_frame.pack(fill="both", expand=True)
text_display = scrolledtext.ScrolledText(text_display_frame, state='disabled', wrap=tk.WORD)
text_display.pack(fill="both", expand=True)

# Checkbox variables and widgets stored in a list
checkbox_vars = []

# Function to toggle all checkboxes based on 'Select All' state
def toggle_all_checkboxes():
    # Set all checkbox variables to the value of the 'select all' variable
    for chk_var in checkbox_vars:
        chk_var.set(select_all_var.get())
    # Refresh the display if necessary, for instance to update the view
    # This may not be necessary if the checkbuttons update automatically
    root.update_idletasks()


# Function to play the audio when text is clicked
def on_text_click(event):
    text_widget = event.widget
    text_index = text_widget.index(f"@{event.x},{event.y}")
    tags = text_widget.tag_names(text_index)

    # Extract the audio_id from the tags
    audio_id_tag = next((tag for tag in tags if 'audio_' in tag), None)
    if audio_id_tag is not None:
        # Retrieve the associated audio file
        audio_file = f"Working_files/generated_audio_clips/{audio_id_tag}.wav"
        print(f"Playing {audio_file}")
        try:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            sound = pygame.mixer.Sound(audio_file)
            sound.play()
        except Exception as e:
            print(f"Could not play the audio file: {e}")

# Function to load the book content and associate each text block with an audio tag
def load_book():
    text_display.configure(state='normal')  # Enable editing to insert text
    text_display.delete('1.0', tk.END)  # Clear the text display
    checkbox_vars.clear()  # Clear previous checkbox variables
    
    # Get selected characters
    selected_indices = character_listbox.curselection()
    selected_speakers = [character_listbox.get(i) for i in selected_indices]
    
    # Filter rows by the selected speakers
    if selected_speakers:
        filtered_data = book_data[book_data['Speaker'].isin(selected_speakers)]
    else:
        filtered_data = book_data
    # Generate a color for each speaker and insert text with tags
    for index, row in filtered_data.iterrows():
        speaker = row['Speaker']
        text = row['Text']
        audio_id = f"{row['audio_id']}"  # Tag for audio

        # Configure the tag for both the speaker and the text
        text_display.tag_configure(speaker, foreground="black", background=speaker_colors[speaker])
        text_display.tag_bind(speaker, "<Button-1>", on_text_click)
        text_display.tag_bind(audio_id, "<Button-1>", on_text_click)

        # Insert the speaker with tag
        try:
            text_display.insert(tk.END, f"{speaker}: ", speaker)
        except Exception as e:
            print(f"An error occured continueing: {e}")
        
        
        # Create a checkbox variable for each line of text
        chk_var = tk.BooleanVar(value=False)
        checkbox_vars.append(chk_var)
        
        # Create a checkbox for each line of text
        checkbox = ttk.Checkbutton(text_display, variable=chk_var)
        text_display.window_create(tk.END, window=checkbox)
        
        # Insert the text with both the speaker and audio_id tags
        text_display.insert(tk.END, f" {text}\n\n", (speaker, audio_id))

    text_display.configure(state='disabled')  # Disable editing after insertion
    text_display.yview_moveto(0)  # Scroll to the top


# Function to print the audio IDs of selected text lines
# Function to print the audio IDs of selected text lines
def print_selected_audio_id(audio_id):
    print(f"Selected Audio ID: {audio_id}")

# Function to populate voice actor dropdown
def populate_voice_actor_dropdown():
    global voice_actor_dropdown_active
    voice_actors = [va for va in os.listdir(voice_actors_folder) if va != "cond_latent_example"]
    voice_actor_dropdown = ttk.Combobox(dropdown_frame, values=voice_actors, state="readonly")
    if voice_actor_dropdown_active == False:
        voice_actor_dropdown.pack(side='left', padx=5, pady=5)
        voice_actor_dropdown_active = True
    return voice_actor_dropdown

# Function to handle voice actor selection and print the selected actor
def on_voice_actor_selected(event):
    selected_voice_actor = voice_actor_dropdown.get()
    print(f"Selected Voice Actor: {selected_voice_actor}")
    # Here you can add more actions to do with the selected voice actor



# Callback function for the action dropdown
def on_action_selected(event):
    selected_action = action_var.get()
    selected_indices = character_listbox.curselection()
    selected_speakers = [character_listbox.get(i) for i in selected_indices]
    
    if selected_speakers:
        filtered_data = book_data[book_data['Speaker'].isin(selected_speakers)]
    else:
        filtered_data = book_data

    if selected_action == "Select Voice Actor":
        global voice_actor_dropdown  # Define as global if it needs to be accessed outside this scope
        voice_actor_dropdown = populate_voice_actor_dropdown()
        voice_actor_dropdown.bind('<<ComboboxSelected>>', on_voice_actor_selected)
    else:
        # Iterate over the filtered data and print audio IDs for selected checkboxes
        for index, (row, chk_var) in enumerate(zip(filtered_data.itertuples(index=False), checkbox_vars)):
            if chk_var.get():  # If the checkbox is selected
                audio_id = row.audio_id
                text = row.Text
                speaker = row.Speaker
                voice_actor = row.voice_actor
                language = row.language
                if selected_action == "Print Selected Audio IDs":
                    print_selected_audio_id(audio_id)
                    print(row)
                if selected_action == "Regenerate Selected Audio":
                    #This is code to apply this function to every selected row
                    #regenerate_audio(text, audio_id, language, speaker)
                    print(f"Generating audio: for {row}")
                    generate_audio(text, audio_id, language, speaker, voice_actor)

action_dropdown.bind('<<ComboboxSelected>>', on_action_selected)

# Bind the Listbox to the callback function
character_listbox.bind('<<ListboxSelect>>', lambda event: load_book())

# Callback function to reload the book based on the selected speaker
def on_character_selected(event):
    load_book()

def generate_audio_voice_actor(text, fileName, voice_actor):
    folder = "Working_files/generated_audio_clips/"
    file_Name = folder+fileName

#def regenerate_audio(text, audio_id, language, speaker):


# Function to generate audio for the text
def generate_audio(text, audio_id, language, speaker, voice_actor):

    audio_id = audio_id
    text = text
    speaker = speaker
    voice_actor = voice_actor
    language = language
    index = int(re.search(r'\d+', audio_id.split('_')[1]).group())
    global chapters

    # Get device
    global multi_voice_model_voice_list1
    global multi_voice_model_voice_list2
    global multi_voice_model_voice_list3
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    global current_model
    global fast_tts


    ensure_temp_folder()

    # List available TTS models
    # print(TTS().list_models())

    # Initialize the TTS model and set the device
    # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    # Update the model initialization to use the selected model
    # tts = TTS(selected_tts_model, progress_bar=True).to(device)
    # fast_tts = TTS(multi_voice_model1, progress_bar=True).to(device)

    random.seed(int(time.time()))
    ensure_output_folder()
    total_rows = len(data)

    chapter_num = 0

    add_voice_actors_to_csv()
    add_languages_to_csv()


    speaker = speaker
    text = text

    language_code = language  # Default to 'en' if not found

#if the chapter list is empty then don't use it if its empty then continue using the set chapter deliminator
    if len(chapters) == 0:
         for chapter in chapters:
            if chapter in text:
                print(f"chapter num: {chapter_num}")
                print(f"CHAPTER IS: {chapter}")
                chapter_num += 1
                
        

    elif CHAPTER_KEYWORD in text.upper():
        chapter_num += 1
        print(f"chapter num: {chapter_num}")
        print(f"CHAPTER KEYWORD IS: {CHAPTER_KEYWORD}")

    voice_actor = voice_actor
    sentences = sent_tokenize(text)

    audio_tensors = []
    temp_count = 0
    for sentence in sentences:
        fragments = split_long_string(sentence)
        for fragment in fragments:
            # Check if the selected model is multilingual
            if 'multilingual' in selected_tts_model:
                language_code = language
            else:
                language_code = None  # No language specification for non-multilingual models

            print(f"Voice actor: {voice_actor}, {language}")
            temp_count = temp_count + 1
            # Use the model and language code to generate the audio
            # tts = TTS(model_name="tts_models/en/ek1/tacotron2", progress_bar=False).to(device)
            # tts.tts_to_file(fragment, speaker_wav=list_reference_files(voice_actor), progress_bar=True, file_path=f"Working_files/temp/{temp_count}.wav")

            # This will make it so that if you're selecting a model as a voice actor name then it'll initialize the voice actor name as the model
            if voice_actor in multi_voice_model_voice_list1:
                print(f"{voice_actor} is a fast model voice: {multi_voice_model1}")
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                if current_model != multi_voice_model1:
                    fast_tts = TTS(multi_voice_model1, progress_bar=True).to("cpu")
                    current_model = multi_voice_model1
                    print(f"The model used in fast_tts has been changed to {current_model}")
                fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
            elif voice_actor in multi_voice_model_voice_list2:
                print(f"{voice_actor} is a fast model voice: {multi_voice_model2}")
                if current_model != multi_voice_model2:
                    fast_tts = TTS(multi_voice_model2, progress_bar=True).to("cpu")
                    current_model = multi_voice_model2
                    print(f"The model used in fast_tts has been changed to {current_model}")
                fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
            elif voice_actor in multi_voice_model_voice_list3:
                print(f"{voice_actor} is a fast model voice: {multi_voice_model3}")
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                if current_model != multi_voice_model3:
                    fast_tts = TTS(multi_voice_model3, progress_bar=True).to("cpu")
                    current_model = multi_voice_model3
                    print(f"The model used in fast_tts has been changed to {current_model}")
                fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker=voice_actor)
            elif "tts_models" in voice_actor and "multi-dataset" not in voice_actor:
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                if current_model != voice_actor:
                    fast_tts = TTS(voice_actor, progress_bar=True).to(device)
                    current_model = voice_actor
                    print(f"The model used in fast_tts has been changed to {current_model}")
                # selected_tts_model = voice_actor
                # "Model is multi-lingual but no `language` is provided."

                print(f"Model for this character has been switched to: {voice_actor} by user")
                try:
                    fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav")
                except ValueError as e:
                    if str(e) == "Model is multi-lingual but no `language` is provided.":
                        print("Attempting to correct....")
                        fast_tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", language=language_code)
                        print("Successfully Corrected!")

                # else:
                #   print(f"{voice_actor} is neither multi-dataset nor multilingual")
                #   tts.tts_to_file(text=fragment,file_path=f"Working_files/temp/{temp_count}.wav")  # Assuming the tts_to_file function has default arguments for unspecified parameters

            # If the model contains both "multilingual" and "multi-dataset"
            elif "multilingual" in selected_tts_model and "multi-dataset" in selected_tts_model:
                if 'tts' not in locals():
                    tts = TTS(selected_tts_model, progress_bar=True).to(device)

                try:
                    if "bark" in selected_tts_model:
                        print(f"{selected_tts_model} is bark so multilingual but has no language code")
                        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                        # tts = TTS(selected_tts_model, progress_bar=True).to(device)
                        tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=list_reference_files(voice_actor))
                    else:
                        print(f"{selected_tts_model} is multi-dataset and multilingual")
                        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

                        # tts = TTS(selected_tts_model, progress_bar=True).to(device)
                        tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=list_reference_files(voice_actor), language=language_code)
                except ValueError as e:
                    if str(e) == "Model is not multi-lingual but `language` is provided.":
                        print("Caught ValueError: Model is not multi-lingual. Ignoring the language parameter.")
                        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                        # tts = TTS(selected_tts_model, progress_bar=True).to(device)
                        tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", speaker_wav=list_reference_files(voice_actor))

            # If the model only contains "multilingual"
            elif "multilingual" in selected_tts_model:
                print(f"{selected_tts_model} is multilingual")
                # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                # tts = TTS(selected_tts_model, progress_bar=True).to(device)
                if 'tts' not in locals():
                    tts = TTS(selected_tts_model, progress_bar=True).to(device)
                tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav", language=language_code)

            # If the model only contains "multi-dataset"
            elif "multi-dataset" in selected_tts_model:
                print(f"{selected_tts_model} is multi-dataset")
                # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                # tts = TTS(selected_tts_model, progress_bar=True).to(device)
                if 'tts' not in locals():
                    tts = TTS(selected_tts_model, progress_bar=True).to(device)
                tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav")

            # If the model contains neither "multilingual" nor "multi-dataset"
            else:
                print(f"{selected_tts_model} is neither multi-dataset nor multilingual")
                # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                # tts = TTS(selected_tts_model, progress_bar=True).to(device)
                if 'tts' not in locals():
                    tts = TTS(selected_tts_model, progress_bar=True).to(device)
                tts.tts_to_file(text=fragment, file_path=f"Working_files/temp/{temp_count}.wav")

    temp_input_directory = "Working_files/temp"  # Replace with the actual input directory path
    output_directory = "Working_files/generated_audio_clips"  # Replace with the desired output directory path
    combine_wav_files(temp_input_directory, output_directory, f"{audio_id}.wav")
    wipe_folder("Working_files/temp")



# Bind the action dropdown to the callback function
action_dropdown.bind('<<ComboboxSelected>>', on_action_selected)

# Load the book content into the Text widget
load_book()

# Run the main loop
root.mainloop()




























#this code here will make sure the folder where all the chapter audio files go i whiped before it starts creating the chapter files cause there might be stuff from the last session
import os
import shutil

def wipe_folder(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        print(f"Folder '{folder_path}' found. Proceeding to wipe...")
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' has been wiped.")
    else:
        print(f"Folder '{folder_path}' does not exist. No action taken.")

# Usage
folder_to_wipe = "Final_combined_output_audio"
wipe_folder(folder_to_wipe)








#this code here will combined all the tiny generated audio files into chapter audio files
import os
import pandas as pd
import torch
import torchaudio
import pygame

colors = ['#FFB6C1', '#ADD8E6', '#FFDAB9', '#98FB98', '#D8BFD8']
speaker_colors = {}
currently_playing = None
INPUT_FOLDER = "Working_files/generated_audio_clips"
OUTPUT_FOLDER = "Final_combined_output_audio"
#marked out cause its not defined earlier on in the code in the field
#SILENCE_DURATION_MS = 0


try:
    pygame.mixer.init()
    print("mixer modual initialized successfully.")
except pygame.error:
    print("mixer modual initialization failed")
    print(pygame.error)


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

        output_path = os.path.join(os.getcwd(), OUTPUT_FOLDER, f"chapter_{chapter_num}.wav")
        torchaudio.save(output_path, combined_tensor, sample_rate)

    print("Combining audio files complete!")

combine_audio_files(SILENCE_DURATION_MS)















#this will convert all of the wav chapter files into a single audiobook file located at output audiobook

"""
import os
import subprocess
from pydub import AudioSegment

def clear_audiobook_temp_files():
    files = glob.glob('/tmp/*.jpg')
    for f in files:
        os.remove(f)

def extract_cover_image_calibre(ebook_file):
    output_image = os.path.join('/tmp', os.path.basename(ebook_file) + '.jpg')
    try:
        subprocess.run(['ebook-meta', ebook_file, '--get-cover', output_image], check=True)
        if os.path.exists(output_image):
            return output_image
        else:
            return None
    except Exception as e:
        print(f"Error extracting cover image: {e}")
        return None

def generate_chapter_metadata(wav_files, metadata_filename):
    with open(metadata_filename, 'w') as file:
        file.write(";FFMETADATA1\n")
        start_time = 0
        for index, wav_file in enumerate(wav_files):
            duration = len(AudioSegment.from_wav(wav_file))
            end_time = start_time + duration
            file.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={start_time}\nEND={end_time}\ntitle=Chapter {index+1:02d}\n")
            start_time = end_time

def combine_wav_to_m4b_ffmpeg(wav_files, m4b_filename, cover_image, metadata_filename):
    print("Combining WAV files into an M4B audiobook using FFmpeg...")
    with open('file_list.txt', 'w') as file:
        for wav_file in wav_files:
            file.write(f"file '{wav_file}'\n")

    os.system(f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy combined.wav")

    print("Converting to M4B with AAC codec and cover art...")
    os.system(f"ffmpeg -i combined.wav -i {cover_image} -i {metadata_filename} -map_metadata 2 -map 0 -map 1 -c:a aac -b:a 192k -c:v copy -disposition:v:0 attached_pic {m4b_filename}")
    print(f"M4B audiobook created: {m4b_filename}")

    # Cleanup
    os.remove('file_list.txt')
    os.remove('combined.wav')
    os.remove(metadata_filename)
    os.remove(cover_image)  # Delete the cover image file

def convert_all_wav_to_m4b(input_dir, ebook_file, output_dir, audiobook_name):
    clear_audiobook_temp_files()  # Clear temporary files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    cover_image = extract_cover_image_calibre(ebook_file)
    if not cover_image:
        print("Cover image extraction failed.")
        return

    wav_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.wav')]
    m4b_filename = os.path.join(output_dir, f'{audiobook_name}.m4b')
    metadata_filename = 'chapter_metadata.txt'

    generate_chapter_metadata(wav_files, metadata_filename)
    combine_wav_to_m4b_ffmpeg(wav_files, m4b_filename, cover_image, metadata_filename)
    clear_audiobook_temp_files()  # Clear temporary files again

# Example usage
input_dir = "Final_combined_output_audio"  # Update this path to your WAV files folder
ebook_file = ebook_file_path      # Update this path to your eBook file
output_dir = 'output_audiobooks' 
audiobook_name = os.path.splitext(os.path.basename(ebook_file))[0]                    # Update this path to your desired output directory

convert_all_wav_to_m4b(input_dir, ebook_file, output_dir, audiobook_name)




"""









#this code here will create the actual nicely formatted m4b file with chapters and image metadata and everything located at output audiobook
import os
import subprocess
from pydub import AudioSegment
import shlex

def sort_chapters(file):
    # Extract chapter number from the filename
    number_part = re.findall(r'\d+', file)
    if number_part:
        return int(number_part[0])
    return 0


def extract_ebook_metadata(ebook_file):
    try:
        metadata_cmd = ['ebook-meta', ebook_file]
        metadata_output = subprocess.run(metadata_cmd, capture_output=True, text=True).stdout
        metadata = {}

        # Extracting various metadata fields
        for line in metadata_output.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        # Extracting the cover image
        output_image = os.path.join('/tmp', os.path.basename(ebook_file) + '.jpg')
        subprocess.run(['ebook-meta', ebook_file, '--get-cover', output_image], check=True)
        if not os.path.exists(output_image):
            output_image = None

        return output_image, metadata
    except Exception as e:
        print(f"Error extracting eBook metadata: {e}")
        return None, {}

def generate_chapter_metadata(wav_files, metadata_filename):
    with open(metadata_filename, 'w') as file:
        file.write(";FFMETADATA1\n")
        start_time = 0
        for index, wav_file in enumerate(wav_files):
            duration = len(AudioSegment.from_wav(wav_file))
            end_time = start_time + duration
            file.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={start_time}\nEND={end_time}\ntitle=Chapter {index+1:02d}\n")
            start_time = end_time

def combine_wav_to_m4b_ffmpeg(wav_files, m4b_filename, cover_image, metadata_filename, metadata):
    print("Combining WAV files into an M4B audiobook using FFmpeg...")
    with open('file_list.txt', 'w') as file:
        for wav_file in wav_files:
            file.write(f"file '{shlex.quote(wav_file)}'\n")

    ffmpeg_cmd = f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy combined.wav"
    ffmpeg_cmd += f" && ffmpeg -i combined.wav -i {shlex.quote(metadata_filename)}"
    if cover_image:
        ffmpeg_cmd += f" -i {shlex.quote(cover_image)}"

    for key, value in metadata.items():
        ffmpeg_cmd += f" -metadata {key}=\"{value}\""

    ffmpeg_cmd += f" -map_metadata 1"
    if cover_image:
        ffmpeg_cmd += f" -map 0 -map 2"
    ffmpeg_cmd += f" -c:a aac -b:a 192k"
    if cover_image:
        ffmpeg_cmd += f" -c:v copy -disposition:v:0 attached_pic"
    ffmpeg_cmd += f" {shlex.quote(m4b_filename)}"
    os.system(ffmpeg_cmd)
    print(f"M4B audiobook created: {m4b_filename}")

    # Cleanup
    os.remove('file_list.txt')
    if os.path.exists('combined.wav'):
        os.remove('combined.wav')
    os.remove(metadata_filename)
    if cover_image and os.path.exists(cover_image):
        os.remove(cover_image)

def convert_all_wav_to_m4b(input_dir, ebook_file, output_dir, audiobook_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    cover_image, ebook_metadata = extract_ebook_metadata(ebook_file)

    wav_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.wav')]
    wav_files.sort(key=sort_chapters)
    m4b_filename = os.path.join(output_dir, f'{audiobook_name}.m4b')
    metadata_filename = 'chapter_metadata.txt'

    # Setting up the metadata
    metadata = {
        'artist': ebook_metadata.get('Author(s)', 'Unknown Author'),
        'album': ebook_metadata.get('Series', 'Unknown Series'), 
        'Title': ebook_metadata.get('Title', f'{audiobook_name}.m4b'),
        'date': ebook_metadata.get('Published', 'Unknown Year'),
        'Genre': ebook_metadata.get('Tags', 'Unknown Genre'),
        'Comment': ebook_metadata.get('Tags', 'No description available.'),
        # Add other metadata fields as needed
    }
    m4b_filename = ebook_metadata.get('Title', f"audiobook_name")
    m4b_filename = os.path.join(output_dir, f'{m4b_filename}.m4b')

    generate_chapter_metadata(wav_files, metadata_filename)
    combine_wav_to_m4b_ffmpeg(wav_files, m4b_filename, cover_image, metadata_filename, metadata)

# Example usage
input_dir = "Final_combined_output_audio"  # Update this path to your WAV files folder
ebook_file = ebook_file_path      # Update this path to your eBook file
output_dir = 'output_audiobooks' 
audiobook_name = os.path.splitext(os.path.basename(ebook_file))[0]                    # Update this path to your desired output directory

convert_all_wav_to_m4b(input_dir, ebook_file, output_dir, audiobook_name)








#this will convert all the audio files into a mp4 format instead of wav to save space


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







#this will add the cover of the epub file to the mp4 combined files
print("Adding Book Artwork to mp4 chatper files if calibre is installed")

import os
import subprocess

def extract_cover_image_calibre(ebook_file):
    """
    Extracts the cover image from an eBook file using Calibre's ebook-meta tool.

    Args:
    ebook_file (str): The path to the eBook file.

    Returns:
    str: The path to the extracted cover image or None if not found.
    """
    output_image = os.path.join('/tmp', os.path.basename(ebook_file) + '.jpg')
    try:
        subprocess.run(['ebook-meta', ebook_file, '--get-cover', output_image], check=True)
        if os.path.exists(output_image):
            return output_image
        else:
            return None
    except Exception as e:
        print(f"Error extracting cover image: {e}")
        return None

def set_cover_to_mp4(cover_image, mp4_folder):
    """
    Sets the extracted cover image to all mp4 files in a specified folder.

    Args:
    cover_image (str): The path to the cover image.
    mp4_folder (str): The path to the folder containing mp4 files.
    """
    if not cover_image or not os.path.exists(cover_image):
        print("Cover image not found.")
        return

    # Process each mp4 file in the folder
    for file in os.listdir(mp4_folder):
        if file.lower().endswith('.mp4'):
            mp4_path = os.path.join(mp4_folder, file)
            # Set the cover image for the mp4 file
            # Note: Requires ffmpeg
            os.system(f'ffmpeg -i "{mp4_path}" -i "{cover_image}" -map 0 -map 1 -c copy -disposition:v:1 attached_pic "{mp4_path}.temp.mp4"')
            os.rename(f"{mp4_path}.temp.mp4", mp4_path)

# Example usage
ebook_file = ebook_file_path  # Update this path to your eBook file
mp4_folder = OUTPUT_FOLDER  # Update this path to your MP4 folder

#if calibre is installed then set the cover image things
# Extract cover image from the eBook file
cover_image = extract_cover_image_calibre(ebook_file)

# Set cover image to all mp4 files in the specified folder
set_cover_to_mp4(cover_image, mp4_folder)
