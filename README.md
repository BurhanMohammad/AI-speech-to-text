# Audio Transcription API

This Flask API allows users to transcribe audio files and generate response audio based on the transcription. It provides authentication using JWT tokens and authorization based on user roles.

## Getting Started

To get started with using this API, follow the instructions below:

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the Flask application using `python app.py`.
4. Use the provided endpoints to interact with the API.

## Endpoints

### Authentication: /login

#### Description

This endpoint allows users to authenticate and obtain a JWT token.

#### Request

- Method: POST
- URL: `/login`
- Headers:
  - Content-Type: application/json

##### Request Body

```json
{
    "username": "admin",
    "password": "admin"
}
```
#### response
- status code : 200 OK
- Body
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoidXNlciJ9.LhQwMXL9yYV5V2DMonBhh7otVC1k2XfA3f5S3JPNKOM"

}
```

# Audio Transcription: /transcribe

##Description

This endpoint transcribes the provided audio file and generates response audio based on the transcription.

#### Request

- Method: POST
- URL: `/transcribe`
- Headers:
  - Authorization: Bearer '<token>'
- Body: Form data with a file field named 'file'



#### response
- status code : 200 OK
- Body
```json
{
    "transcription": "This is the transcribed text.",
    "response_audio": "uploads/response.mp3"
}
```

### Usage Examples

##### Authentication
```json
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}'

```

##### Audio Transcription

```json
curl -X POST http://localhost:5000/transcribe -H "Authorization: Bearer <token>" -F "file=@/path/to/audio/file"


```

Replace <token> with the JWT token obtained from the authentication endpoint and '/path/to/audio/file' with the path to the audio file to transcribe.

#### Error Handling

The API returns appropriate error responses with details in case of invalid requests or unauthorized access.

### Deployment on Google Cloud Platform
#### Google Cloud Platform (GCP) Setup:
- Create a new project in the Google Cloud Console.
- Enable the necessary APIs (Cloud Speech-to-Text, Text-to-Speech).
- Set up authentication for your project (service account).

#### Deployment:
- Deploy your Flask application on Google App Engine or Google Kubernetes Engine.
- Ensure your application is accessible over HTTP or HTTPS.


