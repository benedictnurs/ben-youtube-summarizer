import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as yt


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

            # display transcript
            st.title("Transcript")
            cols = st.columns(1)
            cols[0].write(transcript_text)
            css = '''
            <style>
                section.main>div {
                    padding-bottom: 1rem;
                }
                [data-testid="column"]>div>div>div>div>div {
                    overflow: auto;
                    height: 25vh;
                }
            </style>
            '''
            st.markdown(css, unsafe_allow_html=True)
        except Exception as e:
            st.error("Error")
    else:
        st.error("Invalid YouTube link.")
