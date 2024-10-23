import streamlit as st
import random
import time
from datetime import datetime

def analyze_mistake(problem, correct_answer, user_answer, topic):
    """
    Analyze what went wrong with the user's answer and provide specific feedback.
    Returns detailed explanation of the likely mistake and suggestions for improvement.
    
    Args:
        problem (str): The problem text or equation
        correct_answer (float): The correct numerical answer
        user_answer (float): The user's submitted answer
        topic (str): The topic area ("Arithmetic", "Algebra", or "Geometry")
    
    Returns:
        str: Detailed analysis of the mistake with suggestions
    """
    if topic == "Arithmetic":
        try:
            a, operation, b = problem.split()
            a, b = int(a), int(b)
            
            if operation == '+':
                if user_answer < correct_answer:
                    if abs(user_answer - (a + b % 10)) < 0.01:
                        return f"Your answer {user_answer} is too small. Did you forget to carry the tens digit? Remember to add any carried numbers."
                    return f"Your answer {user_answer} is too small. Check if you carried all digits correctly when adding {a} and {b}."
                else:
                    if abs(user_answer - (a + b + 10)) < 0.01:
                        return f"Your answer {user_answer} is too large. Did you carry a digit when you didn't need to?"
                    return f"Your answer {user_answer} is too large. Double-check your addition steps and make sure you didn't count any digits twice."
            
            elif operation == '-':
                if user_answer > correct_answer:
                    if abs(user_answer - (a - b + 10)) < 0.01:
                        return f"Your answer {user_answer} is too large. Did you forget to complete the borrowing process?"
                    return f"Your answer {user_answer} is too large. When borrowing, remember to subtract 1 from the next digit to the left."
                else:
                    if abs(user_answer - (a - b - 10)) < 0.01:
                        return f"Your answer {user_answer} is too small. Did you borrow when you didn't need to?"
                    return f"Your answer {user_answer} is too small. Check your subtraction steps and make sure you borrowed correctly when needed."
            
            elif operation == '×':
                if abs(user_answer - (a + b)) < 0.01:
                    return f"It looks like you added {a} + {b} instead of multiplying them. Remember, {a} × {b} means adding {a} to itself {b} times."
                elif user_answer < correct_answer:
                    if abs(user_answer - (a * (b-1))) < 0.01:
                        return f"Your answer {user_answer} is too small. Did you multiply by {b-1} instead of {b}?"
                    return f"Your answer {user_answer} is too small. Check if you multiplied all digits correctly and included all partial products."
                else:
                    if abs(user_answer - (a * (b+1))) < 0.01:
                        return f"Your answer {user_answer} is too large. Did you multiply by {b+1} instead of {b}?"
                    return f"Your answer {user_answer} is too large. Check your multiplication steps and make sure you aligned the partial products correctly."
            
            elif operation == '÷':
                if abs(user_answer - (a * b)) < 0.01:
                    return f"It looks like you multiplied {a} × {b} instead of dividing them. Remember, {a} ÷ {b} means 'how many {b}s go into {a}?'"
                elif abs(user_answer - (b / a)) < 0.01:
                    return f"It looks like you divided {b} by {a} instead of {a} by {b}. Remember to keep the order straight: {a} ÷ {b}."
                elif abs(user_answer - correct_answer) < 1:
                    return f"You're close! Did you round your answer correctly? When dividing {a} by {b}, we get {correct_answer}."
                else:
                    return f"Check your division steps. Remember to multiply your answer ({user_answer}) by {b} - it should equal {a}."
        except:
            return "There seems to be an error in processing the arithmetic problem. Let's solve it step by step."
    
    elif topic == "Algebra":
        if "=" not in problem:
            return "Let's solve this step by step to find the correct answer."
        
        if abs(abs(user_answer) - abs(correct_answer)) < 0.01 and user_answer != correct_answer:
            return "Check the sign of your answer. Did you keep track of negative signs when moving terms between sides?"
        
        if "+" in problem:
            try:
                equation = problem.split("=")[0].strip()
                if user_answer * 2 == correct_answer:
                    return f"Did you forget to consider both sides of the equation? When solving {equation}, make sure to isolate the variable completely."
                elif user_answer == correct_answer / 2:
                    return f"Did you divide by 2 when you didn't need to? Check your steps when isolating the variable."
                else:
                    return f"Check how you isolated the variable. Try plugging your answer ({user_answer}) back into the original equation to verify."
            except:
                return "Let's solve this equation step by step to find where the mistake might be."
        
        if "²" in problem or "^2" in problem:
            try:
                if user_answer == -correct_answer:
                    return "Remember that quadratic equations can have two solutions. Did you consider both the positive and negative square root?"
                return "When solving quadratic equations, remember to check both possible solutions."
            except:
                return "Let's solve this quadratic equation step by step."
        
        return f"Try plugging your answer ({user_answer}) back into the original equation to see if it works."
    
    elif topic == "Geometry":
        if "rectangle" in problem.lower():
            try:
                dimensions = problem.split("width")[1].split("and")
                width = int(dimensions[0])
                height = int(dimensions[1].split()[1])
                if abs(user_answer - (width + height)) < 0.01:
                    return f"It looks like you added the width ({width}) and height ({height}) instead of multiplying them. Remember: Area = width × height"
                elif abs(user_answer - correct_answer) < correct_answer * 0.1:
                    return "You're close! Double-check your multiplication. Remember to multiply width × height carefully."
                else:
                    return f"Remember: Area of a rectangle = width × height = {width} × {height}. Try redoing the multiplication."
            except:
                return "Let's solve this step by step using the rectangle area formula: Area = width × height"
        
        elif "triangle" in problem.lower():
            try:
                if user_answer == correct_answer * 2:
                    return "Did you forget to divide by 2? Remember: Area of triangle = (base × height) ÷ 2"
                elif user_answer == correct_answer / 2:
                    return "Did you divide by 4 instead of 2? The formula is: Area = (base × height) ÷ 2"
                else:
                    return "Remember: Area of triangle = (base × height) ÷ 2. Try the calculation again with this formula."
            except:
                return "Let's solve this step by step using the triangle area formula: Area = (base × height) ÷ 2"
        
        elif "circle" in problem.lower():
            try:
                radius = float(problem.split("radius")[1].split("(")[0])
                if abs(user_answer - (2 * 3.14159 * radius)) < 0.01:
                    return f"It looks like you calculated the circumference (2πr) instead of the area (πr²). Remember to square the radius."
                elif abs(user_answer - (3.14159 * radius)) < 0.01:
                    return f"Did you forget to square the radius? Remember: Area = πr² = π × {radius} × {radius}"
                elif abs(user_answer - correct_answer) < 1:
                    return "Almost there! Did you use 3.14159 for π? Check your multiplication steps."
                else:
                    return f"Remember: Area of circle = πr² = 3.14159 × {radius}². Try the calculation again."
            except:
                return "Let's solve this step by step using the circle area formula: Area = πr²"
    
    return "Let's break this down and solve it step by step to understand where the mistake occurred."

