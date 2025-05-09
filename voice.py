import speech_recognition as sr
import tkinter as tk

def capture_voice_input(gui_instance):
    """Capture voice input and insert it into the input field"""
    try:
        sr_recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            gui_instance.add_message("Listening for your voice input...", "bot")
            sr_recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = sr_recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = sr_recognizer.recognize_google(audio)
            gui_instance.input_field.delete(0, tk.END)
            gui_instance.input_field.insert(0, text)
            gui_instance.handle_input_change(None)  # Update Send button state
            gui_instance.send_message()  # Automatically send the message
    except sr.UnknownValueError:
        gui_instance.add_message("Sorry, I couldn't understand what you said. Please try again.", "bot")
    except sr.RequestError as e:
        gui_instance.add_message("Sorry, there was an error with the speech recognition service. Please check your internet connection.", "bot")
    except Exception as e:
        gui_instance.add_message(f"Error capturing voice input: {str(e)}", "bot")