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

                reason = data.get("reason", "")

                if reason == "user_not_found":
                    st.error(
                        f"❌ User ID {int(user_id)} does not exist. "
                        "Please check your User ID."
                    )
                elif reason == "invalid_password":
                    st.error(
                        "❌ Incorrect password. Please try again."
                    )
                else:
                    st.error(
                        "❌ Authentication failed. Please try again."
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

                st.success(
                    "Payment request completed"
                )

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
                f"{API_URL}/agent/analyze",
                json={
                    "user_id": int(st.session_state.user_id)
                }
            )

            # Safely parse JSON — server may return empty/HTML on errors
            try:
                data = response.json()
            except Exception:
                st.error(
                    f"❌ Server error (status {response.status_code}). "
                    "Please log out and log in again, then retry."
                )
                st.stop()

            if response.status_code == 200:

                st.success(
                    "✅ Analysis completed"
                )

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

            elif response.status_code == 401:

                st.warning(
                    "⚠️ Session expired. Please log out and log in again."
                )

            else:

                st.error(
                    data.get(
                        "detail",
                        "Analysis failed. Please try again."
                    )
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI server."
            )


    st.divider()


    # -------------------------
    # LOAN CHECK
    # -------------------------

    st.subheader("🏦 Check Loan Status")

    st.write(
        "Enter your User ID and Name to check your loan details."
    )

    loan_user_id = st.number_input(
        "Loan User ID",
        min_value=1,
        step=1,
        key="loan_user_id"
    )

    loan_name = st.text_input(
        "Name",
        key="loan_name"
    )

    if st.button("Check Loan"):

        if not loan_name.strip():

            st.warning(
                "Please enter your name."
            )

        else:

            try:

                response = requests.post(
                    f"{API_URL}/agent/check-loan",
                    json={
                        "user_id": str(loan_user_id),
                        "name": loan_name
                    }
                )

                data = response.json()

                if response.status_code == 200:

                    # -------------------------
                    # USER HAS LOAN
                    # -------------------------

                    if data.get("has_loan"):

                        st.success(
                            "Loan found"
                        )

                        st.subheader(
                            "Loan Details"
                        )

                        st.write(
                            "**Loan Status:** Yes"
                        )

                        st.write(
                            f"**Loan Amount:** ₹{data.get('loan_amount')}"
                        )

                        st.write(
                            f"**Due Date:** {data.get('due_date')}"
                        )

                    # -------------------------
                    # USER DOES NOT HAVE LOAN
                    # -------------------------

                    else:

                        st.info(
                            "Loan Status: No"
                        )

                        st.write(
                            data.get(
                                "message",
                                "You do not have an active loan."
                            )
                        )

                else:

                    st.error(
                        data.get(
                            "detail",
                            data.get(
                                "message",
                                "Failed to check loan details."
                            )
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