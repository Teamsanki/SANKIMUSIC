from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pytgcalls.types.input_stream.input_file import InputAudioFile
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from config import *

import asyncio
import requests

# Bot and User Clients
bot = Client("sanki_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("sanki_user", api_id=API_ID, api_hash=API_HASH, session_string=USER_SESSION)

# VC Client
vc = PyTgCalls(user)

# Spotify Setup
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_photo(
        photo=TELEGRAPH_PHOTO,
        caption="**Welcome to Sanki Music Bot!**\n\nUse `/play <song>` to play music from Spotify in VC.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Owner", url=OWNER_LINK)],
            [InlineKeyboardButton("Help", callback_data="help")],
            [InlineKeyboardButton("Support", url=SUPPORT_LINK)]
        ])
    )

@bot.on_callback_query(filters.regex("help"))
async def help_cb(_, query):
    await query.message.edit_text("**Available Commands:**\n\n/play <song name> - Play song from Spotify\n/end - Stop the music")

@bot.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a song name.")
    
    song_name = message.text.split(None, 1)[1]
    results = sp.search(q=song_name, type='track', limit=1)

    if not results['tracks']['items']:
        return await message.reply("No song found on Spotify.")

    track = results['tracks']['items'][0]
    title = track['name']
    artist = track['artists'][0]['name']
    preview_url = track['preview_url']

    if not preview_url:
        return await message.reply("Spotify preview not available for this song.")

    # Download preview
    response = requests.get(preview_url)
    file_path = f"{title}.mp3"
    with open(file_path, 'wb') as f:
        f.write(response.content)

    chat_id = message.chat.id

    try:
        await vc.join_group_call(
    chat_id,
    InputStream(
        InputAudioStream(
            InputAudioFile(file_path)
        )
    ),
    stream_type='local_stream'
)
        await message.reply(f"Now Playing: **{title}** by **{artist}**")
    except Exception as e:
        await message.reply(f"Failed to join VC: `{e}`")

@bot.on_message(filters.command("end") & filters.group)
async def end(_, message):
    try:
        await vc.leave_group_call(message.chat.id)
        await message.reply("Music stopped.")
    except Exception as e:
        await message.reply(f"Error: `{e}`")

async def main():
    await user.start()
    await vc.start()
    await bot.start()

    print("Bot is running...")
    await asyncio.get_event_loop().run_forever()

import asyncio
asyncio.run(main())
