# Advanced File Sharing Bot

**AdvancedFileSharingBot** is a Telegram bot for uploading, sharing, and managing files with subscription-based access and security features.

---

## Features

- Upload and download large files (Free & Paid plans)
- Force subscription to channels before use
- Duplicate file detection
- Link generation with expiry & one-time options
- Payment-based subscription using QR / UPI
- Rate limiting & captcha for suspicious activity
- Multi-channel Telegram storage backend
- Support for admins & owners

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/AdvancedFileSharingBot.git
cd AdvancedFileSharingBot

(Optional) Create a virtual environment:
Copy code
Bash
python3 -m venv venv
source venv/bin/activate
Install required packages:
Copy code
Bash
pip install -r requirements.txt
Fill your config.py with your API keys, bot token, channels, and database info.
Usage
Run the bot:
Copy code
Bash
python3 bot.py
Bot will start and connect to Telegram. Ensure your database and Redis are running.
Subscription Plans
Plan
Price (INR)
Duration
Basic
49
20 days
Power
149
70 days
Business
399
6 months
Lifetime
999
365 days
Support
Join our support chat: Support Chat
Notes
Make sure to join the required Telegram channels for access.
Payments are QR / UPI based.
Configure your environment in config.py before running.
Copy code

Ye **README.md** copy-paste ke liye ready hai.  

Agla file? `bot.py` banana hai kya?
