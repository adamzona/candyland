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

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden !important;}
    header {visibility: hidden;}

    .big-font {font-size:24px !important; text-align: center;}
    .question-box {
        font-size: 48px;
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
    .timer-box {
        font-size: 30px;
        font-weight: bold;
        color: white;
        background-color: #ff3333;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
    }
    .animated-text {font-size:22px; text-align:center; animation: fadeIn 2s;}
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* Fade-In Effect for Card */
    .fade-in-card {
        animation: fadeIn 2s ease-in-out;
    }
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
    st.session_state.answered = False
    st.session_state.sweetness_score = 0
    st.session_state.timer = 45  # Start with 45 seconds

# Display Sweetness Score
st.markdown(f"<div class='score-box'>🍭 Sweetness Score: {st.session_state.sweetness_score} 🍭</div>", unsafe_allow_html=True)

# Play a draw card sound
draw_sound = "https://raw.githubusercontent.com/adamzona/candyland/main/sounds/chime.mp3"

def play_sound(sound_url):
    return f"""
    <audio autoplay>
        <source src="{sound_url}" type="audio/mpeg">
    </audio>
    """

if st.button("🎲 Draw a Card"):
    st.session_state.card = None
    st.session_state.answered = False
    st.session_state.timer = 45  # Reset the timer

    # Play Draw Card Sound
    st.markdown(play_sound(draw_sound), unsafe_allow_html=True)

    # 🎉 Add confetti effect!
    st.balloons()

    # Draw a random card
    card_type = random.choices(['easy', 'medium', 'hard'], weights=[50, 40, 10])[0]
    st.session_state.card, st.session_state.question, st.session_state.answer, st.session_state.card_type = get_random_card(card_type)

if st.session_state.card:
    # Apply fade-in effect to the drawn card
    st.image(st.session_state.card, caption="Card Drawn", width=300, use_column_width=True, help="Card")
    st.markdown(f"<div class='question-box'><b>Question:</b> {st.session_state.question}</div>", unsafe_allow_html=True)

    # Countdown Timer Logic
    if not st.session_state.answered:
        start_time = time.time()
        while st.session_state.timer > 0:
            elapsed_time = time.time() - start_time
            st.session_state.timer = max(0, 45 - int(elapsed_time))
            time.sleep(1)
            st.experimental_rerun()  # Refresh page to update timer

        # If timer runs out, auto-submit as incorrect
        if st.session_state.timer == 0 and not st.session_state.answered:
            st.session_state.answered = True
            incorrect_sound = "https://raw.githubusercontent.com/adamzona/candyland/main/sounds/buzzer.mp3"
            st.markdown(play_sound(incorrect_sound), unsafe_allow_html=True)
            st.error(f"⏳ Time's up! The correct answer was: {st.session_state.answer} ❌")

    # Display Timer
    st.markdown(f"<div class='timer-box'>⏳ Time Left: {st.session_state.timer} sec</div>", unsafe_allow_html=True)

    user_answer = st.text_input("Your Answer:", key="answer_input", disabled=st.session_state.answered)

    if st.button("Submit Answer", disabled=st.session_state.answered):
        correct_sound = "https://raw.githubusercontent.com/adamzona/candyland/main/sounds/correct.mp3"
        incorrect_sound = "https://raw.githubusercontent.com/adamzona/candyland/main/sounds/buzzer.mp3"

        if normalize_answer(user_answer) == normalize_answer(st.session_state.answer):
            points = {"easy": 10, "medium": 15, "hard": 20}
            score_earned = points[st.session_state.card_type]
            st.session_state.sweetness_score += score_earned

            correct_feedback = random.choice([
                f"✅ Correct! You earned {score_earned} points! 🍭",
                f"✅ Sweet success! {score_earned} points added! 🍬",
                f"✅ Boom! +{score_earned} points! 🚀"
            ])
            st.markdown(f"<p class='animated-text'>{correct_feedback}</p>", unsafe_allow_html=True)

            # Play correct answer sound
            st.markdown(play_sound(correct_sound), unsafe_allow_html=True)

        else:
            incorrect_feedback = f"❌ Nope! The correct answer was: {st.session_state.answer}."
            st.markdown(f"<p class='animated-text'>{incorrect_feedback}</p>", unsafe_allow_html=True)

            # Play incorrect answer sound
            st.markdown(play_sound(incorrect_sound), unsafe_allow_html=True)

        st.session_state.answered = True

    st.markdown(f"<div class='score-box'>🍭 Sweetness Score: {st.session_state.sweetness_score} 🍭</div>", unsafe_allow_html=True)
