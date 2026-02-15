#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP Telegram Bot - Multilingual Support with Complete Message Display
"""

import requests
import time
import re
from datetime import datetime
import json
import os
import sys

# ==================== CONFIGURATION ====================
API_URL = os.getenv("API_URL", "http://147.135.212.197/crapi/st/viewstats")
API_TOKEN = os.getenv("API_TOKEN", "R1BTQ0hBUzSAild8c2aWV3eYa1NpjVNIUpBzY1qCaWFHh5JUUpWIXQ==")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8130090084:AAE1zfsAVJ0M1FnE3sCQdMQEprBNXlm24o8")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "-1003876856971")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "15"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "50"))
MAX_RECORDS_PER_FETCH = int(os.getenv("MAX_RECORDS_PER_FETCH", "1000000000"))

processed_messages = set()

# ==================== COUNTRY MAPPING ====================
COUNTRY_DATA = {
    "1": {"flag": "🇺🇸", "name": "USA/Canada"},
    "52": {"flag": "🇲🇽", "name": "Mexico"},
    "54": {"flag": "🇦🇷", "name": "Argentina"},
    "55": {"flag": "🇧🇷", "name": "Brazil"},
    "56": {"flag": "🇨🇱", "name": "Chile"},
    "57": {"flag": "🇨🇴", "name": "Colombia"},
    "58": {"flag": "🇻🇪", "name": "Venezuela"},
    "51": {"flag": "🇵🇪", "name": "Peru"},
    "53": {"flag": "🇨🇺", "name": "Cuba"},
    "591": {"flag": "🇧🇴", "name": "Bolivia"},
    "593": {"flag": "🇪🇨", "name": "Ecuador"},
    "595": {"flag": "🇵🇾", "name": "Paraguay"},
    "598": {"flag": "🇺🇾", "name": "Uruguay"},
    "44": {"flag": "🇬🇧", "name": "United Kingdom"},
    "33": {"flag": "🇫🇷", "name": "France"},
    "49": {"flag": "🇩🇪", "name": "Germany"},
    "39": {"flag": "🇮🇹", "name": "Italy"},
    "34": {"flag": "🇪🇸", "name": "Spain"},
    "7": {"flag": "🇷🇺", "name": "Russia"},
    "48": {"flag": "🇵🇱", "name": "Poland"},
    "31": {"flag": "🇳🇱", "name": "Netherlands"},
    "32": {"flag": "🇧🇪", "name": "Belgium"},
    "41": {"flag": "🇨🇭", "name": "Switzerland"},
    "43": {"flag": "🇦🇹", "name": "Austria"},
    "45": {"flag": "🇩🇰", "name": "Denmark"},
    "46": {"flag": "🇸🇪", "name": "Sweden"},
    "47": {"flag": "🇳🇴", "name": "Norway"},
    "358": {"flag": "🇫🇮", "name": "Finland"},
    "30": {"flag": "🇬🇷", "name": "Greece"},
    "351": {"flag": "🇵🇹", "name": "Portugal"},
    "353": {"flag": "🇮🇪", "name": "Ireland"},
    "420": {"flag": "🇨🇿", "name": "Czech Republic"},
    "36": {"flag": "🇭🇺", "name": "Hungary"},
    "40": {"flag": "🇷🇴", "name": "Romania"},
    "380": {"flag": "🇺🇦", "name": "Ukraine"},
    "90": {"flag": "🇹🇷", "name": "Turkey"},
    "86": {"flag": "🇨🇳", "name": "China"},
    "91": {"flag": "🇮🇳", "name": "India"},
    "92": {"flag": "🇵🇰", "name": "Pakistan"},
    "81": {"flag": "🇯🇵", "name": "Japan"},
    "82": {"flag": "🇰🇷", "name": "South Korea"},
    "84": {"flag": "🇻🇳", "name": "Vietnam"},
    "66": {"flag": "🇹🇭", "name": "Thailand"},
    "62": {"flag": "🇮🇩", "name": "Indonesia"},
    "60": {"flag": "🇲🇾", "name": "Malaysia"},
    "63": {"flag": "🇵🇭", "name": "Philippines"},
    "65": {"flag": "🇸🇬", "name": "Singapore"},
    "880": {"flag": "🇧🇩", "name": "Bangladesh"},
    "94": {"flag": "🇱🇰", "name": "Sri Lanka"},
    "95": {"flag": "🇲🇲", "name": "Myanmar"},
    "855": {"flag": "🇰🇭", "name": "Cambodia"},
    "856": {"flag": "🇱🇦", "name": "Laos"},
    "93": {"flag": "🇦🇫", "name": "Afghanistan"},
    "98": {"flag": "🇮🇷", "name": "Iran"},
    "964": {"flag": "🇮🇶", "name": "Iraq"},
    "972": {"flag": "🇮🇱", "name": "Israel"},
    "966": {"flag": "🇸🇦", "name": "Saudi Arabia"},
    "971": {"flag": "🇦🇪", "name": "UAE"},
    "974": {"flag": "🇶🇦", "name": "Qatar"},
    "965": {"flag": "🇰🇼", "name": "Kuwait"},
    "968": {"flag": "🇴🇲", "name": "Oman"},
    "973": {"flag": "🇧🇭", "name": "Bahrain"},
    "962": {"flag": "🇯🇴", "name": "Jordan"},
    "961": {"flag": "🇱🇧", "name": "Lebanon"},
    "963": {"flag": "🇸🇾", "name": "Syria"},
    "967": {"flag": "🇾🇪", "name": "Yemen"},
    "996": {"flag": "🇰🇬", "name": "Kyrgyzstan"},
    "998": {"flag": "🇺🇿", "name": "Uzbekistan"},
    "992": {"flag": "🇹🇯", "name": "Tajikistan"},
    "993": {"flag": "🇹🇲", "name": "Turkmenistan"},
    "994": {"flag": "🇦🇿", "name": "Azerbaijan"},
    "995": {"flag": "🇬🇪", "name": "Georgia"},
    "374": {"flag": "🇦🇲", "name": "Armenia"},
    "977": {"flag": "🇳🇵", "name": "Nepal"},
    "20": {"flag": "🇪🇬", "name": "Egypt"},
    "27": {"flag": "🇿🇦", "name": "South Africa"},
    "234": {"flag": "🇳🇬", "name": "Nigeria"},
    "233": {"flag": "🇬🇭", "name": "Ghana"},
    "254": {"flag": "🇰🇪", "name": "Kenya"},
    "255": {"flag": "🇹🇿", "name": "Tanzania"},
    "256": {"flag": "🇺🇬", "name": "Uganda"},
    "251": {"flag": "🇪🇹", "name": "Ethiopia"},
    "212": {"flag": "🇲🇦", "name": "Morocco"},
    "213": {"flag": "🇩🇿", "name": "Algeria"},
    "216": {"flag": "🇹🇳", "name": "Tunisia"},
    "218": {"flag": "🇱🇾", "name": "Libya"},
    "221": {"flag": "🇸🇳", "name": "Senegal"},
    "225": {"flag": "🇨🇮", "name": "Ivory Coast"},
    "237": {"flag": "🇨🇲", "name": "Cameroon"},
    "243": {"flag": "🇨🇩", "name": "DR Congo"},
    "244": {"flag": "🇦🇴", "name": "Angola"},
    "258": {"flag": "🇲🇿", "name": "Mozambique"},
    "260": {"flag": "🇿🇲", "name": "Zambia"},
    "263": {"flag": "🇿🇼", "name": "Zimbabwe"},
    "61": {"flag": "🇦🇺", "name": "Australia"},
    "64": {"flag": "🇳🇿", "name": "New Zealand"},
    "679": {"flag": "🇫🇯", "name": "Fiji"},
}

SERVICE_NAMES = {
    "whatsapp": "WhatsApp", "facebook": "Facebook", "instagram": "Instagram",
    "snapchat": "Snapchat", "twitter": "Twitter", "tiktok": "TikTok",
    "telegram": "Telegram", "linkedin": "LinkedIn", "discord": "Discord",
    "viber": "Viber", "wechat": "WeChat", "line": "LINE", "kakaotalk": "KakaoTalk",
    "google": "Google", "microsoft": "Microsoft", "apple": "Apple",
    "yahoo": "Yahoo", "amazon": "Amazon", "uber": "Uber", "netflix": "Netflix",
    "paypal": "PayPal", "grab": "Grab", "gojek": "GoJek", "olx": "OLX",
    "steam": "Steam", "roblox": "Roblox", "naver": "Naver",
    "verify": "Verification Service", "otp": "OTP Service",
}

def get_country_info(phone_number):
    phone_str = str(phone_number).strip()
    for code in ["880", "420", "855", "856", "591", "593", "595", "598", "358", "351", "353", "380", "374", "234", "233", "254", "255", "256", "251", "212", "213", "216", "218", "221", "225", "237", "243", "244", "258", "260", "263", "961", "962", "963", "964", "965", "966", "967", "968", "971", "972", "973", "974", "992", "993", "994", "995", "996", "998", "977", "679"]:
        if phone_str.startswith(code):
            return COUNTRY_DATA[code]["flag"], COUNTRY_DATA[code]["name"]
    prefix = phone_str[:2]
    if prefix in COUNTRY_DATA:
        return COUNTRY_DATA[prefix]["flag"], COUNTRY_DATA[prefix]["name"]
    prefix = phone_str[:1]
    if prefix in COUNTRY_DATA:
        return COUNTRY_DATA[prefix]["flag"], COUNTRY_DATA[prefix]["name"]
    return "🌍", "Unknown"

def get_service_name(cli):
    if not cli:
        return "Unknown Service"
    cli_lower = str(cli).lower().strip()
    for key, value in SERVICE_NAMES.items():
        if key in cli_lower:
            return value
    return str(cli).title()

def extract_otp(message):
    """Extract 6-digit numeric OTP - PRIORITY"""
    if not message:
        return "N/A"
    
    message_str = str(message)
    
    # PRIORITY 1: 6-digit numeric OTP (most common)
    match = re.search(r'\b(\d{6})\b', message_str)
    if match:
        return match.group(1)
    
    # PRIORITY 2: Formats like 101-390, 123-456
    match = re.search(r'(\d{3}-\d{3})', message_str)
    if match:
        return match.group(1)
    
    # PRIORITY 3: 4-5 digit codes
    match = re.search(r'\b(\d{4,5})\b', message_str)
    if match:
        return match.group(1)
    
    # If no numeric code found, return N/A
    return "N/A"

def mask_phone_number(phone):
    phone_str = str(phone)
    if len(phone_str) <= 4:
        return phone_str
    return f"{phone_str[:4]}****{phone_str[-3:]}"

def format_telegram_message(data):
    if isinstance(data, dict):
        dt = data.get('dt', '')
        num = data.get('num', '')
        cli = data.get('cli', 'Unknown')
        message = data.get('message', '')
    elif isinstance(data, list) and len(data) >= 4:
        # API format: [CLI, Number, Message, DateTime]
        cli = str(data[0]) if len(data) > 0 else 'Unknown'
        num = str(data[1]) if len(data) > 1 else ''
        message = str(data[2]) if len(data) > 2 else ''
        dt = str(data[3]) if len(data) > 3 else ''
    else:
        print(f"⚠️ Unknown data format: {type(data)}")
        return None, None
    
    # Clean and ensure proper encoding
    message = message.strip()
    if isinstance(message, bytes):
        try:
            message = message.decode('utf-8')
        except:
            message = message.decode('utf-8', errors='ignore')
    
    flag, country = get_country_info(num)
    service = get_service_name(cli)
    otp = extract_otp(message)
    masked_num = mask_phone_number(num)
    
    # Better OTP display
    if otp == "N/A":
        otp_display = "⚠️ <i>Check Full Message Below</i>"
    else:
        otp_display = f"<code>{otp}</code>"
    
    telegram_msg = f"""✨    <b>NEW  OTP   RECEIVED</b>    ✨ 

