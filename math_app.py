import streamlit as st
import random
import time
from datetime import datetime

def get_solution_steps(problem, answer, topic, user_answer):
    if topic == "Arithmetic":
        a, operation, b = problem.split()
        a, b = int(a), int(b)
        steps = []
        
        if operation == '+':
            steps = [
                f"1. Line up the numbers: {a} + {b}",
                f"2. Add from right to left: {a} + {b} = {answer}"
            ]
        elif operation == '-':
            steps = [
                f"1. Line up the numbers: {a} - {b}",
                f"2. Subtract: {a} - {b} = {answer}"
            ]
        elif operation == '×':
            steps = [
                f"1. Multiply the numbers: {a} × {b}",
                f"2. {a} × {b} = {answer}"
            ]
        elif operation == '÷':
            steps = [
                f"1. Set up division: {a} ÷ {b}",
                f"2. {a} ÷ {b} = {answer}"
            ]
    
    elif topic == "Algebra":
        if "+" in problem:
            parts = problem.split("=")
            steps = [
                "1. Start with the equation: " + problem,
                f"2. Isolate the variable: x = {answer}",
                f"3. Check: Plug {answer} back into the original equation"
            ]
        else:
            steps = [
                "1. Start with the equation: " + problem,
                f"2. Solve for x: x = {answer}",
                f"3. Verify your solution by substituting x = {answer}"
            ]
    
    elif topic == "Geometry":
        if "rectangle" in problem:
            width = int(problem.split("width")[1].split("and")[0])
            height = int(problem.split("height")[1])
            steps = [
                "1. Use the formula: Area = width × height",
                f"2. Plug in the values: Area = {width} × {height}",
                f"3. Calculate: Area = {answer} square units"
            ]
        elif "triangle" in problem:
            base = int(problem.split("base")[1].split("and")[0])
            height = int(problem.split("height")[1])
            steps = [
                "1. Use the formula: Area = ½ × base × height",
                f"2. Plug in the values: Area = ½ × {base} × {height}",
                f"3. Calculate: Area = {answer} square units"
            ]
        elif "circle" in problem:
            radius = int(problem.split("radius")[1].split("(")[0])
            steps = [
                "1. Use the formula: Area = πr²",
                f"2. Plug in radius = {radius}: Area = 3.14159 × {radius}²",
                f"3. Calculate: Area = {answer} square units"
            ]
    
    return steps

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
    
    operation = random.choice(['+', '-', '×', '÷'])
    if operation == '+':
        answer = a + b
    elif operation == '-':
        answer = a - b
    elif operation == '×':
        answer = a * b
    else:
        # Ensure clean division
        answer = a
        b = random.randint(1, 10)
        a = answer * b
    
    problem = f"{a} {operation} {b}"
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
        width = random.randint(2, 10)
        height = random.randint(2, 10)
        answer = width * height
        problem = f"Find the area of a rectangle with width {width} and height {height}"
    elif difficulty == "Medium":
        base = random.randint(2, 10)
        height = random.randint(2, 10)
        answer = (base * height) / 2
        problem = f"Find the area of a triangle with base {base} and height {height}"
    else:
        radius = random.randint(2, 10)
        answer = round(3.14159 * radius * radius, 2)
        problem = f"Find the area of a circle with radius {radius} (use π = 3.14159)"
    
    return problem, answer

def main():
    st.set_page_config(page_title="Math Practice", page_icon="🔢")
    
    st.title("🎓 Math Practice")
    st.markdown("""
    Practice your math skills with different topics and difficulty levels.
    Get immediate feedback and learn from detailed explanations!
    """)
    
    # Initialize session state
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    
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
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate problem
        if 'current_problem' not in st.session_state:
            if topic == "Arithmetic":
                st.session_state.current_problem = generate_arithmetic_problem(difficulty)
            elif topic == "Algebra":
                st.session_state.current_problem = generate_algebra_problem(difficulty)
            else:
                st.session_state.current_problem = generate_geometry_problem(difficulty)
        
        problem, answer = st.session_state.current_problem
        
        st.markdown(f"### Problem:")
        st.markdown(f"#### {problem}")
        
        user_answer = st.number_input("Your answer:", step=0.01, format="%.2f")
        
        if st.button("Submit Answer"):
            st.session_state.total_questions += 1
            
            if abs(user_answer - answer) < 0.01:
                st.success("🎉 Correct! Well done!")
                st.session_state.score += 1
                st.session_state.streak += 1
            else:
                st.error("❌ Not quite correct.")
                st.session_state.streak = 0
                
                # Show solution steps
                st.markdown("### Let's solve this step by step:")
                steps = get_solution_steps(problem, answer, topic, user_answer)
                for step in steps:
                    st.markdown(f"- {step}")
                st.markdown(f"**The correct answer is: {answer}**")
            
            # Generate new problem
            if topic == "Arithmetic":
                st.session_state.current_problem = generate_arithmetic_problem(difficulty)
            elif topic == "Algebra":
                st.session_state.current_problem = generate_algebra_problem(difficulty)
            else:
                st.session_state.current_problem = generate_geometry_problem(difficulty)
            
            st.rerun()
    
    with col2:
        # Simple progress bar
        st.markdown("### Your Progress")
        if st.session_state.total_questions > 0:
            progress = st.session_state.score / st.session_state.total_questions
            st.progress(progress)
            st.markdown(f"Accuracy: {(progress * 100):.1f}%")
    
    # Tips section
    with st.expander("Need help? Check these tips!"):
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
