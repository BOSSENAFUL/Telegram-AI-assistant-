import json
import os
from pyrogram import Client, filters

# --- বসের পার্সোনাল আইডি কনফিগারেশন ---
API_ID = 33422392 
API_HASH = "9b66ed5b9e6a307951b3a681c80f9d4b" 

# ইউজারবট ক্লায়েন্ট তৈরি
app = Client("CyberEnafulUserBot", api_id=API_ID, api_hash=API_HASH)

# ডাটাবেজ ফাইলের লিস্ট (২১টি মূল ফাইল + ২২-২৪ এর অ্যাডজাস্ট করা ফাইল)
FILES = [
    "cyber_enaful_file_1.json", "cyber_enaful_file_2.json", "cyber_enaful_file_3.json",
    "cyber_enaful_funny_master.json", "cyber_enaful_hot_aggressive.json", 
    "cyber_enaful_work_profile.json", "cyber_enaful_law_and_ethics.json", 
    "cyber_enaful_ultimate_master_v8.json", "cyber_enaful_legendary_v9.json", 
    "cyber_enaful_master_v10.json", "cyber_enaful_ai_identity_v11.json", 
    "cyber_enaful_personal_biography_v12.json", "cyber_enaful_official_rules_v13.json", 
    "cyber_enaful_main_control_v14.json", "cyber_enaful_feedback_support_v15.json",
    "cyber_enaful_news_updates_v16.json", "cyber_enaful_digital_kingdom_v17.json",
    "cyber_enaful_ai_inner_core_v18.json", "cyber_enaful_tech_guide_v19.json",
    "cyber_enaful_lifestyle_mix_v20.json", "cyber_enaful_extreme_warning_v21.json",
    "cyber_enaful_mega_love_v22_24.json"
]

def load_all_data():
    master_data = {}
    for file_name in FILES:
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    content = f.read()
                    data = json.load(f)
                    master_data.update(data)
            except Exception as e:
                print(f"⚠️ {file_name} লোড করতে সমস্যা: {e}")
    return master_data

# ডাটা লোড
auto_replies = load_all_data()

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🔱 CYBER ENAFUL USERBOT IS ACTIVE!")
print(f"📊 Total Keywords: {len(auto_replies)}")
print("🚫 No Groups | No Channels | No Bots")
print("✅ Only Private Inbox")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

@app.on_message(filters.private & filters.text & ~filters.me & ~filters.bot)
async def handle_private_inbox(client, message):
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
            print(f"মেসেজ পাঠাতে এরর: {e}")

if __name__ == "__main__":
    app.run()
