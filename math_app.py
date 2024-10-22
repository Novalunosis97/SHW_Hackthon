import streamlit as st
import random
import time

def generate_problem(difficulty):
    if difficulty == "Easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
    elif difficulty == "Medium":
        a = random.randint(10, 50)
        b = random.randint(10, 50)
    else:
        a = random.randint(50, 100)
        b = random.randint(50, 100)
    
    operation = random.choice(['+', '-', '*'])
    if operation == '+':
        answer = a + b
    elif operation == '-':
        answer = a - b
    else:
        answer = a * b
    
    return a, b, operation, answer

def main():
    st.set_page_config(page_title="Math Practice App", page_icon="🔢")
    
    st.title("🎓 Math Practice App")
    st.markdown("""
    Welcome to the Math Practice App! Test your math skills with randomly generated problems.
    Keep track of your score and try to improve!
    """)
    
    # Initialize session state variables
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        difficulty = st.selectbox("Choose difficulty:", ["Easy", "Medium", "Hard"])
        st.markdown("---")
        st.markdown(f"**Current Score:** {st.session_state.score}")
        st.markdown(f"**Questions Attempted:** {st.session_state.total_questions}")
        st.markdown(f"**Current Streak:** {st.session_state.streak}🔥")
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if 'problem' not in st.session_state:
            st.session_state.problem = generate_problem(difficulty)
        
        a, b, operation, answer = st.session_state.problem
        st.markdown(f"### What is: {a} {operation} {b} = ?")
        
        user_answer = st.number_input("Your answer:", step=1, key="answer_input")
        
        if st.button("Submit Answer"):
            st.session_state.total_questions += 1
            
            if user_answer == answer:
                st.success("🎉 Correct! Well done!")
                st.session_state.score += 1
                st.session_state.streak += 1
                time.sleep(1)
            else:
                st.error(f"❌ Not quite. The correct answer was {answer}")
                st.session_state.streak = 0
                time.sleep(1)
            
            # Generate new problem
            st.session_state.problem = generate_problem(difficulty)
            st.experimental_rerun()
    
    with col2:
        # Progress indicators
        progress = st.session_state.score / max(st.session_state.total_questions, 1)
        st.markdown("### Progress")
        st.progress(progress)
        
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.markdown(f"Accuracy: {accuracy:.1f}%")

if __name__ == "__main__":
    main()
