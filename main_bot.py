import json
import os
import asyncio
import random
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatType

# --- CONFIGURATION ---
API_ID = 33422392 
API_HASH = "9b66ed5b9e6a307951b3a681c80f9d4b" 

app = Client("CyberEnafulUserBot", api_id=API_ID, api_hash=API_HASH)

# --- DATABASE FILES LIST (৪০টি ফাইলসহ সব অটো লোড) ---
FILES = [f"cyber_enaful_file_{i}.json" for i in range(1, 41)] + [
    "cyber_enaful_all_in_one.json", "cyber_enaful_ultimate_v2.json", 
    "cyber_enaful_funny_master.json", "cyber_enaful_hot_aggressive.json",
    "cyber_enaful_work_profile.json", "cyber_enaful_law_and_ethics.json"
]

def show_banner():
    os.system("clear")
    print("\033[1;32m" + "╔" + "═" * 50 + "╗")
    print("║   ███████╗███╗   ██╗ █████╗ ███████╗██╗   ██╗██╗   ║")
    print("║   ██╔════╝████╗  ██║██╔══██╗██╔════╝██║   ██║██║   ║")
    print("║   █████╗  ██╔██╗ ██║███████║█████╗  ██║   ██║██║   ║")
    print("║   ██╔══╝  ██║╚██╗██║██╔══██║██╔══╝  ██║   ██║██║   ║")
    print("║   ███████╗██║ ╚████║██║  ██║██║     ╚██████╔╝███████╗║")
    print("║   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝║")
    print("╚" + "═" * 50 + "╝")
    print("\033[1;36m" + "      >>> CYBER ENAFUL MEGA SYSTEM v5.0 <<<")
    print("\033[1;37m" + "   STATUS: ACTIVE | ALL FEATURES: FIXED | BRAND: CYBER ENAFUL")
    print("\033[1;32m" + "═" * 52 + "\033[0m")

def load_data():
    master_data = {}
    for file_name in FILES:
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if key in master_data and isinstance(value, list):
                                master_data[key].extend(value)
                            else:
                                master_data[key] = value
            except: continue
    return master_data

auto_replies = load_data()

# --- [FIXED] ১ ঘণ্টা পরপর ব্রডকাস্ট (সব জায়গায়) ---
async def hourly_broadcast_task():
    await asyncio.sleep(10) # স্টার্টআপ ডিলে
    while True:
        broadcast_list = auto_replies.get("hourly_broadcast", [])
        if broadcast_list:
            msg = random.choice(broadcast_list)
            async for dialog in app.get_dialogs():
                try:
                    await app.send_message(dialog.chat.id, msg)
                    await asyncio.sleep(1.5)
                except: continue
        await asyncio.sleep(3600)

# --- [FIXED] প্রতি মিনিটে ব্রডকাস্ট (ইনবক্স + গ্রুপ + চ্যানেল) ---
async def minute_broadcast_task():
    await asyncio.sleep(15) # স্টার্টআপ ডিলে
    counter = 0
    while True:
        minute_list = auto_replies.get("minute_broadcast", [])
        if minute_list:
            msg = minute_list[counter % len(minute_list)]
            counter += 1
            async for dialog in app.get_dialogs():
                try:
                    await app.send_message(dialog.chat.id, msg)
                    await asyncio.sleep(1.0)
                except: continue
        await asyncio.sleep(60)

# --- [FEATURE 3: UPDATED] স্মার্ট + মেগা রিপ্লাই সিস্টেম ---
@app.on_message(filters.text & ~filters.me & ~filters.bot)
async def reply_handler(client, message):
    user_text = message.text.strip().lower()
    
    # ৪০ নম্বর ফাইলের সেই ২০টি বিশাল ডিজাইন (mega_replies) আগে চেক করবে
    mega_list = auto_replies.get("mega_replies", [])
    
    if mega_list:
        # কেউ যেকোনো কিছু লিখলেই (১টি অক্ষর হলেও) বিশাল ডিজাইন রিপ্লাই যাবে
        reply_to_send = random.choice(mega_list)
    else:
        # যদি মেগা রিপ্লাই না থাকে তবে সাধারণ রিপ্লাই
        reply_to_send = None
        for key, value in auto_replies.items():
            if isinstance(value, str) and key.lower() in user_text:
                reply_to_send = value
                break
        if not reply_to_send:
            all_texts = [v for k, v in auto_replies.items() if isinstance(v, str)]
            if all_texts: reply_to_send = random.choice(all_texts)

    if reply_to_send:
        try:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(0.5)
            await message.reply_text(str(reply_to_send))
        except: pass

# --- [FIXED] ২০টি বিশাল ডিজাইন সহ ওয়েলকাম সিস্টেম ---
@app.on_message(filters.group & filters.new_chat_members)
async def welcome_handler(client, message):
    welcome_list = auto_replies.get("welcome_list", [])
    if not welcome_list: return
    
    inviter = message.from_user.mention if message.from_user else "অজানা লিজেন্ড"
    
    for member in message.new_chat_members:
        if not member.is_self:
            user_mention = member.mention
            group_name = message.chat.title
            selected_msg = random.choice(welcome_list)
            try:
                # ডিজাইন ফরম্যাট ঠিক রাখা (replace ব্যবহার করে যাতে এরর না দেয়)
                final_msg = selected_msg.replace("{user}", str(user_mention)).replace("{group}", str(group_name)).replace("{admin}", str(inviter))
                await client.send_message(chat_id=message.chat.id, text=final_msg)
            except: 
                await client.send_message(chat_id=message.chat.id, text=selected_msg)

# --- হার্টবিট স্ট্যাটাস ---
async def status_heartbeat():
    while True:
        print(f"\033[1;32m[SYSTEM CHECK] {datetime.now().strftime('%H:%M:%S')} - CYBER ENAFUL IS LIVE! 🛡️\033[0m")
        await asyncio.sleep(600)

if __name__ == "__main__":
    show_banner()
    print(f"📊 Total Keywords & Designs Synced: {len(auto_replies)} items.")
    loop = asyncio.get_event_loop()
    loop.create_task(hourly_broadcast_task())
    loop.create_task(minute_broadcast_task())
    loop.create_task(status_heartbeat())
    app.run()
