# 💳 AI-Powered Payment Failure Detection and Analysis System

An AI-powered payment application that lets users log in, send money, check loan status, and get AI-generated analysis of their past transactions — including insights into why certain payments failed.

---

## ✨ Features

### 🔐 Login / Authentication
- Users log in with a **User ID** and **Password**.
- Actions like sending money require the user to be authenticated first.
- Unauthenticated attempts return a clear error response (`not_authenticated`).

### 💸 Send Money
- Send money to another user by entering their **Receiver ID** and **Amount**.
- On success, the API returns a detailed JSON response including:
  - `status`, `message`
  - `sender_id`, `receiver_id`, `amount`
  - `remaining_balance`
  - Additional metadata (e.g. network/connection info returned by the backend)
- On failure (e.g. not logged in), a structured error response is returned instead of a silent failure.

### 🤖 AI Transaction Analysis
- Click **"Analyze My Transactions"** to have the AI review your transaction history.
- The AI generates a human-readable report covering:
  - **Transaction Summary** — a breakdown of each transaction and its outcome
  - **Failure Pattern** — common reasons behind failed payments (e.g. insufficient balance, bank declined, timeout)
  - **Likely Reason** — a synthesized explanation of why payments are failing
  - **How to Improve** — actionable suggestions to reduce future failures

### 🏦 Check Loan Status
- Enter your **Loan User ID** and **Name** to check if you have an active loan.
- If a loan exists, the app displays:
  - Loan status (Yes/No)
  - Loan amount
  - Due date status
- If no loan is found, the app clearly states that no active loan exists.

### 🚪 Logout
- Users can securely log out at any time from the dashboard.

---

## 🖼️ Screenshots

| Login | Send Money |
|---|---|
| User authentication screen | Send money with live JSON response |

| AI Transaction Analysis | Check Loan Status |
|---|---|
| AI-generated failure analysis | Loan lookup with status details |

*(Add your actual screenshot images to a `/screenshots` folder and reference them here, e.g. `![Login](screenshots/login.png)`)*

---

## 🛠️ Tech Stack

> _Update this section with the actual stack you used (framework, language, database, AI model/API, etc.)_

- **Frontend:** (e.g. React / HTML-CSS-JS)
- **Backend:** (e.g. Node.js / Python / Flask / FastAPI)
- **Database:** (e.g. PostgreSQL / MongoDB / SQLite)
- **AI Integration:** (e.g. Claude API / OpenAI API) for transaction analysis
- **Authentication:** Session/token-based login system

---

## 🚀 Getting Started

### Prerequisites
- Node.js / Python (whichever your stack uses)
- API keys for the AI service you're using (if applicable)

### Installation
```bash
git clone https://github.com/<your-username>/ai-payment-agent.git
cd ai-payment-agent
npm install        # or: pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the root directory:
```env
AI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

### Run the App
```bash
npm start           # or: python app.py
```

The app will be available at `http://localhost:3000` (or your configured port).

---

## 📡 API Overview

| Endpoint | Method | Description |
|---|---|---|
| `/login` | POST | Authenticates a user with User ID and Password |
| `/send-money` | POST | Sends money from one user to another |
| `/analyze-transactions` | GET/POST | Runs AI analysis on the user's transaction history |
| `/loan-status` | POST | Retrieves loan details for a given User ID and Name |
| `/logout` | POST | Logs the user out |

> _Update these endpoints/methods to match your actual backend routes._

---

## 📌 Example: Send Money Response

```json
{
  "status": "success",
  "message": "Payment successful",
  "sender_id": 1,
  "receiver_id": 2,
  "amount": 1,
  "remaining_balance": 3496
}
```

## 📌 Example: Failed Authentication Response

```json
{
  "status": "failed",
  "error": "not_authenticated",
  "message": "Please authenticate before making a payment."
}
```

---

## 🧩 Future Improvements
- Add transaction history export (CSV/PDF)
- Add real-time balance updates
- Add multi-factor authentication
- Improve AI analysis with retry-suggestion logic for failed payments

---

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request with any improvements.

## 📄 License
This project is licensed under the [MIT License](LICENSE).
