import json
import numpy as np
import yaml
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'data', path)
    
class RandomNames:
    def __init__(self):        
        self.prob_matrices = {}

    def generate_from_config_file(self, file=None):
        returns = {}
        with open(file if file is not None else get_data("config.yml")) as f:
            config = yaml.load(f)
            for key,value in config.items():
                if file is None:
                    value = [get_data(x) for x in value]
                unique_letters, initial_prob_matrix, transition_prob_matrix = RandomNames._generate_prob(value)
                returns[key] = {"unique_letters":unique_letters,\
                                "initial_prob_matrix":initial_prob_matrix,\
                                "transition_prob_matrix":transition_prob_matrix}
        self.prob_matrices = returns
    
    def load_from_json(self,file):
        with open(file) as f:
            self.prob_matrices = json.load(f)

    def write_to_json(self,file):
        with open(file,"w") as f:
            json.dump(self.prob_matrices,f)

    def generate_random_name(self,name_type, length, init = ""):
        if name_type not in self.prob_matrices.keys():
            raise KeyError("name_type %s not in prob_matrices"%(name_type,))
        if type(length) != int:
            raise TypeError("lenght must be integer")
        if length <= 0:
            raise ValueError("length must be greater than 0")
        
        if init != "":
            ret_string = init.lower()
        else:
            ret_string = np.random.choice(self.prob_matrices[name_type]["unique_letters"],\
                                p=self.prob_matrices[name_type]["initial_prob_matrix"])
        
        for _ in range(len(init),length):
            ret_string += np.random.choice(self.prob_matrices[name_type]["unique_letters"],\
                                p=self.prob_matrices[name_type]["transition_prob_matrix"]\
                                    [self.prob_matrices[name_type]["unique_letters"].index(ret_string[-1])])
        return ret_string.capitalize()
        
    
    

    @staticmethod
    def _generate_prob(files):
        transition_prob = {}
        initial_prob = {}
        unique_letters = set()

        for file in files:
            with open(file,encoding="utf-8") as f:
                data = json.load(f)
                for name in data:
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
        transition_prob_matrix = (transition_prob_matrix.T/transition_prob_matrix.sum(axis=1)).T
        return unique_letters, initial_prob_matrix.tolist(), transition_prob_matrix.tolist()

