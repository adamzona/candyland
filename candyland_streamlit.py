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
    
    /* Separate Boxes with Space Between */
    .top-right-container {
        position: absolute;
        top: 20px;
        right: 10px;
        display: flex;
        flex-direction: column;
        gap: 20px; /* Adds white space between Timer & Sweet Score */
    }

    .timer-box {
        font-size: 24px;
        font-weight: bold;
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        width: 120px;
        height: 50px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(to right, #FF69B4, #FF1493, #FFD700);
    }

    .score-box {
        font-size: 24px;
        font-weight: bold;
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        width: 300px;
        height: 50px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(to right, #FFD700, #FFA500, #FF4500);
    }

    .animated-text {font-size:22px; text-align:center; animation: fadeIn 2s;}
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* Fade-In Effect for Card */
    .fade-in-card {
        animation: fadeIn 2s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# **Top Right Container for Timer & Sweet Score (With Space)**
st.markdown("<div class='top-right-container'>", unsafe_allow_html=True)

# Timer & Sweet Score Display
timer_placeholder = st.empty()
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Adds space
sweet_score_placeholder = st.empty()

st.markdown("</div>", unsafe_allow_html=True)

st.title("🍬 Candy Land Digital Card Generator 🍭")
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
    st.session_state.timer_running = True  # Start timer
    st.session_state.start_time = time.time()  # Set start time

    # Play Draw Card Sound
    st.markdown(play_sound(draw_sound), unsafe_allow_html=True)

    # 🎉 Add confetti effect!
    st.balloons()

    # Draw a random card
    card_type = random.choices(['easy', 'medium',
