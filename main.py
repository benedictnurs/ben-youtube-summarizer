import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as yt
import requests



# uses regex
def get_video_id(url):
    pattern = r"(?<=v=)[a-zA-Z0-9_-]+(?=&|\?|$)"
    match = re.search(pattern, url)
    if match:
        return match.group()
    else:
        return None

# setup stuffs
st.set_page_config(
    page_title="Summary AI",
    page_icon="🤓",
)
st.title("Youtube Summarizer")
video_url = st.text_input("Enter YouTube link:")


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
API_TOKEN = st.secrets["API_TOKEN"]
#st.secrets["API_TOKEN"]

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
def remove_prefix(text, prefix):
    index = text.find(prefix)
    if index != -1:
        return text[index + len(prefix):]
    return text


# check url
if video_url:
    video_id = get_video_id(video_url)
    if video_id:
        try:
            transcript = yt.get_transcript(video_id)
            
            # make transcript
            transcript_text = ""
            for i in transcript:
                transcript_text += list(i.values())[0] + " "

            # display summary of transcript
            st.title("Summary:")
            command = f"Strictly only reply in a summary and summarize, {transcript_text} in a paragraph."
            output = query({
	            "inputs": command,
                
            })
            messy = "".join(list(output[0].values()))
            summary = remove_prefix(messy, "in a paragraph.")

            st.write(summary)
            
            # display transcript
            st.title("Transcript:")
            cols = st.columns(1)
            cols[0].write(transcript_text)
            css = '''
            <style>
                section.main>div {
                    padding-bottom: 1rem;
                }
                [data-testid="column"]>div>div>div>div>div {
                    overflow: auto;
                    height: 20vh;
                }
            </style>
            '''
            st.markdown(css)
        except Exception as e:
            st.error("Error")
    else:
        st.error("Invalid YouTube link.")
