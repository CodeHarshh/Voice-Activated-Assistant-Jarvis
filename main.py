import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import requests

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

API_KEY = 'd34daee2fbe84453a151f0546b3b930f'

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    try:
        while True:
            with sr.Microphone() as source:
                print("Listening.......")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            
            try:
                word = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Professor, I could not understand the audio.")
                continue
            except sr.RequestError as e:
                speak(f"Professor, there was an error: {e}")
                continue

            if word.lower() == "hey jarvis":
                speak("Yes, Professor")
                listening = True

                while listening:
                    with sr.Microphone() as source:
                        print("Jarvis Active.......")
                        audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    
                    try:
                        command = recognizer.recognize_google(audio)
                        print(command)
                        speak(command)
                    except sr.UnknownValueError:
                        print("Professor, I could not understand the audio.")
                        continue
                    except sr.RequestError as e:
                        speak(f"Professor, there was an error: {e}")
                        continue
                    
                    if "hello jarvis" in command.lower():
                        speak("Hello, professor! How can I help you?")
                    
                    elif "jarvis" in command.lower():
                        speak("Yes, sir")

                    if "open google" in command.lower():
                        webbrowser.open("https://google.com")
                    elif "open youtube" in command.lower():
                        webbrowser.open("https://youtube.com")
                    elif "open linkedin" in command.lower():
                        webbrowser.open("https://www.linkedin.com/feed/")
                    elif "open github" in command.lower():
                        webbrowser.open("https://github.com")
                    elif "news" in command.lower():
                        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}")
                        if response.status_code == 200:
                            data = response.json()
                            articles = data.get('articles', [])
                            top_articles = articles[:5]
                            for article in top_articles:
                                title = article.get('title', 'No Title')
                                speak(title)
                        else:
                            speak("Sorry, I couldn't fetch the news.")
                    elif command.lower().startswith("play"):
                        song = command.lower().split(" ", 1)[1]
                        link = musicLibrary.music.get(song)
                        if link:
                            webbrowser.open(link)
                        else:
                            speak("Sorry, I couldn't find the song in the music library.")
                    elif "ok goodbye jarvis" in command.lower():
                        speak("Goodbye, Sir!")
                        listening = False
                        break

                if not listening:
                    break  # Exit the outer loop if listening is set to False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak(f"An unexpected error occurred: {e}")
