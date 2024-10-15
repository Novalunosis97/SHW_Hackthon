import streamlit as st
import pandas as pd

def home_page():
    st.title("Welcome to Interest Recommender")
    st.write("This app helps you discover new areas of interest based on your responses.")
    
    if st.button("Start Questionnaire"):
        st.session_state.page = "questions"

def questions_page():
    st.title("Interest Questionnaire")
    
    with st.form("questionnaire"):
        st.write("Please answer the following questions:")
        
        # Add your questions here
        q1 = st.text_input("What's your favorite hobby?")
        q2 = st.selectbox("How much free time do you have per week?", 
                          ["0-5 hours", "6-10 hours", "11-20 hours", "20+ hours"])
        q3 = st.slider("On a scale of 1-10, how adventurous are you?", 1, 10)
        q4 = st.text_area("Describe your ideal day:")
        q5 = st.multiselect("Select areas you're already interested in:", 
                            ["Technology", "Art", "Sports", "Science", "Literature", "Music"])
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Save responses
            responses = {
                "Favorite Hobby": q1,
                "Free Time": q2,
                "Adventurousness": q3,
                "Ideal Day": q4,
                "Current Interests": ", ".join(q5)
            }
            
            # Convert to DataFrame for easy saving/displaying
            df = pd.DataFrame([responses])
            
            # In a real app, you might save this to a database
            # For now, we'll just display it and store in session state
            st.session_state.responses = df
            
            st.success("Thank you for your responses!")
            st.write("Your responses:")
            st.write(df)

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "questions":
        questions_page()

if __name__ == "__main__":
    main()
