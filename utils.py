import os
from dotenv import load_dotenv
load_dotenv() ##load all the nevironment variables
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def yt_transcript(youtube_video_url):
    try:
        video_id_and_list=youtube_video_url.split("=")[1]
        video_id =video_id_and_list.split("&")[0]
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            transcript_text =transcript.translate('en').fetch()
    

        transcript = ""
        count =0
        for i in transcript_text:
            transcript += " " + i["text"]
            count+=1

        return transcript,count

    except Exception as e:
        raise e


def generate_gemini_blog(transcript_text,count):
    if count>1500:
        count=1500
    prompt=f"""
    You are a content writer. Write detailed blog posts for technical domains.
    You will be taking the transcript and writing a useful blog for the transcript 
    without leaving a single point. Include code examplesif the transcript contains 
    code examples. Write a blog post of {count} size in multi-paragraph format.Make sure it is easy to understand,
    to the point, and valuable.
    It most be educational video transcript otherwise write 'It is not a educational video'
    """
    model=genai.GenerativeModel("gemini-pro")
    generation_config = genai.GenerationConfig(
    temperature=0,
    )
    try:
        response=model.generate_content(contents =prompt+transcript_text,generation_config=generation_config)
        response =response.text
    except:
        response ="This video blog might not be possible."
    return response




