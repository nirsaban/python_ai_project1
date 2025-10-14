class CardBuilder:
    @staticmethod
    def build_ticket(name, age, sex, fare, pclass, ticket_num, survival_chance,ai_tip):
        death_chance = 100 - survival_chance
        return (
            f"🎫 TITANIC TICKET\n"
            f"-----------------------------\n"
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Sex: {sex}\n"
            f"Class: {pclass}\n"
            f"Fare: ${fare:.2f}\n"
            f"Ticket Number: {ticket_num}\n"
            f"-----------------------------\n"
            f"Dear {name}, your chances to die on our trip are {death_chance:.1f}%.\n"
            f"Gemini tip {ai_tip}.\n"
            f"Enjoy your trip ☺\n"
        )
