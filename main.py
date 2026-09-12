import streamlit as st
import random
import time

st.set_page_config( page_title='𝙰𝚔𝚊𝚒', page_icon='🍥', layout="centered", initial_sidebar_state="collapsed")

# session default variables
defaults = {
    "game_state": "setup",
    "numbers": [],
    "current_index": 0,
    "correct_answer": 0,
    "start_time": None,
    "user_answer": None,
    "result": None,
    "digit_index": 0,
    "number_count": 2,
    "speed": 1.0,
    "operation_index": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def generate_number(digits, operation):
    minimum = 10 ** (digits - 1)
    maximum = (10 ** digits) - 1
    number = random.randint(minimum, maximum)
    if operation == "Addition":
        return number
    return number * random.choice([1, -1])


def reset_game():
    """Full reset -- go back to setup"""
    st.session_state.game_state = "setup"
    st.session_state.numbers = []
    st.session_state.current_index = 0
    st.session_state.correct_answer = 0
    st.session_state.start_time = None
    st.session_state.user_answer = None
    st.session_state.result = None


def start_new_round():
    """Start a new game with the CURRENT saved settings"""
    operation = "Addition" if st.session_state.operation_index == 0 else "Addition & Subtraction"
    digits = st.session_state.digit_index + 1
    number_count = st.session_state.number_count
    speed = st.session_state.speed

    numbers = [generate_number(digits, operation) for _ in range(number_count)]
    
    st.session_state.numbers = numbers
    st.session_state.correct_answer = sum(numbers)
    st.session_state.current_index = 0
    st.session_state.start_time = time.time()
    st.session_state.user_answer = None
    st.session_state.result = None
    st.session_state.game_state = "playing"


# cc
st.markdown("""
<style>
/* Hide Streamlit chrome */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}

/* Remove extra padding on mobile */
.block-container {
    padding-top: 0.8rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 100% !important;
}

/* Big number */
.number {
    height: 78vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(80px, 28vw, 220px);
    font-weight: 700;
    line-height: 1;
    margin: 0;
    padding: 0;
}

.number-count {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 500;
    margin: 0.3rem 0 0.2rem 0;
}

.calculation {
    text-align: center;
    font-size: 1.3rem;
    font-weight: 600;
    padding: 12px;
    overflow-x: auto;
    white-space: nowrap;
}

/* Make buttons a bit bigger on mobile */
.stButton > button {
    height: 3rem;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)


# set up
if st.session_state.game_state == "setup":

    st.title("Meth Test")
    st.caption("Mental math flash")

    operation = st.selectbox(
        "Operation",
        ["Addition", "Addition & Subtraction"],
        index=st.session_state.operation_index
    )

    digits = st.selectbox(
        "Digits [1-5]",
        [1, 2, 3, 4, 5],
        index=st.session_state.digit_index
    )

    number_count = st.number_input(
        "Numbers [2-100]",
        min_value=2, max_value=100,
        value=st.session_state.number_count, step=1
    )

    speed = st.number_input(
        "Speed [seconds]",
        min_value=0.1, max_value=11.0,
        value=st.session_state.speed, step=0.1, format="%.1f"
    )

    st.write("")

    if st.button("Start Game", use_container_width=True, type="primary"):

        st.session_state.operation_index = 0 if operation == "Addition" else 1
        st.session_state.digit_index = digits - 1
        st.session_state.number_count = number_count
        st.session_state.speed = speed
        
        start_new_round()
        st.rerun()


# display numbers
elif st.session_state.game_state == "playing":

    # Force scroll to top snipt
    st.markdown("""
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
            window.scrollTo(0, 0);
        </script>
    """, unsafe_allow_html=True)

    numbers = st.session_state.numbers
    current_index = st.session_state.current_index
    speed = st.session_state.speed
    total = len(numbers)

    # Tiny top bar: Exit + counter
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Exit", use_container_width=True, type='primary'):
            reset_game()
            st.rerun()
    with col2:
        st.markdown(
            f'<div class="number-count">{current_index + 1} / {total}</div>',
            unsafe_allow_html=True
        )

    # big number area
    number_placeholder = st.empty()
    current_number = numbers[current_index]

    number_placeholder.markdown(
        f'<div class="number">{current_number}</div>',
        unsafe_allow_html=True
    )

    time.sleep(speed)

    # blank transition
    number_placeholder.markdown('<div class="number"></div>', unsafe_allow_html=True)
    time.sleep(0.12)

    if current_index < total - 1:
        st.session_state.current_index += 1
        st.rerun()
    else:
        st.session_state.game_state = "answer"
        st.rerun()


# submit answer
elif st.session_state.game_state == "answer":

    st.subheader("total ballz?")
    user_answer = st.number_input(
        "3220",
        value=None, step=1, placeholder="type here…",
        label_visibility="collapsed"
    )

    if st.button("Submit", use_container_width=True, type="primary"):
        if user_answer is None:
            st.warning("no ballz. enter a number")
        else:
            st.session_state.user_answer = int(user_answer)
            st.session_state.result = (
                "correct" if int(user_answer) == st.session_state.correct_answer
                else "wrong"
            )
            st.session_state.game_state = "result"
            st.rerun()


# result
elif st.session_state.game_state == "result":

    correct = st.session_state.correct_answer
    user = st.session_state.user_answer
    numbers = st.session_state.numbers

    if st.session_state.result == "correct":
        st.success(f"Well done! Lil Vro, your answer: {correct}")
    else:
        st.error(f"Nice Try Lil Vro, your answer: {user}")
        st.info(f"Correct answer: {correct}")


    calc = ""
    for i, n in enumerate(numbers):
        if i == 0:
            calc = str(n)
        elif n >= 0:
            calc += f" + {n}"
        else:
            calc += f" - {abs(n)}"
    calc += f" = {correct}"

    st.markdown(f'<div class="calculation">{calc}</div>', unsafe_allow_html=True)
    st.write("")


    col1, col2 = st.columns(2)

    with col1:
        if st.button("Play Again", use_container_width=True, type="primary"):
            start_new_round()
            st.rerun()
    with col2:
        if st.button("Home", use_container_width=True):
            reset_game()
            st.rerun()