import requests
# import aria2p
from datetime import datetime
# from status import format_progress_bar
import asyncio
import os, time
import logging
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lazydeveloper.lazyprogress import progress_for_pyrogram
from plugins.utitles import Mdata01
from lazydeveloper.thumbnal import extract_thumbnail
from lazydeveloper.ffmpeg import take_screen_shot, fix_thumb
import random
from config import *
from pyrogram import enums
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

from urllib.parse import urlparse
sticker_set = ("CAACAgUAAxkBAAEVrQVnaVjyi7aC6Uzm2hroGb4u832GqwACWAcAAln00VUhdUzK3V0cvDYE CAACAgIAAxkBAAEVrR1naVxRD_oDzi5HekutpX2v1tIlqwAC4wUAAj-VzArYM62l0j-1NDYE CAACAgIAAxkBAAEVrTVnaWP1Fro-Q4gxV4mFRioJbhDX6gACrA0AAuJ8CEocdg_Chn4uTzYE CAACAgIAAxkBAAEVrTdnaWQMR7rnojwn53eOpkM_-Hb8SwACnQ4AAhgmQEguU6H7fNBriTYE CAACAgIAAxkBAAEVrTlnaWQgksf4dBUQae9V4urU7muZUwACZQ0AAulzQEj7mSnMOJpDMTYE CAACAgIAAxkBAAEVrT1naWQ0tB8d6_jv18xEkDvzQTe7fAACtg8AAmvTQEhGlrVX_UMWpDYE CAACAgIAAxkBAAEVrUFnaWRdgff0EQABzFLDVVkOI7tTNMYAAh8RAAKUIAlKz5TAFyAt3Qk2BA CAACAgIAAxkBAAEVrUNnaWRvH8S2p7tOAz6Zb2WKfQvWKgACEwwAAuLLQEgKFkvFN8GyMjYE CAACAgIAAxkBAAEVrUVnaWSBAWVWpmUckS2TEzPhXAr9ggACdQwAAvIBQUiWfrY76Av8aTYE CAACAgIAAxkBAAEVrUdnaWSSjjN433lIpjulonJCMsnyHAACeQwAAqGuQEjW9dENyNgsjDYE CAACAgIAAxkBAAEVrUlnaWSuvK33pJHV2Ao36v2tkPWzdgACWw0AAi8FQUhX8JOWWFWgEzYE CAACAgIAAxkBAAEVrUtnaWS_zaZv7kZrpXdSMWucwfemRwACLQ8AAiQRQUhlbbUC1Bt3HDYE CAACAgIAAxkBAAEVrU1naWTQGZ5D8vGyLwHBjxCzZBMpFQACAgsAAshkSUi_XVq9k7CVPzYE CAACAgIAAxkBAAEVrU9naWTjuM7LkFgX_8jIkigGZAAByQAD9gwAAk3XQEgYd1HmQDgEkDYE CAACAgIAAxkBAAEVrVFnaWTxRGw9xFeGwnRplqeSK5oCEwACBhAAAkAnQUh4teLKJ4bbojYE CAACAgIAAxkBAAEVrVVnaWUMLUvPYXjtBC8zjUtksHoUmQACLQ0AAqxWQUgMdsTbI544PjYE CAACAgIAAxkBAAEVrVdnaWUfxDoxsMDheWwpS-gTfXsM8gACtgwAAqqLQUgSw1FxjYwyvTYE CAACAgIAAxkBAAEVrVlnaWUzkw1ia3CEI4Bc1h8YTCeVLwACGQ8AAgWCQEjWQ4L7-Mn90zYE CAACAgIAAxkBAAEVrVtnaWVIot0sGPvUAz__gh0UNAtVDwACQREAAgNOCUp9w1-UJunSCTYE CAACAgIAAxkBAAEVrV1naWVZPz2Ksyl6CIrrTUEj3aKdJQACewwAAstzAUoR5G-nya3XVjYE CAACAgIAAxkBAAEVrV9naWWsRNY6IHpRRXzdnnLUcATDBwAC8A4AAp3MCEphNwfqbKoeLTYE CAACAgIAAxkBAAEVrTVnaWP1Fro-Q4gxV4mFRioJbhDX6gACrA0AAuJ8CEocdg_Chn4uTzYE CAACAgIAAxkBAAEVrWVnaWXRyrYxWiGz5dN8xkvFBug6sgACxg4AApXLQEqNb_xqmLajBDYE CAACAgIAAxkBAAEVrWlnaWYoll5RfYtgJgtfsRFw7qqneAACBAEAAladvQreBNF6Zmb3bDYE CAACAgIAAxkBAAEVrW1naWZID5jRvKJgWgkwhtR65XRF_QAC6AoAAu6g8Ui8gw9lugYjxTYE")
lazystickerr = sticker_set.split()
lazysticker = random.choice(lazystickerr)

