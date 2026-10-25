'''
Student Grade Analyzer

A simple program demonstrating various concepts such as
- Dictionaries
- Loops
- Exception Handling
'''
def main():
    print("=== Student Grade Analyzer ===")

    subjects = {}
    number_of_subjects = int(input("How many subjects? "))

    if number_of_subjects <= 0:
        print("Please enter at least one subject.")
        return

    for i in range(number_of_subjects):
        subject = input(f"Enter subject {i + 1} name: ").strip()
        
        while not subject:
            subject = input("Subject name cannot be empty. Try again: ").strip()

        while True:
            try:
                marks = float(input(f"Enter marks for {subject} (0-100): "))
                if 0 <= marks <= 100:
                    break
                print("Marks must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

        subjects[subject] = marks

    average = sum(subjects.values()) / len(subjects)

    print("\n=== Results ===")
    for subject, marks in subjects.items():
        print(f"{subject}: {marks:g}/100")

    print(f"\nAverage: {average:.2f}%")
    print(f"Highest: {max(subjects, key=subjects.get)}")
    print(f"Lowest: {min(subjects, key=subjects.get)}")

    if average >= 90:
        category = "Excellent"
    elif average >= 75:
        category = "Very Good"
    elif average >= 60:
        category = "Good"
    elif average >= 40:
        category = "Needs Improvement"
    else:
        category = "Keep Practising"

    print(f"Performance: {category}")


if __name__ == "__main__":
    main()

'''
Sample Input
How many subjects? 3
Enter subject 1 name: Maths
Enter marks for Maths (0-100): 95
Enter subject 2 name: Physics
Enter marks for Physics (0-100): 92
Enter subject 3 name: CS
Enter marks for CS (0-100): 98

Expected Output (Tested in IDLE)
=== Results ===
Maths: 95/100
Physics: 92/100
CS: 98/100

Average: 95.00%
Highest: CS
Lowest: Physics
Performance: Excellent
'''
