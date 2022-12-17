import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
import speech_recognition as sr
from python_speech_features import mfcc, logfbank

#sig_audio - audio signal data
#freq - Original file frequency
#pow_audio_signal - audio signal power
#time_axis - for plotting purpose
#half_length - Half length of the wave form audio
#signal_length - Length of the audio signal
#Sig_Freq - Frequency of the audio signal
#featureMFCC - Extracted from audio file through MFCC
#fb_feature - Extracted from audio file through logfbank

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python main.py audio_sample")
    f, sa = wavfile.read(sys.argv[1])
    asr(f, sa)
    
def asr(freq, sig_audio):
    print('\nShape of Signal:', sig_audio.shape)
    print('Signal Datatype:', sig_audio.dtype)
    print('Signal duration:', round(sig_audio.shape[0] / float(freq), 2), 'seconds')
    pow_audio_signal = sig_audio / np.power(2, 15)
    pow_audio_signal = pow_audio_signal [:100]

    signal_length = len(sig_audio)
    half_length = np.ceil((signal_length + 1) / 2.0).astype(int)
    Sig_Freq = np.fft.fft(sig_audio)
    Sig_Freq = abs(Sig_Freq[0:half_length]) / signal_length
    Sig_Freq **= 2
    transform_len = len(Sig_Freq)
    if signal_length % 2:
        Sig_Freq[1:transform_len] *= 2
    else:
        Sig_Freq[1:transform_len-1] *= 2
    signal_power = 10 * np.log10(Sig_Freq)
    
    sig_audio = sig_audio[:15000]

    featureMFCC = mfcc(sig_audio, freq)
    print('\nMFCC:\nNumber of windows =', featureMFCC.shape[0])
    print('Length of each feature =', featureMFCC.shape[1])

    fb_feature = logfbank(sig_audio, freq)
    print('\nFilter bank\nWindow Count =', fb_feature.shape[0])
    print('Length of each feature =', fb_feature.shape[1])

    rec = sr.Recognizer()
    mic_test = sr.Microphone()
    sr.Microphone.list_microphone_names()
    with sr.Microphone(device_index=0) as source: 
        rec.adjust_for_ambient_noise(source, duration=7)
        print("Mic is on!!")
        audio = rec.listen(source)
    try:
        print("You said: \n" + rec.recognize_google(audio))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
