from Backend.service.speed_service import check_internet_speed
from Backend.service.user_query import query_response
from Backend.repository.user_repo import get_user, save_data

import re

def clean_ai_response(response):
    # Remove Markdown symbols and special characters
    response = re.sub(r'[^a-zA-Z0-9\s.,:₹()-]', '', response)

    # Remove extra spaces
    response = re.sub(r'\s+', ' ', response).strip()

    return response

def analyze_error(sender_id, amount, receiver_id):

    # -----------------------------
    # 1. Get sender
    # -----------------------------

    sender = get_user(sender_id)

    if sender is None:
        return {
            "status": "failed",
            "error": "authentication_error",
            "message": "Sender authentication failed."
        }

    # -----------------------------
    # 2. Get receiver
    # -----------------------------

    receiver = get_user(receiver_id)

    if receiver is None:

        prompt = f"""
You are a Payment Failure Analysis AI Agent.

Authentication: Successful
Sender ID: {sender_id}
Receiver ID: {receiver_id}
Transaction amount: ₹{amount}

The receiver does not exist.

Explain clearly:
Authentication:
Receiver:
Reason:
Solution:

Do not invent information.
"""

        response = query_response(prompt)
        response = clean_ai_response(response)

        return {
            "status": "failed",
            "error": "receiver_not_found",
            "ai_analysis": response
        }

    # -----------------------------
    # 3. Get sender balance
    # -----------------------------

    balance = sender["bank_balance"]

    # -----------------------------
    # 4. Check internet
    # -----------------------------

    internet = check_internet_speed()

    download = internet["download_speed_mbps"]
    upload = internet["upload_speed_mbps"]
    ping = internet["ping_ms"]

    internet_ok = (
        download >= 1
        and upload >= 1
        and ping < 50000000
    )

    # -----------------------------
    # 5. Check balance
    # -----------------------------

    balance_ok = balance >= amount

    # -----------------------------
    # 6. Failure analysis
    # -----------------------------

    if not balance_ok:

        prompt = f"""
You are a Payment Failure Analysis AI Agent.

Authentication: Successful

Sender ID: {sender_id}
Receiver ID: {receiver_id}

Transaction amount: ₹{amount}
Sender balance: ₹{balance}

Internet:
Download: {download} Mbps
Upload: {upload} Mbps
Ping: {ping} ms
Internet is good: {internet_ok}

The transaction failed because the sender has insufficient balance.

Explain:

Authentication:
Internet:
Receiver:
Balance:
Reason:
Solution:

Do not blame the internet because the actual problem is insufficient balance.
"""

        response = query_response(prompt)

        return {
            "status": "failed",
            "error": "insufficient_balance",
            "internet": internet,
            "ai_analysis": response
        }

    # -----------------------------
    # 7. Check internet
    # -----------------------------

    if not internet_ok:

        prompt = f"""
You are a Payment Failure Analysis AI Agent.

Authentication: Successful
Receiver: Exists

Transaction amount: ₹{amount}
Sender balance: ₹{balance}

Internet:
Download: {download} Mbps
Upload: {upload} Mbps
Ping: {ping} ms

The internet connection is not suitable for the payment.

Explain:

Authentication:
Internet:
Receiver:
Balance:
Reason:
Solution:
"""

        response = query_response(prompt)

        return {
            "status": "failed",
            "error": "internet_problem",
            "internet": internet,
            "ai_analysis": response
        }

    # -----------------------------
    # 8. Transfer money
    # -----------------------------

    sender["bank_balance"] -= amount
    receiver["bank_balance"] += amount

    # Save updated balances
    save_data()

    return {
        "status": "success",
        "message": "Payment successful",
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "amount": amount,
        "remaining_balance": sender["bank_balance"],
        "internet": internet
    }