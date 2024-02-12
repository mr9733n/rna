from flask import Flask, render_template, request
import numpy as np
from datetime import date

app = Flask(__name__)

config = {
    'first_number': 1,
    'last_number': 18,
    'numbers_to_select': 3,
    'simulation_runs': 10000000
}

def run_simulation(config):
    total_runs = config['simulation_runs']
    all_numbers = np.arange(config['first_number'], config['last_number'] + 1)
    results = np.random.choice(all_numbers, size=(total_runs, config['numbers_to_select'])).flatten()
    return results

def analyze_results(results, config):
    total_runs = config['simulation_runs']
    unique, counts = np.unique(results, return_counts=True)
    frequencies = counts / (total_runs * config['numbers_to_select']) * 100
    
    analysis = {
        'frequency': dict(zip(unique, frequencies)),
        'top': unique[np.argsort(-counts)[:config['numbers_to_select']]],
        'missing_numbers': [number for number in range(config['first_number'], config['last_number'] + 1) if number not in unique]
    }

    return analysis

@app.route('/', methods=['GET', 'POST'])
def index():
    default_first_number = config['first_number']
    default_last_number = config['last_number']
    default_numbers_to_select = config['numbers_to_select']
    default_simulation_runs = config['simulation_runs']
    
    if request.method == 'POST':
        user_input = {}
        
        user_input['first_number'] = int(request.form.get('first_number', default_first_number))
        user_input['last_number'] = int(request.form.get('last_number', default_last_number))
        user_input['numbers_to_select'] = int(request.form.get('numbers_to_select', default_numbers_to_select))
        user_input['simulation_runs'] = int(request.form.get('simulation_runs', default_simulation_runs))
        
        results = run_simulation(user_input)
        analysis = analyze_results(results, user_input)
        # save_to_file(analysis, user_input)
        
        return render_template('index.html', analysis=analysis, 
                               default_first_number=user_input['first_number'], 
                               default_last_number=user_input['last_number'], 
                               default_numbers_to_select=user_input['numbers_to_select'], 
                               default_simulation_runs=user_input['simulation_runs'])
    
    return render_template('index.html', 
                           default_first_number=default_first_number, 
                           default_last_number=default_last_number, 
                           default_numbers_to_select=default_numbers_to_select, 
                           default_simulation_runs=default_simulation_runs)

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

if __name__ == '__main__':
    app.run(debug=True)
