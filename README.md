# Tamo
Tamo is a AI that can be trained to play the game tank war by itself using q-learning and deep learning algorithm
unlike the deep learning that we do traditionally, all of the target value we use would be obtaining from the environment
and target value will be used to get the loss function, by minimizing the loss function we would get the
best w and b for the neural network.

 first we set up a neural network with input size of 11 and output size of 3 because we have 11 numbers in one sate
and 3 number in one action. and only 2 layer needs the relu function. then we need to improve our neural network by
using trainstep in the qtrainer class. Qtrainer class needs to be modified because we have tp deal with both long and
short term memory. Both long and short memory training is to improve the w and b in each neuron. for long term memory
tensor, there is no need to change anything but for short term it needs to be modified to be a list of tensors just like
long term memory. after we finished these steps, we can start to get our predict value, which is also a tensor with shape
[1,3](because we have 3 as the output size so there should be 3 numbers come out). the maximum value of these 3 numbers will
determine the action that the agent will do next. so every number could be viewed as a q value(the ideology if q learning is that
the agent should move based on the maximum q value) after this we should get out target value to do the algorithm.(which is bellman
equation), idx is there to help us locate the correct state or other value for each step(because all the states are stored in a
list of tensor) so we get out target value and use it to calulate our loss function, and after that we do gradient descent to improve out
 w and b in each neuron.
