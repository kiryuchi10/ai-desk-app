# main.py
from modules.preview import generate_preview
from modules.user_interaction import ask_mode, confirm_preview
from modules.extractor import extract_by_mode
from modules.logger import log_feedback

def main():
    file_path = input("Enter full path to the PDF file: ").strip()
    mode = ask_mode()

    # Preview the table layout or OCR output
    preview_success = generate_preview(file_path, mode)

    if not preview_success or not confirm_preview():
        print("[INFO] User rejected preview or no valid preview. Aborting.")
        return

    result = extract_by_mode(file_path, mode)
    print("[RESULT] Extraction Complete\n", result)

    log_feedback(file_path, mode, success=True)

if __name__ == "__main__":
    main()
