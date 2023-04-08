import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QPushButton
from backend import Bot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QKeyEvent, QIcon
import speech_recognition as sr
import autopep8
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Evie")
        self.setGeometry(100, 100, 600, 600)

        # Set window icon
        self.setWindowIcon(QIcon('icons/AI3.png'))

        # Set dark background color
        self.setStyleSheet("background-color: #333;")

        # Create text box for chat history
        self.chat_history = QPlainTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.chat_history.setGeometry(50, 50, 500, 400)
        self.chat_history.setStyleSheet("background-color: #444; color: #fff;")

        # Create text box for user input
        self.user_input = QPlainTextEdit(self)        
        self.user_input.setGeometry(50, 470, 400, 50)
        self.user_input.setStyleSheet("background-color: #444; color: #fff;")
        self.user_input.installEventFilter(self)

        # Create "Send" button
        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(470, 470, 70, 50)
        self.send_button.setStyleSheet("background-color: #666; color: #fff;")
        self.send_button.clicked.connect(self.send_message)

        # Create "Speech" button
        self.speech_button = QPushButton("Speech", self)
        self.speech_button.setGeometry(560, 470, 70, 50)  # adjust the x position to be to the right of the input section
        self.speech_button.setStyleSheet("background-color: #666; color: #fff;")
        self.speech_button.clicked.connect(self.get_speech_input)

        # Create Bot instance
        self.bot = Bot()

        # Create variable to keep track of current interaction
        self.current_interaction = None


    def eventFilter(self, obj, event):
        if obj == self.user_input and event.type() == QKeyEvent.KeyPress and event.key() == 16777220:
            # Enter key pressed in user input field
            self.send_message()
            return True
        return super().eventFilter(obj, event)

    def send_message(self):
        font = self.chat_history.font()
        font.setPointSize(14)
        self.chat_history.setFont(font)
        # Get user input from text box
        message = self.user_input.toPlainText()
        self.user_input.clear()

        write_code = False
        if "code" in message.lower():
            write_code = True

        #<span style='color: black;'>You: </span>
        user_message = f"<span style='color: black;'>{message}</span></div><br>"
        if self.current_interaction is None:
            self.current_interaction = user_message
        else:
            self.current_interaction += user_message

        # Get response from Bot
        response = self.bot.get_response(message) 

        # Format Evie's response with autopep if writing Python code
        if write_code:
            formatted_response = autopep8.fix_code(response)
        else:
            formatted_response = response
            

        # Add Bot response to current interaction with custom color
        #<span style='color: red;'>Evie: </span>
        bot_response = f"{formatted_response}</div><br>"
        self.current_interaction += bot_response 
        

        # Add current interaction to chat history
        self.chat_history.appendHtml(self.current_interaction)


        # Reset current interaction
        self.current_interaction = None

        # Set speech recognition to off by default
        self.speech_recognition_on = False     


    def get_speech_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            self.user_input.setPlainText(text)
            self.send_message()
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Set the minimum and maximum sizes of the input and dialogue sections to the same value as the window
        width = self.width()
        height = self.height()

        self.chat_history.setMinimumSize(width - 100, height - 150)
        self.chat_history.setMaximumSize(width - 100, height - 150)

        self.user_input.setMinimumSize(width - 260, 50)
        self.user_input.setMaximumSize(width - 260, 50)
        self.user_input.setGeometry(50, height - 80, width - 220, 50)

        # Adjust the position of the send button
        send_button_width = self.send_button.width()
        send_button_height = self.send_button.height()
        send_button_x = self.user_input.x() + self.user_input.width() + 10
        send_button_y = self.user_input.y() + (self.user_input.height() - send_button_height) / 2
        self.send_button.setGeometry(send_button_x, send_button_y, send_button_width, send_button_height)

        # Adjust the position of the speech button
        speech_button_width = self.speech_button.width()
        speech_button_height = self.speech_button.height()
        speech_button_x = self.send_button.x() + self.send_button.width() + 10
        speech_button_y = self.send_button.y()
        self.speech_button.setGeometry(speech_button_x, speech_button_y, speech_button_width, speech_button_height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

