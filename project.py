import tkinter as tk
from tkinter import messagebox
import os

# Folder where notes will be saved
NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

# Main App Class
class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking App")

        # Note Title
        tk.Label(root, text="Note Title:").pack()
        self.title_entry = tk.Entry(root, width=40)
        self.title_entry.pack()

        # Note Content
        tk.Label(root, text="Note Content:").pack()
        self.content_text = tk.Text(root, height=10, width=50)
        self.content_text.pack()

        # Buttons
        tk.Button(root, text="Save Note", command=self.save_note).pack(pady=5)
        tk.Button(root, text="Load Note", command=self.load_note).pack(pady=5)
        tk.Button(root, text="Delete Note", command=self.delete_note).pack(pady=5)

        # Note List
        tk.Label(root, text="Saved Notes:").pack()
        self.note_listbox = tk.Listbox(root, width=50)
        self.note_listbox.pack()
        self.refresh_note_list()

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if title == "":
            messagebox.showwarning("Error", "Title cannot be empty!")
            return

        file_path = os.path.join(NOTES_DIR, f"{title}.txt")
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Note '{title}' saved successfully.")
        self.refresh_note_list()

    def load_note(self):
        selected = self.note_listbox.curselection()
        if not selected:
            messagebox.showwarning("Error", "Please select a note to load.")
            return
        title = self.note_listbox.get(selected[0])
        file_path = os.path.join(NOTES_DIR, f"{title}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, content)

    def delete_note(self):
        selected = self.note_listbox.curselection()
        if not selected:
            messagebox.showwarning("Error", "Please select a note to delete.")
            return
        title = self.note_listbox.get(selected[0])
        file_path = os.path.join(NOTES_DIR, f"{title}.txt")
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Deleted", f"Note '{title}' deleted.")
            self.refresh_note_list()

    def refresh_note_list(self):
        self.note_listbox.delete(0, tk.END)
        for filename in os.listdir(NOTES_DIR):
            if filename.endswith(".txt"):
                self.note_listbox.insert(tk.END, filename[:-4])

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
