# readability.py
# compute Coleman-Liau index

def main():
    text = input("Text: ")

    letters = sum(1 for c in text if c.isalpha())
    words = len(text.split())
    sentences = sum(1 for c in text if c in ".!?")

    L = (letters / words) * 100
    S = (sentences / words) * 100

    grade = round(0.0588 * L - 0.296 * S - 15.8)

    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")

if __name__ == "__main__":
    main()
