import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)




class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)
        #this is for the long term training because we got a lot of samples already

        if len(state.shape) == 1:#this is for the short term memory because we only have one sample for each training
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: predicted Q values with current state
        pred = self.model(state)# it seems like if state is a list of tensors the model will predict a list of actions

        target = pred.clone()#get the same pred value again
        for idx in range(len(done)):#every step will generate a new done, so this series of code means for every step we need to do the code down for once
            Q_new = reward[idx]#reward are put into "reward" by order, so by using index we can get the reward that we want
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))#reward is the reward for s0 to s1, torch max... is the maximum value of the action of S2

            target[idx][torch.argmax(action[idx]).item()] = Q_new#this code means renew the maximum value of s0

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)#this will work because only one value in target is renewed and the other values are the same, so the loss function between them will only be due to the value that is modified
        loss.backward()#using gradient descent to renew the w and b s.

        self.optimizer.step()
#unlike the deep learning that we do traditionally, all of the target value we use would be obtaining from the environment
#and target value will be used to get the loss function, by minimizing the loss function we would get the
#best w and b for the neural network.

# first we set up a neural network with input size of 11 and output size of 3 because we have 11 numbers in one sate
#and 3 number in one action. and only 2 layer needs the relu function. then we need to improve our neural network by
#using trainstep in the qtrainer class. Qtrainer class needs to be modified because we have tp deal with both long and
#short term memory. Both long and short memory training is to improve the w and b in each neuron. for long term memory
#tensor, there is no need to change anything but for short term it needs to be modified to be a list of tensors just like
#long term memory. after we finished these steps, we can start to get our predict value, which is also a tensor with shape
#[1,3](because we have 3 as the output size so there should be 3 numbers come out). the maximum value of these 3 numbers will
#determine the action that the agent will do next. so every number could be viewed as a q value(the ideology if q learning is that
#the agent should move based on the maximum q value) after this we should get out target value to do the algorithm.(which is bellman
#equation), idx is there to help us locate the correct state or other value for each step(because all the states are stored in a
#list of tensor) so we get out target value and use it to calulate our loss function, and after that we do gradient descent to improve out
# w and b in each neuron.
