import random
from flask import Flask, render_template, request


app = Flask(__name__)


organism_data = {
    'custom': {
        'codon_usage': {
            # Add your custom codon usage here
        },
        'target_cai': 0.9,
        'default_cai_range': (0.8, 0.9)
    },
    'human': {
        #Homo Sapiens
    'codon_usage': {
        'UUU':17.6, 'UCU':15.2,'UAU':12.2, 'UGU':10.6,
        'UUC':20.3, 'UCC':17.7, 'UAC':15.3, 'UGC':12.6,
        'UUA':7.7, 'UCA':12.2, 'UAA':1.0, 'UGA':1.6,
        'UUG':12.9, 'UCG':4.4, 'UAG':0.8, 'UGG':13.2,
       
        'CUU':13.2, 'CCU':17.5, 'CAU':10.9, 'CGU':4.5,
        'CUC':19.6, 'CCC':19.8, 'CAC':15.1, 'CGC':10.4,
        'CUA':7.2, 'CCA':16.9, 'CAA':12.3, 'CGA':6.2,
        'CUG':39.6, 'CCG':6.9, 'CAG':34.2, 'CGG':11.4,
       
        'AUU':16.0, 'ACU':13.1, 'AAU':17.0, 'AGU':12.1,
        'AUC':20.8, 'ACC':18.9, 'AAC':19.1, 'AGC':19.5,
        'AUA':7.5, 'ACA':15.1, 'AAA':24.4, 'AGA':12.2,
        'AUG':22.0, 'ACG':6.1, 'AAG':31.9, 'AGG':12.0,
       
        'GUU':11.0, 'GCU':18.4, 'GAU':21.8, 'GGU':10.8,
        'GUC':14.5, 'GCC':27.7, 'GAC':25.1, 'GGC':22.2,
        'GUA':7.1, 'GCA':15.8, 'GAA':29.0, 'GGA':16.5,
        'GUG':28.1, 'GCG':7.4, 'GAG':39.6, 'GGG':16.5,},


    'target_cai': 0.9,
    'default_cai_range': (0.8, 1.0)
    },
    'wolf': {
        #Canis lupus
    'codon_usage': {
        'UUU': 7.4, 'UCU': 8.1, 'UAU': 9.6, 'UGU': 8.9,
        'UUC':29.2, 'UCC':19.9, 'UAC':16.2, 'UGC':14.0,
        'UUA': 3.0, 'UCA': 6.6, 'UAA': 0.7, 'UGA': 3.0,
        'UUG': 7.0, 'UCG': 2.2, 'UAG': 0.4, 'UGG':15.5,


        'CUU': 8.5, 'CCU':11.8, 'CAU': 7.4, 'CGU': 4.8,
        'CUC':28.4, 'CCC':26.2, 'CAC':23.6, 'CGC':16.6,
        'CUA': 5.2, 'CCA':11.8, 'CAA': 9.6, 'CGA': 4.8,
        'CUG':57.6, 'CCG': 6.6, 'CAG':39.5, 'CGG':13.3,


        'AUU':11.4, 'ACU': 7.0, 'AAU':11.8, 'AGU': 6.3,
        'AUC':26.2, 'ACC':24.0, 'AAC':26.2, 'AGC':16.2,
        'AUA': 7.0, 'ACA':14.4, 'AAA':19.9, 'AGA': 8.1,
        'AUG':28.8, 'ACG': 5.2, 'AAG':40.2, 'AGG': 8.9,


        'GUU': 3.7, 'GCU':13.7, 'GAU':15.9, 'GGU':11.8,
        'GUC':17.3, 'GCC':33.2, 'GAC':34.7, 'GGC':36.9,
        'GUA': 6.3, 'GCA': 9.6, 'GAA':17.7, 'GGA': 7.0,
        'GUG':37.6, 'GCG': 6.3, 'GAG':43.5, 'GGG':15.9},
       
    'target_cai': 0.4,
    'default_cai_range': (0.4, 0.6)


    },
    'cow': {
        #Entamoeba histolytica
    'codon_usage': {
        'UUU':16.4, 'UCU':13.1, 'UAU':11.4, 'UGU': 9.3,
        'UUC':22.3, 'UCC':17.3, 'UAC':17.5, 'UGC':12.6,
        'UUA': 6.3, 'UCA': 9.9, 'UAA': 0.7, 'UGA': 1.3,
        'UUG':12.0, 'UCG': 5.0, 'UAG': 0.6, 'UGG':13.5,


        'CUU':11.9, 'CCU':15.8, 'CAU': 9.4, 'CGU': 4.6,
        'CUC':21.2, 'CCC':20.4, 'CAC':15.5, 'CGC':11.1,
        'CUA': 6.1, 'CCA':14.6, 'CAA':10.5, 'CGA': 6.4,
        'CUG':43.5, 'CCG': 7.8, 'CAG':35.0, 'CGG':12.5,


        'AUU':14.6, 'ACU':11.5, 'AAU':14.7, 'AGU':11.0,
        'AUC':23.3, 'ACC':20.1, 'AAC':21.4, 'AGC':19.3,
        'AUA': 6.7, 'ACA':13.0, 'AAA':22.4, 'AGA':10.7,
        'AUG':22.5, 'ACG': 7.2, 'AAG':34.7, 'AGG':11.4,


        'GUU':10.1, 'GCU':17.9, 'GAU':20.5, 'GGU':10.8,
        'GUC':15.9, 'GCC':30.5, 'GAC':28.2, 'GGC':24.4,
        'GUA': 6.3, 'GCA':14.3, 'GAA':26.9, 'GGA':16.2,
        'GUG':30.8, 'GCG': 8.6, 'GAG':41.9, 'GGG':16.8},
   
    'target_cai': 0.6,
    'default_cai_range': (0.6, 0.8)


    },
   
    'mushroom': {
        #Agaricus bisporus
    'codon_usage': {
        'UUU':14.0, 'UCU':17.8, 'UAU':13.0, 'UGU':6.8,
        'UUC':27.4, 'UCC':14.3, 'UAC':16.1, 'UGC':9.3,
        'UUA': 4.4, 'UCA':9.8, 'UAA':1.1, 'UGA':1.0,
        'UUG':15.2, 'UCG':10.5, 'UAG':0.8, 'UGG':14.8,


        'CUU':19.8, 'CCU': 19.3, 'CAU':12.1, 'CGU':11.2,
        'CUC':26.6, 'CCC':16.5, 'CAC':11.1, 'CGC':9.2,
        'CUA':5.8, 'CCA':9.0, 'CAA':20.5, 'CGA':6.3,
        'CUG':9.5, 'CCG':8.0, 'CAG':14.5, 'CGG':4.0,


        'AUU':22.9, 'ACU':21.0, 'AAU':21.3, 'AGU':10.3,
        'AUC':28.4, 'ACC':21.7, 'AAC':28.1, 'AGC':11.2,
        'AUA':5.6, 'ACA':11.5, 'AAA':21.0, 'AGA':5.1,
        'AUG':18.4, 'ACG':9.2, 'AAG':26.9, 'AGG':6.9,


        'GUU':23.6, 'GCU':32.2, 'GAU':30.5, 'GGU':32.4,
        'GUC':31.0, 'GCC':25.7, 'GAC':25.0, 'GGC':26.4,
        'GUA':7.3, 'GCA':16.8, 'GAA':26.5, 'GGA':21.5,
        'GUG':9.7, 'GCG':11.6, 'GAG':22.7, 'GGG':8.1},
   
    'target_cai': 0.9,
    'default_cai_range': (0.8, 1.0)


    },
    'gorilla': {
        #Agaricus bisporus
    'codon_usage': {
        'UUU':17.5, 'UCU':16.2, 'UAU':14.0, 'UGU':11.2,
        'UUC':23.9, 'UCC':17.0,  'UAC':17.0, 'UGC':13.5,
        'UUA':7.6, 'UCA':11.2,  'UAA':0.9,  'UGA':1.8,
        'UUG':13.2, 'UCG':3.4,  'UAG':0.7,  'UGG':15.6,




        'CUU': 13.2, 'CCU':15.8, 'CAU':11.9, 'CGU':4.8,
        'CUC':22.3,  'CCC':18.8, 'CAC':16.2, 'CGC':10.9,
        'CUA': 7.8,  'CCA':14.4, 'CAA':14.5, 'CGA': 5.7,
        'CUG':43.2,  'CCG': 6.5, 'CAG':37.5, 'CGG': 9.7,




        'AUU':16.9,  'ACU':13.5, 'AAU':16.1, 'AGU':10.6,
        'AUC':22.9,  'ACC':20.8, 'AAC':18.7, 'AGC':17.5,
        'AUA': 8.9,  'ACA':15.3, 'AAA':23.6, 'AGA':14.9,
        'AUG':22.9,  'ACG': 5.8, 'AAG':29.3, 'AGG':12.9,




        'GUU':12.1,  'GCU':18.9, 'GAU':16.6, 'GGU': 9.4,
        'GUC':15.2,  'GCC':26.8, 'GAC':22.2, 'GGC':19.4,
        'GUA': 6.9,  'GCA':14.7, 'GAA':22.9, 'GGA':15.2,
        'GUG':29.1,  'GCG': 7.6, 'GAG':36.9, 'GGG':17.4,},
   
    'target_cai': 0.8,
    'default_cai_range': (0.7, 0.9)


    }    
}
def is_valid_dna(sequence):
    valid_nucleotides = set("ATCGU")


    # Check if all characters in the sequence are valid nucleotides
    return all(char in valid_nucleotides for char in sequence)


