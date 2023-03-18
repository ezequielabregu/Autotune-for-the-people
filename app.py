
from distutils.log import debug
from fileinput import filename
from flask import * #Flask, send_file, render_template, request 

import librosa
from pathlib import Path
import soundfile as sf
import psola 
import numpy as np
import scipy.signal as sig
import os 

#audio_input = "voice.wav"
#key = 'C:min' 
 
app = Flask(__name__, template_folder='templates')  

#global filename
def fname():
    name = request.files['file']    
    return name 
#get the values from the slidedown menu
def key():
    key_select = request.form['key_select']
    mode_select = request.form['mode_select']
    key_menu = str(key_select + ":" + mode_select)
    #print(key_menu)
    return key_menu 

#home page
@app.route('/')  
def main():  
    return render_template('index.html',
                           data=[{'key': 'C'}, {'key': 'C#'}, {'key': 'D'}, {'key': 'D#'}, {'key': 'E'}, {'key': 'F'}, {'key': 'F#'}, {'key': 'G'}, {'key': 'G#'}, {'key': 'A'}, {'key': 'A#'}, {'key': 'B'}],
                           data1=[{'mode':'maj'}, {'mode':'min'}])

#file uploaded
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        f = fname()
        #f = request.files['file']
        f.save(f.filename)
        #run autotune main function
        main_at(f.filename)
        #remove audio after get the optput.wav
        os.remove(f.filename)
        return render_template("Acknowledgement.html", name = f.filename)
   
#file downloader
@app.route('/download', methods = ['GET'])
def download_file():
    return send_file("static/output.wav", as_attachment=True)

# audio player
@app.route("/audio")
def serve_audio():
    message = "Audio Route"
    return render_template('audio.html', message=message)

def correct(f0):
    #8) .isnan: Test element-wise for NaN and return result as a boolean array.
    # is a numeric data type used to represent any value that is undefined or unpresentable
    if np.isnan(f0):
        return np.nan
    #9) get the key degrees
    key_degrees = librosa.key_to_degrees(key())
    #10) .concatenate --> Join a sequence of arrays along an existing axis.
    key_degrees = np.concatenate((key_degrees, [key_degrees[0] + 12]))

    #11) convert hz to MIDI
    midi_note = librosa.hz_to_midi(f0)
    #12) calculate the degree of the MIDI note
    degree = midi_note % 12
    #13) find the closer degree in comparison with the key_degrees 
    # .argmin Returns the indices of the minimum values along an axis.
    closest_degree_id = np.argmin(np.abs(key_degrees - degree))
    #14) calculate the diference between the degree and the closest degree
    degree_diferrence = degree - key_degrees[closest_degree_id]

    #15) substract the MIDI note with the corrected
    midi_note -= degree_diferrence
    #16) convert MIDI to frequency
    return librosa.midi_to_hz(midi_note)


def correct_pitch(f0):
    #7) .zeros_like: Return an array of zeros with the same shape and type as a given array.
    corrected_f0 = np.zeros_like(f0)
    #8) iteration: .shape->returns a tuple with each index having the number of corresponding elements
    for i in range(f0.shape[0]):
        corrected_f0[i] = correct(f0[i])
    #17) smooth the correction with a median filter (smooth correction over the time)
    #.medfilt--> Perform a median filter on an N-dimensional array.
    smoothed_corrected_f0 = sig.medfilt(corrected_f0, kernel_size=11)
    #18) preserve the NaN, ???
    smoothed_corrected_f0[np.isnan(smoothed_corrected_f0)] = corrected_f0[np.isnan(smoothed_corrected_f0)]

    return smoothed_corrected_f0

def autotune(y, sr):
    #--------[1]. TRACK PITCH
    #analisys windows size
    frame_length = 2048
    # number of audio samples between adjacent pYIN predictions ???
    hop_length = frame_length // 4
    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C7')
    #6) pitch detection
    f0, _, _ =librosa.pyin(y, 
                  frame_length=frame_length,
                  hop_length=hop_length,
                  sr=sr,
                  fmin=fmin,
                  fmax=fmax)

    #-----------[2] CALCULATE DESIRE PITCH
    corrected_f0 = correct_pitch(f0)

    #-----------[3]. pitch shifting
    return psola.vocode(y, sample_rate=int(sr), target_pitch=corrected_f0, fmin=fmin, fmax=fmax)

def main_at(audio_input):
    #1) load the audio file input
    y, sr = librosa.load(audio_input, sr=None, mono=False)
    #2) process only one channel
    #n dim = from numpy library ---> number of array dimensions
    #if the audio input is stereo, use only one channel
    if y.ndim > 1:
        y = y[0, :]

    #3) call the autotune
    pitch_corrected_y = autotune(y, sr)

    #4) audio output path
    filepath = Path(audio_input)
    output_filepath = filepath.parent / (filepath.stem + "_pitch_corrected" + filepath.suffix)
    #5) soundfile lib ---> .write the file pitch corrected 
    sf.write("static/output.wav", pitch_corrected_y, sr)
    #sf.write(str(output_filepath), pitch_corrected_y, sr)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
#    app.run(debug=True)
        