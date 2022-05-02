import cv2
import pytesseract
import time
import pyttsx3
import speech_recognition as sr
from summarizer import Summarizer,TransformerSummarizer

def load_model():
    print('Loading model')
    model = TransformerSummarizer(transformer_type="GPT2",transformer_model_key="gpt2")
    print('Done')
    return model

def get_ocr(img):
    text = pytesseract.image_to_string(img)
    return text

def captureImage():
        cam = cv2.VideoCapture(0)
        time.sleep(1.2)
        res,img = cam.read()
        cam.release()
        # cv2.imshow("Image",img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        time.sleep(0.5)
        if res:
            text = get_ocr(img)
            text = text.strip()
            if(len(text)>0):
                print(text)
                # speak(text)
                return text
            else:
                speak('No text recognized')
                print("No image")
                return ""
        else:
            speak('Please capture the image properly')
            return ""

def setVoice(engine):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def processCommand(command,model):
    if('cap' in command):
        speak('Hi. How can I help you')
    if('get summary' in command):
        speak('Capturing image')
        text = captureImage()
        if(len(text)>0):
            summary = ''.join(model(text,max_length=100))
            speak(summary)
        # captureImage()
    if('read it' in command):
        speak('Capturing image')
        text = captureImage()
        if(len(text)>0):
            speak(text)

def listenSpeech(model):
    while(True):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.adjust_for_ambient_noise(source)
                audio = r.record(source,duration=2.0)
                command = r.recognize_google(audio_data = audio)
                print(command)
                if('bye' in command):
                    speak('Bye. Take care')
                    return
                elif(len(command)>0):
                    processCommand(command,model)
        except:
            continue

if __name__=="__main__":
    model = load_model()
    listenSpeech(model)
    # captureImage()