import streamlit as st
import random
import json
import os
from fractions import Fraction

# Load questions from the provided JSON file
with open("questions.json", "r") as file:
    questions_data = json.load(file)

# Define card categories
def get_random_card(category):
    card_data = random.choice(questions_data[category])
    card_image_path = f"https://raw.githubusercontent.com/adamzona/candyland/main/cards/{card_data['card']}"  # Ensure image is loaded from 'cards' folder
    return card_image_path, card_data["question"], card_data["answer"], category  # Return category as well

# Function to normalize numeric answers, allowing decimals and fractions
def normalize_answer(answer):
    try:
        return str(float(answer))  # Convert numbers to float then back to string for consistency
    except ValueError:
        try:
            return str(float(Fraction(answer)))  # Convert fractions to float
        except ValueError:
            return answer.strip().lower()  # For non-numeric answers, use lowercase stripping

# Streamlit UI Customization
st.set_page_config(page_title="Candy Land Game", page_icon="🍭", layout="centered")

st.markdown("""
    <style>
    .big-font {font-size:24px !important; text-align: center;}
    .question-box {
        font-size: 48px;  /* Increased font size */
        border: 2px solid #FF69B4;
        padding: 15px;
        border-radius: 10px;
        background-color: #FFF0F5;
        text-align: center;
    }
    .score-box {
        font-size: 36px;
        font-weight: bold;
        color: white;
        background-color: #ff66b2;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .animated-text {font-size:22px; text-align:center; animation: fadeIn 2s;}
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

st.title("🍬 Candy Land Digital Card Generator 🍭")
st.markdown("<h2 class='big-font'>Draw a Card & Answer the Question!</h2>", unsafe_allow_html=True)

# Ensure session state exists
if "card" not in st.session_state:
    st.session_state.card = None
    st.session_state.question = None
    st.session_state.answer = None
    st.session_state.card_type = None
    st.session_state.answered = False  # Tracks if the question was answered
    st.session_state.sweetness_score = 0  # Initialize score

# Display Sweetness Score
st.markdown(f"<div class='score-box'>🍭 Sweetness Score: {st.session_state.sweetness_score} 🍭</div>", unsafe_allow_html=True)

if st.button("🎲 Draw a Card"):  
    card_type = random.choices(
        ['easy', 'medium', 'hard'], weights=[50, 40, 10]
    )[0]  # Probabilities for each type
    
    st.session_state.card, st.session_state.question, st.session_state.answer, st.session_state.card_type = get_random_card(card_type)
    st.session_state.answered = False  # Reset answer state when drawing a new card

if st.session_state.card:
    st.image(st.session_state.card, caption="Card Drawn", width=300)
    st.markdown(f"<div class='question-box'><b>Question:</b> {st.session_state.question}</div>", unsafe_allow_html=True)
    
    # Disable input & submit button if question was already answered
    user_answer = st.text_input("Your Answer:", key="answer_input", disabled=st.session_state.answered)
    
    if st.button("Submit Answer", disabled=st.session_state.answered):
        if normalize_answer(user_answer) == normalize_answer(st.session_state.answer):
            # Determine points based on difficulty
            points = {"easy": 10, "medium": 15, "hard": 20}
            score_earned = points[st.session_state.card_type]
            st.session_state.sweetness_score += score_earned

            correct_feedback = random.choice([
                f"✅ Correct! You earned {score_earned} points! 🍭",
                f"✅ Sweet success! {score_earned} points added! 🍬",
                f"✅ Boom! +{score_earned} points! 🚀",
                f"✅ That was smoother than chocolate! +{score_earned} 🍫",
                f"✅ You’re on fire! 🔥 {score_earned} points earned!"
            ])
            st.markdown(f"<p class='animated-text'>{correct_feedback}</p>", unsafe_allow_html=True)
        else:
            incorrect_feedback = random.choice([
                f"❌ Nope! The correct answer was: {st.session_state.answer}. Try again! 🤔",
                f"❌ Oof, close but no candy! The answer was: {st.session_state.answer}. 🍭",
                f"❌ Not quite! The answer was: {st.session_state.answer}. Better luck next time! 🎲",
                f"❌ Almost! The answer was: {st.session_state.answer}. Keep going! 🚀",
                f"❌ Whoops! The answer was: {st.session_state.answer}. Don't give up! 💪"
            ])
            st.markdown(f"<p class='animated-text'>{incorrect_feedback}</p>", unsafe_allow_html=True)
        
        # Set answered flag to prevent re-answering
        st.session_state.answered = True

    # Update the Sweetness Score in real-time
    st.markdown(f"<div class='score-box'>🍭 Sweetness Score: {st.session_state.sweetness_score} 🍭</div>", unsafe_allow_html=True)
