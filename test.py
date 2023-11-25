
import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
import itertools
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the book data from CSV
csv_file = 'Working_files/Book/book.csv'  # Replace with your actual CSV file path
book_data = pd.read_csv(csv_file)
speakers = book_data['Speaker'].unique()  # List of unique speakers

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
actions = ["Print Selected Audio IDs"]
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
        text_display.insert(tk.END, f"{speaker}: ", speaker)
        
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
def print_selected_audio_ids():
    selected_indices = character_listbox.curselection()
    selected_speakers = [character_listbox.get(i) for i in selected_indices]
    
    if selected_speakers:
        filtered_data = book_data[book_data['Speaker'].isin(selected_speakers)]
    else:
        filtered_data = book_data

    # Iterate over the filtered data and print audio IDs for selected checkboxes
    for index, (row, chk_var) in enumerate(zip(filtered_data.itertuples(index=False), checkbox_vars)):
        if chk_var.get():  # If the checkbox is selected
            audio_id = row.audio_id
            print(f"Selected Audio ID: {audio_id}")
            print(row.Text)
            print()
            print(row)


# Callback function for the action dropdown
def on_action_selected(event):
    selected_action = action_var.get()
    if selected_action == "Print Selected Audio IDs":
        print_selected_audio_ids()

action_dropdown.bind('<<ComboboxSelected>>', on_action_selected)

# Bind the Listbox to the callback function
character_listbox.bind('<<ListboxSelect>>', lambda event: load_book())

# Callback function to reload the book based on the selected speaker
def on_character_selected(event):
    load_book()

def generate_audio_voice_actor(text, fileName, voice_actor):
	folder = "Working_files/generated_audio_clips/"
	file_Name = folder+fileName

def regenerate_audio(index):
	#with this ill be using the index to pull extra needed info from the csv file
	csv_file ="Working_files/Book/book.csv"



# Bind the action dropdown to the callback function
action_dropdown.bind('<<ComboboxSelected>>', on_action_selected)

# Load the book content into the Text widget
load_book()

# Run the main loop
root.mainloop()

