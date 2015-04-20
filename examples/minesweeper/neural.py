
import math
import random

class Neuron(object):
    def __init__(self, n_inputs):
        self.weights = [random.random() for _ in range(n_inputs+1)]

class NeuronLayer(object):
    def __init__(self, n_neurons, n_inputs_per_neuron):

        self.neurons = []
        for _ in range(n_neurons):
            self.neurons.append(Neuron(n_inputs_per_neuron))

class NeuralNet(object):
    def __init__(self, n_inputs, n_hidden_layers, n_neurons_per_hlayer, n_outputs):

        self.n_inputs = n_inputs
        self.n_hidden_layers = n_hidden_layers

        if n_hidden_layers > 0:
            self.layers = [NeuronLayer(n_neurons_per_hlayer, n_inputs)]

            for _ in range(n_hidden_layers - 1):
                self.layers.append(NeuronLayer(n_neurons_per_hlayer, n_neurons_per_hlayer))
        else:
            self.layers = [NeuronLayer(n_outputs, n_inputs)]

    def sigmoid(self, netinput, response):
        return 1 / (1 + math.exp(-netinput / response))

    def get_weights(self):
        weights = []
        for l, layer in enumerate(self.layers):
            for n, neuron in enumerate(layer.neurons):
                for w in range( 0, len(neuron.weights) - 1):
                    weights.append(neuron.weights[w])
        return weights

    def set_weights(self, weights):
        c = 0
        for l, layer in enumerate(self.layers):
            for n, neuron in enumerate(layer.neurons):
                for w in range( 0, len(neuron.weights) - 1):
                    neuron.weights[w] = weights[c]
                    c += 1

    def update(self, inputs):

        if len(inputs) != self.n_inputs:
            return []

        for l, layer in enumerate(self.layers):
            i = 0
            netinput = 0
            outputs = []
            if l > 0:
                inputs = outputs

            for n, neuron in enumerate(layer.neurons):
                for w in range( 0, len(neuron.weights) - 1):
                    netinput += inputs[i] * neuron.weights[w]
                    i += 1

                netinput += (-1) * neuron.weights[len(inputs) - 1]
                outputs.append(self.sigmoid( netinput, 1 ))

                i = 0

        return outputs

