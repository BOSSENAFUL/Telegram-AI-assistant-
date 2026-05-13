from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "CYBER ENAFUL SYSTEM IS LIVE 🛡️"

def run_bot():
    # এখানে আপনার মেইন বটের ফাইলটি রান হবে
    os.system("python main_bot.py") # আপনার মেইন ফাইলের নাম এখানে দিন

if __name__ == "__main__":
    # বটকে আলাদা থ্রেডে চালানো যাতে ওয়েব সার্ভারও চালু থাকে
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=7860)
