from gtts import gTTS 
import os 
mytext="Sample Audio"
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False) 
myobj.save("AI_Session.mp3") 
