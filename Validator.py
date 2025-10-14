# Validator.py
class Validator:
    @staticmethod
    def clean_name(name: str) -> str:
        return name.strip().title()

    @staticmethod
    def validate_age(age: str) -> float:
        while True:
            try:
                age = float(age)
                if 0 <= age <= 130:
                    return age
                else:
                    age = input("❌ Age must be between 0 and 130: ")
            except ValueError:
                age = input("❌ Invalid input. Enter age again: ")

    @staticmethod
    def validate_sex(sex: str) -> str:
        while True:
            sex = sex.strip().lower()
            if sex in ["male", "female"]:
                return sex
            sex = input("❌ Invalid sex. Enter 'male' or 'female': ")

    @staticmethod
    def validate_fare(fare: str, min_fare: float, max_fare: float) -> float:
        while True:
            try:
                fare = float(fare)
                if min_fare <= fare <= max_fare:
                    return fare
                else:
                    fare = input(f"❌ Fare must be between {min_fare:.2f} and {max_fare:.2f}: ")
            except ValueError:
                fare = input("❌ Invalid number. Enter fare again: ")
