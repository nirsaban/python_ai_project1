# main.py
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
        ai_prompt = self.gemini_assistant.build_gemini_prompt(name,age,sex,fare,survival_chance)
        ai_tip = self.gemini_assistant.ask_gemini(ai_prompt)
        # Build and save ticket

        ticket_text = self.builder.build_ticket(name, age, sex, fare, pclass, ticket_num, survival_chance,ai_tip)
        print(ticket_text)
        self.file_manager.save_ticket(name, ticket_text)


if __name__ == "__main__":
    app = TitanicApp("data.csv")
    app.run()
