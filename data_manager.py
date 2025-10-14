# data_manager.py
import csv
import random

class DataManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = self.load_data()
        self.class_ranges = self._compute_class_ranges()
        self.min_fare, self.max_fare = self._get_min_max_fares()
        self.existing_tickets = set()

    def load_data(self):
        data = []
        with open(self.data_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    fare = float(row["Fare"]) if row["Fare"] else 0.0
                    pclass = int(row["Pclass"]) if row["Pclass"] else None
                    survived = int(row["Survived"]) if row["Survived"] else None
                    sex = row["Sex"].strip().lower() if row["Sex"] else None
                    if pclass and sex:
                        data.append({
                            "fare": fare,
                            "pclass": pclass,
                            "sex": sex,
                            "survived": survived
                        })
                except Exception:
                    continue
        return data

    def _get_min_max_fares(self):
        fares = [d["fare"] for d in self.data if d["fare"] > 0]
        return min(fares), max(fares)

    def _compute_class_ranges(self):
        class_ranges = {}
        for cls in [1, 2, 3]:
            fares = [d["fare"] for d in self.data if d["pclass"] == cls and d["fare"] > 0]
            if fares:
                class_ranges[cls] = (min(fares), max(fares))
        return class_ranges

    def determine_class(self, fare: float):
        for cls, (low, high) in sorted(self.class_ranges.items()):
            if low <= fare <= high:
                return cls
        return 3  # default lowest class

    def calculate_survival_chance(self, sex: str, pclass: int):
        group = [d for d in self.data if d["sex"] == sex and d["pclass"] == pclass]
        if not group:
            return 0.0
        survived = sum(d["survived"] for d in group)
        return round((survived / len(group)) * 100, 1)

    def generate_ticket_number(self):
        while True:
            ticket = random.randint(100000, 999999)
            if ticket not in self.existing_tickets:
                self.existing_tickets.add(ticket)
                return ticket
