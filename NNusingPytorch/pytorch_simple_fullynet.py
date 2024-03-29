#Imports
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torch.optim as optim

#create fully connected network
class NN(nn.Module):
    def __init__(self , input_size, num_classes):
        super(NN, self).__init__()
        self.fc1 = nn.Linear(input_size, 50)
        self.fc2 = nn.Linear(50, num_classes)
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return  x

# set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

#hyperparameters
input_size = 784
num_classes = 10
learning_rate = 0.001
batch_size = 64
num_epochs =1

#load data

train_dataset = datasets.MNIST(root='dataset/', train=True, transform=transforms.ToTensor(), download=True)
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_dataset = datasets.MNIST(root='dataset/', train=False, transform=transforms.ToTensor(), download=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)


#initialize network
model = NN(input_size=input_size, num_classes=num_classes).to(device)
# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters() , lr = learning_rate)
#train network

for epoch in range(num_epochs):
    for batch_idx , (data,targets) in enumerate(train_loader):
        #get data to cuda if possible
        data = data.to(device=device)
        targets = targets.to(device=device)

        data = data.reshape(data.shape[0] , -1) # converting into single dimension

      #forward
        scores = model(data)
        loss = criterion(scores,targets)
        #backward
        optimizer.zero_grad()
        loss.backward()
        #gradient descent or adam step
        optimizer.step()

#check accuracy on training and test to see  how good our model is

def check_accuracy(loader, model):
    if loader.dataset.train:
        print("Checking accuracy on training data")
    else:
        print("Checking accuracy on test data")
    num_correct =0
    num_samples =0
    model.eval()

    with torch.no_grad():
        for x,y in loader:
            x = x.to(device=device)
            y= y.to(device=device)
            x = x.reshape(x.shape[0],-1)

            scores = model(x)
            # 64*10
            _, predictions =scores.max(1)
            num_correct += (predictions == y).sum()
            num_samples += predictions.size(0)

            print(f'Got {num_correct} / {num_samples} with accuracy {float(num_correct)/float(num_samples)*100:.2f}')


#check_accuracy(train_loader, model)
check_accuracy(test_loader , model)