━━━━━━━━━━━━━━━━━━━━━━━━━━

🕐 <b>Time:</b> {dt}

{flag} <b>Country:</b> {country}

🟢 <b>Service:</b> {service}

📞 <b>Number:</b> +{masked_num}

🔑 <b>OTP Code:</b> {otp_display}

━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 <b>Complete Message:</b>

<pre>{message}</pre>


https://t.me/+IsFHolLYjmhiYWM0

<code>MALIK SAHIB 🎭 CHATTING ZONE 👆</code>
━━━━━━━━━━━━
<code>https://t.me/maliksahib786</code>

<code>NUMBERS HERE 🎭 👆</code> ━━━━━━━━━━━━━━
<code>Powered By Malik Sahib 🎭</code>"""
    
    return telegram_msg, otp

def send_telegram_message(message, otp_code):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    keyboard = {
        "inline_keyboard": [[{
            "text": f"📋 Copy OTP: {otp_code}",
            "callback_data": f"copy_{otp_code}"
        }]]
    }
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard)
    }
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            elif response.status_code == 429:
                retry_after = int(response.json().get('parameters', {}).get('retry_after', 5))
                print(f"⏳ Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            else:
                if attempt < max_retries - 1:
                    time.sleep(2)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
    return False

def fetch_api_data():
    params = {"token": API_TOKEN, "records": MAX_RECORDS_PER_FETCH}
    try:
        print(f"📡 Fetching data from API...")
        response = requests.get(API_URL, params=params, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Fetched {len(data)} records")
                return data
            elif isinstance(data, dict):
                if data.get('status') == 'success':
                    records = data.get('data', [])
                    print(f"✅ Fetched {len(records)} records")
                    return records
                else:
                    print(f"⚠️ API Error: {data.get('msg', 'Unknown')}")
                    return []
            else:
                return []
        else:
            print(f"⚠️ HTTP Error: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print(f"⚠️ API timeout")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def create_message_id(data):
    if isinstance(data, dict):
        dt = data.get('dt', '')
        num = data.get('num', '')
        cli = data.get('cli', '')
        message = data.get('message', '')[:50]
    elif isinstance(data, list) and len(data) >= 4:
        cli = str(data[0]) if len(data) > 0 else ''
        num = str(data[1]) if len(data) > 1 else ''
        message = (str(data[2]) if len(data) > 2 else '')[:50]
        dt = str(data[3]) if len(data) > 3 else ''
    else:
        return str(data)[:100]
    return f"{dt}_{num}_{cli}_{message}"

def process_records_in_batches(records):
    total_records = len(records)
    new_count = 0
    duplicate_count = 0
    error_count = 0
    print(f"📦 Processing {total_records} records in batches of {BATCH_SIZE}...")
    for i in range(0, total_records, BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (total_records + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"🔄 Batch {batch_num}/{total_batches} ({len(batch)} records)...")
        for record in batch:
            try:
                if not record or (isinstance(record, list) and len(record) < 4):
                    error_count += 1
                    continue
                msg_id = create_message_id(record)
                if msg_id not in processed_messages:
                    result = format_telegram_message(record)
                    if result[0] is None:
                        error_count += 1
                        continue
                    telegram_msg, otp = result
                    if send_telegram_message(telegram_msg, otp):
                        processed_messages.add(msg_id)
                        new_count += 1
                        print(f"  ✅ Sent OTP: {otp} ({new_count})")
                    else:
                        error_count += 1
                    if len(processed_messages) > 5000:
                        oldest_entries = list(processed_messages)[:1000]
                        for entry in oldest_entries:
                            processed_messages.discard(entry)
                    time.sleep(0.5)
                else:
                    duplicate_count += 1
            except Exception as e:
                error_count += 1
                print(f"  ❌ Error: {e}")
        if i + BATCH_SIZE < total_records:
            time.sleep(2)
    return new_count, duplicate_count, error_count

def health_check():
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot connected: @{bot_info['result']['username']}")
            return True
        return False
    except:
        return False

def main():
    print("=" * 70)
    print("🚀 OTP TELEGRAM BOT - COMPLETE MESSAGE DISPLAY")
    print("=" * 70)
    print(f"📡 API URL: {API_URL}")
    print(f"📢 Channel ID: {TELEGRAM_CHANNEL_ID}")
    print(f"⏱️  Check Interval: {CHECK_INTERVAL} seconds")
    print(f"📦 Batch Size: {BATCH_SIZE}")
    print(f"🔢 Priority: 6-digit numeric OTP codes")
    print("=" * 70)
    if health_check():
        print("✅ Telegram verified!")
    print()
    consecutive_errors = 0
    max_consecutive_errors = 5
    while True:
        try:
            print(f"\n{'='*70}")
            print(f"🔍 Fetch cycle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*70}\n")
            records = fetch_api_data()
            if records:
                new_count, duplicate_count, error_count = process_records_in_batches(records)
                print(f"\n{'='*70}")
                print(f"📊 SUMMARY:")
                print(f"  📥 Total fetched: {len(records)}")
                print(f"  ✨ New sent: {new_count}")
                print(f"  ⏭️  Duplicates: {duplicate_count}")
                print(f"  ❌ Errors: {error_count}")
                print(f"{'='*70}\n")
                consecutive_errors = 0
            else:
                print("📭 No records\n")
                consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                print(f"⚠️ Too many errors. Taking longer break...")
                time.sleep(CHECK_INTERVAL * 5)
                consecutive_errors = 0
            else:
                print(f"⏳ Waiting {CHECK_INTERVAL} seconds...\n")
                sys.stdout.flush()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n" + "=" * 70)
            print("🛑 Bot stopped")
            print("=" * 70)
            break
        except Exception as e:
            consecutive_errors += 1
            print(f"❌ Error: {e}")
            print(f"🔄 Retrying in {CHECK_INTERVAL} seconds...")
            sys.stdout.flush()
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
