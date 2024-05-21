import numpy as np
import random

from brain import Brain

neural_network = Brain

class Controller:
    def __init__(self, pop_size, select_perc, error_range, mutate) -> None:
        self.population = [Individual(neural_network()) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range
        self.mutate = mutate

    def evaluation():
        #fitness function
        pass

    def selection(self):
        self.population.sort(key=lambda s: s.score, reverse=True)
        selected = self.population[:int(self.select_perc * (len(self.population)))]
        return selected

    def reproduction(self, parent_1,parent_2):
        weights = []
        for i in range(len(parent_1.dna)):
            # for every layer average
            weights.append(np.mean(np.array([parent_1.dna[i], parent_2.dna[i]]), axis=0))
        child = Individual(neural_network(weights=weights))
        return child
    
    def crossover(self, selected):
        children = []
        # create couples that will give birth
        parent_1 = [selected[rand] for rand in
                    np.random.randint(len(selected), size=int(self.pop_size))]
        parent_2 = [selected[rand] for rand in np.random.randint(len(selected), size=int(self.pop_size))]
        for i in range(int(self.pop_size)):
            # Crossover
            child = self.birth(parent_1[i], parent_2[i])
            children.append(child)
        return children
    
    def mutation(self, children):
        for i in range(self.pop_size):
            if random.random() < self.mutate:
                weights = []
                #print("before mutation: ", children[i].dna)
                for j in range(len(children[i].dna)):
                    bias = np.random.uniform(-1,1, [children[i].dna[j].shape[0], children[i].dna[j].shape[1]])
                    bias = np.where(abs(bias) > 0.05, 0, bias)
                    weights.append(children[i].dna[j] + bias)
                    #print("bias term", bias)
                children[i].dna = weights
                print("after mutation: ", children[i].dna)
        return children
    
    def run(self):
        #life cycle

        selected = self.selection()
        #print("dna of first: ", selected[0].dna)
        children = self.crossover(selected)
        #print("dna of first after cross over: ", children[0].dna)
        children = self.mutation(children)
        #print("dna of first after mutation: ", children[0].dna)

        # keep the best the same
        children[0:2] = selected[0:2]
        self.population = children

        return self.population


class Individual():
    def __init__(self, NN):
        self.NN = NN
        self.dna = NN.weights # float number
        self.score = 0

    def update_score(self, score):
        self.score = score

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Robot score: ' + str(self.score)