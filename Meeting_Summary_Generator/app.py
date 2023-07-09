from flask import Flask, render_template, request, redirect
from summary import Sumarizer
from api_communication import *
import os


app = Flask(__name__)

# Target Folder for save the Upload File
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'audio_uploaded/')

@app.route("/")
def index():
    return render_template('index.html')

# Function : Upload The File and Save in Local Folder
@app.route("/upload", methods=['POST', 'GET'])
def upload():

    # If System Unable to Find the Target Folder
    # System Create A New Folder
    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files.get('file')
    filename = file.filename

    if file.filename == '':
        err_msg = "No file is uploaded"
        return redirect('index.html')
    else:
        # The Upload File Saved in The Target Folder
        # Display An Sucess Message
        destination = "/".join([target, "meeting.wav"])
        file.save(destination)
        msg = filename + " Is Success upload"
        
    return render_template('summary.html', upload_msg=msg)


# Function : Summarization The Audio File
@app.route("/summary", methods=['POST', 'GET'])
def summary():
    if request.method=="POST":

        # Detect the Audio File
        filename =  target + '/meeting.wav'

        # Process Speech-to-Text
        audio_file = uploadAudio(filename)
        data, error = get_transcription_result_url(audio_file)

        # If Detect Data, Pass Data to Summary Function
        if data:
            print(data)
            summaryOutput = Sumarizer.summary(data)

        return render_template('summary.html', result=summaryOutput)
    else:
        return render_template('summary.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # app.run()
