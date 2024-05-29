import torch
import torch.nn as nn
import torch.nn.functional as F


class Brain(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Brain, self).__init__()
        self.hidden_size = hidden_size
        if torch.backends.mps.is_available():
            self.device = torch.device("mps") 
        else:
            self.device = torch.device("cpu") 
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True, device=self.device)
        self.fc1 = nn.Linear(hidden_size, hidden_size, device=self.device)
        self.fc2 = nn.Linear(hidden_size, output_size, device=self.device)

    def forward(self, x, h):
        out, h = self.rnn(x, h)
        out = F.relu(self.fc1(out[:, -1, :]))
        out = self.fc2(out)
        return out, h

    def init_hidden(self, batch_size):
        return torch.zeros(1, batch_size, self.hidden_size, device=self.device)

    @staticmethod
    def create():
        # 16 = 12 sensors + 2 velocity + 1 angle + 1 bias
        # 64 = hidden layer size
        # 6 = 6 actions
        return Brain(16, 64, 6)

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
