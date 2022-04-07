#requires deepspeech model and scorer files, can be found at:
#https://deepspeech.readthedocs.io/en/r0.9/?badge=latest
#or by downloading with the following commands:
#curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
#curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer


import deepspeech
import recorder

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

    #recorder setup
    recorder = recorder.RecordingFile("recording", "wb", 2, 16000, 1024)

    def begin_record(self):
        self.recorder.start_recording()

    def end_recording(self):
        self.recorder.stop_recording()
        self.recorder.close()