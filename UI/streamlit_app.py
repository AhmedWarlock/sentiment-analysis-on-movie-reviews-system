
import streamlit as st
import requests
from PIL import Image

# Define the FastAPI URL endpoint
API_URL = "http://127.0.0.1:8000/predict"  # Make sure your FastAPI server is running at this URL


# Set Streamlit page configuration
st.set_page_config(
    page_title="🎬 Movie Review Sentiment Analysis 🎬",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="auto"
)

# Add a header image and styling
st.markdown(
    """a
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

# User input
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
            # Send a POST request to the FastAPI endpoint
            response = requests.post(API_URL, json=payload)

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

# Footer
st.markdown(
    """
    <hr style="border: 1px solid #f0c929;">
    <div style="text-align: center; color: #f0c929;">
        Made with ❤️ by Duaa | Powered by Streamlit
    </div>
    """, unsafe_allow_html=True
)
