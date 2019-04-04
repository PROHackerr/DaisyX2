
import time

from sophie_bot.events import register
from sophie_bot.modules.users import is_user_admin


@register(incoming=True, pattern="^/purge")
async def event(event):
    K = await is_user_admin(event.chat_id, event.from_id)
    if K is False:
        await event.reply("You don't have rights to purge here!")
        return
    msg = await event.get_reply_message()

    chat = await event.get_input_chat()
    msgs = []
    msg_id = msg.id
    message = await event.reply("Purge started!")
    delete_to = event.message.id - 1
    start_time = time.time()
    await event.client.delete_messages(chat, event.message.id)
    msgs.append(event.reply_to_msg_id)
    for m_id in range(int(delete_to), msg_id - 1, -1):
        msgs.append(m_id)
        if len(msgs) == 100:
            await event.client.delete_messages(chat, msgs)
            msgs = []

    await event.client.delete_messages(chat, msgs)
    end_time = time.time()
    sec = round(float(end_time - start_time) * 1000)
    text = "**Purge completed!**\nMessages deleted for {} ms".format(sec)
    await message.edit(text)


@register(incoming=True, pattern="^/del")
async def event(event):
    K = await is_user_admin(event.chat_id, event.from_id)
    if K is False:
        await event.reply("You don't have rights to delete messsages here!")
        return
    msg = await event.get_reply_message()
    chat = await event.get_input_chat()
    msgs = [msg, event.message]
    await event.client.delete_messages(chat, msgs)