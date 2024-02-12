import random
from collections import Counter
import sys
from datetime import date

config = {
    'first_number': 1,     # First number in the sequence
    'last_number': 18,     # Last number in the sequence
    'numbers_to_select': 3,  # How many numbers to select in each draw
    'simulation_runs': 10000000  # Number of times to run the simulation
}

def run_simulation(config):
    all_numbers = list(range(config['first_number'], config['last_number'] + 1))
    results = []

    for i in range(config['simulation_runs']):
        selected_numbers = random.sample(all_numbers, config['numbers_to_select'])
        results.extend(selected_numbers)
        
        # Print progress every 100,000 runs
        if (i + 1) % 100000 == 0:
            sys.stdout.write('\rProgress: {:.2f}%'.format((i + 1) / config['simulation_runs'] * 100))
            sys.stdout.flush()

    sys.stdout.write('\n')
    return results

def analyze_results(results, config):
    counts = Counter(results)
    total_runs = len(results) / config['numbers_to_select']

    analysis = {
        'frequency': {},
        'top_3': [],
        'missing_numbers': []
    }

    print("Analysis of rolled values:")
    for number in range(config['first_number'], config['last_number'] + 1):
        percentage = counts[number] / total_runs * 100
        analysis['frequency'][number] = percentage
        print(f"Number {number}: {percentage:.8f}%")

    top_3 = counts.most_common(3)
    analysis['top_3'] = top_3

    missing_numbers = [number for number in range(config['first_number'], config['last_number'] + 1) if counts[number] == 0]
    analysis['missing_numbers'] = missing_numbers

    return analysis

def save_to_file(analysis, total_runs):
    today = date.today().strftime("%Y-%m-%d")
    filename = f"simulation_results_{today}.txt"
    
    with open(filename, "w") as file:
        file.write("***Application: Random Number Analysis***\n\n")
        file.write("Simulation Results:\n\n")
        file.write("Analysis of rolled numbers:\n")
        
        for number, percentage in analysis['frequency'].items():
            file.write(f"Number {number}: {percentage / total_runs * 100:.8f}%\n")
        
        file.write("\nTop 3 most frequently rolled numbers:\n")
        top_3_numbers = [number for number, _ in analysis['top_3']]
        file.write(f"Numbers: {top_3_numbers}\n")
        for number, count in analysis['top_3']:
            file.write(f"Number {number}: {count} times\n")
        
        file.write("\nNumbers that did not roll:\n")
        if analysis['missing_numbers']:
            for number in analysis['missing_numbers']:
                file.write(f"{number}\n")
        else:
            file.write("All numbers rolled at least once.\n")

def display_results(analysis):
    print("\nTop 3 most frequently rolled numbers:")
    for number, count in analysis['top_3']:
        print(f"Number {number}: {count} times")

    if analysis['missing_numbers']:
        print("\nNumbers that did not roll:")
        for number in analysis['missing_numbers']:
            print(number)
    else:
        print("\nAll numbers rolled at least once.")

def main(config):
    results = run_simulation(config)
    analysis = analyze_results(results, config)
    save_to_file(analysis, len(results))
    display_results(analysis)

main(config)
