import streamlit as st
import requests
from PIL import Image

# Define the FastAPI URL endpoints
BASE_API_URL = "http://127.0.0.1:8000"
TOKEN_URL = f"{BASE_API_URL}/token"
PREDICT_URL = f"{BASE_API_URL}/predict"
USER_INFO_URL = f"{BASE_API_URL}/users/me/"

# Set Streamlit page configuration
st.set_page_config(
    page_title="🎬 Movie Review Sentiment Analysis 🎬",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="auto"  # Sidebar will start visible but can be hidden automatically
)

# Add a header image and styling
st.markdown(
    """
    <style>
    .header {
        background-color: #1f1f1f;
        padding: 15px;
        text-align: center;
        color: #f0c929;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stApp {
        background: linear-gradient(to right, #141E30, #243B55);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="header"><h1>🎬 Movie Review Sentiment Analysis 🎥</h1></div>', unsafe_allow_html=True)

# Display a movie-themed image
image = Image.open("/Users/ahmedawad/Desktop/sentiment-analysis-on-movie-reviews-system/UI/images/movies.jpg")
st.image(image, caption='Let’s find out what people think about this movie!', use_column_width=True)

# Initialize session state for storing the token
if "token" not in st.session_state:
    st.session_state.token = None

# Function to login and get a token
def login(username, password):
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(TOKEN_URL, data=payload)
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.success("Login successful!")

            # JavaScript to hide the sidebar after successful login
            st.markdown(
                """
                <script>
                const sidebar = parent.document.querySelector('section[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.style.display = 'none';
                }
                </script>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Login failed: Incorrect username or password.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the authentication service: {e}")

# User login section
st.sidebar.markdown("## Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    login(username, password)

# Check if the user is logged in by checking if the token is stored
if st.session_state.token:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Display the user information if logged in
    try:
        user_info_response = requests.get(USER_INFO_URL, headers=headers)
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            st.sidebar.markdown(f"### Logged in as: {user_info.get('username')}")
        else:
            st.sidebar.error("Unable to fetch user information.")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Error fetching user information: {e}")

    # User input for movie review
    review_input = st.text_area("Enter a movie review:", "")

    # Create a button to make a prediction
    if st.button("🎬 Analyze Sentiment 🎬"):
        if not review_input:
            st.error("Please enter a review to analyze.")
        else:
            # Prepare the data payload
            payload = {
                "review": review_input
            }
            
            try:
                # Send a POST request to the FastAPI prediction endpoint with the JWT token
                response = requests.post(PREDICT_URL, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 200:
                    result = response.json()
                    # Display the results
                    sentiment_label = result.get("sentiment", "Unknown")
                    probability = result.get("Model Confidence Score", 0)

                    st.markdown(f"### 🎭 Sentiment Analysis Result 🎭")
                    if sentiment_label == "Positive":
                        st.markdown(
                            f"<div style='background-color: #28a745; padding: 10px; border-radius: 5px; text-align: center;'>"
                            f"<h3 style='color: white;'>{sentiment_label} (Confidence: {probability:.2f})</h3></div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<div style='background-color: #dc3545; padding: 10px; border-radius: 5px; text-align: center;'>"
                            f"<h3 style='color: white;'>{sentiment_label} (Confidence: {probability:.2f})</h3></div>",
                            unsafe_allow_html=True
                        )

                else:
                    st.error("An error occurred with the prediction request.")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the prediction service: {e}")

else:
    st.warning("Please log in to access the sentiment analysis service.")

# Footer
st.markdown(
    """
    <hr style="border: 1px solid #f0c929;">
    <div style="text-align: center; color: #f0c929;">
        Made with ❤️ by Group 2 | Powered by Streamlit
    </div>
    """, unsafe_allow_html=True
)