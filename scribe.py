#requires deepspeech model and scorer files, can be found at:
#https://deepspeech.readthedocs.io/en/r0.9/?badge=latest
#or by downloading with the following commands:
#curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
#curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer


import deepspeech
import recorder
import wave
import numpy
import tkinter
from tkinter.font import NORMAL
from tracemalloc import start

class scribe():

    #path variables for model and scorer files
    model_file_path = "Resources\deepspeech-0.9.3-models.pbmm"
    scorer_file_path = "Resources\deepspeech-0.9.3-models.scorer"

    #stt setup
    model = deepspeech.Model(model_file_path)
    model.enableExternalScorer(scorer_file_path)

    lm_alpha = 0.75
    lm_beta = 1.85
    model.setScorerAlphaBeta(lm_alpha, lm_beta)

    beam_width = 500
    model.setBeamWidth(beam_width)

    def begin_record(self):
        self.recorder.start_recording()

    def end_recording(self):
        self.recorder.stop_recording()
        self.recorder.close()

    def process_recording(self):
        #wave file setup
        filename = self.recorder.fname
        w = wave.open(filename, "r")
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)

        #convert buffer to 16 bit array
        data16 = numpy.frombuffer(buffer, dtype=numpy.int16)

        #process text
        self.result_text = self.model.stt(data16)

        
    def begin_helper(self, start_button, end_button):
        #recorder setup
        #set channel count to 1 for bluetooth mic, 2 for laptop mic
        self.recorder = recorder.RecordingFile("ScribeRecording.wav", "wb", 1, 16000, 1024)

        #call scribe function
        self.begin_record()

        #update button states
        start_button["state"] = tkinter.DISABLED
        end_button["state"] = tkinter.NORMAL
        

    def end_helper(self, start_button, end_button, text_box):
        #call scribe function
        self.end_recording()

        #update button states
        start_button["state"] = tkinter.NORMAL
        end_button["state"] = tkinter.DISABLED

        #process audio
        self.process_recording()

        #add text from audio stt to text box
        result = self.result_text
        text_box.insert("1.0", result)


    def setup_window(self):
        #setup tkinter window
        self.window = tkinter.Tk()
        self.window.title("StageScribe")

        #setup text box
        text = tkinter.Text(self.window, height=8)
        text.pack()

        #setup buttons
        start_record_button = tkinter.Button(self.window, text="Begin Recording", command=lambda: self.begin_helper(start_record_button, end_record_button))
        end_record_button = tkinter.Button(self.window, text="End Recording", command=lambda: self.end_helper(start_record_button, end_record_button, text))

        start_record_button.pack()
        end_record_button.pack()

        end_record_button["state"] = tkinter.DISABLED