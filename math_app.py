import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
from datetime import datetime

# Custom problem generators for different topics
def generate_arithmetic_problem(difficulty):
    if difficulty == "Easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
    elif difficulty == "Medium":
        a = random.randint(10, 50)
        b = random.randint(10, 50)
    else:
        a = random.randint(50, 100)
        b = random.randint(50, 100)
    
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        answer = a + b
        problem = f"{a} + {b}"
    elif operation == '-':
        answer = a - b
        problem = f"{a} - {b}"
    elif operation == '*':
        answer = a * b
        problem = f"{a} × {b}"
    else:
        # Ensure clean division
        answer = a
        b = random.randint(1, 10)
        a = answer * b
        problem = f"{a} ÷ {b}"
    
    return problem, answer

def generate_algebra_problem(difficulty):
    if difficulty == "Easy":
        x = random.randint(1, 10)
        a = random.randint(1, 5)
        b = random.randint(1, 10)
        answer = x
        problem = f"{a}x + {b} = {a*x + b}"
    elif difficulty == "Medium":
        x = random.randint(1, 10)
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        c = random.randint(1, 5)
        answer = x
        problem = f"{a}x + {b} = {c}x + {a*x + b - c*x}"
    else:
        x = random.randint(1, 10)
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        answer = x
        problem = f"{a}x² + {b}x = {a*x*x + b*x}"
    
    return f"Solve for x: {problem}", answer

def generate_geometry_problem(difficulty):
    if difficulty == "Easy":
        # Area of rectangle
        width = random.randint(2, 10)
        height = random.randint(2, 10)
        answer = width * height
        problem = f"Find the area of a rectangle with width {width} and height {height}"
    elif difficulty == "Medium":
        # Area of triangle
        base = random.randint(2, 10)
        height = random.randint(2, 10)
        answer = (base * height) / 2
        problem = f"Find the area of a triangle with base {base} and height {height}"
    else:
        # Area of circle
        radius = random.randint(2, 10)
        answer = round(3.14159 * radius * radius, 2)
        problem = f"Find the area of a circle with radius {radius} (use π = 3.14159)"
    
    return problem, answer

def save_progress():
    if 'history' in st.session_state:
        df = pd.DataFrame(st.session_state.history)
        df.to_csv('math_progress.csv', index=False)

def load_progress():
    try:
        return pd.read_csv('math_progress.csv')
    except:
        return pd.DataFrame(columns=['timestamp', 'topic', 'difficulty', 'correct', 'time_taken'])

def main():
    st.set_page_config(page_title="Advanced Math Practice", page_icon="🔢", layout="wide")
    
    # Initialize session state
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    # Header
    st.title("🎓 Advanced Math Practice")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        topic = st.selectbox("Choose topic:", ["Arithmetic", "Algebra", "Geometry"])
        difficulty = st.selectbox("Choose difficulty:", ["Easy", "Medium", "Hard"])
        
        st.markdown("---")
        st.markdown(f"**Score:** {st.session_state.score}")
        st.markdown(f"**Questions:** {st.session_state.total_questions}")
        st.markdown(f"**Streak:** {st.session_state.streak}🔥")
        
        if st.button("Reset Progress"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.streak = 0
            st.session_state.history = []
            st.rerun()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate problem based on topic
        if 'current_problem' not in st.session_state:
            if topic == "Arithmetic":
                st.session_state.current_problem = generate_arithmetic_problem(difficulty)
            elif topic == "Algebra":
                st.session_state.current_problem = generate_algebra_problem(difficulty)
            else:
                st.session_state.current_problem = generate_geometry_problem(difficulty)
        
        problem, answer = st.session_state.current_problem
        
        # Display problem
        st.markdown(f"### Problem:")
        st.markdown(f"#### {problem}")
        
        # Answer input
        user_answer = st.number_input("Your answer:", step=0.01, format="%.2f")
        
        # Submit button
        if st.button("Submit Answer"):
            time_taken = time.time() - st.session_state.start_time
            st.session_state.total_questions += 1
            
            # Record attempt in history
            st.session_state.history.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'topic': topic,
                'difficulty': difficulty,
                'correct': abs(user_answer - answer) < 0.01,
                'time_taken': round(time_taken, 2)
            })
            
            if abs(user_answer - answer) < 0.01:  # Allow for small floating-point differences
                st.success("🎉 Correct! Well done!")
                st.session_state.score += 1
                st.session_state.streak += 1
            else:
                st.error(f"❌ Not quite. The correct answer was {answer}")
                st.session_state.streak = 0
            
            # Save progress
            save_progress()
            
            # Generate new problem
            if topic == "Arithmetic":
                st.session_state.current_problem = generate_arithmetic_problem(difficulty)
            elif topic == "Algebra":
                st.session_state.current_problem = generate_algebra_problem(difficulty)
            else:
                st.session_state.current_problem = generate_geometry_problem(difficulty)
            
            st.session_state.start_time = time.time()
            st.rerun()
    
    with col2:
        # Analytics section
        st.markdown("### Your Progress")
        
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            
            # Success rate chart
            success_rate = df['correct'].rolling(window=5).mean()
            fig1 = px.line(success_rate, title='Success Rate (Last 5 Questions)')
            fig1.update_layout(yaxis_range=[0, 1])
            st.plotly_chart(fig1, use_container_width=True)
            
            # Topic performance
            st.markdown("#### Topic Performance")
            topic_stats = df.groupby('topic')['correct'].agg(['count', 'mean']).round(2)
            st.dataframe(topic_stats)
            
            # Average time per difficulty
            st.markdown("#### Average Time by Difficulty")
            time_stats = df.groupby('difficulty')['time_taken'].mean().round(2)
            st.dataframe(time_stats)
    
    # Tips and hints
    with st.expander("Tips & Formulas"):
        if topic == "Arithmetic":
            st.markdown("""
            - Remember order of operations (PEMDAS)
            - For division, check if your answer needs rounding
            - Use multiplication to check division
            """)
        elif topic == "Algebra":
            st.markdown("""
            - Isolate the variable on one side
            - What you do to one side, do to the other
            - For quadratic equations, factor or use quadratic formula
            """)
        else:
            st.markdown("""
            - Area of rectangle = length × width
            - Area of triangle = ½ × base × height
            - Area of circle = πr²
            - π ≈ 3.14159
            """)

if __name__ == "__main__":
    main()
