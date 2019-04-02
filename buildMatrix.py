import json
import argparse
from tqdm import tqdm
import numpy as np
import yaml


    

def generate_prob(files):
    transition_prob = {}
    initial_prob = {}
    unique_letters = set()

    for file in files:
        print(file)
        with open(file,encoding="utf-8") as f:
            data = json.load(f)
            for name in tqdm(data):
                name = name.lower()
                try:
                    initial_prob[name[0]] += 1
                except:
                    initial_prob[name[0]] = 1
                for idx in range(1,len(name)):
                    if name[idx-1] not in transition_prob.keys():
                        transition_prob[name[idx-1]] = {}
                    if name[idx] not in transition_prob[name[idx-1]].keys():
                        transition_prob[name[idx-1]][name[idx]] = 0
                    transition_prob[name[idx-1]][name[idx]] += 1
    
    unique_letters = unique_letters.union(set(initial_prob.keys()))
    unique_letters = unique_letters.union(set(transition_prob.keys()))
    for key in transition_prob.keys():
        unique_letters = unique_letters.union(set(transition_prob[key].keys()))
    unique_letters = list(unique_letters)
    
    initial_prob_matrix = np.zeros(len(unique_letters))
    transition_prob_matrix = np.zeros((len(unique_letters),len(unique_letters)))
    for idx, char in enumerate(unique_letters):
        try:
            initial_prob_matrix[idx] = initial_prob[char]
        except:
            pass
        for idx2, char2 in enumerate(unique_letters):
            try:
                transition_prob_matrix[idx][idx2] = transition_prob[char][char2]
            except:
                pass
    initial_prob_matrix /= initial_prob_matrix.sum()
    initial_prob_matrix = initial_prob_matrix.cumsum().round(5)
    transition_prob_matrix = (transition_prob_matrix.T/transition_prob_matrix.sum(axis=1)).T.cumsum(axis=1).round(5)
    return unique_letters, initial_prob_matrix.tolist(), transition_prob_matrix.tolist()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file",help="YAML file used to create matrix")
    parser.add_argument("output", help="json file containing the matrices")
    args = parser.parse_args()
    returns = {}
    with open(args.config_file) as f:
        config = yaml.load(f)
        for key,value in config.items():
            unique_letters, initial_prob_matrix, transition_prob_matrix = generate_prob(value)
            returns[key] = {"unique_letters":unique_letters,\
                            "initial_prob_matrix":initial_prob_matrix,\
                            "transition_prob_matrix":transition_prob_matrix}
    with open(args.output,"w") as f:
        json.dump(returns, f)

    



    
