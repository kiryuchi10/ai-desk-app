# modules/user_interaction.py

def get_extraction_mode():
    print("Select extraction mode:")
    print("1. OCR only")
    print("2. Table detection only")
    print("3. Hybrid (table + OCR)")
    choice = input("Enter choice (1/2/3): ").strip()
    if choice == "1":
        return "ocr"
    elif choice == "2":
        return "table"
    elif choice == "3":
        return "hybrid"
    else:
        print("Invalid choice. Defaulting to OCR.")
        return "ocr"

def confirm_preview():
    confirm = input("Is the table preview correct? (y/n): ").strip().lower()
    return confirm == "y"
