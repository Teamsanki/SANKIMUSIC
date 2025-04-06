from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from config import *

import asyncio
import requests

# Setup Pyrogram user client with string session
user = Client(
    name="sanki_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION  # from config.py
)

# Setup VC client
vc = PyTgCalls(user)

# Spotify setup
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@bot.on_message(filters.command("start"))
async def start(_, message):
    user = message.from_user
    log_text = f"✨ **New /start**\n\n👤 Name: [{user.first_name}](tg://user?id={user.id})\n🆔 ID: `{user.id}`"
    await bot.send_message(LOGGER_GROUP_ID, log_text)

    await message.reply_photo(
        photo=TELEGRAPH_PHOTO,
        caption="**Welcome to Sanki Music Bot!**\n\nUse `/play <song>` to play music from Spotify in VC.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Owner", url=OWNER_LINK)],
            [InlineKeyboardButton("Help", callback_data="help")],
            [InlineKeyboardButton("Support", url=SUPPORT_LINK)]
        ])
    )

@bot.on_chat_member_updated()
async def added_to_group(_, chat_member):
    if chat_member.new_chat_member.user.is_self:
        chat = chat_member.chat
        link = f"https://t.me/c/{str(chat.id)[4:]}" if str(chat.id).startswith("-100") else "No Link"

        log_text = f"🚀 **Bot Added to New Group**\n\n🏷️ Group: `{chat.title}`\n🆔 ID: `{chat.id}`\n🔗 Link: {link}"
        await bot.send_message(LOGGER_GROUP_ID, log_text)

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

    response = requests.get(preview_url)
    file_path = f"{title}.mp3"
    with open(file_path, 'wb') as f:
        f.write(response.content)

    try:
        await vc.join_group_call(
            message.chat.id,
            AudioPiped(file_path),
            stream_type='local_stream'
        )
        await message.reply(f"Now Playing: **{title}** by **{artist}**")

        log_text = (
            f"🎶 **Song Played**\n\n"
            f"👤 User: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
            f"🆔 User ID: `{message.from_user.id}`\n"
            f"🎵 Song: **{title}** by **{artist}**\n"
            f"🏷️ Group: `{message.chat.title}`\n"
            f"🆔 Group ID: `{message.chat.id}`"
        )
        await bot.send_message(LOGGER_GROUP_ID, log_text)

    except Exception as e:
        await message.reply(f"Failed to join VC: `{e}`")

@bot.on_message(filters.command("end") & filters.group)
async def end(_, message):
    try:
        await vc.leave_group_call(message.chat.id)
        await message.reply("Music stopped.")
    except Exception as e:
        await message.reply(f"Error: `{e}`")

# Start the bot
async def main():
    await user.start()
    await vc.start()
    await bot.start()
    print("Bot is running...")
    await idle()

import asyncio
asyncio.run(main())
