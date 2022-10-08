# TDEE and Macro Calculator

Replaces the functionality of a few spreadsheets I use to calculate TDEE (Total Daily Estimated Expenditure) and macros for weight loss. Based on a general guide [here](https://thefitness.wiki/weight-loss-101/).

Inspired by the [nSuns TDEE spreadsheet](https://docs.google.com/spreadsheets/d/1QTWDxFaB0r-7U6vZmG1s8of7jwd2GHHi/edit#gid=770164572).

## Installation

Clone this repository:
```
git clone https://github.com/mattpauls/tdee-macro-calc
```

Install using `pip`. If you're developing on this project, use the "dev" install (by adding a `-e`):
```
pip install -e .
```
This will pick up any changes you make after the installation without requiring you to install again.

## Basic Usage

TDEE Macro Calculator is a command line tool with a single entry-point. After installing, you can run the program from anywhere in your terminal by calling:
```
tdee
```

## Notes and Methodology
### TDEE
TDEE is the running average of daily calories. To lose weight, IN GENERAL, one must achieve a calorie deficit. Calculating a TDEE helps because it provides a baseline of current caloric intake to make decisions.

Once the current TDEE is calculated, a goal daily calorie intake can be obtained by determining how much and how quickly weight should be lost. This goal calorie intake is the number of calories one should eat in a day to achieve a relative calorie deficit and begin to lose weight. This is calculated using the formula $goal calorie intake = TDEE - (weight * 3.2cal)$

### Macros
For weight loss, macros, or the amount of protein, fat, and carbs one should eat, is secondary to the number of daily calories one should eat. Within the macro hierarchy, the general recommendation is to prioritize calories from protein, then fat, and then fill the rest of the daily calorie intake with carbs or fat, depending on your goals. For protein, a good number to start with is 0.8g/lb. Fat, 0.3g/lb. For carbs, this program simply fills the balance of the available calories with calories from carbohydrates.

## Sources
Lose weight and build muscle simultaneously: https://thefitness.wiki/faq/can-i-lose-fat-and-build-muscle-at-the-same-time/

Recommended Macros: https://thefitness.wiki/improving-your-diet/#General_Diet_Improvement