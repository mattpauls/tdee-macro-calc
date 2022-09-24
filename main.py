
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
    "tdee": [
        {
            "date": "9/20/22",
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

def main():
    # Get current stats
    # current_weight = input("Your current weight (lbs): ")
    current_weight = data["user"]["current_weight"]
    # current_tdee = input("Your current TDEE (calories): ")
    current_tdee = data["user"]["current_tdee"]


    # Calculate calorie deficit
    target_calorie_deficit = 3.2 * float(current_weight)
    target_calorie_intake = float(current_tdee) - float(target_calorie_deficit)

    # Calculate Macros
    protein_grams = .8 * float(current_weight)
    fat_grams = .3 * float(current_weight)
    carbs_grams = (target_calorie_intake - (protein_grams * 4) - (fat_grams * 9))/4

    # Output info to user
    print("\n")
    print("====== STATS ======")
    print("Your current weight:", str(current_weight))
    print("Your current TDEE:", str(current_tdee))
    print("\n")
    print("====== CALORIES ======")
    print("Target calorie intake:", str(target_calorie_intake))
    print("Target calorie deficit:", str(target_calorie_deficit))
    print("\n")
    print("====== MACROS ======")
    print("Target protein intake (grams):", str(protein_grams))
    print("Target fat intake (grams):", str(fat_grams))
    print("Target carbs intake (grams):", str(carbs_grams))

if __name__ == "__main__":
    main()
