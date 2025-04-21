import speech_recognition as sr
import pyttsx3
import openai
from tkinter import Tk, Label, Button, Text, Scrollbar, END, VERTICAL

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set OpenAI API Key for GPT-based responses
openai.api_key = "YOUR_OPENAI_API_KEY"

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Voice Assistant")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Title Label
        self.title_label = Label(
            root, text="AI Voice Assistant", font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Text area for displaying conversation
        self.text_area = Text(root, wrap="word", font=("Helvetica", 12))
        self.text_area.pack(padx=10, pady=10, expand=True, fill="both")
        
        # Scrollbar for text area
        self.scrollbar = Scrollbar(self.text_area, orient=VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        
        # Buttons
        self.listen_button = Button(
            root, text="🎤 Listen", command=self.start_listening, bg="#4CAF50", fg="white",
            font=("Helvetica", 12), relief="raised", width=15
        )
        self.listen_button.pack(pady=10)

        self.exit_button = Button(
            root, text="Exit", command=self.exit_program, bg="#f44336", fg="white",
            font=("Helvetica", 12), relief="raised", width=15
        )
        self.exit_button.pack(pady=10)

    def speak(self, text):
        """Converts text to speech."""
        engine.say(text)
        engine.runAndWait()

    def listen(self):
        """Listens to user input via microphone."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_area.insert(END, "Listening...\n")
            self.text_area.see(END)
            self.text_area.update()
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source)
                query = recognizer.recognize_google(audio)
                self.text_area.insert(END, f"You: {query}\n")
                self.text_area.see(END)
                return query
            except sr.UnknownValueError:
                self.text_area.insert(END, "Sorry, I didn't catch that. Could you repeat?\n")
                self.text_area.see(END)
                return None
            except sr.RequestError:
                self.text_area.insert(END, "Sorry, there was an issue with the speech recognition service.\n")
                self.text_area.see(END)
                return None

    def handle_query(self, query):
        """Handles user queries via OpenAI GPT."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query},
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            return answer
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def start_listening(self):
        """Start listening and responding to user queries."""
        query = self.listen()
        if query:
            if "stop" in query.lower() or "exit" in query.lower():
                self.speak("Goodbye! Have a great day.")
                self.exit_program()
            else:
                response = self.handle_query(query)
                self.text_area.insert(END, f"Assistant: {response}\n")
                self.text_area.see(END)
                self.speak(response)

    def exit_program(self):
        """Exit the program."""
        self.speak("Goodbye!")
        self.root.destroy()

# Main function
if __name__ == "__main__":
    root = Tk()
    assistant = VoiceAssistantGUI(root)
    root.mainloop()