class FileManagement:
    @staticmethod
    def save_ticket(name: str, content: str):
        file_name = f"ticket_{name.replace(' ', '_')}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n✅ Ticket saved as {file_name}\n")