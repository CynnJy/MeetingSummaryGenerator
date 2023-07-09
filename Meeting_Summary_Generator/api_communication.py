import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time

# Endpoint for Upload & Transcript
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

# API KEY for Header
headers = {'authorization': API_KEY_ASSEMBLYAI}

# Upload the audio file
def uploadAudio(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url = upload_response.json()['upload_url']
    return audio_url


# Transcript the audio file
def transcribe(audio_url):
    transcript_request = { 
        "audio_url": audio_url
        }
    transcript_headers = {
        'authorization': API_KEY_ASSEMBLYAI,
        "content-type": "application/json"}

    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=transcript_headers)

    job_id = transcript_response.json()['id']
    return job_id


# Pass the Transcript.json as ID to Poll the result of transcript
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers) # Ask for information

    return polling_response.json()

# Generate the transcription 
def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        
        if data['status'] == 'completed':
            return data['text'], None

        elif data['status'] == 'error':
            print("Error!!")
            return data, data['error']

        print('Waiting 30 seconds ...')
        time.sleep(30)