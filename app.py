import streamlit as st
from utils import generate_gemini_blog,yt_transcript
from youtube_transcript_api import YouTubeTranscriptApi
possible =True




st.title("YouTube Transcript to Detailed Blog")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = youtube_link.split("=")
        try:
            # https://youtu.be/P3VErRW2HHY?si=6xYucgYF7ykYWrNI
            if video_id[0] != "https://www.youtube.com/watch?v":
                raise Exception
            video_id =video_id[1].split("&")[0]
        except:
            video_id =video_id[0].split("/")
            video_id =video_id[3].split("?")[0]
    except:
        st.write("This is not a youtube link")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except:
        st.write("video transcript not available !")
        possible =False
    

if possible and st.button("Get Detailed Blog"):
    transcript_text,count=yt_transcript(video_id)

    if transcript_text:
        blog=generate_gemini_blog(transcript_text,count)
        st.markdown("## Detailed Blog:")
        # st.write("Blog length"+f"{count}")
        st.write(blog)
