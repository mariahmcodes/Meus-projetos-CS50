def main():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
        except ValueError:
            continue

    for i in range(1, height + 1):
        spaces = " " * (height - i)
        blocks = "#" * i
        print(f"{spaces}{blocks}")

if __name__ == "__main__":
    main()
