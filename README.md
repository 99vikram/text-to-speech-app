# Google Cloud Text-to-Speech App

This is a Text-to-Speech (TTS) application built with [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech) and [Streamlit](https://streamlit.io/). It allows you to convert text into speech using Google Cloud's TTS API and offers a user-friendly interface to select voice options.

## Prerequisites

Before running the app, you need the following:
- Google Cloud account with the Text-to-Speech API enabled
- Python 3.7 or higher
- Streamlit and other required libraries installed

## Setup and Installation

### 1. Clone the repository

Clone the repository to your local machine.

```bash
git clone https://github.com/99vikram/text-to-speech-app.git
cd text-to-speech-app
```

### 2. Set up Google Cloud Credentials
You must authenticate your app with Google Cloud.

- Go to Google Cloud Console.
- Create a project and enable the Text-to-Speech API.
- Download the Service Account Key JSON file from Google Cloud and place it in the project folder.
- Update the SERVICE_ACCOUNT_JSON path in the app.py to point to your Service Account Key file.

### 3. Install Dependencies
Create a virtual environment and install required Python packages.

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Running the App
To run the app, simply use the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server and open the app in your default web browser.


### 6. Usage
- Select the desired language, voice type, and gender.
- Enter text in the provided text area.
- Click Generate and Download Audio to create the audio file and play it in your browser.

### Notes:
- Ensure your Google Cloud API credentials are properly set up and accessible.
- The free-tier usage limits for Standard and WaveNet voices apply.
- The generated audio is available for download and playback.
- The app keeps track of usage and provides character limits for each voice type.

### Summary of Files
Repository structure looks something like this:

```bash
text-to-speech-app/
├── app.py            # Main Streamlit app
├── README.md         # Setup instructions
├── requirements.txt  # List of dependencies
└── usage.json        # Tracks character usage
```