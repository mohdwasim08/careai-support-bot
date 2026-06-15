import streamlit as st
from careai import get_response, update_history

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="CareAI Support",
    page_icon="🤖",
    layout="centered"
)

# ── Session state setup ──────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "analytics" not in st.session_state:
    st.session_state.analytics = {
        "total_messages": 0,
        "escalations": 0,
        "resolved": 0,
        "order_queries": 0,
        "return_queries": 0,
        "shipping_queries": 0,
        "other_queries": 0
    }

# ── Intent detector ──────────────────────────────────────────
def detect_intent(message: str) -> str:
    message = message.lower()
    if any(word in message for word in ["order", "track", "status", "#"]):
        return "order"
    elif any(word in message for word in ["return", "refund", "exchange"]):
        return "return"
    elif any(word in message for word in ["shipping", "delivery", "deliver"]):
        return "shipping"
    elif any(word in message for word in ["human", "agent", "person", "speak"]):
        return "escalation"
    else:
        return "other"

# ── Sidebar analytics ────────────────────────────────────────
with st.sidebar:
    st.title("📊 CareAI Analytics")
    st.caption("Live session stats")
    st.divider()

    a = st.session_state.analytics
    total = a["total_messages"]

    st.metric("💬 Total Messages", total)
    st.metric("✅ Resolved", a["resolved"])
    st.metric("🔁 Escalated to Agent", a["escalations"])

    st.divider()
    st.subheader("Query Breakdown")

    if total > 0:
        st.progress(a["order_queries"] / max(total, 1),
                    text=f"📦 Order tracking: {a['order_queries']}")
        st.progress(a["return_queries"] / max(total, 1),
                    text=f"🔄 Returns: {a['return_queries']}")
        st.progress(a["shipping_queries"] / max(total, 1),
                    text=f"🚚 Shipping: {a['shipping_queries']}")
        st.progress(a["other_queries"] / max(total, 1),
                    text=f"💡 Other: {a['other_queries']}")
    else:
        st.caption("No queries yet. Start chatting!")

    st.divider()

    # Resolution rate
    if total > 0:
        rate = round((a["resolved"] / total) * 100)
        st.metric("📈 Resolution Rate", f"{rate}%")
    
    # Reset button
    if st.button("🔄 Reset Session"):
        st.session_state.chat_history = []
        st.session_state.messages = []
        st.session_state.analytics = {
            "total_messages": 0,
            "escalations": 0,
            "resolved": 0,
            "order_queries": 0,
            "return_queries": 0,
            "shipping_queries": 0,
            "other_queries": 0
        }
        st.rerun()

# ── Main chat area ───────────────────────────────────────────
st.title("🤖 CareAI")
st.caption("ShopEase customer support — available 24/7")
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Quick reply buttons ──────────────────────────────────────
st.write("**Quick actions:**")
col1, col2, col3, col4 = st.columns(4)

quick_reply = None
with col1:
    if st.button("📦 Track order"):
        quick_reply = "I want to track my order"
with col2:
    if st.button("🔄 Return item"):
        quick_reply = "I want to return an item"
with col3:
    if st.button("🚚 Shipping info"):
        quick_reply = "What are your shipping options?"
with col4:
    if st.button("👤 Talk to agent"):
        quick_reply = "I want to speak to a human agent"

# ── Chat input ───────────────────────────────────────────────
user_input = st.chat_input("Type your message here...")

if quick_reply:
    user_input = quick_reply

# ── Process message ──────────────────────────────────────────
if user_input:

    # Detect intent and update analytics
    intent = detect_intent(user_input)
    st.session_state.analytics["total_messages"] += 1

    if intent == "order":
        st.session_state.analytics["order_queries"] += 1
    elif intent == "return":
        st.session_state.analytics["return_queries"] += 1
    elif intent == "shipping":
        st.session_state.analytics["shipping_queries"] += 1
    elif intent == "escalation":
        st.session_state.analytics["escalations"] += 1
    else:
        st.session_state.analytics["other_queries"] += 1

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get CareAI reply
    with st.chat_message("assistant"):
        with st.spinner("CareAI is typing..."):
            reply = get_response(st.session_state.chat_history, user_input)
        st.markdown(reply)

    # Track resolved vs escalated
    if "connecting you now" in reply.lower() or "support specialist" in reply.lower():
        st.session_state.analytics["escalations"] += 0  # already counted above
    else:
        st.session_state.analytics["resolved"] += 1

    # Save to display history
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Update Gemini conversation history
    st.session_state.chat_history = update_history(
        st.session_state.chat_history,
        user_input,
        reply
    )