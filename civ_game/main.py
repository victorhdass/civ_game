from .game import Game
from .civilization_traits import CIVILIZATION_TRAITS
import pickle
import os

def main():
    """
    Main function to run the game.
    """
    print("--- Welcome to Civ Game ---")
    
    # NOTE: Disabled save loading for debugging.
    # if os.path.exists("savegame.pkl"):
    #     choice = input("Do you want to (1) Start a new game or (2) Load saved game? ")
    #     if choice == '2':
    #         try:
    #             with open("savegame.pkl", "rb") as f:
    #                 game = pickle.load(f)
    #             print("Game loaded successfully!")
    #             game.run()
    #             return
    #         except Exception as e:
    #             print(f"Error loading game: {e}. Starting a new game.")

    print("\nChoose your civilization for a new game:")
    civ_choices = list(CIVILIZATION_TRAITS.keys())
    for i, civ_name in enumerate(civ_choices):
        print(f"\n{i + 1}. {civ_name}")
        traits = CIVILIZATION_TRAITS[civ_name]
        print(f"  Description: {traits['description']}")
        print("  Advantages:")
        for adv in traits['advantages']:
            print(f"    - {adv}")
        print("  Disadvantages:")
        for disadv in traits['disadvantages']:
            print(f"    - {disadv}")

    try:
        civ_choice = int(input("\nEnter the number of your civilization: "))
        if 1 <= civ_choice <= len(civ_choices):
            player_civ_name = civ_choices[civ_choice - 1]
            
            print("\nChoose difficulty:")
            print("1. Easy")
            print("2. Normal")
            print("3. Hard")
            diff_choice = int(input("Enter the number for difficulty: "))
            
            difficulty_levels = {1: "Easy", 2: "Normal", 3: "Hard"}
            difficulty = difficulty_levels.get(diff_choice, "Normal")

            all_civ_names = [player_civ_name] + [name for name in civ_choices if name != player_civ_name]
            
            game = Game(all_civ_names, difficulty)
            game.run()
        else:
            print("Invalid civilization choice. Exiting.")
    except ValueError:
        print("Invalid input. Exiting.")

if __name__ == "__main__":
    main()