import os
import subprocess
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

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
    if not os.path.exists(directory):
        os.makedirs(directory)

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
input_ebook = 'shattering.epub'  # Replace with your eBook file path
output_epub = 'Working_files/temp.epub'

if os.path.exists(output_epub):
    os.remove(output_epub)
    print(f"File {output_epub} has been removed.")
else:
    print(f"The file {output_epub} does not exist.")

if convert_to_epub(input_ebook, output_epub):
    save_chapters_as_text(output_epub)








import os
import csv
import nltk

# Download the necessary NLTK data (if not already present)
nltk.download('punkt')

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

# Example usage
folder_path = "Working_files/temp_ebook"  # Replace with your folder path
output_csv = 'Working_files/Book/Other_book.csv'
process_chapter_files(folder_path, output_csv)





#this will wipe the folder containing the temp ebook files
import os

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
folder_to_wipe = 'Working_files/temp_ebook'  # Replace with the path to your folder
wipe_folder(folder_to_wipe)
