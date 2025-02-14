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
    return card_image_path, card_data["question"], card_data["answer"]

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
    .question-box {border: 2px solid #FF69B4; padding: 15px; border-radius: 10px; background-color: #FFF0F5; text-align: center;}
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

if st.button("🎲 Draw a Card"):  
    card_type = random.choices([
        'easy', 'medium', 'hard'
    ], weights=[50, 40, 10])[0]  # Probabilities for each type
    
    st.session_state.card, st.session_state.question, st.session_state.answer = get_random_card(card_type)

if st.session_state.card:
    st.image(st.session_state.card, caption="Card Drawn", width=300)
    st.markdown(f"<div class='question-box'><b>Question:</b> {st.session_state.question}</div>", unsafe_allow_html=True)
    
    user_answer = st.text_input("Your Answer:", key="answer_input")
    if st.button("Submit Answer"):
        if normalize_answer(user_answer) == normalize_answer(st.session_state.answer):
            st.markdown(f"<p class='animated-text'>{random.choice([
                "✅ Correct! You're on fire! 🔥",
                "✅ Sweet success! 🍬",
                "✅ You nailed it! 🎯",
                "✅ Boom! Genius alert! 🚀",
                "✅ That was smoother than chocolate! 🍫"
            ])}</p>", unsafe_allow_html=True)
            
        else:
            st.markdown(f"<p class='animated-text'>{random.choice([
                f"❌ Nope! The correct answer was: {st.session_state.answer}. Try again! 🤔",
                f"❌ Oof, close but no candy! The answer was: {st.session_state.answer}. 🍭",
                f"❌ Not quite! The answer was: {st.session_state.answer}. Better luck next time! 🎲",
                f"❌ Almost! The answer was: {st.session_state.answer}. Keep going! 🚀",
                f"❌ Whoops! The answer was: {st.session_state.answer}. Don't give up! 💪"
            ])}</p>", unsafe_allow_html=True)
            

            
