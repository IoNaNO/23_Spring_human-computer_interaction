from PyQt5 import QtWidgets, QtGui, QtCore, uic
from threading import Thread
from asrInterface import Ui_MainWindow
import win32api
import time
import sys

import speech_recognition as sr

recognizer=sr.Recognizer()
microphone=sr.Microphone()

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def parse_command(sentence):
    if sentence.__contains__('pad') or sentence.__contains__('note') or sentence.__contains__('pa'):
        # print('notepad')
        win32api.ShellExecute(0, 'open', 'code', '', '', 1)
        time.sleep(1)
    elif sentence.__contains__('play') or sentence.__contains__('playing') or sentence.__contains__('music'):
        # print('music')
        win32api.ShellExecute(0, 'open', '.\\music.mp3', '', '', 1)
        time.sleep(1)
    elif sentence.__contains__('check') or sentence.__contains__('weather') or sentence.__contains__('wea'):
        win32api.ShellExecute(0,'open','msedge','https://www.weather.com','',1)
        time.sleep(1)

class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
    def mainfunc(self):
        global recognizer,microphone
        # This is the mian function of the progress
        while True:
            while True:
                result=recognize_speech_from_mic(recognizer,microphone)
                if result['transcription']:
                    break
                if not result['success']:
                    break
                self.ui.add_reText_info("I didn't catch that. What did you say?\n")
            if result['error']:
                self.ui.add_reText_info(result["error"])
                break
            self.ui.add_reText_info(result["transcription"])
            self.myCommand=result["transcription"]
            parse_command(self.myCommand)
    def run(self):
        self.show()
        thread=Thread(target=self.mainfunc)
        thread.setDaemon(True)
        thread.start()

app = QtWidgets.QApplication([])
application = myWindow()
application.run()

sys.exit(app.exec())

