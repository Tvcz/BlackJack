from ai import AIPlayer
from time import sleep

ai = AIPlayer()

def advisor():
    state = input("Enter the current state of the game in the format of\n[Player points]|[visible House points]\n>>> ")
    result = ai.play(state)
    if result == "h":
        print("According to the recorded data, you should hit.")
    if result == "s":
        print("According to the recorded data, you should stay.")
    print()
    sleep(1)

while True:
    try:
        advisor()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
