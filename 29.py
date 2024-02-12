import random
from collections import Counter
import sys
from datetime import date

def run_simulation(runs):
    all_numbers = list(range(1, 19))
    results = []

    for i in range(runs):
        selected_numbers = random.sample(all_numbers, 3)
        results.extend(selected_numbers)
        
        # Print progress every 100,000 runs
        if (i + 1) % 100000 == 0:
            sys.stdout.write('\rProgress: {:.2f}%'.format((i + 1) / runs * 100))
            sys.stdout.flush()

    sys.stdout.write('\n')
    return results

def analyze_results(results):
    counts = Counter(results)
    total_runs = len(results)

    print("Analysis of rolled values:")
    for number in range(1, 19):
        percentage = counts[number] / total_runs * 100
        print(f"Number {number}: {percentage:.8f}%")

    return counts

def find_top_3(counts):
    print("\nTop 3 most frequently rolled numbers:")
    top_3 = counts.most_common(3)
    top_3_numbers = [number for number, count in top_3]
    print(f"Numbers: {top_3_numbers}")
    for number, count in top_3:
        print(f"Number {number}: {count} times")

def find_missing_numbers(counts):
    missing_numbers = [number for number, count in counts.items() if count == 0]
    if missing_numbers:
        print("\nNumbers that did not roll:")
        for number in missing_numbers:
            print(number)
    else:
        print("\nAll numbers rolled at least once.")

def save_to_file(counts, total_runs):
    today = date.today().strftime("%Y-%m-%d")
    filename = f"simulation_results_{today}.txt"
    with open(filename, "w") as file:
        file.write("***Application: Random Number Analysis***\n\n")
        file.write("Simulation Results:\n\n")
        file.write("Analysis of rolled numbers:\n")
        for number in range(1, 19):
            percentage = counts[number] / total_runs * 100
            file.write(f"Number {number}: {percentage:.8f}%\n")
        file.write("\nTop 3 most frequently rolled numbers:\n")
        top_3 = counts.most_common(3)
        numbers_to_copy = [number for number, _ in top_3]
        file.write(f"Numbers: {numbers_to_copy}\n")
        for number, count in top_3:
            file.write(f"Number {number}: {count} times\n")
        file.write("\nNumbers that did not roll:\n")
        missing_numbers = [number for number, count in counts.items() if count == 0]
        if missing_numbers:
            for number in missing_numbers:
                file.write(f"{number}\n")
        else:
            file.write("All numbers rolled at least once.\n")

def main(runs):
    results = run_simulation(runs)
    counts = analyze_results(results)
    save_to_file(counts, len(results))
    find_top_3(counts)
    find_missing_numbers(counts)

main(10000000)