def extract_short_url(url):
    """
    Extracts the short URL (identifier) from a given TeraBox URL.

    Args:
        url (str): The TeraBox URL.

    Returns:
        str: The short URL (identifier).
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract the path and split to get the last part
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) > 1 and path_parts[0] == "s":
        return path_parts[1]
    return None

async def new_progress_for_pyrogram(current, total, message, start_time):
    now = time.time()
    diff = now - start_time
    if round(diff % 10.00) == 0 or current == total:
        percentage = (current / total) * 100
        speed = current / diff  # Bytes per second
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(diff))
        estimated_total_time = time.strftime("%H:%M:%S", time.gmtime(total / speed)) if speed > 0 else "--:--:--"
        progress_text = (
            f"<b>🍟Saving your file to the server...</b>\n"
            f"<code>{current / 1024:.2f} KB / {total / 1024:.2f} KB</code>\n"
            f"<i>Progress:</i> {percentage:.2f}%\n"
            f"<i>Speed:</i> {speed / 1024:.2f} KB/s\n"
            f"<i>Elapsed:</i> {elapsed_time}\n"
            f"<i>ETA:</i> {estimated_total_time}"
        )
        try:
            await message.edit_text(progress_text)
        except Exception as e:
            print(f"Progress update error: {e}")

import aiohttp

async def download_file(url, dest_path, current_size, file_size, start_time, progress_message2, filename):
    chunk_size = 5 * 1024 * 1024  # 1 MB
    if isinstance(file_size, str):
        file_size = int(file_size)
        
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(dest_path, 'wb') as file:
                while chunk := await response.content.read(chunk_size):
                    file.write(chunk)
                    current_size += len(chunk)
                    if isinstance(current_size, str):
                        current_size = int(current_size)

                    await progress_for_pyrogram(current_size, file_size, "<blockquote>♻ ᴜᴘʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ ᴛᴏ sᴇʀᴠᴇʀ</blockquote>\n<blockquote><code>{filename}</code></blockquote>", progress_message2, start_time)



async def download_from_terabox(client, message, url, platform):
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    progress_message2 = await message.reply("<i>⚙ ᴘʀᴇᴘᴀʀɪɴɢ\nᴀɴᴀʟʏsɪɴɢ yᴏᴜʀ ᴜʀʟ...</i>")
    TEMP_DOWNLOAD_FOLDER = f"./downloads/{message.from_user.id}/{time.time()}"
    if not os.path.exists(TEMP_DOWNLOAD_FOLDER):
        os.makedirs(TEMP_DOWNLOAD_FOLDER)
    # Using the temporary download folder
    destination_folder = TEMP_DOWNLOAD_FOLDER
    # -------------------------------------
    # -------------------------------------
    # -------------------------------------
    short_url = extract_short_url(url)
    print(f"Extracted Short URL: {short_url}")
    
    try:
        response = requests.get(f"https://terabox.hnn.workers.dev/api/get-info?shorturl={short_url}")
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            await progress_message2.edit(f"Hey, {message.from_user.mention} ! We are temporarily rate limited (<b>server down 😢</b>). Check back later once traffic has gone down... \n<b><u>⏳MAX-WAIT-TIME : 5 Hours</u></b>\n<blockquote><b>Powered by @LazyDeveloperr<b></blockquote>")
            await message.reply_sticker("CAACAgIAAxkBAAEVrSNnaV06VH29ak8TEcli6IL7AAHQNO8AAgwBAAJWnb0Kqm_10kDc4j02BA")
            return
    except Exception as lazydeveloepr:
        print(lazydeveloepr)

    if data.get("ok") and "list" in data and len(data["list"]) > 0:
        video_info = data["list"][0]
        video_title = video_info.get("filename", "Untitled Video")
        video_size = int(video_info.get("size", 0))
        fs_id = video_info.get("fs_id")
        shareid = data.get("shareid")
        uk = data.get("uk")
        sign = data.get("sign")
        timestamp = data.get("timestamp")

        # Format the file size (human-readable)
        def format_file_size(size):
            units = ['B', 'KB', 'MB', 'GB', 'TB']
            unit_index = 0
            while size >= 1024 and unit_index < len(units) - 1:
                size /= 1024
                unit_index += 1
            return f"{size:.2f} {units[unit_index]}"

        file_size = format_file_size(video_size)

        # Notify user with file details
        file_info_message = (
            f"<blockquote><b>🎉ᴜʀʟ ꜰᴇᴛᴄʜᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ🎊</b></blockquote>\n"
            f"<blockquote><b>🎥ᴠɪᴅᴇᴏ ᴛɪᴛʟᴇ::</b> {video_title}\n"
            f"<b>🧵ꜰɪʟᴇ ꜱɪᴢᴇ:</b> {file_size}</blockquote>\n"
            "<blockquote>👆👇</blockquote>\n"
            "<blockquote><b><u><i>⏳ᴛʀʏɪɴɢ ᴛᴏ ꜰᴇᴛᴄʜ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ...</i></u></b></blockquote>"
        )
        await progress_message2.edit_text(file_info_message)
        load_link_stick = await message.reply_sticker("CAACAgUAAxkBAAEVrQtnaVkmz__5DuSrlPdFl1TkhI8bCgACKwADvJY1KvfgJFBaB4jENgQ")
        
        # api
        api_url = "https://terabox.hnn.workers.dev/api/get-download"

        # Payload
        payload = {
            "fs_id": fs_id,
            "shareid": shareid,
            "sign": sign,
            "timestamp": timestamp,
            "uk": uk
        }

        # Headers
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # Send POST Request
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            # Parse JSON Response
            data = response.json()
            if data.get("ok"):
                await load_link_stick.delete()
                # await asyncio.sleep(1)
                download_link = data["downloadLink"]
                shortlink = download_link[:190]
                await progress_message2.edit(f"<blockquote><b>🎉 ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ... </b></blockquote>\n<blockquote>🎯: {shortlink}... 🥂 </blockquote>")
                got_stick = await message.reply_sticker("CAACAgUAAxkBAAEVrSdnaV-YAAHTHFqUohHpJp6TQbF5ghoAAiwAA7yWNSr8WI87aGngHjYE")

                # 
                # response = requests.get(download_link, stream=True)
                # response.raise_for_status()
                video_filename = os.path.join(destination_folder, video_title)  # Define the path to save the file
                # 
                # file_size = int(response.headers.get('content-length', 0))
                current_size = 0
                start_time = time.time()
               
                # with open(video_filename, "wb") as file:
                #    for chunk in response.iter_content(chunk_size=128):  # Save in chunks
                #        file.write(chunk)
                #        current_size += len(chunk)
                #        await progress_for_pyrogram(current_size, file_size, "Uploading file to server", progress_message2, start_time)
                await asyncio.sleep(2)
                await got_stick.delete()
                uploding_stick = await message.reply_sticker("CAACAgUAAxkBAAEVrQdnaVkVUQllH2VoGMkUgtEKgcf_qAACKQADvJY1KhDT2MoRzkuCNgQ")
                await download_file(download_link, video_filename, current_size, video_size, start_time, progress_message2, video_title)
                await uploding_stick.delete()
                
                
                download_stick = await message.reply_sticker(lazysticker)
                #======================================
                bot_username = client.username if client.username else "👩‍💻ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʟᴀᴢʏᴅᴇᴠᴇʟᴏᴘᴇʀ"
                caption_lazy = f"ᴡɪᴛʜ❤@{bot_username}"
                caption = video_title if video_title else "===========🍟==========="
                while len(caption) + len(caption_lazy) > 1024:
                    caption = caption[:-1]  # Trim caption if it's too long
                log_cap = f'<b><a href="{url}">{video_title}</a>'
                caption = f'<b><a href="{url}">{video_title}</a>\n\n<blockquote>{caption_lazy}</blockquote></b>'
 
                #====================================== 
                xlx = await progress_message2.edit_text("⚡ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ꜰɪʟᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ...")
                start_time = time.time()

                width, height, duration = await Mdata01(video_filename)
                print(f"w-{width}===>h-{height}===>d-{duration}")
                try:
                    ph_path_ = await take_screen_shot(video_filename, os.path.dirname(os.path.abspath(video_filename)), random.randint(0, duration - 1))
                    ph_path = await fix_thumb(ph_path_)
                except Exception as e:
                    ph_path = None
                    print(e)
               # width, height, duration = await Mdata01(video_filename)
                succ = await client.send_video(
                    message.chat.id,
                    video_filename,
                    caption=caption,
                    duration=duration,
                    width=width,
                    thumb=ph_path,
                    height=height,
                    parse_mode=enums.ParseMode.HTML,
                    supports_streaming=True,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        f"<blockquote>🍟ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ.</blockquote>\n<blockquote>📽<code>{caption}</code></blockquote>",
                        xlx,
                        start_time,
                    )
                )

                # -----------------------------------
                # -----------------------------------
                await xlx.delete()
                await download_stick.delete()
                sticker_message = await message.reply_sticker("CAACAgUAAxkBAAEVrQlnaVkcs_0t3ERo7U25A0YdCaY2oQACKgADvJY1KsIyiYK2RJbrNgQ")
                if succ:
                    # Send the video to the log channel with details
                    caption = (
                            f"<b>📂 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜰᴏʀ ᴜsᴇʀ... ❤</b>"
                            f"<blockquote><b>📽{log_cap}</b></blockquote>\n"
                            f"<blockquote>👤 <b>ᴜsᴇʀ ɪᴅ:</b> <code>{message.from_user.id}</code></blockquote>\n"
                            f"<blockquote>📩 <b>ɴᴀᴍᴇ:</b> {message.from_user.mention}</blockquote>\n"
                            f"<blockquote>🔗 <b>ᴜʀʟ:</b> {url}</blockquote>\n"
                            "💘\n"
                            f"<blockquote><b>🦋 ᴘᴏᴡᴇʀᴇᴅ ʙʏ <a href='https://t.me/LazyDeveloperr'> ʟᴀᴢʏᴅᴇᴠᴇʟᴏᴘᴇʀ </a></b></blockquote>"
                        )
                    await client.copy_message(
                                chat_id=LOG_CHANNEL,
                                from_chat_id=message.chat.id,
                                message_id=succ.id,
                                caption=caption,
                                parse_mode=enums.ParseMode.HTML
                            )
                await asyncio.sleep(1)
                await sticker_message.delete()

                final_stick = await message.reply_sticker(lazysticker)
                if os.path.exists(video_filename):
                    os.remove(video_filename)
                if os.path.exists(ph_path):
                    os.remove(ph_path)
                await asyncio.sleep(5)
                await final_stick.delete()
            else:
                print(f"API Error: {data.get('message')}")
                return 
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return



