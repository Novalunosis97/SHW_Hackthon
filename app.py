import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Custom CSS
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# Lottie animations
lottie_home = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_1pxqjqps.json")
lottie_question = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_5tl1xxnz.json")

def home_page():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h1 class='fancy-title'>Discover Your Passion</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Embark on a journey to uncover new interests and hobbies!</p>", unsafe_allow_html=True)
        
        if st.button("Start Your Adventure", key="start_button"):
            st.session_state.page = "questions"
    
    with col2:
        st_lottie(lottie_home, height=300, key="home_animation")

def questions_page():
    st.markdown("<h1 class='fancy-title'>Interest Explorer</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("questionnaire"):
            st.markdown("<p class='form-header'>Let's dive into your preferences:</p>", unsafe_allow_html=True)
            
            q1 = st.text_input("🌟 What's your ultimate passion?")
            q2 = st.select_slider("🕰️ How much leisure time do you have weekly?", 
                                  options=["0-5 hrs", "6-10 hrs", "11-20 hrs", "20+ hrs"])
            q3 = st.slider("🚀 Rate your thirst for adventure (1-10):", 1, 10)
            q4 = st.text_area("🌈 Paint a picture of your perfect day:")
            q5 = st.multiselect("🔍 Select domains that pique your curiosity:", 
                                ["Tech & Innovation", "Arts & Creativity", "Sports & Fitness", 
                                 "Science & Discovery", "Literature & Writing", "Music & Performance"])
            
            submitted = st.form_submit_button("Reveal My Interests")
            
            if submitted:
                responses = {
                    "Ultimate Passion": q1,
                    "Weekly Leisure": q2,
                    "Adventure Rating": q3,
                    "Perfect Day": q4,
                    "Curiosity Domains": ", ".join(q5)
                }
                df = pd.DataFrame([responses])
                st.session_state.responses = df
                st.success("Thanks for sharing your world with us!")
                st.balloons()
                st.markdown("<div class='results-container'>", unsafe_allow_html=True)
                st.markdown("<h3 class='results-header'>Your Unique Profile:</h3>", unsafe_allow_html=True)
                st.write(df)
                st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st_lottie(lottie_question, height=300, key="question_animation")

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "questions":
        questions_page()

if __name__ == "__main__":
    main()
