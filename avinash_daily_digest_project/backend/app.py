
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, random, os

API_KEY = os.getenv("YOUTUBE_API_KEY", "PASTE_YOUR_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CHANNELS = ["Bloomberg","CNBC","Reuters","WSJ","CBC News","Financial Times","NDTV","India Today","CNBC Awaaz","Al Jazeera English"]
TOPICS = ["Canada economy","Canada politics","US economy","US politics","India economy","India politics","global markets","world news"]

@app.get("/digest/{count}")
def get_digest(count:int):
    videos=[]
    for _ in range(count):
        query=random.choice(TOPICS)+" "+random.choice(CHANNELS)
        url="https://www.googleapis.com/youtube/v3/search"
        params={"part":"snippet","q":query,"type":"video","maxResults":1,"order":"date","key":API_KEY}
        r=requests.get(url,params=params).json()
        if "items" in r and len(r["items"])>0:
            item=r["items"][0]
            vid=item["id"]["videoId"]
            videos.append({"title":item["snippet"]["title"],"channel":item["snippet"]["channelTitle"],"url":f"https://youtube.com/watch?v={vid}"})
    return {"title":"Avinash’s Daily Digest","videos":videos}
