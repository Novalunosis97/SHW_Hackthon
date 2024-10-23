import streamlit as st
import random
import time
from datetime import datetime

def analyze_mistake(problem, correct_answer, user_answer, topic):
    """Analyze what went wrong with the user's answer"""
    if topic == "Arithmetic":
        a, operation, b = problem.split()
        a, b = int(a), int(b)
        
        if operation == '+':
            if user_answer < correct_answer:
                return f"Your answer {user_answer} is too small. Did you carry all digits correctly?"
            else:
                return f"Your answer {user_answer} is too large. Check if you added all digits correctly."
        
        elif operation == '-':
            if user_answer > correct_answer:
                return f"Your answer {user_answer} is too large. Did you borrow correctly?"
            else:
                return f"Your answer {user_answer} is too small. Check your subtraction steps."
        
        elif operation == '×':
            if user_answer == a + b:
                return f"It looks like you added {a} + {b} instead of multiplying them."
            elif user_answer < correct_answer:
                return f"Your answer {user_answer} is too small. Check if you multiplied all digits correctly."
            else:
                return f"Your answer {user_answer} is too large. Check your multiplication steps."
        
        elif operation == '÷':
            if user_answer == a * b:
                return f"It looks like you multiplied {a} × {b} instead of dividing them."
            elif abs(user_answer - correct_answer) < 1:
                return f"You're close! Did you round your answer correctly?"
            else:
                return f"Check your division steps. Remember, {a} ÷ {b} means 'how many {b}s go into {a}?'"
            
        elif topic == "Algebra":
        if abs(user_answer) == abs(correct_answer) and user_answer != correct_answer:
            return "Check the sign of your answer. Did you move terms correctly between sides?"
        elif "+" in problem:
            equation = problem.split("=")[0].strip()
            if user_answer * 2 == correct_answer:
                return f"Did you forget to consider both sides of the equation? Remember to isolate the variable."
            else:
                return f"Check how you isolated the variable. What steps did you take to solve for x?"
        else:
            return f"Your answer {user_answer} doesn't satisfy the equation. Try plugging it back in to check."
            
        elif topic == "Geometry":
        if "rectangle" in problem:
            if abs(user_answer - correct_answer) < correct_answer * 0.1:
                return "You're close! Double-check your multiplication."
            else:
                return "Remember: Area of a rectangle = width × height. Did you multiply both dimensions?"
                
            elif "triangle" in problem:
            if user_answer == correct_answer * 2:
                return "Did you forget to divide by 2? Remember: Area of triangle = (base × height) ÷ 2"
            else:
                return "Remember: Area of triangle = (base × height) ÷ 2. Check your calculations."
                
            elif "circle" in problem:
            if abs(user_answer - correct_answer) < 1:
                return "Almost there! Did you use 3.14159 for π?"
            elif user_answer == correct_answer / 2:
                return "Did you forget to square the radius? Area = πr²"
            else:
                return "Remember: Area of circle = πr². Check your calculations."
    
    return "Let's look at how to solve this step by step."

