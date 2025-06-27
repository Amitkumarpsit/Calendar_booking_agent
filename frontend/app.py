import requests
import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="Calendar Booking Agent",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Calendar Booking Agent")
st.markdown("---")

# Force reset session state if it contains old format data
if "history" in st.session_state:
    if st.session_state.history and isinstance(st.session_state.history[0], str):
        st.session_state.history = []  # Clear old string format data

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar with instructions
with st.sidebar:
    st.header("📝 How to use")
    st.markdown("""
    **Examples of what you can say:**
    - "Book a meeting tomorrow at 3 PM"
    - "Schedule appointment for Monday at 10 AM"
    - "Book a slot between 2-3 PM today"
    - "Meeting next Friday at 4 PM"
    
    **Supported formats:**
    - Tomorrow at [time]
    - [Day] at [time]
    - Between [time1] and [time2]
    - [Date] at [time]
    """)
    
    # Add manual reset button in sidebar
    if st.button("🔄 Reset Chat", help="Clear all chat history"):
        st.session_state.history = []
        st.rerun()

# Main chat interface
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("💬 Your message:", placeholder="e.g., Book a meeting tomorrow at 3 PM", key="user_input")

with col2:
    send_button = st.button("📤 Send", type="primary")

# Handle message sending
if send_button and user_input:
    with st.spinner("🔄 Processing your request..."):
        bot_response = None
        try:
            # Make API request
            response = requests.post(
                "http://127.0.0.1:8000/chat", 
                json={"message": user_input},
                timeout=30
            )
            try:
                # Try to parse JSON response
                result = response.json()
                bot_response = result.get("response", "⚠️ Invalid response from server.")
            except Exception as json_error:
                # If not JSON, show error and log raw response
                bot_response = f"⚠️ Server response parsing error: {json_error}. Raw response: {response.text}"
        except requests.exceptions.Timeout:
            bot_response = "⚠️ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            bot_response = "⚠️ Could not connect to server. Make sure the FastAPI server is running on http://127.0.0.1:8000"
        except Exception as e:
            bot_response = f"⚠️ Error: {e}"

        # Add to history as dictionary (ensure correct format)
        if isinstance(bot_response, str) and isinstance(user_input, str):
            st.session_state.history.append({
                "user": user_input, 
                "bot": bot_response, 
                "timestamp": time.time()
            })
        else:
            # Fallback for unexpected types
            st.session_state.history.append(str(bot_response))
        
        # Clear the input field by rerunning
        st.rerun()

# Display chat history
st.markdown("### 💬 Chat History")
if st.session_state.history:
    for i, chat in enumerate(reversed(st.session_state.history)):
        with st.container():
            try:
                # Safety check to ensure chat is a dictionary
                if isinstance(chat, dict) and "user" in chat and "bot" in chat:
                    st.markdown(f"**👤 You:** {chat['user']}")
                    st.markdown(f"**🤖 Agent:** {chat['bot']}")
                else:
                    # Handle unexpected format
                    st.markdown(f"**Message:** {str(chat)}")
            except Exception as e:
                st.error(f"Error displaying message: {e}")
            
            st.markdown("---")
else:
    st.info("👋 Start by typing a message above to book your first meeting!")

# Display server status
with st.expander("🔧 Server Status", expanded=False):
    try:
        health_response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API Server is running")
        else:
            st.error("❌ API Server responded with error")
    except:
        st.error("❌ Cannot connect to API server. Make sure it's running on http://127.0.0.1:8000")