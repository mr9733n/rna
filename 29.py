import sys
import numpy as np
from datetime import date

config = {
    'first_number': 1,
    'last_number': 18,
    'numbers_to_select': 3,
    'simulation_runs': 10000000
}

def run_simulation(config):
    sys.stdout.write('\rStarting..\n')
    total_runs = config['simulation_runs']
    all_numbers = np.arange(config['first_number'], config['last_number'] + 1)
    
    sys.stdout.write('\rGenerating Results..\n')
    results = np.random.choice(all_numbers, size=(total_runs, config['numbers_to_select'])).flatten()
    
    sys.stdout.write('\rResults generated.\n')  

    return results

def analyze_results(results, config):
    total_runs = config['simulation_runs']
    unique, counts = np.unique(results, return_counts=True)
    frequencies = counts / (total_runs * config['numbers_to_select']) * 100
    sys.stdout.write('\rAnalyzing results..\n')
    
    analysis = {
        'frequency': dict(zip(unique, frequencies)),
        'top': unique[np.argsort(-counts)[:config['numbers_to_select']]],
        'missing_numbers': [number for number in range(config['first_number'], config['last_number'] + 1) if number not in unique]
    }

    return analysis

def save_to_file(analysis, config):
    today = date.today().strftime("%Y-%m-%d")
    filename = f"simulation_results_{today}.txt"
    
    with open(filename, "w") as file:
        file.write("***Application: Random Number Analysis***\n")
        file.write(f"Configuration: {config}\n\n")
        file.write("Simulation Results:\n\n")
        file.write("Analysis of rolled numbers:\n")
        for number, percentage in analysis['frequency'].items():
            file.write(f"Number {number}: {percentage:.8f}%\n")
        
        file.write("\nTop most frequently rolled numbers:\n")
        file.write(f"Copy: {analysis['top'].tolist()}\n")
        for number in analysis['top']:
            file.write(f"Number {number}: {analysis['frequency'][number]:.8f}%\n")
        
        file.write("\nNumbers that did not roll:\n")
        if analysis['missing_numbers']:
            for number in analysis['missing_numbers']:
                file.write(f"{number}\n")
        else:
            file.write("All numbers rolled at least once.\n")

def display_results(analysis):
    today = date.today().strftime("%Y-%m-%d")
    print(f"\nCopy {analysis['top'].tolist()} most frequently rolled numbers:")
    
    for number in analysis['top']:
        print(f"Number {number}: {analysis['frequency'][number]:.8f}%")

    if analysis['missing_numbers']:
        print("\nNumbers that did not roll:")
        for number in analysis['missing_numbers']:
            print(number)
    else:
        print("\nAll numbers rolled at least once.")
    print(f"simulation_results_{today}.txt")

def main(config):
    results = run_simulation(config)
    analysis = analyze_results(results, config)
    save_to_file(analysis, config)
    display_results(analysis)

main(config)

