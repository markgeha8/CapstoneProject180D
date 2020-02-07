#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:24:33 2020

@author: qz
"""

from __future__ import division

import re
import sys

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Undercooked-90c83dcc7c9c.json"

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from gameenums import VoiceCommand, Ingredient
import threading

# Audio recording parameters
global transcript
currentVoice = VoiceCommand.NONE
newVoice = False
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def setVoice(trofa):
    global newVoice

    newVoice = trofa

def listen_print_loop(responses, num):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript
        #print('\n text = ', transcript)
        #print('loop')
        
        
        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)
            print()

        else:
            spokenWord = transcript + overwrite_chars
            if(spokenWord == "plate" or spokenWord == " plate"):
                tempVoice = VoiceCommand.PLATE
            elif(spokenWord == "submit" or spokenWord == " submit"):
                tempVoice = VoiceCommand.SUBMIT
            elif(spokenWord == "trash" or spokenWord == " trash"):
                tempVoice = VoiceCommand.TRASH
            elif(spokenWord == "rice" or spokenWord == " rice"):
                tempVoice = Ingredient.RICE
            elif(spokenWord == "fish" or spokenWord == " fish"):
                tempVoice = Ingredient.FISH
            elif(spokenWord == "seaweed" or spokenWord == " seaweed"):
                tempVoice = Ingredient.SEAWEED
            elif(spokenWord == "lettuce" or spokenWord == " lettuce"):
                tempVoice = Ingredient.LETTUCE
            elif(spokenWord == "tomato" or spokenWord == " tomato"):
                tempVoice = Ingredient.TOMATO
            else:
                tempVoice = VoiceCommand.NONE
            
            setCurrentVoice(tempVoice)
            setVoice(True)

            

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break
            
            num_chars_printed = 0
            
       
def RunVoice():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    global currentVoice

    language_code = 'en-US'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    num=0
    
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        
        num = num+1
        #print('num=', num)
        # Now, put the transcription responses to use.
        
        listen_print_loop(responses,num)

def setCurrentVoice(tempVoice):
    global currentVoice

    currentVoice = tempVoice

if __name__ == '__main__':
    RunVoice()