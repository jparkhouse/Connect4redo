import numpy as np
from copy import deepcopy as dc


def sigmoid(x):
    return np.power(1 + np.exp(-x), -1)


def it(x):
    return range(len(x))


def getnumber(x):
    lx = [s for s in x]
    for i in it(lx):
        if not lx[i].isnumeric():
            lx[i] = ""
    return int("".join(lx))


def getmutate(evolution_factor):
    if np.random.random() > sigmoid(abs(1/evolution_factor)):
        return np.random.choice([1,-1])*np.random.random()*(np.log(6-evolution_factor)/np.log(10))
    else:
        return 0


class Layer(object):
    def __init__(self, weights, length, previous_length, bias):
        if weights == "r":
            self.weights = np.random.random((previous_length, length))-0.5
            # print(self.weights)
            self.bias = np.random.random((1, length))-0.5
            # print(self.bias)
        else:
            self.weights = weights
            self.bias = bias
        self.length = length
        self.previous_length = previous_length

    def retval(self, input):
        return np.matmul(input, self.weights) + self.bias

    def getLength(self):
        return self.length

    def export(self):
        weights = []
        i, j = self.weights.shape
        for x in range(i):
            temp = []
            for y in range(j):
                temp.append(str(self.weights[x][y]))
            weights.append(",".join(temp))
        weights = "/".join(weights)
        bias = []
        i, j = self.bias.shape
        for x in range(i):
            temp = []
            for y in range(j):
                temp.append(str(self.bias[x][y]))
            bias.append(dc(temp))
        for i in range(len(bias)):
            bias[i] = ",".join(bias[i])
        return weights+"//"+bias[0]


class Network(object):
    def __init__(self, mode, layers, weights=None, biases=None):
        '''
        '''
        self.layers = layers
        self.layer_list = []
        if mode != "r":
            for i in it(layers):
                if i > 0:
                    self.layer_list.append(Layer(weights[i-1], layers[i],
                                                 layers[i-1], biases[i-1]))
        else:
            for i in it(layers):
                if i > 0:
                    self.layer_list.append(Layer("r", layers[i],
                                                 layers[i-1], None))

    def retval(self, input):
        count = dc(input)
        for i in self.layer_list:
            count = dc(i.retval(count))
        return sigmoid(count)

    def export(self):
        lengths = ",".join([str(i) for i in self.layers])
        details = []
        for each in self.layer_list:
            details.append(each.export())
        details = lengths+";\n"+";\n".join(details)
        return details


class NetworkGeneration(object):
    def __init__(self, mode, lengths=None, file_name=None, generation_size=50):
        if mode == "r":
            self.generation_size = generation_size
            self.network_list = []
            self.generation_number = 0
            for i in range(self.generation_size):
                self.network_list.append(Network("r", lengths))
            print("Successfully generated")
        elif mode == "f":
            self.network_list = []
            with open(file_name, "r") as txt:
                data = txt.read().split("!n\n")
            self.generation_size = len(data)
            for i in it(data):
                networkdata = data[i].split(";\n")
                if i < 1:
                    layers = [int(x) for x in networkdata[0].split("\n")[1].split(",")]
                    self.generation_number = getnumber(networkdata[0].split("\n")[0])
                else:
                    layers = [int(x) for x in networkdata[0].split(",")]
                network = networkdata[1:]
                weightlist, biaslist = [], []
                for j in it(network):
                    weights, bias = network[j].split("//")
                    weights = weights.split("/")
                    for k in it(weights):
                        weights[k] = [float(x) for x in weights[k].split(",")]
                    weightlist.append(np.array(weights))
                    bias = bias.split(",")
                    for k in it(bias):
                        bias[k] = float(bias[k])
                    biaslist.append(np.transpose(np.array([bias])))
                self.network_list.append(Network("f", layers, weightlist,
                                                 biaslist))
            print("Successfully loaded")

    def export(self):
        data = []
        for i in range(self.generation_size):
            data.append(self.network_list[i].export())
        data = ("generation {0}\n".format(self.generation_number) +
                "\n".join(data))
        with open("generation{0}.txt".format(self.generation_number), "w") as txtfile:
            txtfile.write(data)

    def evolve(self, scores, evolution_factor=1):
        if self.generation_number % 10 == 0:
            self.export()
        parents = [j[0] for j in
                   sorted([[self.network_list[i], scores[i]]
                          for i in it(scores)], key=lambda x: x[1],
                          reverse=True)][0:int(np.floor(0.20 *
                                                        self.generation_size))]
        nextgeneration = [i for i in parents]
        print(parents)
        while len(nextgeneration) < 0.6*self.generation_size:
            parent = [np.random.choice(parents).export(),
                      np.random.choice(parents).export()]
            while parent[0] == parent[1]:
                parent[1] = np.random.choice(parents).export()
            for i in it(parent):  # convert network into a workable list of
                # arrays
                parent[i] = parent[i].split(";\n")
                temp = [[], [], []]
                temp[0] = [int(x) for x in parent[i][0].split(",")]
                for j in it(parent[i]):
                    if j < 1:
                        pass
                    else:
                        weights, bias = parent[i][j].split("//")
                        weights = weights.split("/")
                        for k in it(weights):
                            weights[k] = [float(x)
                                          for x in weights[k].split(",")]
                        temp[1].append(np.array(weights))
                        bias = bias.split(",")
                        bias = [float(k) for k in bias]
                        temp[2].append(bias)
                parent[i] = dc(temp)
            child = [[], [], []]
            child[0] = parent[0][0]
            for i in range(len(child[0])-1):
                weights = np.zeros((child[0][i], child[0][i+1]))
                bias = np.zeros((1, child[0][i+1]))
                for j in range(child[0][i + 1]):
                    for k in range(child[0][i]):
                        weights[k][j] = np.random.choice([parent[0][1][i][k][j], parent[1][1][i][k][j]]) + getmutate(evolution_factor)
                    bias[0][j] = np.random.choice([parent[0][2][i][j], parent[1][2][i][j]]) + getmutate(evolution_factor)
                child[1].append(weights)
                child[2].append(bias)
            nextgeneration.append(Network("f", child[0], child[1], child[2]))
        while len(nextgeneration) < 0.8*self.generation_size:
            child = np.random.choice(self.network_list)
            while child in parents or child in nextgeneration:
                child = np.random.choice(self.network_list)
            nextgeneration.append(child)
        while len(nextgeneration) < self.generation_size:
            nextgeneration.append(Network("r", parent[0][0]))
        np.random.shuffle(nextgeneration)
        self.network_list = dc(nextgeneration)
        self.generation_number += 1
