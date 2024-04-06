from FallenRobot import app
from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
import random 
from PIL import Image, ImageDraw, ImageFont
import asyncio

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)


async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((435, 435))
        bg.paste(resized, (67, 153), resized)

    img_draw = ImageDraw.Draw(bg)

    img_draw.text(
        (140, 624),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )


    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path


bg_path = "FallenRobot/resources/Lefttt.png"
font_path = "FallenRobot/resources/font.ttf"


@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {
            "banned", "left", "restricted"
        }
        and member.old_chat_member
    ):
        pass
    else:
        return

    user = (
        member.old_chat_member.user
        if member.old_chat_member
        else member.from_user
    )

    # Check if the user has a profile photo
    if user.photo and user.photo.big_file_id:
        try:
            # Add the photo path, caption, and button details
            photo = await app.download_media(user.photo.big_file_id)

            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )

            caption = f"**ᴀ ᴍᴇᴍʙᴇʀ ʟᴇғᴛ ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🥹\n\n✧══════•❁❀❁•══════✧\n╠╼➪ ✨ 𝐍𝐀𝐌𝐄 = {user.mention}\n╠╼➪ 💫 𝐔𝐒𝐄𝐑 𝐈𝐃 = {user.id}\n╠╼➪  🎁 𝐔𝐒𝐄𝐑𝐍𝐀𝐌𝐄 = @{user.username}\n✧══════•❁❀❁•══════✧\n\n๏sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ..!**"
            button_text = " Kɪᴅɴᴀᴘ ᴍᴇ 🥹 "

            # Generate a deep link to open the user's profile
            deep_link = f"https://t.me/CutieXmusicBot?startgroup=new"

            # Send the message with the photo, caption, and button
            await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)]
                ])
)

        except RPCError as e:
            print(e)
            return
    else:
        # Handle the case where the user has no profile photo
        caption = f"**ᴀ ᴍᴇᴍʙᴇʀ ʟᴇғᴛ ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🥹\n\n✧══════•❁❀❁•══════✧\n╠╼➪ ✨ 𝐍𝐀𝐌𝐄 = {user.mention}\n╠╼➪ 💫 𝐔𝐒𝐄𝐑 𝐈𝐃 = {user.id}\n╠╼➪  🎁 𝐔𝐒𝐄𝐑𝐍𝐀𝐌𝐄 = @{user.username}\n✧══════•❁❀❁•══════✧\n\n๏sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ..!**"
        button_text = " Kɪᴅɴᴀᴘ ᴍᴇ 🥹 "
        deep_link = f"https://t.me/CutieXmusicBot?startgroup=new"
        
        await client.send_photo(
                chat_id=member.chat.id,
                photo="https://telegra.ph/file/62da6bcf25c3aa28ddaa9.jpg",
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)]
                ])
) 
