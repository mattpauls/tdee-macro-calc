import json
from datetime import datetime, date
from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown

c = Console()

def check_data_file() -> dict:
    """
    Checks to see if the file data.json exists, and if not it creates it with default values.

    Returns a dictionary of the user and tdee information in the file.
    """
    try:
        with open("data.json") as f:
            data = json.load(f)

    except FileNotFoundError:
        with open("data.json", "x") as f:
            data = {
                        "user": {
                            "per_lb_calorie_deficit": 3.2, # use 3.2 as default but allow user to change, possibly. TODO look at study to confirm dropping this number works
                            "per_lb_protein": .8, # use .8 as default but allow user to change, and/or play with different numbers in memory
                            "per_lb_fat": .3 # use .3 as default but allow user to change, and/or play with different numbers in memory
                        },
                        "tdee": []
                    }
            f.write(json.dumps(data))
    print(data)
    return data

def tdee_input(data):
    """
    Adds TDEE record(s) to the data.json file under the 'tdee' key.

    Asks user for the date, weight, and calories for each entry.
    """
    # TODO type check values
    # TODO make it easier to enter dates, once one is added, increment as a default
    try:
        with open("data.json", "r+") as f:
            f_data = json.load(f)

            while True:
                print("Add TDEE record. Enter 'e' to exit.")

                # Prompt user for date of entry
                today = datetime.strftime(date.today(), "%m/%d/%Y")
                print(datetime.strftime(date.today(), "%m/%d/%Y"))

                record_date = Prompt.ask("Date (%s)" % today)
                if record_date == "e":
                    break
                if record_date == "":
                    print("using default date", today)
                else:
                    try:
                        my_date = datetime.strptime(record_date, "%m/%d/%Y").date()
                        print(my_date)
                    except ValueError:
                        print("Invalid date, try again")

                # Prompt user for weight
                weight = Prompt.ask("Weight")
                if weight == "e":
                    break

                # Prompt user for calories consumed
                calories = Prompt.ask("Calories")
                if calories == "e":
                    break

                # Append to tdee file
                f_data["tdee"].append({
                    "date": record_date,
                    "weight": float(weight),
                    "calories": int(calories)
                })

                f.seek(0)

                json.dump(f_data, f)

    except FileNotFoundError:
        print("file wasn't found")
    

def display_data(data):
    """
    Calculates and displays calorie and macro data to the user.

    If no entries exist, prompts the user to enter data.
    """
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

        input("Press Enter to continue...")
    except:
        print("No current weight or tdee data!")
        record_data = Prompt.ask("Would you like to record some data?", choices=["y", "n"])

        if record_data == "y":
            tdee_input(data)

def menu():
    """
    Displays the main menu to the user.
    """
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
            display_data(data)
        elif option == 2:
            print("Record TDEE")
            tdee_input(data)
        elif option == 3:
            print("Change or update calorie and macro targets")
        elif option == 4:
            print("Start over")
        elif option == 5:
            exit()
        else:
            print("Invalid option, please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
