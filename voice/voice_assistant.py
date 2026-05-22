import speech_recognition as sr
import pyttsx3
import requests
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant"""
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.api_url = "http://localhost:5000/predict"
        
        # Configure voice settings
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)  # Speech rate
        
    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error speaking: {e}")
    
    def listen(self):
        """Listen for voice commands"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("Recognizing...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("Listening timeout. No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
        except Exception as e:
            print(f"Error listening: {e}")
            return ""
    
    def get_traffic_prediction(self):
        """Get traffic prediction from API"""
        try:
            print("Getting traffic prediction...")
            response = requests.get(self.api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to API: {e}")
            return None
    
    def process_command(self, command):
        """Process voice commands"""
        if "predict traffic" in command or "traffic prediction" in command:
            self.speak("Getting traffic prediction...")
            
            data = self.get_traffic_prediction()
            if data:
                traffic = data.get('predicted_traffic', 0)
                servers = data.get('required_servers', 0)
                time_str = data.get('current_time', 'unknown time')
                
                self.speak(f"At {time_str}, predicted traffic is {traffic} requests")
                self.speak(f"Required servers are {servers}")
            else:
                self.speak("Sorry, I couldn't get the traffic prediction. Please make sure the web server is running.")
                
        elif "server status" in command or "how many servers" in command:
            self.speak("Checking server status...")
            
            data = self.get_traffic_prediction()
            if data:
                servers = data.get('required_servers', 0)
                self.speak(f"Currently requiring {servers} servers")
            else:
                self.speak("Sorry, I couldn't get the server status.")
                
        elif "help" in command or "what can you do" in command:
            help_text = """
            I can help you with:
            - Say 'predict traffic' to get current traffic prediction
            - Say 'server status' to check required servers
            - Say 'exit' or 'quit' to close the assistant
            """
            self.speak("I can help you with traffic predictions and server status. Say 'predict traffic' to get started.")
            
        elif "exit" in command or "quit" in command or "stop" in command:
            self.speak("System shutting down. Goodbye!")
            return False
            
        elif command:
            self.speak("I didn't understand that. Try saying 'predict traffic' or 'help' for assistance.")
        
        return True
    
    def run(self):
        """Main loop for the voice assistant"""
        print("Voice Assistant Starting...")
        print("Make sure the Flask web server is running on localhost:5000")
        print("Say 'help' for available commands or 'exit' to quit")
        
        # Initial greeting
        self.speak("Voice assistant activated. Say 'predict traffic' to get started, or 'help' for commands.")
        
        try:
            while True:
                command = self.listen()
                
                if command:
                    should_continue = self.process_command(command)
                    if not should_continue:
                        break
                
                # Small delay between commands
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nVoice assistant stopped by user")
            self.speak("Voice assistant stopped. Goodbye!")
        except Exception as e:
            print(f"Error in voice assistant: {e}")
            self.speak("An error occurred. Shutting down.")

def main():
    """Main function to run the voice assistant"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to start voice assistant: {e}")

if __name__ == "__main__":
    main()
