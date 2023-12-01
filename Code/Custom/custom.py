import csv
import random
from flask import Flask, jsonify, render_template, request
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


organism_data = {'custom': {}}


def is_valid_dna(sequence):
    valid_nucleotides = set("ATCG")


    # Check if all characters in the sequence are valid nucleotides
    return all(char in valid_nucleotides for char in sequence)


def calculate_cai(sequence, codon_usage):
    codon_counts = {}
    total_codons = 0
    for i in range(0, len(sequence), 3):
        codon = sequence[i:i + 3]
        codon_counts[codon] = codon_counts.get(codon, 0) + 1


        total_codons += 1


    cai = 1.0


    for codon, count in codon_counts.items():
        if codon in codon_usage:
            cai *= (codon_usage[codon] ** count)


    cai = cai ** (1 / total_codons)
    return cai


def random_mutation(sequence, codon_usage):
    position_to_mutate = random.randint(0, len(sequence) - 3)
    new_sequence = list(sequence)
    new_codon = random.choice(list(codon_usage.keys()))
    new_sequence[position_to_mutate:position_to_mutate + 3] = list(new_codon)
    return ''.join(new_sequence)


def crossover(parent1, parent2):
    crossover_points = sorted(random.sample(range(len(parent1)), 2))
    child1 = parent1[:crossover_points[0]] + parent2[crossover_points[0]:crossover_points[1]] + parent1[crossover_points[1]:]
    child2 = parent2[:crossover_points[0]] + parent1[crossover_points[0]:crossover_points[1]] + parent2[crossover_points[1]:]


    return child1, child2


def optimize_codon_sequence(target_cai, current_sequence, codon_usage, max_iterations=10000, mutation_rate=0.1):
    current_cai = calculate_cai(current_sequence, codon_usage)
    best_sequence = current_sequence
    best_cai = current_cai


    for iteration in range(max_iterations):
        mutated_sequence = random_mutation(best_sequence, codon_usage)
        mutated_cai = calculate_cai(mutated_sequence, codon_usage)


        crossovered_sequence1, crossovered_sequence2 = crossover(best_sequence, mutated_sequence)
        crossovered_cai1 = calculate_cai(crossovered_sequence1, codon_usage)
        crossovered_cai2 = calculate_cai(crossovered_sequence2, codon_usage)


        if mutated_cai < best_cai:
            best_sequence = mutated_sequence
            best_cai = mutated_cai
        elif crossovered_cai1 < best_cai:
            best_sequence = crossovered_sequence1
            best_cai = crossovered_cai1
        elif crossovered_cai2 < best_cai:
            best_sequence = crossovered_sequence2
            best_cai = crossovered_cai2


        if abs(best_cai - target_cai) < 0.001:
            break


    return best_sequence, best_cai


@app.route('/', methods=['GET', 'POST'])
def custom():
    codon_data = []
    if request.method == 'POST':
        file = request.files['codon_file']
       
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)


            with open(filepath, 'r') as file:
                csv_reader = csv.DictReader(file)
                codon_data = [row for row in csv_reader]


        if codon_data:
            codon_usage = codon_data[0]
            codon_usage = {key: float(value) for key, value in codon_usage.items()}


        target_cai = float(request.form['target_cai'])
        default_cai_range = request.form['default_cai_range']


        sequence = request.form['sequence']
        sequence = sequence.strip()
        sequence = ''.join(sequence.split())


        if is_valid_dna(sequence):
            optimized_sequence, optimized_cai = optimize_codon_sequence(target_cai, sequence, codon_usage)
            return jsonify({'status': 'success', 'optimized_sequence': optimized_sequence, 'optimized_cai': optimized_cai})
        else:
            return jsonify({'status': 'error', 'message': 'Not a Proper Sequence'})


    return render_template('custom.html')
