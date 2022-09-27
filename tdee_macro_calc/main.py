import json
import os
from rich.console import Console
from rich.prompt import Prompt

c = Console()

# TDEE Calculation
# Gather input from user
    # First/initial input of weight should set "current weight" to be that one.
    # Input should include date, weight, and calories
    # To make it easy, it might be helpful to default to the next day for the date, since this is a command line program, currently
    # All this data needs to be stored somewhere, likely a dictionary in memory to start but would be helpful to have a database or, possibly, a CSV file if we want to be more hacky
        # Actually JSON makes more sense I think.

# Run calculations
    # Once the input is done, we can take all the input and get an average of calories
    # Ideally, we'd have two weeks worth of data. Perhaps add some disclaimers if we don't have enough data points to make a good call
    # Perhaps if the dates are too far apart, we can suggest starting over

# Input
    # Current weight
    # Current TDEE
        # Calculated off of TDEE calculator
    # (optional, maybe just default to .8) Per-lb protein intake (.8-1.0)
    # (optional, maybe just default to .4) Per-lb fat intake (.4-.5)

# Output
    # Current TDEE (average of current daily calories)
    # Current average weight
    # Target daily calorie deficit (3.2kcal/lb)
    # Target daily calorie intake (Current TDEE minus target daily calorie deficit)
    # Macros - first hit the calorie goal, then protein, then fat, then fill rest with carbs
        # Protein 4 cal per gram, .8-1.0g/lb for building muscle, 120g-160g/day is a good place to start
            # Output: how many grams of protein you should eat (and as an FYI, how many calories that is)
        # Fat 9 cal per gram, minimum .3g/lb
            # Output: how many grams of fat you should eat (and as an FYI, how many calories that is)
        # Carbs 4 cal per gram Essentially, take the calories eaten in protein and fat, subtract from your goal calories per day, and the rest is what you can eat in carbs. However, carbs/fat really doesn't matter, what is most important is protein.
            # Output: how many grams of carbs you should eat (and as an FYI, how many calories that is)

# JSON Data structure DRAFT
data = {
    "user": {
        "current_weight": 176, # this will be updated with a rolling 7-day average
        "current_tdee": 2400, # this will be updated with a max 4 week (?) average
        "sex": "male", # this determines default of 3.2, if female can go to 4.5 I believe. Not sure if I want to actually include this as functionality right now or not
        "target_calorie_intake": 1700,
        "per_lb_calorie_deficit": 3.2, # use 3.2 as default but allow user to change, possibly. TODO look at study to confirm dropping this number works
        "per_lb_protein": .8, # use .8 as default but allow user to change, and/or play with different numbers in memory
        "per_lb_fat": .3 # use .3 as default but allow user to change, and/or play with different numbers in memory
    },
    "tdee": [ # TODO This could totally be an object, same with user
        {
            "date": "9/20/22", # TODO this should be a datetime object and need to handle type checking
            "weight": 178.1,
            "calories": 2531
        },
        {
            "date": "9/21/22",
            "weight": 177.3,
            "calories": 1971
        },
        {
            "date": "9/22/22",
            "weight": 179.2,
            "calories": 2391
        }
    ]
}

def check_data_file() -> dict:
    try:
        with open("data.json") as f:
            new_data = json.load(f)
            print(new_data)

    except FileNotFoundError:
        with open("data.json", "x") as f:
            new_data = {
                        "user": {
                            "per_lb_calorie_deficit": 3.2, # use 3.2 as default but allow user to change, possibly. TODO look at study to confirm dropping this number works
                            "per_lb_protein": .8, # use .8 as default but allow user to change, and/or play with different numbers in memory
                            "per_lb_fat": .3 # use .3 as default but allow user to change, and/or play with different numbers in memory
                        },
                        "tdee": []
                    }
            f.write(json.dumps(new_data))

    return new_data

def add_to_file():
    try:
        with open("data.json") as f:
            new_data = json.load(f)
            print(new_data)
    except:
        print("error opening file")

def tdee_input():
    while True:
        print("Add TDEE record. Enter 'e' to exit.")

        # Prompt user for date of entry
        date = Prompt.ask("Date")
        if date == "e":
            break

        # Prompt user for weight
        weight = Prompt.ask("Weight: ")
        if weight == "e":
            break

        # Prompt user for calories consumed
        calories = Prompt.ask("Calories: ")
        if calories == "e":
            break

        # Append to data
        data["tdee"].append({
            "date": date,
            "weight": float(weight),
            "calories": int(calories)
        })

    print(data["tdee"])

def display_data():
    try:
        current_weight = data["user"]["current_weight"]
        current_tdee = data["user"]["current_tdee"]

        # Calculate calorie deficit
        target_calorie_deficit = 3.2 * float(current_weight)
        target_calorie_intake = round(float(current_tdee) - float(target_calorie_deficit))

        # Calculate Macros
        protein_grams = round(.8 * float(current_weight))
        fat_grams = round(.3 * float(current_weight))
        carbs_grams = round((target_calorie_intake - (protein_grams * 4) - (fat_grams * 9))/4)

        # Output info to user
        c.rule(title="Statistics")
        c.print("Your current weight:", str(current_weight))
        c.print("Your current TDEE:", str(current_tdee))
        c.rule(title="Calories")
        c.print("Target calorie intake:", str(target_calorie_intake))
        c.print("Target calorie deficit:", str(target_calorie_deficit))
        c.rule(title="Macros")
        c.print("Target protein intake (grams):", str(protein_grams))
        c.print("Target fat intake (grams):", str(fat_grams))
        c.print("Target carbs intake (grams):", str(carbs_grams))
    except:
        print("No current weight or tdee data")

    input("Press Enter to continue...")

def menu():
    menu_options = {
        1: "View current calorie and macro goal",
        2: "Record TDEE",
        3: "Change or update calorie and macro targets",
        4: "Start over and delete all data",
        5: "Exit"
    }
    
    for key in menu_options.keys():
        print(key, ":", menu_options[key])


def main():
    # Check to see if there's a data.json file, and create it with defaults if not.
    data = check_data_file()

    # Display menu
    while(True):
        menu()
        option = 0
        try:
            option = int(input("Enter your choice: "))
        except:
            print("Wrong input, please enter a number.")
        if option == 1:
            print("View current info")
            display_data()
        elif option == 2:
            print("Record TDEE")
        elif option == 3:
            print("Change or update calorie and macro targets")
        elif option == 4:
            print("Start over")
        elif option == 5:
            exit()
        else:
            print("Invalid option, please enter a number between 1 and 5.")

    # Get current stats
    # current_weight = input("Your current weight (lbs): ")
    
    # current_tdee = input("Your current TDEE (calories): ")
    

    

if __name__ == "__main__":
    main()
    # tdee_input()
