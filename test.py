import csv


if __name__ == "__main__":
    with open("results/char_counts.csv", 'r', newline='', encoding='utf-8') as f:
        writer = csv.reader(f,delimiter="\t")
        for row in writer:
            print(row)
