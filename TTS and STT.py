import tkinter as tk #(pip install tk)
from tkinter import ttk, filedialog, messagebox
import pyttsx3 #(pip install pyttsx3)
import speech_recognition as sr #(pip install SpeechRecognition)
from gtts import gTTS #(pip install gtts)
#(pip install pyaudio)

class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x300")
        self.master.title("Text-to-Speech and Speech-to-Text")
        self.bgcolor = "#E0F2F1"
        self.button_color = "#00ACC1"
        self.text_color = "#000000"
        self.font = ('Arial', 12)
        self.style = ttk.Style()
        self.style.configure('TButton', padding=10, font=self.font, background=self.button_color, foreground=self.text_color)
        self.style.configure('TLabel', font=self.font, background=self.bgcolor, foreground=self.text_color)
        self.style.configure('TFrame', background=self.bgcolor)
        self.mainpage()

    def mainpage(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.mainPageFrame = ttk.Frame(self.master)
        self.mainPageFrame.pack(pady=20)
        self.welcomeText = ttk.Label(self.mainPageFrame, text="Welcome!\nSelect an option:", style='TLabel')
        self.welcomeText.pack(pady=10)
        self.tts = ttk.Button(self.mainPageFrame, text="Text to Speech", style='TButton', command=self.textToSpeech)
        self.stt = ttk.Button(self.mainPageFrame, text="Speech to Text", style='TButton', command=self.speechToText)
        self.tts.pack(pady=10)
        self.stt.pack(pady=10)

    def add_back_button(self, back_command):
        back_button = ttk.Button(self.master, text="Back", style='TButton', command=back_command)
        back_button.pack(pady=10)

    def textToSpeech(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.textToSpeechFrame = ttk.Frame(self.master)
        self.textToSpeechFrame.pack(pady=20)
        self.save = ttk.Button(self.textToSpeechFrame, text="Save to File (Higher Quality)", style='TButton', command=self.save_file_tts)
        self.instant = ttk.Button(self.textToSpeechFrame, text="Play Instantly (Lower Quality)", style='TButton', command=self.insbutton)
        self.save.pack(pady=10)
        self.instant.pack(pady=10)
        self.add_back_button(self.mainpage)

    def insbutton(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.insButtonFrame = ttk.Frame(self.master)
        self.insButtonFrame.pack(pady=20)
        self.insEntry = ttk.Entry(self.insButtonFrame, width=40, font=self.font)
        self.insEntry.pack(pady=10)
        self.instant_play_button = ttk.Button(self.insButtonFrame, text="Play", style='TButton', command=self.play_instantly)
        self.instant_play_button.pack(pady=10)
        self.add_back_button(self.textToSpeech)

    def play_instantly(self):
        text_to_speak = self.insEntry.get()
        engine = pyttsx3.init()
        engine.say(text_to_speak)
        engine.runAndWait()
        engine.stop()

    def save_file_tts(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.saveFileTTsFrame = ttk.Frame(self.master)
        self.saveFileTTsFrame.pack(pady=20)
        self.save_entry = ttk.Entry(self.saveFileTTsFrame, width=40, font=self.font)
        self.name = ttk.Entry(self.saveFileTTsFrame, width=40, font=self.font)
        self.save_button = ttk.Button(self.saveFileTTsFrame, text="Save", style='TButton', command=self.save_voice)
        self.directory_selector_button = ttk.Button(self.saveFileTTsFrame, text="Select Directory", style='TButton', command=self.select_directory)
        label1 = ttk.Label(self.saveFileTTsFrame, text="Enter your text:", style='TLabel', font=self.font)
        label2 = ttk.Label(self.saveFileTTsFrame, text="Enter file name (without .mp3):", style='TLabel', font=self.font)
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)
        self.save_entry.grid(row=0, column=1)
        self.name.grid(row=1, column=1)
        self.save_button.grid(row=2, column=1)
        self.directory_selector_button.grid(row=3, column=1)
        self.add_back_button(self.textToSpeech)

    def select_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.directory_path = directory_path
            self.directory_selector_button.config(text="Selected Directory: " + directory_path)

    def save_voice(self):
        filename = self.name.get()
        language = 'en'
        text_to_save = self.save_entry.get()
        if hasattr(self, "directory_path"):
            speech = gTTS(text=text_to_save, lang=language, slow=False, tld="us")
            file_path = f"{self.directory_path}/{filename}.mp3"
            speech.save(file_path)
            self.directory_selector_button.config(text="Select Directory")
            messagebox.showinfo("File Saved", f"File '{filename}.mp3' saved to directory '{self.directory_path}'.")
        else:
            messagebox.showerror("Error", "Please select a directory to save the file.")

    def speechToText(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.speechToTextFrame = ttk.Frame(self.master)
        self.speechToTextFrame.pack(pady=20)
        self.add_back_button(self.mainpage)
        self.startHearing = ttk.Button(self.speechToTextFrame, text="Start Listening", style='TButton', command=self.start_listening)
        self.stopHearing = ttk.Button(self.speechToTextFrame, text="Stop Listening", style='TButton', command=self.stop_listening)
        self.result = ttk.Label(self.speechToTextFrame, text="", wraplength=350, style='TLabel', font=self.font)
        self.saySomething = ttk.Label(self.speechToTextFrame, text="Say something in English...", style='TLabel', wraplength=350, font=self.font)
        self.saySomething.pack(pady=10)
        self.startHearing.pack(pady=10)
        self.stopHearing.pack(pady=10)
        self.result.pack()

    def start_listening(self):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            self.result.config(text=f"You said: {text}")
        except sr.UnknownValueError:
            self.result.config(text="Google Web Speech API could not understand audio")
            messagebox.showerror("Speech Recognition Error", "Could not understand audio.")
        except sr.RequestError as e:
            self.result.config(text="Could not request results from Google Web Speech API; {0}".format(e))
            messagebox.showerror("Speech Recognition Error", "Could not connect to Google Web Speech API. Please check your internet connection.")
        except Exception as e:
            self.result.config(text="An error occurred: {0}".format(e))
            messagebox.showerror("Error", "An error occurred while processing the audio.")

    def stop_listening(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()