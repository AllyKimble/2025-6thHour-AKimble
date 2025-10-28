#Name: Ally Kimble
#Class: 6th Hour
#Assignment: SC2


#A local health clinic is looking to add a quick BMI calculator to their website so that their
#patients can quickly input their height and weight and be given a number as well as their
#classification. The classifications are as follows:

# - Underweight: Less than 18.5 BMI
# - Normal Weight: 18.5 to 24.9 BMI
# - Overweight: 25 to 29.9 BMI
# - Obese: 30 or more BMI

#It is up to you to figure out the calculation for an accurate BMI reading and tying it to
#the right classification

#Code Here:

feet = int(input("Height in Feet:"))
inches = int(input("Additional Inches:"))
weight = int(input("Weight in Pounds:"))

total_height = (feet * 12) + inches


bmi = (weight / (total_height ** 2)) * 703

print("Your BMI is:", bmi )

if bmi < 18.5:
    print("You are underweight")
elif 18.5 <= bmi < 25:
    print("You are normal")
elif 25 <= bmi < 30:
    print("You are overweight")
elif bmi >= 30:
    print("You are obese")



