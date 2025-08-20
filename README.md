    # 🎙️ TTS-and-STT  

    This is a simple **Text-to-Speech (TTS)** and **Speech-to-Text (STT)** program built with **Python** and **Tkinter**.  
    It lets you convert text into speech, and speech into text, with a graphical interface.  

    ---

    ## 🚀 Setup  

    ### Windows (Recommended)  
    1. Clone the repository:  
    ```bash
    git clone https://github.com/undeadmoon84/TTS-and-STT.git
    cd TTS-and-STT
    ```

    2. Run the setup script:  
    ```bash
    setup.bat
    ```  
    This will:  
    - Create a virtual environment  
    - Install all dependencies  
    - Upgrade pip  

    3. After setup is complete, you’ll see this message:  
    ```
    For future use, just run:
        run.bat
    ```

    ---

    ## ▶️ Usage  
    - To launch the app later, simply run:  
    ```bash
    run.bat
    ```

    ---

    ## ⚙️ Dependencies  
    The following Python packages are used:  
    - `tk` (GUI with Tkinter)  
    - `pyttsx3` (offline TTS engine)  
    - `SpeechRecognition` (STT engine)  
    - `gTTS` (Google Text-to-Speech, requires internet)  
    - `pyaudio` (microphone input)  

    All of these are automatically installed by `setup.bat`.  

    ---

    ## 💻 Notes  
    - Python **3.13.7** is required.  
    - On some Windows systems, `pyaudio` may need manual installation using:  
    ```bash
    pip install pipwin
    pipwin install pyaudio
    ```
