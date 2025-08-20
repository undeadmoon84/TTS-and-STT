import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
from pathlib import Path
import os
import tempfile
import playsound

class TTSSTTApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Text-to-Speech and Speech-to-Text")
        self.master.geometry("600x350")
        self.bgcolor = "#E0F2F1"
        self.button_color = "#00ACC1"
        self.text_color = "#000000"
        self.font = ('Arial', 12)

        # Initialize pyttsx3 engine once
        self.engine = pyttsx3.init()

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', padding=6, font=self.font, background=self.button_color, foreground=self.text_color)
        self.style.configure('TLabel', font=self.font, background=self.bgcolor, foreground=self.text_color)
        self.style.configure('TFrame', background=self.bgcolor)

        self.mainpage()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def mainpage(self):
        self.clear_frame()
        frame = ttk.Frame(self.master)
        frame.pack(pady=20)

        ttk.Label(frame, text="Welcome!\nSelect an option:", style='TLabel').pack(pady=10)

        ttk.Button(frame, text="Text to Speech", style='TButton', command=self.text_to_speech_page).pack(pady=10)
        ttk.Button(frame, text="Speech to Text", style='TButton', command=self.speech_to_text_page).pack(pady=10)

    def add_back_button(self, command):
        ttk.Button(self.master, text="Back", style='TButton', command=command).pack(pady=10)

    # ---------------- TEXT TO SPEECH ----------------
    def text_to_speech_page(self):
        self.clear_frame()
        frame = ttk.Frame(self.master)
        frame.pack(pady=20)

        ttk.Button(frame, text="Save to File (High Quality)", style='TButton', command=self.save_file_tts).pack(pady=10)
        ttk.Button(frame, text="Play Instantly (Lower Quality)", style='TButton', command=self.instant_play_page).pack(pady=10)

        self.add_back_button(self.mainpage)

    def instant_play_page(self):
        self.clear_frame()
        frame = ttk.Frame(self.master)
        frame.pack(pady=20)

        ttk.Label(frame, text="Enter text to play instantly:", style='TLabel').pack(pady=5)
        self.instant_entry = tk.Text(frame, height=5, width=40, font=self.font)
        self.instant_entry.pack(pady=5)

        ttk.Button(frame, text="Play", style='TButton', command=self.play_instantly_thread).pack(pady=10)
        self.add_back_button(self.text_to_speech_page)

    def play_instantly_thread(self):
        threading.Thread(target=self.play_instantly, daemon=True).start()

    def play_instantly(self):
        text = self.instant_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter text to play.")
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Error", f"Could not play text: {e}")

    def save_file_tts(self):
        self.clear_frame()
        frame = ttk.Frame(self.master)
        frame.pack(pady=20)

        ttk.Label(frame, text="Enter text to save:", style='TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.save_text = tk.Text(frame, height=5, width=40, font=self.font)
        self.save_text.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="File name (without extension):", style='TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.filename_entry = ttk.Entry(frame, width=40, font=self.font)
        self.filename_entry.grid(row=1, column=1, pady=5)

        self.dir_button = ttk.Button(frame, text="Select Directory", style='TButton', command=self.select_directory)
        self.dir_button.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="Save", style='TButton', command=self.save_voice_thread).grid(row=3, column=1, pady=10)

        self.add_back_button(self.text_to_speech_page)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_path = directory
            self.dir_button.config(text=f"Selected: {directory}")

    def save_voice_thread(self):
        threading.Thread(target=self.save_voice, daemon=True).start()

    def save_voice(self):
        text = self.save_text.get("1.0", tk.END).strip()
        filename = self.filename_entry.get().strip()

        if not text or not filename:
            messagebox.showerror("Error", "Please enter both text and filename.")
            return
        if not hasattr(self, "directory_path"):
            messagebox.showerror("Error", "Please select a directory.")
            return

        try:
            file_path = Path(self.directory_path) / f"{filename}.mp3"
            tts = gTTS(text=text, lang='en', slow=False, tld="us")
            tts.save(file_path)
            messagebox.showinfo("Saved", f"File saved to {file_path}")
            self.dir_button.config(text="Select Directory")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    # ---------------- SPEECH TO TEXT ----------------
    def speech_to_text_page(self):
        self.clear_frame()
        frame = ttk.Frame(self.master)
        frame.pack(pady=20)

        self.stt_result = ttk.Label(frame, text="", wraplength=500, style='TLabel', font=self.font)
        self.stt_result.pack(pady=10)

        ttk.Label(frame, text="Say something in English...", style='TLabel', wraplength=500).pack(pady=5)

        ttk.Button(frame, text="Start Listening", style='TButton', command=self.start_listening_thread).pack(pady=5)
        ttk.Button(frame, text="Stop Listening", style='TButton', command=self.stop_listening).pack(pady=5)

        self.add_back_button(self.mainpage)

    def start_listening_thread(self):
        threading.Thread(target=self.start_listening, daemon=True).start()

    def start_listening(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            self.stt_result.config(text=f"You said: {text}")
        except sr.UnknownValueError:
            self.stt_result.config(text="Could not understand audio.")
            messagebox.showerror("Error", "Could not understand audio.")
        except sr.RequestError as e:
            self.stt_result.config(text=f"API request failed: {e}")
            messagebox.showerror("Error", "Could not connect to Google Speech API.")
        except Exception as e:
            self.stt_result.config(text=f"Error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def stop_listening(self):
        # For future improvement: implement continuous listening stop
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = TTSSTTApp(root)
    root.mainloop()
