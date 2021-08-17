# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 04:37:07 2019

@author: Jasmine
"""
import numpy as np
import matplotlib.pylab as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_dvt(x):
    return sigmoid(x) * (1 - sigmoid(x))

def train(weight, bias, training_inputs,training_outputs, iterations):
    for i in range(iterations):
        input_layer = training_inputs  #training data
        outputs = (sigmoid(np.dot(input_layer, weight)+bias)) #calculated output

        error = (training_outputs - outputs)  #error between trained data & output  
        #error2 = (training_outputs**2 + outputs**2)**0.5
        adjustments = np.dot(input_layer.T, error*sigmoid_dvt(outputs))
        #calculates the adjustment needed to perform on output function to bring it closer to the training dataset
        
        weight = weight + adjustments # adjustment is added to weight
        bias = bias + adjustments     # adjustment is added to bias
    # is an array, mean value is extracted 
    weight = np.mean(weight[0])       
    bias = np.mean(bias[0])
    return weight ,bias,  outputs

def think(input, weight, bias):
    output = sigmoid(np.dot(input, weight)+bias)
    return output

# Constants
iterations = 10000
weight_start= 1.0
bias_start = 1.0
step_size = 0.01 
    
training_inputs = np.array([[3], [5], [-3], [3.1]])
training_outputs = np.array([[0.3], [0.35], [0.36], [0.39]]).T 

training = train(weight_start,bias_start, training_inputs,training_outputs,iterations)

i = 0
print (training_outputs[0][i])
print (think(training_inputs[i],  weight_start, bias_start))
print ('adjusted',think(training_inputs[i], training[0] , training[1] ))

x= np.linspace(-5, 5, iterations)

y2 = sigmoid(x)                        #start function
y = sigmoid(x*weight_start+bias_start) #trained function
y1 = sigmoid(x*training[0]+training[1]) #original function
plt.plot(x, y)
plt.plot(x, y1)
plt.plot(x, y2)
plt.grid('true')
plt.xlabel('x')
plt.ylabel('y = sigmoid(x)')
plt.gca().legend(('start','trained', 'original'))
plt.title('Weight = 1')
plt.show()