def get_solution_steps(problem, answer, topic, user_answer):
    """Generate step-by-step solution explanation"""
    steps = []
    
    if topic == "Arithmetic":
        try:
            a, operation, b = problem.split()
            a, b = int(a), int(b)
            
            if operation == '+':
                steps = [
                    f"1. Line up the numbers vertically:\n   {a}\n   + {b}",
                    f"2. Add digits from right to left\n   {a}\n   + {b}\n   ———\n   {answer}",
                    "3. Check: Does each column sum correctly?",
                    f"The correct answer is {answer}"
                ]
            elif operation == '-':
                steps = [
                    f"1. Line up the numbers vertically:\n   {a}\n   - {b}",
                    f"2. Subtract digits from right to left\n   {a}\n   - {b}\n   ———\n   {answer}",
                    "3. Check: Do you need to borrow from the next column?",
                    f"The correct answer is {answer}"
                ]
            elif operation == '×':
                steps = [
                    f"1. Set up multiplication:\n   {a}\n   × {b}",
                    f"2. Multiply each digit:\n   {a}\n   × {b}\n   ———\n   {answer}",
                    "3. Check: Did you add the products correctly?",
                    f"The correct answer is {answer}"
                ]
            elif operation == '÷':
                steps = [
                    f"1. Set up division: {a} ÷ {b}",
                    f"2. How many times does {b} go into {a}?",
                    f"3. Multiply: {b} × {answer} = {a}",
                    f"The correct answer is {answer}"
                ]
    
    elif topic == "Algebra":
        if "+" in problem:
            left_side = problem.split("=")[0].strip()
            right_side = problem.split("=")[1].strip()
            steps = [
                f"1. Original equation: {problem}",
                f"2. Subtract the constant from both sides",
                f"3. Combine like terms",
                f"4. Divide both sides to isolate x",
                f"The correct answer is x = {answer}"
            ]
        else:
            steps = [
                f"1. Original equation: {problem}",
                "2. Move all terms with x to one side",
                "3. Move all constant terms to the other side",
                f"4. Solve for x: x = {answer}",
                f"5. Check: Plug {answer} back into the original equation"
            ]
    
    elif topic == "Geometry":
        if "rectangle" in problem:
            dimensions = problem.split("with")[1].strip()
            steps = [
                f"1. Problem: {problem}",
                "2. Formula: Area of rectangle = width × height",
                f"3. Given {dimensions}",
                f"4. Calculate: {answer} square units",
                f"Your answer: {user_answer}, Correct answer: {answer}"
            ]
        elif "triangle" in problem:
            dimensions = problem.split("with")[1].strip()
            steps = [
                f"1. Problem: {problem}",
                "2. Formula: Area of triangle = ½ × base × height",
                f"3. Given {dimensions}",
                f"4. Calculate: {answer} square units",
                f"Your answer: {user_answer}, Correct answer: {answer}"
            ]
        elif "circle" in problem:
            radius = problem.split("radius")[1].split("(")[0].strip()
            steps = [
                f"1. Problem: {problem}",
                "2. Formula: Area of circle = πr²",
                f"3. Given radius = {radius}",
                f"4. Calculate: π × {radius}² = {answer} square units",
                f"Your answer: {user_answer}, Correct answer: {answer}"
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
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    
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
            st.session_state.current_problem = None
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate problem
        if st.session_state.current_problem is None:
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
                
                # Show error analysis and solution in separate expanders
                with st.expander("📝 See Analysis", expanded=True):
                    mistake_analysis = analyze_mistake(problem, answer, user_answer, topic)
                    st.markdown("### Understanding Your Answer:")
                    st.markdown(f"**Your answer:** {user_answer}")
                    st.markdown(f"**Correct answer:** {answer}")
                    st.markdown(f"**What went wrong:** {mistake_analysis}")
                
                with st.expander("✨ See Solution Steps", expanded=True):
                    st.markdown("### Step-by-Step Solution:")
                    steps = get_solution_steps(problem, answer, topic, user_answer)
                    for step in steps:
                        st.markdown(f"{step}")
                        st.markdown("---")
                
                # Show comparison if relevant
                if topic == "Arithmetic":
                    with st.expander("🔍 Compare Solutions", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Your approach:**")
                            st.markdown(f"{problem} = {user_answer}")
                        with col2:
                            st.markdown("**Correct approach:**")
                            st.markdown(f"{problem} = {answer}")
            
            # Generate new problem for next attempt
            if topic == "Arithmetic":
                st.session_state.current_problem = generate_arithmetic_problem(difficulty)
            elif topic == "Algebra":
                st.session_state.current_problem = generate_algebra_problem(difficulty)
            else:
                st.session_state.current_problem = generate_geometry_problem(difficulty)
            
            # Force a rerun to show the new problem
            st.rerun()
    
    with col2:
        # Progress bar and accuracy
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
            - Break down large numbers into smaller parts
            - Practice estimation to check if your answer makes sense
            """)
        elif topic == "Algebra":
            st.markdown("""
            - Isolate the variable on one side
            - What you do to one side, do to the other
            - For quadratic equations, factor or use quadratic formula
            - Check your solution by substituting back into the original equation
            - Keep track of signs when moving terms
            """)
        else:
            st.markdown("""
            - Area of rectangle = length × width
            - Area of triangle = ½ × base × height
            - Area of circle = πr²
            - π ≈ 3.14159
            - Double-check your units
            - Draw a diagram if helpful
            """)

if __name__ == "__main__":
    main()

