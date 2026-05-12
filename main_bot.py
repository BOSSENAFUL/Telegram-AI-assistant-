import json
import os
from pyrogram import Client, filters

# --- CONFIGURATION ---
API_ID = 33422392 
API_HASH = "9b66ed5b9e6a307951b3a681c80f9d4b" 

app = Client("CyberEnafulUserBot", api_id=API_ID, api_hash=API_HASH)

# --- DATABASE FILES LIST (Names Corrected Based on Github) ---
FILES = [
    "cyber_enaful_all_in_one.json", 
    "cyber_enaful_ultimate_v2.json", 
    "cyber_enaful_file_3.json",
    "cyber_enaful_funny_master.json", "cyber_enaful_hot_aggressive.json", 
    "cyber_enaful_work_profile.json", "cyber_enaful_law_and_ethics.json", 
    "cyber_enaful_ultimate_master_v8.json", "cyber_enaful_legendary_v9.json", 
    "cyber_enaful_master_v10.json", "cyber_enaful_ai_identity_v11.json", 
    "cyber_enaful_personal_biography_v12.json", "cyber_enaful_official_rules_v13.json", 
    "cyber_enaful_main_control_v14.json", "cyber_enaful_feedback_support_v15.json",
    "cyber_enaful_news_updates_v16.json", "cyber_enaful_digital_kingdom_v17.json",
    "cyber_enaful_ai_inner_core_v18.json", "cyber_enaful_tech_guide_v19.json",
    "cyber_enaful_lifestyle_mix_v20.json", "cyber_enaful_extreme_warning_v21.json",
    "cyber_enaful_mega_love_v22_24.json", 
    "cyber_enaful_file_25.json", "cyber_enaful_file_26.json", 
    "cyber_enaful_file_27.json", "cyber_enaful_file_28.json", 
    "cyber_enaful_file_29.json", "cyber_enaful_file_30.json"
]

def load_data():
    master_data = {}
    for file_name in FILES:
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    master_data.update(data)
            except Exception as e:
                print(f"⚠️ Error loading {file_name}: {e}")
        else:
            print(f"❌ File Not Found: {file_name}")
    return master_data

auto_replies = load_data()

print("-" * 35)
print("🔱 CYBER ENAFUL USERBOT IS LIVE")
print(f"📊 Total Keywords Loaded: {len(auto_replies)}")
print("🛡️ Protection: Private Inbox Mode")
print("-" * 35)

@app.on_message(filters.private & filters.text & ~filters.me & ~filters.bot)
async def inbox_handler(client, message):
    user_text = message.text.strip().lower()
    
    reply = None
    for key in auto_replies:
        if key.lower() in user_text:
            reply = auto_replies[key]
            break
    
    if reply:
        try:
            await message.reply_text(reply)
        except Exception as e:
            print(f"Reply Error: {e}")

if __name__ == "__main__":
    app.run()
