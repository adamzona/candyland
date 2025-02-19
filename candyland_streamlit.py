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
    .animated-text {font-size:22px; text-align:center; animation: fadeIn 2s;}
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* Flashing and Shaking Button */
    @keyframes flash {
        0% {background-color: #FF69B4;}
        50% {background-color: #FFC0CB;}
        100% {background-color: #FF69B4;}
    }
    @keyframes shake {
        0% {transform: translateX(0);}
        25% {transform: translateX(-5px);}
        50% {transform: translateX(5px);}
        75% {transform: translateX(-5px);}
        100% {transform: translateX(5px);}
    }
    .flash-button {
        animation: flash 1s infinite, shake 0.5s infinite;
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

# Display Sweetness Score
st.markdown(f"<div class='score-box'>🍭 Sweetness Score: {st.session_state.sweetness_score} 🍭</div>", unsafe_allow_html=True)

# Draw Card Button with Effects
draw_card_html = '<button class="flash-button">🎲 Draw a Card</button>'
draw_card_clicked = st.button("🎲 Draw a Card")

# Play a draw card sound
draw_sound = "https://raw.githubusercontent.com/adamzona/candyland/main/sounds/chime.mp3"
shuffle_sound = "https://raw.githubusercontent.com/adamzona/candyland/main/sounds/shuffle.mp3"

def play_sound(sound_url):
    return f"""
    <audio autoplay>
        <source src="{sound_url}" type="audio/mpeg">
    </audio>
    """

if draw_card_clicked:
    st.session_state.card = None
    st.session_state.answered = False

    # Play Draw Card Sound
    st.markdown(play_sound(draw_sound), unsafe_allow_html=True)

    # Display "Shuffling..." Effect
    with st.spinner("🔄 Shuffling cards..."):
        st.markdown(play_sound(shuffle_sound), unsafe_allow_html=True)  # Play shuffle sound
        time.sleep(1.5)  # Simulate card shuffling delay

    # Draw a random card
    card_type = random.choices(
        ['easy', 'medium', 'hard'], weights=[50, 40, 10]
    )[0]
    st.session_state.card, st.session_state.question, st.session_state.answer, st.session_state.card_type = get_random_card(card_type)

    # 🎉 Add confetti effect!
    st.balloons()

if st.session_state.card:
    st.image(st.session_state.card, caption="Card Drawn", width=300)
    st.markdown(f"<div class='question-box'><b>Question:</b> {st.session_state.question}</div>", unsafe_allow_html=True)
    
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
            incorrect_feedback = random.choice([
                f"❌ Nope! The correct answer was: {st.session_state.answer}. Try again! 🤔",
                f"❌ Oof, close but no candy! The answer was: {st.session_state.answer}. 🍭"
            ])
            st.markdown(f"<p class='animated-text'>{incorrect_feedback}</p>", unsafe_allow_html=True)

            # Play incorrect answer sound
            st.markdown(play_sound(incorrect_sound), unsafe_allow_html=True)

        st.session_state.answered = True

    st.markdown(f"<div class='score-box'>🍭 Sweetness Score: {st.session_state.sweetness_score} 🍭</div>", unsafe_allow_html=True)
