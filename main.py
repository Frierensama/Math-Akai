import streamlit as st
import random
import time

st.set_page_config(page_title='𝙰𝚔𝚊𝚒',page_icon='🍥',layout="centered")

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

# gen number
def generate_number(digits, operation):

    minimum = 10 ** (digits - 1)
    maximum = (10 ** digits) - 1

    number = random.randint(minimum, maximum)

    if operation == "Addition":
        return number

    return number * random.choice([1, -1])

# rest game
def reset_game():

    st.session_state.game_state = "setup"
    st.session_state.numbers = []
    st.session_state.current_index = 0
    st.session_state.correct_answer = 0
    st.session_state.start_time = None
    st.session_state.user_answer = None
    st.session_state.result = None

# ---------- global CSS ----------
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


# page setup --game state
if st.session_state.game_state == "setup":

    st.title("Meth Test")
    st.subheader("Settings")

    operation = st.selectbox(
        "Operation type",
        [
            "Addition",
            "Addition & Subtraction"
        ],
        index=st.session_state.operation_index
    )

    digits = st.selectbox(
        "Digits length [1-5]",
        [1, 2, 3, 4, 5],
        index=st.session_state.digit_index
    )

    number_count = st.number_input(
        "Numbers count [2-100]", value=st.session_state.number_count,
        min_value=2,
        max_value=100,
        step=1
    )

    speed = st.number_input(
        "Speed [seconds]",
        min_value=0.1,
        max_value=11.0,
        value=st.session_state.speed,
        step=0.1,
        format="%.1f"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Operation:** {operation}")
        st.write(f"**Digits:** {digits}")
    
    with col2:
        st.write(f"**Numbers:** {number_count}")
        st.write(f"**Speed:** {speed:.1f} sec")

    st.divider()

    if st.button(
        "Start Game",
        use_container_width=True,
        type="primary"
    ):

        numbers = [
            generate_number(digits, operation)
            for _ in range(number_count)
        ]

        st.session_state.numbers = numbers
        st.session_state.correct_answer = sum(numbers)
        st.session_state.operation_index = 0 if operation == 'Addition' else 1
        st.session_state.digit_index =  int(digits) - 1
        st.session_state.number_count = number_count
        st.session_state.current_index = 0
        st.session_state.start_time = time.time()
        st.session_state.speed = speed
        st.session_state.game_state = "playing"

        st.rerun()

elif st.session_state.game_state == "playing":
    
    st.markdown(
            """
            <script>
                window.parent.scrollTo(0, 0);
            </script>
            """,
            unsafe_allow_html=True
        )

    numbers = st.session_state.numbers
    current_index = st.session_state.current_index
    speed = st.session_state.speed

    total_numbers = len(numbers)

    if st.button("exit",  use_container_width=True, type="primary"):
        reset_game()
        st.rerun()
    
    # Number counter
    st.markdown(
        f"""
        <div class="number-count">
            {current_index + 1} / {total_numbers}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create one placeholder
    number_placeholder = st.empty()

    # Show number
    current_number = numbers[current_index]

    number_placeholder.markdown(
        f"""
        <div class="number">
            {current_number}
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(speed)


    number_placeholder.markdown(
        f"""
        <div class="number">
            
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.11)

    if current_index < total_numbers - 1:
        st.session_state.current_index += 1
        st.session_state.start_time = time.time()
        st.rerun()
    else:
        st.session_state.game_state = "answer"
        st.rerun()

# submit answer
elif st.session_state.game_state == "answer":

    st.subheader("Solution")
    st.write("What is the total?")

    user_answer = st.number_input("Enter your answer",
        value=None,
        step=1,
        placeholder="3220"
    )

    if st.button( "Submit", use_container_width=True, type="primary"):

        if user_answer is None:
            st.warning("you got no ballz? enter a value lil vro")
        else:
            st.session_state.user_answer = int(user_answer)

            if int(user_answer) == st.session_state.correct_answer:
                st.session_state.result = "correct"
            else:
                st.session_state.result = "wrong"

            st.session_state.game_state = "result"
            st.rerun()


elif st.session_state.game_state == "result":

    correct_answer = st.session_state.correct_answer
    user_answer = st.session_state.user_answer
    numbers = st.session_state.numbers

    if st.session_state.result == "correct":
        st.success(f"Well done lil vro. correct answer: {correct_answer}")
    else:
        st.error(f"Nice Try lil vro, your answer: {user_answer}")
        st.info(f"Correct answer: {correct_answer}")

    st.divider()

    calculation = ""

    for i, number in enumerate(numbers):

        if i == 0:
            calculation = str(number)
        elif number >= 0:
            calculation += f" + {number}"
        else:
            calculation += f" - {abs(number)}"

    calculation += f" = {correct_answer}"

    st.markdown(
        f"""
        <div class="calculation">
            {calculation}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    if st.button( "Re-Try", use_container_width=True,type="primary"):
        reset_game()
        st.rerun()