import os
import json
import time
import pandas as pd
import streamlit as st
from google.cloud import texttospeech
from google.oauth2 import service_account

# Path to your service account JSON key
SERVICE_ACCOUNT_JSON = "/Users/vikramsingh/Downloads/lyrical-marker-440206-k4-f611918ec5d4.json"

# Free tier limits
FREE_TIER_LIMIT = {"Standard": 4_000_000, "WaveNet": 1_000_000}

# File to store character usage
USAGE_FILE = "usage.json"

# Load usage data
if os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, 'r') as f:
        character_count = json.load(f)
else:
    character_count = {"Standard": 0, "WaveNet": 0}

# Save usage data
def save_usage():
    with open(USAGE_FILE, 'w') as f:
        json.dump(character_count, f)

# Load Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_JSON)
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Load CSV with voice options
VOICE_DATA_FILE = "/Users/vikramsingh/Downloads/languages.csv"  # Update with actual path
languages_df = pd.read_csv(VOICE_DATA_FILE)
languages_df.columns = ['Index', 'Language', 'Voice_Type', 'Language_Code', 'Voice_Name', 'SSML_Gender', 'Sample']
languages_df = languages_df.iloc[1:].reset_index(drop=True).drop(columns=['Index', 'Sample'])

# Streamlit UI
st.title("Google Cloud Text-to-Speech")
st.write("Convert text to speech with Google Cloud TTS, choose from different voices and options.")

# Dropdown for selecting language
languages = sorted(languages_df['Language'].unique())
language = st.selectbox("Select Language", languages)

# Dropdown for selecting voice type
voice_types = ["Standard", "Premium"]
voice_type = st.selectbox("Select Voice Type", voice_types)

# Dropdown for selecting gender
genders = sorted(languages_df['SSML_Gender'].unique())
gender = st.selectbox("Select Gender", genders)

# Filter voices based on selection
filtered_voices = languages_df[
    (languages_df['Language'] == language) &
    (languages_df['Voice_Type'] == voice_type) &
    (languages_df['SSML_Gender'] == gender)
]
voice_names = filtered_voices[['Language_Code', 'Voice_Name']].reset_index(drop=True)

# Dropdown for selecting specific voice
voice = st.selectbox("Select Voice", voice_names['Voice_Name'])

# Display remaining characters
standard_remaining = max(4000000 - character_count.get("Standard", 0), 0)
wavenet_remaining = max(1000000 - character_count.get("WaveNet", 0), 0)
st.write(f"Remaining Characters: Standard: {standard_remaining} | WaveNet: {wavenet_remaining}")

# Text input
text = st.text_area("Enter Text", height=200)

# Button to generate and download audio
if st.button("Generate and Download Audio"):
    if text:
        try:
            # Check voice type
            selected_voice_type = "WaveNet" if voice_type == "Premium" else "Standard"

            # Update character count and check limits
            character_count[selected_voice_type] += len(text)
            if character_count[selected_voice_type] > FREE_TIER_LIMIT[selected_voice_type]:
                st.error(f"Exceeded free tier for {selected_voice_type} voices")
            else:
                # Synthesize speech
                synthesis_input = texttospeech.SynthesisInput(text=text)
                language_code = filtered_voices.iloc[0]['Language_Code']
                voice_name = voice
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code=language_code,
                    name=voice_name
                )
                audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

                response = client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice_params,
                    audio_config=audio_config
                )

                # Save audio file
                output_file = f"output_{selected_voice_type}_{int(time.time())}.mp3"
                with open(output_file, "wb") as out:
                    out.write(response.audio_content)

                # Save usage
                save_usage()

                # Provide download link
                st.audio(output_file, format="audio/mp3")
                st.success(f"Audio file generated successfully: {output_file}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display usage information
st.write(f"Usage data: Standard: {character_count['Standard']} | WaveNet: {character_count['WaveNet']}")
