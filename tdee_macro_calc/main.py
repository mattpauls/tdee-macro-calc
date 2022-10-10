import json
from datetime import datetime, date, timedelta
from operator import add
from xmlrpc.client import Boolean
from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown
from pathlib import Path
from dateutil.parser import *

c = Console()

def check_data_file():
    """
    Checks to see if the file data.json exists, and if not it creates it with default values.

    Returns a dictionary of the user and tdee information in the file.
    """

    # Gather current user's directory information and set up ~/.tdee/data.json
    home = Path.home()
    tdee_directory = home / ".tdee"
    tdee_directory.mkdir(exist_ok=True)
    tdee_data = tdee_directory / "data.json"

    # Try opening the data.json file in the .tdee folder
    try:
        contents = tdee_data.read_text()
        data = json.loads(contents)

    # If ~/.tdee/data.json does not exist, create it and add default data
    except FileNotFoundError:
        tdee_data.touch()
        data = {
                "user": {
                    "per_lb_calorie_deficit": 3.2, # use 3.2 as default but allow user to change, possibly. TODO look at study to confirm dropping this number works
                    "per_lb_protein": .8, # use .8 as default but allow user to change, and/or play with different numbers in memory
                    "per_lb_fat": .3 # use .3 as default but allow user to change, and/or play with different numbers in memory
                },
                "tdee": []
            }
        tdee_data.write_text(json.dumps(data))
    return (tdee_data, data)

def check_valid_date(my_date: str) -> Boolean:
    """
    Checks if the input is a valid date string, in the format MM/DD/YYYY.

    Returns True if so, False if not.
    """
    try:
        datetime.strptime(my_date, "%m/%d/%Y").date()
        return True
    except:
        return False

def convert_date(my_date):
    """
    Converts a date to a string, formatted as MM/DD/YYYY.
    """
    if isinstance(my_date, datetime) or isinstance(my_date, date):
        return datetime.strftime(my_date, "%m/%d/%Y")
    elif isinstance(my_date, str):
        return my_date
    else:
        return


def tdee_input(tdee_data_file, data):
    """
    Adds TDEE record(s) to the data.json file under the 'tdee' key.

    Asks user for the date, weight, and calories for each entry.
    """

    default_date = date.today()
    added_record = False

    while True:
        print("Add TDEE record(s). Enter 'e' to save and exit.")

        if added_record:
            # Increment the default_date by a day, if this is not the first record we've added
            default_date = record_date + timedelta(days=1)
            record_date = ""
        
        # Prompt user for date of entry
        record_date = Prompt.ask("Date (%s)" % datetime.strftime(default_date, "%m/%d/%Y"))
        
        # Exit if requested
        if record_date == "e":
            break
        
        # Otherwise, if Enter is pressed, use today's date
        if record_date == "":
            print("Using default date", str(default_date))
            record_date = default_date
        # If something was entered, then check to see if it's a valid date, convert it if possible, and then continue on with the rest of the record
        else:
            # Convert entered string into a date, either with the 4-digit year or 2-digit year
            while True:
                try:
                    record_date = parse(record_date)
                    break
                except:
                    record_date = Prompt.ask("Please enter a valid date (MM/DD/YYYY)")

        # Get weight
        while True:
            # Prompt user for weight in lbs
            weight = Prompt.ask("Weight")

            if not weight == "e":
                try:
                    # If weight isn't 'e', check the type of weight, make sure it's an int
                    float(weight)
                    break
                except ValueError:
                    print("Please enter a valid number.")
            else:
                break

        if weight == "e":
            break

        # Get calories consumed
        while True:
            # Prompt user for weight in lbs
            calories = Prompt.ask("Calories")

            if not calories == "e":
                try:
                    # If weight isn't 'e', check the type of weight, make sure it's an int
                    int(calories)
                    break
                except ValueError:
                    print("Please enter a valid number.")
            else:
                break

        if calories == "e":
            break
        
        # Append to tdee data dictionary
        data["tdee"].append({
            "date": convert_date(record_date), # Convert the datetime object to string
            "weight": float(weight),
            "calories": int(calories)
        })

        # We've added a record, so set added_record to True
        added_record = True

    try:
        # Write JSON data to file
        tdee_data_file.write_text(json.dumps(data))
    except FileNotFoundError:
        print("file wasn't found")
    

def display_data(tdee_data_file, data):
    """
    Calculates and displays calorie and macro data to the user.

    If no entries exist, prompts the user to enter data.
    """
    try:
        # TODO change these to calculate based off of recorded data, if it exists
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
            tdee_input(tdee_data_file, data)

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
    (tdee_data_file, data) = check_data_file()

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
            display_data(tdee_data_file, data)
        elif option == 2:
            print("Record TDEE")
            tdee_input(tdee_data_file, data)
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
