import os
import torch


#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#print("Low default mode turned on: ", str(device) )

os.environ['CUDA_VISIBLE_DEVICES'] = ''
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Low Vram mode turned on : ", str(device) )



#del os.environ['CUDA_VISIBLE_DEVICES']
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#print("Low Vram mode turned off : ", str(device) )



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