def get_solution_steps(problem, answer, topic, user_answer):
    """Generate step-by-step solution explanation"""
    steps = []
    
    if topic == "Arithmetic":
        try:
            a, operation, b = problem.split()
            a, b = int(a), int(b)
            
            if operation == '+':
                steps = [
                    f"Step 1: Let's add {a} and {b}",
                    f"First, write the numbers vertically:\n\n   {a}\n   + {b}\n   ___",
                    f"Add from right to left:",
                    f"The sum is: {answer}",
                    f"To check: {a} + {b} = {answer}"
                ]
            elif operation == '-':
                steps = [
                    f"Step 1: Let's subtract {b} from {a}",
                    f"Write the numbers vertically:\n\n   {a}\n   - {b}\n   ___",
                    f"Subtract from right to left:",
                    f"The difference is: {answer}",
                    f"To check: {a} - {b} = {answer}"
                ]
            elif operation == '×':
                steps = [
                    f"Step 1: Let's multiply {a} and {b}",
                    f"Write the multiplication vertically:\n\n   {a}\n   × {b}\n   ___",
                    f"Multiply each digit:",
                    f"The product is: {answer}",
                    f"To check: {a} × {b} = {answer}"
                ]
            elif operation == '÷':
                steps = [
                    f"Step 1: Let's divide {a} by {b}",
                    f"Think: How many times does {b} go into {a}?",
                    f"Divide: {a} ÷ {b} = {answer}",
                    f"To check: {answer} × {b} = {a}"
                ]
        except:
            steps = [
                "Let's solve this step by step:",
                f"1. The problem is: {problem}",
                f"2. The correct answer is: {answer}",
                "3. Try writing out each step of your calculation"
            ]
    
    elif topic == "Algebra":
        if "=" in problem:
            equation = problem.split(": ")[1]  
            left_side = equation.split("=")[0].strip()
            right_side = equation.split("=")[1].strip()
            steps = [
                f"Step 1: Start with the equation\n{equation}",
                "Step 2: Move all terms with x to the left side, all other terms to the right side",
                f"Step 3: Combine like terms",
                f"Step 4: Solve for x: x = {answer}",
                f"Step 5: Check your answer by plugging x = {answer} back into the original equation"
            ]
            if "²" in problem or "^2" in problem:
                steps.insert(2, "Remember: When solving quadratic equations, consider both positive and negative solutions")
    
    elif topic == "Geometry":
        if "rectangle" in problem.lower():
            width = problem.split("width")[1].split("and")[0].strip()
            height = problem.split("height")[1].strip()
            steps = [
                f"Step 1: Identify the formula\nArea of rectangle = width × height",
                f"Step 2: Plug in the values\nwidth = {width}\nheight = {height}",
                f"Step 3: Calculate\n{width} × {height} = {answer}",
                f"The area is {answer} square units"
            ]
        elif "triangle" in problem.lower():
            base = problem.split("base")[1].split("and")[0].strip()
            height = problem.split("height")[1].strip()
            steps = [
                f"Step 1: Identify the formula\nArea of triangle = ½ × base × height",
                f"Step 2: Plug in the values\nbase = {base}\nheight = {height}",
                f"Step 3: Calculate\n½ × {base} × {height} = {answer}",
                f"The area is {answer} square units"
            ]
        elif "circle" in problem.lower():
            radius = problem.split("radius")[1].split("(")[0].strip()
            steps = [
                f"Step 1: Identify the formula\nArea of circle = πr²",
                f"Step 2: Use π = 3.14159",
                f"Step 3: Plug in radius = {radius}",
                f"Step 4: Calculate\n3.14159 × {radius} × {radius} = {answer}",
                f"The area is {answer} square units"
            ]
    
    formatted_steps = []
    for i, step in enumerate(steps, 1):
        formatted_steps.append(f"{step}")
        formatted_steps.append("---")  
    
    return formatted_steps

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
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    
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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
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
                st.markdown("🎉 Correct! Well done!")
                st.session_state.score += 1
                st.session_state.streak += 1
            else:
                st.error("❌ Not quite correct.")
                st.session_state.streak = 0
                
                st.markdown("### How to Solve This Problem:")
                steps = get_solution_steps(problem, answer, topic, user_answer)
                for step in steps:
                    st.markdown(f"{step}")
                
                st.markdown("### Understanding the Mistake:")
                st.markdown(f"**Your answer:** {user_answer}")
                st.markdown(f"**Correct answer:** {answer}")
                mistake_analysis = analyze_mistake(problem, answer, user_answer, topic)
                st.markdown(f"**Explanation:** {mistake_analysis}")
                
                if topic == "Arithmetic":
                    st.markdown("### Side by Side Comparison:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Your approach:**")
                        st.markdown(f"{problem} = {user_answer}")
                    with col2:
                        st.markdown("**Correct approach:**")
                        st.markdown(f"{problem} = {answer}")
            
            if topic == "Arithmetic":
                st.session_state.current_problem = generate_arithmetic_problem(difficulty)
            elif topic == "Algebra":
                st.session_state.current_problem = generate_algebra_problem(difficulty)
            else:
                st.session_state.current_problem = generate_geometry_problem(difficulty)
            
            st.rerun()
    
    with col2:
        st.markdown("### Your Progress")
        if st.session_state.total_questions > 0:
            progress = st.session_state.score / st.session_state.total_questions
            st.progress(progress)
            st.markdown(f"Accuracy: {(progress * 100):.1f}%")
    
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

