import random, sys

# Deklaracja stałych:
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'tył'


def main():
    """Definicja funkcji o nazwie main()."""
    print('''Oczko, Klasyczna gra karciana.\n
    Zasady:
          Spróbuj uzyskać liczbę punktów jak najbardziej zbliżoną do 21, ale nie większą.
          Króle, damy i walety mają 10 punktów.
          Asy mają 1 lub 11 punktów.
          Karty od 2 do 10 mają odpowiednia do swojego numeru liczbę punktów.
          Naciśnij H, by wziąć kolejną kartę.
          Klawisz S zatrzymuje dobieranie kart.
          Przy swojej pierwszej rozgrywce możesz wcisnąć P, by podwoić swój zakład,
          ale musisz to zrobić dokładnie jeden raz przed zakończeniem dobierania kart.
          W przypadku remisu postawiona kwota jest zwracana graczowi.
          Krupier kończy dobierać karty przy wartości 17.''')
    
    money = 5000
    # Główna pętla gry.
    while True:
        # Sprawdź, czy gracz ma jeszcze pieniądze.
        if money <=0:
            print("Jesteś spłukany!")
            print("Dobrze, że nie grałeś na prawdziwe pieniądze.")
            print("Dziękuję za grę!")
            sys.exit()

        # Gracz podaje wysokość zakładu w tej rundzie.
        print("Budżet: ", money)
        bet = getBet(money)

        # Daj krupierowi i graczowi po dwie karty z talii.
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Obsługa ruchów gracza.
        print("Zakład: ", bet)
        # Wykonuje pętle, dopóki gracz nie przestanie dobierać karty lub nie przekroczy 21.
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            # Sprawdź czy gracz przekroczył 21.
            if getHandValue(playerHand) > 21:
                break

            # Odczytaj ruchy gracza: S lub P.
            move = getMove(playerHand, money - bet)

            # Obsługa ruchów gracza.
            if move == "P":
                # Gracz podwaja zakład, można zwiększyć zakład.
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print("Zakład zwiększony do kwoty {}.".format(bet))
                print("Zakład :", bet)

            if move in ("D", "P"):
                # Wciśnięcie klawisza D lub P powoduje dobranie karty.
                newCard = deck.pop()
                rank, suit = newCard
                print("Wziąłeś {} {}.".format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # Gracz przekroczył 21.
                    continue
            
            if move in ("S", "P"):
                # Wciśnięcie klawisza S lub P kończy kolejkę gracza.
                break

        # Obsługa ruchów krupiera.
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # Krupier dobiera kartę.
                print("Krupier dobiera kartę...")
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    # Krupier przekroczył 21.
                    break
                input("Naciśnij Enter, by kontynuować...")
                print("\n\n")

        # Pokazanie kart w dłoni.
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        # Ustalenie czy gracz wygrał, przegrał czy był remis.
        if dealerValue > 21:
            print("Krupier przekroczył 21! Wygrałeś {} PLN!".format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print("Przegrałeś!")
            money -= bet
        elif playerValue > dealerValue:
            print("Wygrałeś! {} PLN!".format(bet))
            money += bet
        elif playerValue == dealerValue:
            print("Jest remis, zakład wraca do Ciebie.")

        input("Naciśnij Enter, by kontynuować...")
        print("\n\n")


def getBet(maxBet):
    """Definicja funkcji getBet(), zapytanie gracza ile chce w tej rundzie postawić."""
    deck = []
    for suit in [HEARTS, DIAMONDS, SPADES, CLUBS]:
        for rank in range(2, 11):
            # Dodanie kart numerowanych.
            deck.append((str(rank), suit))
        for rank in ("J", "Q", "K", "A"):
            # Dodanie figur i asa.
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """Pokazanie kart gracza i krupiera. Najpierw ukryj karty krupiera, jeśli zmienna showDealerHand jest równa False."""
    print()
    if showDealerHand:
        print("KRUPIER: ", getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print("KRUPIER: ???")
        # Najpier ukryj karty krupiera.
        displayCards([BACKSIDE] + dealerHand[1:])

    # Pokaż karty gracza.
    print("GRACZ: ", getHandValue(playerHand))
    displayCards(playerHand)
    