def calculate_cai(sequence, codon_usage):
    codon_counts = {}
    total_codons = 0
    for i in range(0, len(sequence), 3):
        codon = sequence[i:i + 3]
        codon_counts[codon] = codon_counts.get(codon, 0) + 1

        total_codons += 1


    #print (codon_counts)
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
    # Perform a two-point crossover between two parents
    crossover_points = sorted(random.sample(range(len(parent1)), 2))
    child1 = parent1[:crossover_points[0]] + parent2[crossover_points[0]:crossover_points[1]] + parent1[crossover_points[1]:]
    child2 = parent2[:crossover_points[0]] + parent1[crossover_points[0]:crossover_points[1]] + parent2[crossover_points[1]:]


    return child1, child2


def optimize_codon_sequence(target_cai, current_sequence, codon_usage, max_iterations=10000, mutation_rate=0.1):
    current_cai = calculate_cai(current_sequence, codon_usage)
    best_sequence = current_sequence
    best_cai = current_cai


    for iteration in range(max_iterations):
        # Apply random mutation
        mutated_sequence = random_mutation(best_sequence, codon_usage)
        mutated_cai = calculate_cai(mutated_sequence, codon_usage)


        # Apply enhanced two-point crossover with the current best sequence
        crossovered_sequence1, crossovered_sequence2 = crossover(best_sequence, mutated_sequence)
        crossovered_cai1 = calculate_cai(crossovered_sequence1, codon_usage)
        crossovered_cai2 = calculate_cai(crossovered_sequence2, codon_usage)


        # Select the sequence with the lowest CAI among the three
        if mutated_cai < best_cai:
            best_sequence = mutated_sequence
            best_cai = mutated_cai
        elif crossovered_cai1 < best_cai:
            best_sequence = crossovered_sequence1
            best_cai = crossovered_cai1
        elif crossovered_cai2 < best_cai:
            best_sequence = crossovered_sequence2
            best_cai = crossovered_cai2


        # Check for convergence
        if abs(best_cai - target_cai) < 0.001:
            break
    return best_sequence


@app.route('/', methods=['GET', 'POST'])
def index():
    optimized_sequence = None
    optimized_cai = None
    default_cai_range = (0, 1)


    if request.method == 'POST':
        sequence = request.form['sequence']
        sequence = sequence.strip()
        sequence = ''.join(sequence.split())
        organism = request.form['organism']


        if is_valid_dna(sequence):
            # Get organism data from the dictionary
            organism_info = organism_data.get(organism, {})
            codon_usage = organism_info.get('codon_usage', {})
            target_cai = organism_info.get('target_cai', 0.0)
            default_cai_range=organism_info.get('default_cai_range',(0,1))
            optimized_sequence = optimize_codon_sequence(target_cai, sequence, codon_usage)
            optimized_cai = calculate_cai(optimized_sequence, codon_usage)
        else:
            optimized_sequence = "Not a Proper Sequence"
            optimized_cai = "Error"


    return render_template('optimize.html', optimized_sequence=optimized_sequence, optimized_cai=optimized_cai, default_target_cai=default_cai_range)
if __name__ == '__main__':
    app.run(debug=True, port=5011)




