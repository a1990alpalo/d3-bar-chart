import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    PROJECT_ROOT.parent
    / "Data_Project_1"
    / "data"
    / "processed"
    / "nypd_arrests_clean.csv"
)
OUTPUT = PROJECT_ROOT / "data" / "nypd_arrests_by_borough.csv"


def count_arrests(source):
    counts = Counter()
    total = 0

    with source.open(newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            borough = row["borough"].strip() or "UNKNOWN"
            offense_level = row["offense_level"].strip() or "UNKNOW"
            counts[(borough,offense_level)] += 1
            total += 1

    return counts, total

def export_counts(counts, output):
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["borough", "offense_level", "arrest_count"])

        for (borough, offense_level), count in sorted(counts.items()):
            writer.writerow([borough, offense_level, count])

def main():
    counts, total = count_arrests(SOURCE)

    if sum(counts.values()) != total:
        raise ValueError ("Aggregated counts do not match the source total.")

    export_counts(counts, OUTPUT)
    print(f"Source records: {total:,}")
    print(f"Exported groups: {len(counts)}")
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()