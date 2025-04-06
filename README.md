# Sanki Music Bot

A Telegram bot that plays Spotify songs in VC using Pyrogram.

## Commands

- `/start` - Welcome message with buttons
- `/help` - Show bot commands
- `/play <song name>` - Play song from Spotify
- `/end` - Stop the music

## Hosting

1. Create `.env` file using config template.
2. Install requirements with: `pip install -r requirements.txt`
3. Run bot: `python3 bot.py`

## Docker

```bash
docker build -t sanki-bot .
docker run -it sanki-bot
