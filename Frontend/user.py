import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Payment Agent",
    page_icon="💳"
)

st.title("💳 AI Payment Agent")


# -----------------------------
# SESSION STATE
# -----------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None


# -----------------------------
# LOGIN
# -----------------------------

if not st.session_state.authenticated:

    st.subheader("🔐 Login")

    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:

            response = requests.post(
                f"{API_URL}/agent/authenticate",
                params={
                    "user_id": user_id,
                    "password": password
                }
            )

            data = response.json()

            if response.status_code == 200 and data.get("authenticated"):

                st.session_state.authenticated = True
                st.session_state.user_id = data["user_id"]

                st.success("Login successful!")
                st.rerun()

            else:

                st.error(
                    data.get(
                        "reason",
                        "Authentication failed"
                    )
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI server."
            )


# -----------------------------
# DASHBOARD
# -----------------------------

else:

    st.success(
        f"Authenticated User: {st.session_state.user_id}"
    )

    st.divider()

    # -------------------------
    # PAYMENT
    # -------------------------

    st.subheader("💸 Send Money")

    receiver_id = st.number_input(
        "Receiver ID",
        min_value=1,
        step=1
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=1.0,
        step=100.0
    )

    if st.button("Send Money"):

        try:

            response = requests.post(
                f"{API_URL}/agent/pay",
                json={
                    "receiver_id": receiver_id,
                    "amount": amount
                }
            )

            data = response.json()

            if response.status_code == 200:

                st.success("Payment request completed")

                st.json(data)

            else:

                st.error("Payment failed")

                st.json(data)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI server."
            )

    st.divider()

    # -------------------------
    # AI ANALYSIS
    # -------------------------

    st.subheader("🤖 AI Transaction Analysis")

    st.write(
        "Analyze your previous transactions "
        "and understand why payments failed."
    )

    if st.button("🔍 Analyze My Transactions"):

        try:

            response = requests.post(
                f"{API_URL}/agent/analyze"
            )

            data = response.json()

            if response.status_code == 200:

                st.success("Analysis completed")

                st.subheader("AI Analysis")

                st.write(
                    data.get(
                        "ai_analysis",
                        "No analysis available."
                    )
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Total Transactions",
                        data.get(
                            "total_transactions",
                            0
                        )
                    )

                with col2:
                    st.metric(
                        "Successful",
                        data.get(
                            "successful_transactions",
                            0
                        )
                    )

                with col3:
                    st.metric(
                        "Failed",
                        data.get(
                            "failed_transactions",
                            0
                        )
                    )

            else:

                st.error(
                    data.get(
                        "detail",
                        "Analysis failed"
                    )
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI server."
            )

    st.divider()

    # -------------------------
    # LOGOUT
    # -------------------------

    if st.button("Logout"):

        st.session_state.authenticated = False
        st.session_state.user_id = None

        st.rerun()