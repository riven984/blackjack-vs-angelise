import random
import os
import time

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def card_value(rank):
    if rank in ["J", "Q", "K"]:
        return 10
    elif rank == "A":
        return [1, 11]
    else:
        return int(rank)

def hand_value(hand):
    total = 0
    aces = 0
    for card, value in hand:
        if isinstance(value, list):
            total += 11
            aces += 1
        else:
            total += value
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def prepare_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            card = f"{rank}{suit}"
            value = card_value(rank)
            deck.append((card, value))
    random.shuffle(deck)
    return deck

def show_hand(name, hand, is_angelise=False):
    print(f"\n{'🎀' if is_angelise else '🧍'} {name}'s hand:")
    cards = "  ".join(card for card, _ in hand)
    total = hand_value(hand)
    print(f"🃏 Cards: {cards}")
    print(f"🔢 Total: {total}")
    print("──────────────────────────────")  # separator linia

def play_hand(deck, hand, bet, balance, allow_double=True):
    doubled = False
    while True:
        clear_screen()
        print(f"💰 Balance: {balance} chips    💵 Current bet: {bet} chips")
        show_hand("You", hand)
        total = hand_value(hand)
        if total > 21:
            print("❌ You busted!")
            print("····························")
            time.sleep(2)
            return hand, -bet  # przegrana
        if allow_double and balance >= bet:
            action = input("👉 Type 'hit', 'stand', or 'double': ").lower()
        else:
            action = input("👉 Type 'hit' or 'stand': ").lower()

        if action == "hit":
            hand.append(deck.pop())
            print("\n💥 You drew a card!")
            print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")
            time.sleep(1)
        elif action == "double" and allow_double and balance >= bet:
            hand.append(deck.pop())
            doubled = True
            bet *= 2
            clear_screen()
            print(f"💰 Balance: {balance} chips    💵 Current bet: {bet} chips")
            show_hand("You", hand)
            print("💥 You doubled down! One more card:")
            print("______________________________")
            time.sleep(2)
            break
        elif action == "stand":
            print("\n🛑 You stand.")
            print("····························")
            time.sleep(1)
            break
        else:
            print("⚠️ Invalid or unavailable option.")
            time.sleep(1)
    return hand, bet

def angelise_turn(deck, hand):
    clear_screen()
    print("🎀 Angelise's turn...")
    show_hand("Angelise", hand, is_angelise=True)
    time.sleep(1)
    while hand_value(hand) < 17:
        print("🎀 Angelise draws a card...")
        time.sleep(1)
        hand.append(deck.pop())
        clear_screen()
        show_hand("Angelise", hand, is_angelise=True)
        time.sleep(1)
    return hand

def blackjack(balance):
    clear_screen()
    print("🎰 Welcome to Blackjack vs Angelise 🎀")
    print(f"💎 Your current balance: {balance} chips")

    try:
        bet = int(input("💰 Place your bet: "))
    except ValueError:
        print("❌ Invalid input.")
        time.sleep(1.5)
        return balance

    if bet > balance or bet <= 0:
        print("⚠️ Invalid bet amount.")
        time.sleep(1.5)
        return balance

    deck = prepare_deck()
    player_hand = [deck.pop(), deck.pop()]
    angelise_hand = [deck.pop(), deck.pop()]

    split = False
    results = []
    total_bet = bet

    # --- Check for split ---
    if player_hand[0][0][:-1] == player_hand[1][0][:-1] and balance >= bet * 2:
        choice = input(f"🃓 You have a pair of {player_hand[0][0][:-1]}s. Split? (yes/no): ").lower()
        if choice == "yes":
            split = True
            hand1 = [player_hand[0], deck.pop()]
            hand2 = [player_hand[1], deck.pop()]
            print("\n🔀 You split your hand.")
            print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")
            show_hand("Hand 1", hand1)
            show_hand("Hand 2", hand2)
            time.sleep(2)

            # Gra dla każdej ręki osobno (double niedostępne po split)
            final_hand1, bet1 = play_hand(deck, hand1, bet, balance, allow_double=False)
            if bet1 < 0:
                results.append(([], bet))  # busted ręka
            else:
                results.append((final_hand1, bet))

            final_hand2, bet2 = play_hand(deck, hand2, bet, balance, allow_double=False)
            if bet2 < 0:
                results.append(([], bet))
            else:
                results.append((final_hand2, bet))

            total_bet = bet * 2

    if not split:
        # Normalna rozgrywka z możliwością double down
        result = play_hand(deck, player_hand, bet, balance)
        if isinstance(result, tuple):
            player_hand, bet = result
            total_bet = bet
            results = [(player_hand, bet)]
        else:
            print(f"❌ You lost {bet} chips.")
            time.sleep(1.5)
            return balance - bet

    # --- Angelise turn ---
    angelise_hand = angelise_turn(deck, angelise_hand)
    angelise_total = hand_value(angelise_hand)
    print(f"\n🎀 Angelise's total: {angelise_total}")
    print("──────────────────────────────")
    time.sleep(2)

    # --- Evaluate each hand ---
    for i, (hand, hand_bet) in enumerate(results, 1):
        if not hand:
            print(f"\n🟥 Hand {i}: Busted. Lost {hand_bet} chips.")
            balance -= hand_bet
            print("····························")
            continue
        player_total = hand_value(hand)
        print(f"\n🃏 Hand {i}: {player_total} vs 🎀 Angelise: {angelise_total}")
        if player_total > 21:
            print(f"🟥 You busted. Lost {hand_bet} chips.")
            balance -= hand_bet
        elif angelise_total > 21 or player_total > angelise_total:
            print(f"✅ You win hand {i}! Gained {hand_bet} chips.")
            balance += hand_bet
        elif player_total == angelise_total:
            print(f"🤝 Hand {i} is a tie. Bet returned.")
        else:
            print(f"❌ Angelise wins hand {i}. Lost {hand_bet} chips.")
            balance -= hand_bet
        print("──────────────────────────────")
        time.sleep(2)
    return balance

# --- MAIN LOOP ---
balance = 100

while True:
    if balance <= 0:
        print("💀 You're out of chips! Game over.")
        break

    response = input("\n🎮 Play Blackjack with Angelise? (yes/no): ").lower()
    if response == "yes":
        balance = blackjack(balance)
        print(f"\n💰 Current balance: {balance} chips")
        input("🔁 Press Enter to continue...")
    elif response == "no":
        print(f"👋 You left the table with {balance} chips. Bye!")
        break
    else:
        print("⚠️ Please type 'yes' or 'no'.")
