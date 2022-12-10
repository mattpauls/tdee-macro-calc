import json
from datetime import datetime, date, timedelta
from typing import Union
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
from pathlib import Path
from dateutil.parser import *

c = Console()

HOME = Path.home()


def check_data_file(home_dir: Path = HOME) -> dict:
    """
    Checks to see if the file data.json exists, and if not it creates it with default values.

    Returns a dictionary of the user and tdee information in the file.
    """
    # Gather current user's directory information and set up ~/.tdee/data.json
    tdee_directory = home_dir / ".tdee"
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

def check_valid_date(my_date: str) -> bool:
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


def prompt_or_exit(
    prompt: str,
    default: Optional[Union[str, int, float]] = None,
    dtype: type = str,
    exit_char: str = "e"
) -> Union[str, int, float]:
    """Build a prompt that validates input.

    Returns when the user 'exits' using the
    exit character or enters valid input.

    Parameters
    ----------
    prompt: str
        The prompt to ask the user.
    default:
        The default value of the prompt if no answer is given.
    dtype:
    """
    while True:
        resp = Prompt.ask(prompt, default=default)
        # Is this an exit
        if resp == exit_char:
            return resp
        try:
            # Handle an empty entry.
            if not resp:
                raise ValueError
            resp = dtype(resp)
            return resp
        # Re-prompt user if value is invalid.
        except (ValueError, TypeError):
            text = Text()
            text.append("\nOops, looks like there was a mistake...\n", style="bold red")
            text.append(
                f"\nExpected a value of type '{dtype.__name__}'. Please enter a valid value.\n",
            )
            c.print(text)


def tdee_input(tdee_data_file, data):
    """
    Adds TDEE record(s) to the data.json file under the 'tdee' key.

    Asks user for the date, weight, and calories for each entry.
    """

    record_date = date.today()
    added_record = False

    while True:
        c.print("\n")
        c.rule(title="Record TDEE")
        c.print("Add TDEE record(s). Enter 'e' to save and exit.")
        c.print("\n")

        if added_record:
            # Increment the record_date by a day, if this is not the first record we've added
            record_date+= timedelta(days=1)

        # Prompt user for date of entry
        record_date = Prompt.ask("Date", default=datetime.strftime(record_date, "%m/%d/%Y"))

        # Exit if requested
        if record_date == "e":
            break
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
        # TODO add checking to make sure that input is reasonable (e.g. not larger than 4 digits etc.)
        weight = prompt_or_exit("Weight", dtype=float)
        if weight == "e":
            break

        # Get calories consumed
        calories = prompt_or_exit("Calories", dtype=float)
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


def calculate(data):
    """
    Calculates averages for calories and weight, based on saved settings in the data.json file.

    Returns...dictionary with information?
    """

    if data["tdee"]:  # Check if tdee list has data (returns true if it does have data)
        # Calculate current_weight and current_calories
        # TODO figure out how to handle duplicate entries on the same date? Perhaps restructure to a dict with date as the key?
        # TODO perhaps restrict the number of records we calculate on to the most recent two weeks or month? Either total number of records or date range.
        number_records = len(data["tdee"])

        average_weight = 0
        average_calories = 0

        for record in data["tdee"]:
            average_weight += record["weight"]
            average_calories += record["calories"]

        average_weight = round((average_weight/number_records), 1)
        average_calories = round(average_calories/number_records)

        # Save average_weight and average_calories to data
        # This may be unnecessary, I'm not referencing it anywhere else and doing the calculations all at once.
        data["user"]["average_weight"] = average_weight
        data["user"]["average_calories"] = average_calories

        # Calculate calorie deficit
        # TODO allow user to choose a custom calorie deficit - the default feels pretty agressive
        target_calorie_deficit = round(data["user"]["per_lb_calorie_deficit"] * float(average_weight))
        target_calorie_intake = round(float(average_calories) - float(target_calorie_deficit))

        # Calculate Macros
        protein_grams = round(data["user"]["per_lb_protein"] * float(average_weight))
        fat_grams = round(data["user"]["per_lb_fat"] * float(average_weight))
        carbs_grams = round((target_calorie_intake - (protein_grams * 4) - (fat_grams * 9))/4)

        # Save calculated data to data
        data["user"]["protein_grams"] = protein_grams
        data["user"]["fat_grams"] = fat_grams
        data["user"]["carbs_grams"] = carbs_grams


def save_calculations(tdee_data_file, data) -> None:
    """"
    Saves the results of calculate() to file.
    """
    tdee_data_file.write_text(json.dumps(data))


def display_data(tdee_data_file, data):
    """
    Displays calculated calorie and macro data to the user.

    If no entries exist, prompts the user to enter data.
    """
    c.print(data)

    if data["tdee"]:  # Check if tdee list has data (returns true if it does have data)
        # Calculate current_weight and current_calories
        data = calculate(data)
        save_calculations(tdee_data_file, data)

        # Output info to user
        c.print("\n")
        c.rule(title="Statistics")
        c.print("Your current average weight:", str(data["user"]["average_weight"]))
        c.print("Your current TDEE:", str(data["user"]["average_calories"]))
        c.rule(title="Calories")
        c.print("Target calorie intake:", str(data["user"]["target_calorie_intake"]))
        c.print("Target calorie deficit:", str(data["user"]["target_calorie_deficit"]))
        c.rule(title="Macros")
        c.print("Target protein intake (grams):", str(data["user"]["protein_grams"]))
        c.print("Target fat intake (grams):", str(data["user"]["fat_grams"]))
        c.print("Target carbs intake (grams):", str(data["user"]["carbs_grams"]))
        c.print("\n")
        input("Press Enter to continue...")
    else:  # if no entry exists, prompt to enter some data (can't display no data!)
        print("No TDEE data!")
        record_data = Prompt.ask("Would you like to record some data now?", choices=["y", "n"])

        if record_data == "y":
            tdee_input(tdee_data_file, data)


def display_tdee_data(data):
    tdee_table = Table(title="Recorded TDEE Data")

    tdee_table.add_column("Date", style="green")
    tdee_table.add_column("Weight")
    tdee_table.add_column("Calories")

    for record in data["tdee"]:
        tdee_table.add_row(record["date"], str(record["weight"]), str(record["calories"]))

    c.print("\n")
    c.print(tdee_table)


def menu():
    """
    Displays the main menu to the user.
    """
    menu_options = {
        1: "View current calorie and macro goal",
        2: "View recorded TDEE data",
        3: "Record TDEE",
        4: "Change or update calorie and macro targets",
        5: "Start over and delete all data",
        6: "Exit"
    }
    print("\n")
    c.rule(title="TDEE and Macro Calculator")
    for key in menu_options.keys():
        print(key, ":", menu_options[key])
    print("\n")


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
            display_data(tdee_data_file, data)
        elif option == 2:
            display_tdee_data(data)
        elif option == 3:
            tdee_input(tdee_data_file, data)
        elif option == 4:
            print("Change or update calorie and macro targets")
        elif option == 5:
            print("Start over")
        elif option == 6:
            exit()
        else:
            print("Invalid option, please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
