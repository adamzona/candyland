import streamlit as st
import random
import json
import time
from fractions import Fraction

# Load questions from the provided JSON file
with open("questions.json", "r") as file:
    questions_data = json.load(file)

# Define card categories
def get_random_card(category):
    card_data = random.choice(questions_data[category])
    card_image_path = f"https://raw.githubusercontent.com/adamzona/candyland/main/cards/{card_data['card']}"
    return card_image_path, card_data["question"], card_data["answer"], category

# Function to normalize numeric answers, allowing decimals and fractions
def normalize_answer(answer):
    try:
        return str(float(answer))
    except ValueError:
        try:
            return str(float(Fraction(answer)))
        except ValueError:
            return answer.strip().lower()

# Streamlit UI Customization
st.set_page_config(page_title="Candy Land Game", page_icon="🍭", layout="centered")

st.title("🍬 Candy Land Digital Card Generator 🍽")
st.markdown("<h2 class='big-font'>Draw a Card & Answer the Question!</h2>", unsafe_allow_html=True)

# Ensure session state exists
if "card" not in st.session_state:
    st.session_state.card = None
    st.session_state.question = None
    st.session_state.answer = None
    st.session_state.card_type = None
    st.session_state.answered = False
    st.session_state.sweet_score = 0  # Renamed from Sweetness Score
    st.session_state.timer = 45  # Start with 45 seconds
    st.session_state.timer_running = False  # Control for stopping timer
    st.session_state.start_time = None  # Timer start time

# Play a draw card sound
draw_sound = "https://raw.githubusercontent.com/adamzona/candyland/main/sounds/chime.mp3"

# Function to play a sound
def play_sound(sound_url):
    return f"""
    <audio autoplay>
        <source src="{sound_url}" type="audio/mpeg">
    </audio>
    """

# Draw a card button
if st.button("🎲 Draw a Card"):
    st.session_state.answered = False
    st.session_state.timer = 45  # Reset the timer
    st.session_state.timer_running = True  # Start timer
    st.session_state.start_time = time.time()  # Set start time

    # Play Draw Card Sound
    st.markdown(play_sound(draw_sound), unsafe_allow_html=True)

    # 🎉 Add confetti effect!
    st.balloons()

    # Draw a random card
    card_type = random.choices(['easy', 'medium', 'hard'], weights=[50, 35, 15])[0]
    st.session_state.card, st.session_state.question, st.session_state.answer, st.session_state.card_type = get_random_card(card_type)

# Display the drawn card
if st.session_state.card:
    st.image(st.session_state.card, caption=f"{st.session_state.card_type.capitalize()} Card", use_container_width=True)
    st.markdown(f"<div class='question-box'>{st.session_state.question}</div>", unsafe_allow_html=True)
    
    # Answer input
    user_answer = st.text_input("Enter your answer:")
    
    # Check answer button
    if st.button("Check Answer") and not st.session_state.answered:
        normalized_user_answer = normalize_answer(user_answer)
        normalized_correct_answer = normalize_answer(st.session_state.answer)
        
        if normalized_user_answer == normalized_correct_answer:
            st.success("Correct! 🎉")
            st.session_state.sweet_score += 10  # Increase score
        else:
            st.error(f"Incorrect! The correct answer is: {st.session_state.answer}")
        
        st.session_state.answered = True  # Prevent multiple submissions

# Display timer and score
if st.session_state.timer_running:
    time_elapsed = time.time() - st.session_state.start_time
    remaining_time = max(0, st.session_state.timer - int(time_elapsed))
    
    if remaining_time == 0:
        st.session_state.timer_running = False  # Stop timer
        st.error("Time's up! Try again next turn.")
    
    st.write(f"⏳ Time Left: {remaining_time} seconds")

st.write(f"🍭 Sweet Score: {st.session_state.sweet_score}")
