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

# --- DATABASE FILES LIST ---
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
    print("\033[1;36m" + "      >>> CYBER ENAFUL MEGA SYSTEM v6.0 <<<")
    print("\033[1;37m" + "   STATUS: ACTIVE | BROADCAST: GROUPS ONLY | BRAND: ENAFUL")
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

# --- [FIXED] ব্রডকাস্ট সিস্টেম (শুধুমাত্র গ্রুপে যাবে) ---
async def group_broadcast_task(interval, list_key):
    await asyncio.sleep(20) # স্টার্টআপ ডিলে
    while True:
        msg_list = auto_replies.get(list_key, [])
        if msg_list:
            msg = random.choice(msg_list)
            async for dialog in app.get_dialogs():
                # চেক করবে এটা গ্রুপ কি না (SUPERGROUP বা GROUP)
                if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    try:
                        await app.send_message(dialog.chat.id, msg)
                        await asyncio.sleep(2.0) # স্প্যাম প্রোটেকশন
                    except: continue
        await asyncio.sleep(interval)

# --- [FEATURE: RECOVERY] স্মার্ট + মেগা রিপ্লাই সিস্টেম ---
@app.on_message(filters.text & ~filters.me & ~filters.bot)
async def reply_handler(client, message):
    user_text = message.text.strip().lower()
    mega_list = auto_replies.get("mega_replies", [])
    
    reply_to_send = None

    # ১. প্রথমে নির্দিষ্ট কী-ওয়ার্ড চেক করবে (পুরানো ফিচার ব্যাক)
    for key, value in auto_replies.items():
        if isinstance(key, str) and key.lower() in user_text:
            reply_to_send = random.choice(value) if isinstance(value, list) else value
            break
    
    # ২. যদি কী-ওয়ার্ড না মেলে তবে মেগা রিপ্লাই থেকে র‍্যান্ডম ডিজাইন নেবে
    if not reply_to_send and mega_list:
        reply_to_send = random.choice(mega_list)

    if reply_to_send:
        try:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(0.8)
            await message.reply_text(str(reply_to_send))
        except: pass

# --- [FIXED] ২০টি বিশাল ডিজাইন সহ ওয়েলকাম সিস্টেম ---
@app.on_message(filters.group & filters.new_chat_members)
async def welcome_handler(client, message):
    welcome_list = auto_replies.get("welcome_list", [])
    if not welcome_list: return
    
    inviter = message.from_user.mention if message.from_user else "Legend"
    for member in message.new_chat_members:
        if not member.is_self:
            selected_msg = random.choice(welcome_list)
            try:
                final_msg = selected_msg.replace("{user}", str(member.mention)).replace("{group}", str(message.chat.title)).replace("{admin}", str(inviter))
                await client.send_message(chat_id=message.chat.id, text=final_msg)
            except: 
                await client.send_message(chat_id=message.chat.id, text=selected_msg)

# --- স্ট্যাটাস চেক ---
async def status_heartbeat():
    while True:
        print(f"\033[1;32m[LIVE] {datetime.now().strftime('%H:%M:%S')} - CYBER ENAFUL IS RUNNING... 🛡️\033[0m")
        await asyncio.sleep(600)

if __name__ == "__main__":
    show_banner()
    print(f"📊 Total Items Loaded: {len(auto_replies)}")
    
    loop = asyncio.get_event_loop()
    # ১ ঘণ্টা পরপর গ্রুপ ব্রডকাস্ট
    loop.create_task(group_broadcast_task(3600, "hourly_broadcast"))
    # ২ মিনিট পরপর গ্রুপ ব্রডকাস্ট (মিনিট ব্রডকাস্টকে ২ মিনিট করা হয়েছে সেফটির জন্য)
    loop.create_task(group_broadcast_task(120, "minute_broadcast"))
    loop.create_task(status_heartbeat())
    
    app.run()
