from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import jwt

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'your_secret_key' 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Mock user data for demonstration purposes
USERS = {
    'admin': {
        'password': 'admm',
        'role': 'admin'
    },
    'user': {
        'password': 'user',
        'role': 'user'
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def authenticate(username, password):
    if username in USERS and USERS[username]['password'] == password:
        return USERS[username]

def authorize(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return jsonify(error='Authorization header is missing'), 401

            token = request.headers['Authorization'].split()[1]
            try:
                decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                if decoded_token['role'] != role:
                    return jsonify(error='Unauthorized access'), 403
            except jwt.ExpiredSignatureError:
                return jsonify(error='Token has expired'), 401
            except jwt.InvalidTokenError:
                return jsonify(error='Invalid token'), 401

            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username, password)
    if user:
        token = jwt.encode({'username': username, 'role': user['role']}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify(token=token), 200
    return jsonify(error='Invalid username or password'), 401


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the audio file (transcription and response generation)
        transcription = transcribe(filepath)
        response_audio = generate_response_audio(transcription)
        
        return jsonify(transcription=transcription, response_audio=response_audio)

    return jsonify(error="File type not allowed"), 400

from google.cloud import speech, texttospeech

def transcribe(filepath):
    client = speech.SpeechClient()
    with open(filepath, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript

def generate_response_audio(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'response.mp3')
    with open(audio_filepath, "wb") as out:
        out.write(response.audio_content)
    return audio_filepath


@app.route('/')
def index():
    return """
    <h1>API Documentation</h1>
    <p>Visit /login to authenticate and obtain a JWT token.</p>
    <p>After authentication, use the obtained token in the Authorization header as Bearer token.</p>
    <p>Visit /transcribe to transcribe audio. Send a POST request with an audio file in the body.</p>
    """


if __name__ == '__main__':
    app.run(debug=True)
