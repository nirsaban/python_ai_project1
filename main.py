# main.py
from typing import Any, Callable
from data_manager import DataManager
from Validator import Validator
from FileMangment import FileManagement
from card_builder import CardBuilder
from gemini import Gemini


class TitanicApp:
    def __init__(self, data_path: str):
        self.data_manager = DataManager(data_path)
        self.validator = Validator()
        self.file_manager = FileManagement()
        self.builder = CardBuilder()
        self.gemini_assistant = Gemini()

    def run(self):
        print("🚢 Welcome to the Titanic Ticket System!\n")

        # Collect and validate user inputs
        name = self.validator.clean_name(input("Enter your name: "))
        age = self.validator.validate_age(input("Enter your age: "))
        sex = self.validator.validate_sex(input("Enter your sex (male/female): "))
        fare = self.validator.validate_fare(
            input("Enter your fare: "),
            self.data_manager.min_fare,
            self.data_manager.max_fare
        )

        # Determine class, ticket, and survival chance
        pclass = self.data_manager.determine_class(fare)
        ticket_num = self.data_manager.generate_ticket_number()
        survival_chance = self.data_manager.calculate_survival_chance(sex, pclass)

        ai_prompt = self.gemini_assistant.build_gemini_prompt(name, age, sex, fare, survival_chance)
        ai_tip = self.gemini_assistant.ask_gemini(ai_prompt)

        # Build and save ticket
        ticket_text = self.builder.build_ticket(
            name, age, sex, fare, pclass, ticket_num, survival_chance, ai_tip
        )
        print(ticket_text)
        self.file_manager.save_ticket(name, ticket_text)

    # --- Single Generic Filtering Method ---
    def getGenericData(self, conditions: dict[str, Callable[[Any], bool]]):
        results = []

        for row in self.data_manager.data:
            match = True
            for key, cond in conditions.items():
                if key in row:
                    try:
                        if not cond(row[key]):
                            match = False
                            break
                    except Exception as e:
                        print(f"⚠️ Condition error on key '{key}': {e}")
                        match = False
                        break
                else:
                    match = False
                    break

            if match:
                results.append(row)

        return results


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    app = TitanicApp("data.csv")

    # Example 1: count all males
    males = app.getGenericData({
        "sex": lambda sex: sex.lower() == "male"
    })
    print("🚹 Sum of males:", len(males))

    # Example 2: count all minors
    minors = app.getGenericData({
        "age": lambda age: age is not None and int(age) < 18
    })
    print("👶 Sum of minors:", len(minors))

    # Example 3: count all female survivors
    female_survivors = app.getGenericData({
        "sex": lambda sex: sex.lower() == "female",
        "survived": lambda s: int(s) == 1
    })
    print("🚺 Female survivors:", len(female_survivors))

    # Example 4: calculate survival percentage by gender (using getGenericData)
    for gender in ["male", "female"]:
        total = len(app.getGenericData({
            "sex": lambda sex, g=gender: sex.lower() == g
        }))
        survived = len(app.getGenericData({
            "sex": lambda sex, g=gender: sex.lower() == g,
            "survived": lambda s: int(s) == 1
        }))
        percent = (survived / total * 100) if total else 0
        print(f"💡 {gender.capitalize()} survival rate: {percent:.2f}%")

    # Example 5: minors who survived
    minor_survivors = app.getGenericData({
        "age": lambda age: age is not None and int(age) < 18,
        "survived": lambda s: int(s) == 1
    })
    print("✅ Minors who survived:", len(minor_survivors))

    app.run()  # Uncomment to use the interactive ticket system
