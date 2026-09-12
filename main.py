import streamlit as st
import random
import time

st.set_page_config(page_title='𝙰𝚔𝚊𝚒',page_icon='🍥',layout="centered")

# session state vars

if "game_state" not in st.session_state:
    st.session_state.game_state = "setup"

if "numbers" not in st.session_state:
    st.session_state.numbers = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "user_answer" not in st.session_state:
    st.session_state.user_answer = None

if "result" not in st.session_state:
    st.session_state.result = None

if 'digit_index' not in st.session_state:
    st.session_state.digit_index = 0

if 'number_count' not in st.session_state:
    st.session_state.number_count = 2

if 'speed' not in st.session_state:
    st.session_state.speed = 1.0

if 'operation_index' not in st.session_state:
    st.session_state.operation_index = 0


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


st.markdown("""
<style>

.number {
    font-size: 180px;
    font-weight: 700;
    text-align: center;
    line-height: 1;
    margin-top: 20vh;
    margin-bottom: 20vh;
}

.number-count {
    text-align: center;
    font-size: 20px;
    font-weight: 500;
}

.calculation {
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    padding: 20px;
    overflow-x: auto;
    white-space: nowrap;
}

</style>
""", unsafe_allow_html=True)


st.title("Meth Test")

# page setup --game state
if st.session_state.game_state == "setup":

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

    numbers = st.session_state.numbers
    current_index = st.session_state.current_index
    speed = st.session_state.speed

    total_numbers = len(numbers)

    # Number counter
    st.markdown(
        f"""
        <div class="number-count">
            {current_index + 1} / {total_numbers}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Current number
    current_number = numbers[current_index]

    st.markdown(
        f"""
        <div class="number">
            {current_number}
        </div>
        """,
        unsafe_allow_html=True
    )

    # timer
    elapsed = time.time() - st.session_state.start_time
    remaining = speed - elapsed

    if remaining > 0:
        time.sleep(min(0.05, remaining))
        st.rerun()
    else:

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
        st.error(f"Try again lil vro, your answer: {user_answer}")
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