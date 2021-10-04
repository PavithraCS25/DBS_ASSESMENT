import numpy as np
from base import BaseMLP
import sklearn #sklearn is imported mainly for sample dataset



class NeuralNetworkClassifier(BaseMLP):
    def __init__(self, *args):
        super().__init__(*args)
    
    #function to define the number of layers in the neural network.
    #Use the shape of x,y  for n_x and n_y respectively. set n_h to be 5
    def nn_layer_size_def(self,x,y):
        
        np.random.seed(self.random_state)
        n_x = x.shape[0]
        n_y = y.shape[0]
        
        return (n_x, n_y)
    
    #function defines the weights and bias based on n_x and n_y 
    #function returns the weights and bias as parameters
    def initialize_parameters(self,n_x,n_h,n_y):
        
        np.random.seed(self.random_state) #set up random seed to maintain uniformity
        weight1 = np.random.randn(n_h, n_x) * 0.01
        bias1 = np.zeros((n_h, 1))
        weight2 = np.random.randn(n_y, n_h) * 0.01
        bias2 = np.zeros((n_y,1))
        nn_parameters = {"weight1": weight1,"bias1": bias1,"weight2": weight2,"bias2": bias2}
        
        return nn_parameters
        

    #function implements forward propagation to calculate activation function probability
    def forward_propagation(self,x, nn_parameters):
        
        weight1 = nn_parameters['weight1']
        bias1 = nn_parameters['bias1']
        weight2 = nn_parameters['weight2']
        bias2 = nn_parameters['bias2']
        
        
        Z1 = np.dot(weight1, x) + bias1
        A1 =  np.tanh(Z1)
        Z2 = np.dot(weight2, A1) + bias2
        A2 = 1/(1+np.exp(-Z2))
        
        hidden_value = {"Z1": Z1, "A1": A1,"Z2": Z2, "A2": A2}
        
        return A2, hidden_value
    
    #Function to compute the cross-entropy cost
    def compute_cost(self,A2, y):
       
        m = y.shape[1]
        
        logprobs = np.multiply(np.log(A2),y) +  np.multiply(np.log(1-A2), (1-y))
        cost = -1/m*np.sum(logprobs)
        cost = np.squeeze(cost)   
        
        return cost
    
    #function implements backward propagation to calculate weights and bias
    def backward_propagation(self,nn_parameters, hidden_value, x, y):
        m = x.shape[1]
        weight2 = nn_parameters["weight2"]
        A1 = hidden_value["A1"]
        A2 =  hidden_value["A2"]
        
        
        dZ2= A2-y
        dweight2 = 1./m*np.dot(dZ2, A1.T)
        dbias2 = 1./m*np.sum(dZ2, axis = 1, keepdims=True)
        dZ1 = np.dot(weight2.T, dZ2) * (1 - np.power(A1, 2))
        dweight1 = 1./m* np.dot(dZ1, x.T)
        dbias1 = 1./m*np.sum(dZ1, axis = 1, keepdims=True)
        
        result = {"dweight1": dweight1,"dbias1": dbias1,"dweight2": dweight2, "dbias2": dbias2}
        
        return result
        
    #update parameter with new learning rate
    def update_parameters(self,nn_parameters, result, learning_rate = 1.2):
    
        weight1 = nn_parameters["weight1"]
        weight2 = nn_parameters["weight2"]
        bias1 = nn_parameters["bias1"]
        bias2 = nn_parameters["bias2"]
        
        dweight1 = result["dweight1"]
        dbias1 = result["dbias1"]
        dweight2 = result["dweight2"]
        dbias2 = result["dbias2"]

        weight1 = weight1 - dweight1 * learning_rate
        bias1 = bias1 - dbias1 * learning_rate
        weight2 = weight2 - dweight2 * learning_rate
        bias2 = bias2 - dbias2 * learning_rate
        
        parameters = {"weight1": weight1,
                      "bias1": bias1,
                      "weight2": weight2,
                      "bias2": bias2}
        
        return parameters

    
    def fit(self, x, y) -> None:
        """Fit the model to data matrix X and target(s) y.

        Parameters
        ----------
        x : list or sparse matrix of shape (n_samples, n_features)
            The input data.

        y : list of shape (n_samples,) or (n_samples, n_outputs)
            The target values (class labels for classification).

        """
        
        
        np.random.seed(self.random_state)
        n_x = self.nn_layer_size_def(x,y)[0]
        n_y = self.nn_layer_size_def(x,y)[1]
        n_h = self.hidden_layer_sizes
        num_iter = self.max_iter
        p_cost=False
        
        nn_parameters = self.initialize_parameters(n_x,n_h,n_y)
        
        for i in range(0, num_iter):
            A2, hidden_value = self.forward_propagation(x, nn_parameters)
            cost = self.compute_cost(A2, y)
            result = self.backward_propagation(nn_parameters, hidden_value, x, y)
            nn_parameters = self.update_parameters(nn_parameters, result)
            
            if p_cost and i % 1000 == 0:
                print ("Cost after iteration %i: %f" %(i, cost))
            
            
        return nn_parameters

    def predict(self, x,nn_parameters):
        """Predict using the multi-layer perceptron classifier

        Parameters
        ----------
        x : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        y : list, shape (n_samples,) or (n_samples, n_classes)
            The predicted classes.
        """
        A2, cache = self.forward_propagation(x, nn_parameters)
        predictions = A2 > 0.5
        
        return predictions
    
    
