import sys
import discord
import asyncio
import requests
import json


# -- if v3.0 or greater
if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen

channel_id = 'YOUTUBE CHANNEL ID HERE'
discord_channel_id = 'DISCORD CHANNEL ID HERE'
discord_key = 'DISCORD KEY HERE'
youtube_api_key = 'API KEY HERE'
client = discord.Client()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
hasInitRun = False
latest_URL = 'Initial URL Here'

def init():
    latest_URL = get_latest_video_in_channel(channel_id)
    hasInitRun = True;

def get_latest_video_in_channel(channel_id):
    api_key = youtube_api_key
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)

    video_links = ''
    url = first_url

    with urlopen(url) as url:
        inp = url.read()
        resp = json.loads(inp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_link = base_video_url + i['id']['videoId']
                break
    return video_link

async def background_loop(latest_URL):
    await client.wait_until_ready()
    if not hasInitRun:
        init()
    discord_channel = discord.Object(id=discord_channel_id)
    while not client.is_closed:
        new_URL = get_latest_video_in_channel(channel_id)
        if not latest_URL == new_URL:
            await client.send_message(discord_channel, new_URL)
            latest_URL = new_URL
        await asyncio.sleep(60)

client.loop.create_task(background_loop(latest_URL))
client.run(discord_key)
