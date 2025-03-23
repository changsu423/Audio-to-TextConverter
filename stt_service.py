import os
from google.cloud import speech
from google.oauth2 import service_account
import io

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def transcribe_audio(audio_content, language_code="ko-KR"):
    """
    Transcribe audio to text using Google Cloud Speech-to-Text API.
    
    Args:
        audio_content (bytes): The audio file content
        language_code (str): The language code (default: Korean)
        
    Returns:
        str: The transcribed text
    """
    # Check if credentials file path is provided in environment variables
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not credentials_path:
        raise ValueError("Google Cloud credentials not found. Please set GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    
    # Initialize Speech-to-Text client
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = speech.SpeechClient(credentials=credentials)
    
    # Configure audio
    audio = speech.RecognitionAudio(content=audio_content)
    
    # Configure request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Adjust based on your audio sample rate
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="default",  # You can use "video" for better results with lectures
    )
    
    # Perform transcription
    response = client.recognize(config=config, audio=audio)
    
    # Extract results
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    return transcript.strip()

# Example usage:
if __name__ == "__main__":
    # Test with a sample audio file
    with open("sample.wav", "rb") as audio_file:
        content = audio_file.read()
        transcript = transcribe_audio(content)
        print(transcript)
