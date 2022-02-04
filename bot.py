from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os


logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)

bot = TelegramClient(
        "Whisper",
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e"
        ).start(
                bot_token=TOKEN
                )
db = {}

@bot.on(events.NewMessage(pattern="^[!?/]start$"))
async def stsrt(event):
    await event.reply(
            "**Tôi là bot gửi tin nhắn bảo mật**",
            buttons=[
                [Button.switch_inline("Go Inline", query="")]
                ]
            )


@bot.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await bot.get_me()).username
    dn = event.builder.article(
            title="Tin nhắn bảo mật 🔓",
            description="@{me} send [UserID] [Message]",
            text=f"@{me} send [UserID] [Message]",
            buttons=[
                [Button.switch_inline("🔒 Gửi tin nhắn bảo mật 🔒", query="send ")]
                ]
            )
    await event.answer([dn])
    
@bot.on(events.InlineQuery(send))
async def inline(event):
    me = (await bot.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split(" ")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} send [UserID] [Message]",
                switch_pm_param="start"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Cung cấp một tin nhắn!",
                switch_pm_param="start"
                )
    try:
        ui = await bot(us(send))
    except BaseException:
        await event.answer(
                [],
                switch_pm="ID người dùng / Tên người dùng không hợp lệ",
                switch_pm_param="start"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
Có một tin nhắn ẩn đã được gửi cho [{ui.user.first_name}](tg://user?id={ui.user.id})! Bấm vào nút bên dưới để xem tin nhắn!
**Note:** __Chỉ có {ui.user.first_name} mới có thể mở cái này!__
    """
    dn = event.builder.article(
            title="Đó là một thông điệp bí mật! Sssh",
            description="Đó là một thông điệp bí mật! Sssh!",
            text=text,
            buttons=[
                [Button.inline("🔐 Hiện tin nhắn 🔐", data="send")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="Đó là một thông điệp bí mật! Sssh",
            switch_pm_param="start"
            )


@bot.on(events.CallbackQuery(data="send"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("🔐 Tin nhắn này không dành cho bạn!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Oops!\nCó vẻ như tin nhắn đã bị xóa khỏi máy chủ của tôi!", alert=True)
        return
    await event.answer(msg, alert=True)

print("Succesfully Started Bot!")
bot.run_until_disconnected()
