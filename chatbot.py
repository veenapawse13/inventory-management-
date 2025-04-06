import tkinter as tk
from tkinter import scrolledtext
import nltk
from transformers import pipeline
from nltk.tokenize import word_tokenize

# Download NLTK data
nltk.download('punkt')

# Initialize the GPT-2 model pipeline
chatbot = pipeline('text-generation', model='gpt2')

# Function to generate a response from the chatbot
def get_response(user_input):
    # Simple token-based check for basic responses
    tokens = word_tokenize(user_input.lower())
    if 'hello' in tokens:
        return "Hello! How can I help you today?"
    elif 'how' in tokens and 'you' in tokens:
        return "I'm doing great, thanks for asking!"
    else:
        # Use GPT-2 for generating more complex responses
        response = chatbot(user_input, max_length=50, num_return_sequences=1)
        return response[0]['generated_text']

# Create the main window
window = tk.Tk()
window.title("AI Chatbot")

# Set the window size
window.geometry("400x500")

# Create a text area for displaying the conversation
chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled', width=50, height=20)
chat_display.grid(row=0, column=0, padx=10, pady=10)

# Create an entry widget for the user to type messages
user_input = tk.Entry(window, width=40)
user_input.grid(row=1, column=0, padx=10, pady=10)

# Function to display user input and AI response
def send_message():
    user_message = user_input.get()
    if user_message.strip():
        chat_display.config(state='normal')
        chat_display.insert(tk.END, "You: " + user_message + "\n")
        chat_display.insert(tk.END, "Bot: " + get_response(user_message) + "\n\n")
        chat_display.config(state='disabled')
        user_input.delete(0, tk.END)

# Create a send button
send_button = tk.Button(window, text="Send", width=10, command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=10)

# Run the application
window.mainloop()
