# import packages
import torch
import torch.nn as nn

# Define a custom classifier
class CustomClassifier(nn.Module):
    def __init__(self, in_features, hidden_features, out_features):
        super(CustomClassifier, self).__init__()
        self.fc1 = nn.Linear(in_features, hidden_features[0])
        self.bn1 = nn.BatchNorm1d(hidden_features[0])
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_features[0], hidden_features[1])
        self.bn2 = nn.BatchNorm1d(hidden_features[1])             
        self.fc3 = nn.Linear(hidden_features[1], hidden_features[2])
        self.bn3 = nn.BatchNorm1d(hidden_features[2])        
        self.out = nn.Linear(hidden_features[2], out_features)    

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.out(x)
        return x
        
    def total_parameters(self):
        return sum(p.numel() for p in self.parameters())
