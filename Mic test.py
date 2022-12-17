import speech_recognition as sr
mic_test = sr.Microphone()
mic = [sr.Microphone.list_microphone_names()]
print(mic)