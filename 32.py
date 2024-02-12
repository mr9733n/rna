from flask import Flask, render_template, request
from datetime import date
import numpy as np
import sys

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    default_first_number = config['first_number']
    default_last_number = config['last_number']
    default_numbers_to_select = config['numbers_to_select']
    default_simulation_runs = config['simulation_runs']
    
    if request.method == 'POST':
        results = run_simulation(config)
        analysis = analyze_results(results, config)
        # save_to_file(analysis, config)
        return render_template('index.html', analysis=analysis, 
                               default_first_number=default_first_number, 
                               default_last_number=default_last_number, 
                               default_numbers_to_select=default_numbers_to_select, 
                               default_simulation_runs=default_simulation_runs)
    return render_template('index.html', 
                           default_first_number=default_first_number, 
                           default_last_number=default_last_number, 
                           default_numbers_to_select=default_numbers_to_select, 
                           default_simulation_runs=default_simulation_runs)

if __name__ == '__main__':
    app.run(debug=True)
