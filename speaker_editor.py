import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
import itertools
import random

class BookEditor(tk.Tk):
    def __init__(self, csv_file):
        super().__init__()
        self.title("Manual Speaker Assignment Correction (if needed)")
        self.geometry("900x600")
        self.csv_file = csv_file
        self.data = pd.read_csv(csv_file)

        # Initialize speaker colors
        self.speaker_colors = {}

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Scrollable text display
        self.text_frame = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20)
        self.text_frame.pack(side="left", fill="both", expand=True)

        # Speaker selection and buttons frame
        speaker_frame = ttk.Frame(main_frame)
        speaker_frame.pack(side="right", fill="y")

        ttk.Label(speaker_frame, text="Speaker to change selected lines to").pack(pady=10)
        self.speaker_combobox = ttk.Combobox(speaker_frame, state="readonly", width=30)
        self.speaker_combobox.pack(pady=5)

        self.update_button = ttk.Button(speaker_frame, text="Update Selected Speakers", command=self.apply_changes)
        self.update_button.pack(pady=10)

        self.deselect_button = ttk.Button(speaker_frame, text="Deselect All", command=self.deselect_all)
        self.deselect_button.pack(pady=10)

        self.exit_button = ttk.Button(speaker_frame, text="Continue", command=self.destroy)
        self.exit_button.pack(pady=10)

        # Instructions label under the buttons
        instructions_label = tk.Label(
            speaker_frame,
            text=(
                "This tool allows you to manually correct the speaker assignment for specific lines.\n\n"
                "1. Select the lines you want to change by checking the boxes.\n"
                "2. Choose the speaker from the dropdown menu.\n"
                "3. Click 'Update Selected Speakers' to apply the changes.\n"
                "4. The book will be updated and displayed with your changes.\n"
                "5. Click 'Deselect All' to uncheck all checkboxes.\n"
                "6. Click 'Continue' when you are done."
            ),
            justify="left",
            wraplength=200
        )
        instructions_label.pack(pady=10)

        self.speakers = sorted(set(self.data['Speaker'].dropna()))
        self.assign_speaker_colors()
        self.populate_speaker_combobox()

        self.checkbox_vars = {}
        self.checkboxes = []

        self.load_book()

        # Adding tooltips
        self.add_tooltip(self.speaker_combobox, "Select the speaker to assign to the selected lines.")
        self.add_tooltip(self.update_button, "Apply the selected speaker to the selected lines.")
        self.add_tooltip(self.deselect_button, "Deselect all checkboxes.")
        self.add_tooltip(self.exit_button, "Exit the tool and continue to the next step.")

    def assign_speaker_colors(self):
        # Use a consistent color palette
        sublime_colors = ['#66D9EF', '#A6E22E', '#F92672', '#FD971F', '#E6DB74', '#AE81FF']
        color_cycle = itertools.cycle(sublime_colors)

        # Assign colors to speakers if they haven't been assigned yet
        for speaker in self.speakers:
            if speaker not in self.speaker_colors:
                self.speaker_colors[speaker] = next(color_cycle)

    def populate_speaker_combobox(self):
        # Create custom list of values with colored text
        self.speaker_combobox['values'] = self.speakers
        self.speaker_combobox.bind("<Configure>", self.update_combobox_colors)

    def update_combobox_colors(self, event=None):
        if hasattr(self.speaker_combobox, 'tk'):  # Make sure tk attribute exists
            self.speaker_combobox['menu'].delete(0, 'end')
            for speaker in self.speakers:
                color = self.speaker_colors[speaker]
                self.speaker_combobox['menu'].add_command(
                    label=speaker,
                    foreground=color,
                    command=tk._setit(self.speaker_combobox, speaker)
                )

    def load_book(self):
        # Save the current scroll position
        current_scroll_pos = self.text_frame.yview()

        # Clear and reload the text
        self.text_frame.delete(1.0, tk.END)

        for index, row in self.data.iterrows():
            speaker = row['Speaker']
            text = row['Text']

            tag_name = f"{index}"
            self.text_frame.tag_configure(tag_name, background=self.speaker_colors[speaker])

            checkbox_var = tk.BooleanVar(value=False)
            self.checkbox_vars[index] = checkbox_var

            self.text_frame.window_create(tk.END, window=tk.Checkbutton(self.text_frame, variable=checkbox_var))
            self.text_frame.insert(tk.END, f" {speaker}: {text}\n\n", tag_name)

        # Restore the scroll position
        self.text_frame.yview_moveto(current_scroll_pos[0])

    def apply_changes(self):
        selected_speaker = self.speaker_combobox.get()
        selected_lines = [index for index, checkbox_var in self.checkbox_vars.items() if checkbox_var.get()]

        if not selected_speaker:
            messagebox.showwarning("No speaker selected", "Please select a speaker.")
            return

        if not selected_lines:
            messagebox.showwarning("No lines selected", "Please select the lines you want to change.")
            return

        for index in selected_lines:
            self.data.at[index, 'Speaker'] = selected_speaker

        self.data.to_csv(self.csv_file, index=False)
        self.load_book()
        messagebox.showinfo("Update", "Speaker updated successfully.")

    def deselect_all(self):
        for checkbox_var in self.checkbox_vars.values():
            checkbox_var.set(False)

    def add_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        label = ttk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
        label.pack()
        tooltip.withdraw()

        def enter(event):
            x = event.widget.winfo_rootx() + 20
            y = event.widget.winfo_rooty() + 20
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

if __name__ == "__main__":
    app = BookEditor("Working_files/Book/book.csv")
    app.mainloop()
