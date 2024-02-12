
# Random Number Simulation Analysis

## Overview
This Python script conducts a simulation of randomly selecting numbers from a defined range, analyzes the frequency of each number being selected, identifies the top three most frequently selected numbers, and checks for any numbers that were never selected.

## Configuration
The script uses a configuration dictionary to define key parameters of the simulation:
- `first_number`: The first number in the sequence (default 1).
- `last_number`: The last number in the sequence (default 18).
- `numbers_to_select`: How many numbers to select in each draw (default 3).
- `simulation_runs`: Number of times to run the simulation (default 10,000,000).

## Functions
- `run_simulation(config)`: Runs the simulation according to the specified configuration.
- `analyze_results(results, config)`: Analyzes the results of the simulation.
- `save_to_file(analysis, total_runs)`: Saves the analysis results to a file.
- `display_results(analysis)`: Displays the results of the analysis in the console.
- `main(config)`: The main function that orchestrates the simulation, analysis, and display of results.

## Usage
To run the simulation with the default configuration, simply execute the script. Modify the `config` dictionary in the script to change the simulation parameters.

## Output
The script outputs the analysis to the console and saves a detailed report in a text file named `simulation_results_<date>.txt`.
