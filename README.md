# SkyGem-AI-Chatbot

SkyGem-AI-Chatbot is an AI-powered chatbot designed to provide an interactive and user-friendly experience. With voice input support, real-time weather updates, and general query handling via Google's Gemini API, SkyGem offers a seamless way to access information. The application features a modern indigo-themed UI built with Python and Tkinter, complete with a tabbed interface for chatting and viewing conversation history.

## Features

- **Voice Input**: Speak your queries using the microphone, powered by the `speech_recognition` library.
- **Weather Updates**: Fetch real-time weather data for any city using the OpenWeatherMap API.
- **General Queries**: Answer a wide range of questions using Google’s Gemini API.
- **Modern UI**: A sleek indigo-themed interface with a tabbed layout (Chat and History tabs) built with Tkinter.
- **Conversation History**: Save and revisit past conversations in the History tab.

## Prerequisites

Before running the project, ensure you have the following:

- **Python 3.6+**: The project is built with Python. Download it from [python.org](https://www.python.org/downloads/) if not already installed.
- **Git**: Required to clone the repository. Install it from [git-scm.com](https://git-scm.com/downloads) or via Homebrew on macOS (`brew install git`).
- **Internet Connection**: Needed for API calls (OpenWeatherMap, Gemini API) and voice recognition (Google Speech Recognition).
- **Microphone**: Required for voice input functionality.

## Installation

### 1. Clone the Repository

Clone the SkyGem-AI-Chatbot repository to your local machine:

```bash
git clone https://github.com/ishahzebali/SkyGem-chatbot.git
cd SkyGem-chatbot
```
### 2. Install Dependencies
The project requires several Python libraries. Install them using the provided requirements.txt file.

On macOS/Linux/Windows:

```bash
pip install -r requirements.txt
```
#### Dependencies:

requests: For making API calls to OpenWeatherMap and Gemini API.
SpeechRecognition: For voice input functionality.
PyAudio: Required by SpeechRecognition for microphone access.
Additional Setup for PyAudio on macOS:

PyAudio requires PortAudio, which can be installed via Homebrew:

```bash
brew install portaudio
pip install PyAudio
```
If you encounter issues, refer to the PyAudio documentation for platform-specific instructions.

#### On Windows:

PyAudio should install directly via pip, but if you encounter issues, you may need to install a pre-built wheel:

```bash
pip install pipwin
pipwin install PyAudio
```

### 3. Ensure Icon Files Are Present
The application uses two icon files:

skygem_icon.png: The window icon for the application.
These files should be in the project root directory. If they are missing, the application will still run, but the Mic button will display "Mic" as text, and the window icon may not appear.

#### Running the Project
Once the dependencies are installed, you can run the application:

```bash
python main.py
```
#### What to Expect:
- A splash screen will appear for 3 seconds, displaying the SkyGem logo.
- The main window will open with a tabbed interface:
  1. Chat Tab: Type or speak your queries (e.g., "What’s the weather in London?").
  2. History Tab: View and manage past conversations.
- Use the Mic button to speak your query, and the Send button to submit typed queries.

#### Usage
- Ask Questions: Type or speak queries like:
  1. "What’s the weather in New York?"
  2. "Tell me about the solar system."
  3. "Hi" (triggers a greeting response).
- View History: Switch to the History tab to see past conversations. You can delete sessions using the "Delete Session" button.
- Clear Chat: Use the "Clear Chat" button in the Chat tab to start a new conversation.


#### Troubleshooting
##### Voice Input Not Working:
  1. Ensure your microphone is connected and has permission to be accessed (macOS may prompt you to allow access).
  2. Check your internet connection, as Google Speech Recognition requires online access.
  3. Verify that PyAudio and SpeechRecognition are installed correctly.


#### API Errors:
- If weather or Gemini API queries fail, check your internet connection.
- Ensure the API keys in gui.py (weather_api_key and gemini_api_key) are valid. Replace them with your own keys.


#### Icons Not Loading:
- Ensure skygem_icon.png is in the project root directory.


#### Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature).
3. Make your changes and commit them (git commit -m "Add your feature").
4. Push to your branch (git push origin feature/your-feature).
5. Open a pull request on GitHub.
Please ensure your code follows Python PEP 8 style guidelines and includes appropriate documentation.

### License
This project is licensed under the MIT License. See the  file for details.

### Acknowledgements
- Built with Python and Tkinter.
- Voice input powered by SpeechRecognition.
- Weather data provided by OpenWeatherMap.
- General queries answered using Google Gemini API.
