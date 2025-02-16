import json

def get_user_choice(prompt, choices):
    """Helper function to get a valid user input from a list of choices."""
    while True:
        print(prompt)
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")
        
        selection = input("Enter your choice (number): ").strip()
        
        if selection.isdigit() and 1 <= int(selection) <= len(choices):
            return choices[int(selection) - 1]
        
        print("❌ Invalid choice. Please try again.")

def get_multiple_choices(prompt, choices):
    """Helper function to get multiple valid user inputs."""
    selected_options = []
    
    while True:
        print(prompt)
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")
        print("0. Done selecting")

        selection = input("Enter your choice (number): ").strip()

        if selection == "0":
            break
        elif selection.isdigit() and 1 <= int(selection) <= len(choices):
            option = choices[int(selection) - 1]
            if option not in selected_options:
                selected_options.append(option)
            else:
                print("✅ Already selected.")
        else:
            print("❌ Invalid choice. Please try again.")
    
    return selected_options

def create_rule():
    """Function to interactively create a new rule."""
    print("\n📜 Creating a new rule...")

    # Select "All" or "Any"
    predicate = get_user_choice("Should all conditions match, or any one condition?", ["All", "Any"])

    # Condition selection
    conditions = []
    while True:
        field = get_user_choice("Select the field for condition:", ["from", "subject", "snippet", "received_at"])
        operator = get_user_choice("Select the condition type:", ["contains", "does_not_contain", "equals", "does_not_equal"])
        value = input(f"Enter the value for '{field}': ").strip()

        conditions.append({"field": field, "operator": operator, "value": value})

        more_conditions = get_user_choice("Do you want to add another condition?", ["Yes", "No"])
        if more_conditions == "No":
            break

    # Action selection
    actions = get_multiple_choices("Select the actions:", ["mark_as_read", "mark_as_unread", "move_to_folder"])

    if "move_to_folder" in actions:
        folder_name = input("Enter the folder name to move emails to: ").strip()
        actions[actions.index("move_to_folder")] = f"move_to_folder:{folder_name}"

    # Rule dictionary
    rule = {
        "predicate": predicate,
        "conditions": conditions,
        "actions": actions
    }

    # Save rule to JSON
    try:
        with open("rules.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"rules": []}

    data["rules"].append(rule)

    try:
        with open("rules.json", "w") as file:
            json.dump(data, file, indent=4)
        print("\n✅ Rule saved successfully!")
    except Exception as e:
        print(f"❌ Error saving the rule: {e}")

if __name__ == "__main__":
    create_rule()
