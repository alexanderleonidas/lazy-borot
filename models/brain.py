import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


import torch
import torch.nn as nn
import torch.nn.functional as F


# class Brain(nn.Module):
#     def __init__(self, input_size, hidden_size, output_size):
#         super(Brain, self).__init__()
#         self.hidden_size = hidden_size
#         self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
#         self.fc1 = nn.Linear(hidden_size, hidden_size)
#         self.fc2 = nn.Linear(hidden_size, output_size)

# #     def forward(self, x, h):
# #         out, h = self.rnn(x, h)
# #         out = F.relu(self.fc1(out[:, -1, :]))
# #         out = self.fc2(out)
# #         return out, h

#     def init_hidden(self, batch_size):
#         return torch.zeros(1, batch_size, self.hidden_size)

#     @staticmethod
#     def create():
#         # 16 = 12 sensors + 2 velocity + 1 angle + 1 bias
#         # 64 = hidden layer size
#         # 6 = 6 actions
#         return Brain(16, 64, 6)

# class Brain(nn.Module):
#     def __init__(self, input_size, hidden_size, output_size):
#         super(Brain, self).__init__()
#         self.fc1 = nn.Linear(input_size, hidden_size)
#         self.fc2 = nn.Linear(hidden_size, output_size)
#         self.relu = nn.ReLU()
#
#     def forward(self, x):
#         x = self.relu(self.fc1(x))
#         x = self.fc2(x)
#         return x

class Brain:
    def __init__(self, weights=None):
        self.num_inputs = 20  # Adjusted to match the actual input size (16 sensors + 4 feedback)
        self.num_hidden = 4
        self.num_outputs = 7  # Ensure the number of outputs matches the action space size
        self.feedback = [0, 0, 0, 0]
        self.weights = weights

        if weights is None:
            self.hidden_layer1 = Brain.Layer(self.num_inputs, self.num_hidden)
            self.act_sigmoid1 = Brain.Activation_Sigmoid()
            self.output_layer2 = Brain.Layer(self.num_hidden, self.num_outputs)
            self.act_tanh = Brain.Activation_Tanh()
            self.weights = [self.hidden_layer1.weights, self.output_layer2.weights]
        else:
            self.hidden_layer1 = Brain.Layer(self.num_inputs, self.num_hidden, self.weights[0])
            self.act_sigmoid1 = Brain.Activation_Sigmoid()
            self.output_layer2 = Brain.Layer(self.num_hidden, self.num_outputs, self.weights[1])
            self.act_tanh = Brain.Activation_Tanh()
            self.weights = [self.hidden_layer1.weights, self.output_layer2.weights]

    class Layer:
        def __init__(self, n_inputs, n_neurons, weights=None):
            if weights is None:
                self.weights = np.random.uniform(low=-1, high=1, size=(n_inputs, n_neurons))
            else:
                self.weights = weights

        def forward(self, inputs):
            self.output = np.dot(inputs, self.weights)

    class Activation_Tanh:
        def forward(self, inputs):
            self.output = np.tanh(inputs)

    class Activation_Sigmoid:
        def forward(self, inputs):
            self.output = 1.0 / (1 + np.exp(-inputs))

    def runNN(self, sensors):
        sensors = np.array(sensors)
        noise = np.random.normal(0, 0.01, size=sensors.shape)
        noisy_sensors = sensors + noise
        sensor_input = np.concatenate((noisy_sensors, self.feedback))

        self.hidden_layer1.forward(sensor_input)
        self.act_sigmoid1.forward(self.hidden_layer1.output)
        hidden_layer_output = self.act_sigmoid1.output  # Also feedback
        self.feedback = hidden_layer_output

        self.output_layer2.forward(self.act_sigmoid1.output)
        self.act_tanh.forward(self.output_layer2.output)
        motor_output = self.act_tanh.output

        # Ensure motor_output has exactly 7 elements
        if len(motor_output) != 6:
            motor_output = np.resize(motor_output, 6)

        return motor_output, hidden_layer_output
