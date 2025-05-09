import random
import sys
import os
import re
from api import search_web

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # In development, use the current directory
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def parse_markdown(text):
    segments = []
    lines = text.split('\n')

    for line in lines:
        line_segments = []
        if line.strip().startswith(('* ', '- ')):
            line_segments.append(("bullet", '• '))
            line = line.strip()[2:]

        pos = 0
        pattern = r'(\*\*[^*]+\*\*)|(\*[^*]+\*)'
        matches = list(re.finditer(pattern, line))
        for match in matches:
            start, end = match.span()
            if start > pos:
                line_segments.append(("plain", line[pos:start]))
            matched_text = match.group(0)
            if matched_text.startswith('**') and matched_text.endswith('**'):
                line_segments.append(("italic", matched_text[2:-2]))
            elif matched_text.startswith('*') and matched_text.endswith('*'):
                line_segments.append(("bold", matched_text[1:-1]))
            pos = end
        if pos < len(line):
            line_segments.append(("plain", line[pos:]))

        segments.extend(line_segments)
        segments.append(("plain", "\n"))

    return segments

def get_response(user_input, weather_api_key, gemini_api_key, history):
    user_input_lower = user_input.lower()
    responses = {
        "greetings": {
            "patterns": ["hi", "hello", "hey", "good morning"],
            "replies": ["Hey there!", "Hello! How can I help you?", "Hi! Nice to see you!"]
        },
        "goodbye": {
            "patterns": ["bye", "goodbye", "see you", "take care"],
            "replies": ["Goodbye!", "See you later!", "Take care!"]
        },
        "thanks": {
            "patterns": ["thank you", "thanks", "appreciate it"],
            "replies": ["You're welcome!", "Happy to help!", "No problem!"]
        },
        "help": {
            "patterns": ["what can you do", "how can you help me", "assist me", "what are you capable of"],
            "replies": ["I can answer questions or fetch info from the web. I use OpenWeatherMap for weather queries and Gemini API for other questions. Try asking about the weather or a simple fact! You can also speak your query using the Mic button."]
        }
    }

    for category, data in responses.items():
        if user_input_lower in data["patterns"]:
            return random.choice(data["replies"])
    
    return search_web(user_input, weather_api_key, gemini_api_key, history)