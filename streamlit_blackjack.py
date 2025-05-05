import streamlit as st
import random

# --- Helper functions ---
def create_deck():
    """Create and shuffle a standard 52-card deck."""
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(deck)
    return deck


def calculate_value(hand):
    """Calculate the value of a blackjack hand, adjusting for Aces."""
    value = sum(hand)
    aces = hand.count(11)
    # Convert Aces from 11 to 1 as needed
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def deal_card():
    """Deal a single card from the deck."""
    return st.session_state.deck.pop()


def start_game():
    """Initialize game state for a new round."""
    st.session_state.deck = create_deck()
    st.session_state.player_hand = []
    st.session_state.dealer_hand = []
    st.session_state.in_game = True
    st.session_state.player_stand = False
    st.session_state.message = ""
    # Deal initial cards
    for _ in range(2):
        st.session_state.player_hand.append(deal_card())
        st.session_state.dealer_hand.append(deal_card())


# --- Initialize session state ---
if 'in_game' not in st.session_state:
    start_game()

# --- Streamlit UI ---
st.title("Blackjack")

# Dealer's hand (hide second card if game in progress)
st.subheader("Dealer's Hand")
if st.session_state.in_game:
    first_card = st.session_state.dealer_hand[0]
    st.write(f"[{first_card}, ?]")
else:
    st.write(st.session_state.dealer_hand)
    st.write("Value:", calculate_value(st.session_state.dealer_hand))

# Player's hand
st.subheader("Your Hand")
st.write(st.session_state.player_hand)
st.write("Value:", calculate_value(st.session_state.player_hand))

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Hit") and st.session_state.in_game and not st.session_state.player_stand:
        st.session_state.player_hand.append(deal_card())
        if calculate_value(st.session_state.player_hand) > 21:
            st.session_state.message = "You busted! Dealer wins."
            st.session_state.in_game = False
with col2:
    if st.button("Stand") and st.session_state.in_game and not st.session_state.player_stand:
        st.session_state.player_stand = True
        # Dealer plays
        while calculate_value(st.session_state.dealer_hand) < 17:
            st.session_state.dealer_hand.append(deal_card())
        # Determine outcome
        player_val = calculate_value(st.session_state.player_hand)
        dealer_val = calculate_value(st.session_state.dealer_hand)
        if dealer_val > 21 or player_val > dealer_val:
            st.session_state.message = "You win!"
        elif player_val < dealer_val:
            st.session_state.message = "Dealer wins."
        else:
            st.session_state.message = "Push."
        st.session_state.in_game = False
with col3:
    if st.button("New Game"):
        start_game()

# Display result message
if not st.session_state.in_game:
    st.subheader(st.session_state.message)
