import speech_recognition as sr

# Set audio file path
audio_file = "audio.wav"

# Create a recognizer object
r = sr.Recognizer()

# Load audio file into AudioFile object
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)

    # Convert speech to text
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        text = ''  # Set text to empty string
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
        text = ''  # Set text to empty string

    # Check for abusive content in the text
    abusive = False
    if text and ('abuse' in text.lower() or 'hate' in text.lower() or 'threat' in text.lower()):
        abusive = True

    # Output result
    if abusive:
        print('Audio is abusive.')
    else:
        print('Audio is not abusive.')
