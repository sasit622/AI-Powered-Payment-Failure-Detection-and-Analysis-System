from Backend.service.user_query import query_response


def analyze_user_transactions(user_id, user):

    transactions = user.get("transactions", [])

    if not transactions:
        return {
            "user_id": user_id,
            "message": "No transaction history available."
        }

    successful = [
        t for t in transactions
        if t.get("status") == "success"
    ]

    failed = [
        t for t in transactions
        if t.get("status") == "failed"
    ]

    failure_reasons = [
        t.get("failure_reason")
        for t in failed
        if t.get("failure_reason")
    ]

    prompt = f"""
You are a Payment Failure Analysis AI Agent.

Analyze the CURRENT user's previous transactions.

User ID:
{user_id}

Transactions:
{transactions}

Total transactions: {len(transactions)}
Successful transactions: {len(successful)}
Failed transactions: {len(failed)}

Failure reasons:
{failure_reasons}

Explain:

1. What happened with the user's previous payments.
2. How many payments succeeded.
3. How many payments failed.
4. The common failure reasons.
5. Whether there is a repeated failure pattern.
6. Why the user may be experiencing payment failures.
7. How the user can improve future payment success.
8. If a bank-related problem is present, tell the user to contact the bank.

Do NOT reveal the user's password.
Do NOT invent information.

Use this format:

Transaction Summary:
Failure Pattern:
Likely Reason:
How To Improve:
Bank Contact:
"""

    ai_response = query_response(prompt)

    return {
        "user_id": user_id,
        "total_transactions": len(transactions),
        "successful_transactions": len(successful),
        "failed_transactions": len(failed),
        "failure_reasons": failure_reasons,
        "ai_analysis": ai_response
    }