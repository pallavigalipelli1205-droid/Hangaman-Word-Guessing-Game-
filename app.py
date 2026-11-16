
from database import create_tables
import streamlit as st

from auth import register_user, login_user

from game_logic import (
    select_word,
    display_word,
    check_guess,
    check_win
)

# Page configuration
st.set_page_config(
    page_title="Hangman Game",
    page_icon="🎮",
    layout="centered"
)
# Initialize database tables
create_tables()

st.title("🎮 Hangman Word Challenge")
st.write("Welcome to the Hangman Internship Project!")

# Initialize session state
defaults = {
    "logged_in": False,
    "user": None,
    "started": False,
    "guessed_letters": [],
    "attempts": 6,
    "word": "",
    "difficulty": "Easy"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# LOGIN AND REGISTRATION
if not st.session_state.logged_in:

    choice = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True
    )

    if choice == "Register":

        st.subheader("Create Account")

        with st.form("register_form"):

            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input(
                "Password",
                type="password"
            )

            submit = st.form_submit_button("Register")

            if submit:

                success, message = register_user(
                    username,
                    email,
                    password
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

    else:

        st.subheader("User Login")

        with st.form("login_form"):

            username = st.text_input("Username")
            password = st.text_input(
                "Password",
                type="password"
            )

            submit = st.form_submit_button("Login")

            if submit:

                user = login_user(username, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error("Invalid username or password.")


# USER DASHBOARD AND GAME
else:

    username = st.session_state.user["username"]

    st.success(f"Welcome, {username}!")

    st.divider()

    # Select difficulty
    difficulty = st.selectbox(
        "Select Difficulty",
        ["Easy", "Medium", "Hard"],
        key="difficulty"
    )

    # START GAME / MAIN DASHBOARD
    if not st.session_state.started:

        st.subheader("🏠 Game Dashboard")

        st.write("Ready to test your word guessing skills?")

        st.info(
            "Select your difficulty and click Start Game "
            "to begin playing."
        )

        if st.button("🎮 Start Game", use_container_width=True):

            st.session_state.word = select_word(difficulty)
            st.session_state.guessed_letters = []
            st.session_state.attempts = 6
            st.session_state.started = True

            st.rerun()

    # GAME INTERFACE
    else:

        won = check_win(
            st.session_state.word,
            st.session_state.guessed_letters
        )

        lost = st.session_state.attempts <= 0 and not won

        # PLAYING THE GAME
        if not won and not lost:

            st.subheader("🎯 Hangman Game")

            st.write(
                "Word:",
                display_word(
                    st.session_state.word,
                    st.session_state.guessed_letters
                )
            )

            st.write(
                f"❤️ Attempts remaining: {st.session_state.attempts}"
            )

            st.progress(st.session_state.attempts / 6)

            st.subheader("Choose a Letter")

            alphabet = "abcdefghijklmnopqrstuvwxyz"

            cols = st.columns(7)

            for i, letter in enumerate(alphabet):

                with cols[i % 7]:

                    if st.button(
                        letter.upper(),
                        key=letter,
                        disabled=letter in st.session_state.guessed_letters
                    ):

                        st.session_state.guessed_letters.append(letter)

                        if not check_guess(
                            st.session_state.word,
                            letter
                        ):
                            st.session_state.attempts -= 1

                        st.rerun()

        # RESULT DASHBOARD
        else:

            st.divider()

            st.title("📊 Game Result Dashboard")

            if won:

                st.success("🎉 Congratulations! YOU WON!")

                st.balloons()

                # Score calculation
                base_score = {
                    "Easy": 100,
                    "Medium": 150,
                    "Hard": 200
                }

                score = (
                    base_score[difficulty]
                    + st.session_state.attempts * 10
                )

            else:

                st.error("😢 GAME OVER! YOU LOST.")

                score = 0

            # Game statistics
            attempts_used = 6 - st.session_state.attempts

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🏆 Final Score",
                    score
                )

            with col2:
                st.metric(
                    "🎯 Attempts Used",
                    attempts_used
                )

            st.metric(
                "❤️ Remaining Attempts",
                st.session_state.attempts
            )

            st.write("**Correct Word:**")

            st.code(st.session_state.word.upper())

            st.write("**Difficulty:**", difficulty)

            st.write("**Letters Guessed:**")

            if st.session_state.guessed_letters:
                st.write(
                    ", ".join(
                        letter.upper()
                        for letter in st.session_state.guessed_letters
                    )
                )
            else:
                st.write("No letters guessed.")

            st.divider()

            # PLAY AGAIN
            if st.button(
                "🔄 Play Again",
                use_container_width=True
            ):

                st.session_state.word = select_word(difficulty)
                st.session_state.guessed_letters = []
                st.session_state.attempts = 6
                st.session_state.started = True

                st.rerun()

            # BACK TO DASHBOARD
            if st.button(
                "🏠 Back to Dashboard",
                use_container_width=True
            ):

                st.session_state.started = False
                st.session_state.word = ""
                st.session_state.guessed_letters = []
                st.session_state.attempts = 6

                st.rerun()

    st.divider()

    # LOGOUT
    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.started = False
        st.session_state.word = ""
        st.session_state.guessed_letters = []
        st.session_state.attempts = 6

        st.rerun()
