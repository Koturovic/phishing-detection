import numpy as np
import math

class LogisticRegression:
	# Class constructor
	def __init__(self, learning_rate=0.01, n_iterations=1000, lambda_ = 0.1, printnum = 10): 
		self.learning_rate = learning_rate
		self.n_iterations = n_iterations
		self.lambda_ = lambda_
		self.weights = None
		self.bias = None
		self.printnum = printnum
	
	# Sigmoid function
	def sigmoid(self, z): 
		z = np.array(z, dtype=float)
		return 1 / (1 + np.exp(-z))

	# Fitting a model -> training the model using the training data
	def fit(self, X, y):
		X = np.array(X)
		y = np.array(y)

		n_samples, n_features = X.shape
		self.weights = np.zeros(n_features)
		self.bias = 0
		
		s=f"Hyperparameters: Learning rate = {self.learning_rate}, Number of iterations = {self.n_iterations}, Lambda = {self.lambda_} \n"
		for i in range(self.n_iterations):
			linear_model = np.dot(X, self.weights) + self.bias
			y_predicted = self.sigmoid(linear_model)
			
			error = y_predicted - y
			
			dw = (1 / n_samples) * np.dot(X.T, (error)) + (self.lambda_ / n_samples) * self.weights
			db = (1 / n_samples) * np.sum(error)
			    
			self.weights -= self.learning_rate * np.array(dw, dtype=float)
			self.bias -= self.learning_rate * db
			
			
			if i% math.ceil(self.n_iterations/self.printnum) == 0 or i == (self.n_iterations-1):
				weights_str = np.array2string(self.weights, precision=4, suppress_small=True, separator=', ')
				s+=f"Iteration {i:4d} | Bias: {self.bias: .4f} | Weights: {weights_str}\n"
				print(f"Iteration {i:4d} | Bias: {self.bias: .4f} | Weights: {weights_str}")
		return s

	# Predicting probability
	def predict_proba(self, X):
		linear_model = np.dot(X, self.weights) + self.bias
		return self.sigmoid(linear_model)

	# Predicting output
	def predict(self, X):
		proba = self.predict_proba(X)
		return [1 if p >= 0.5 else 0 for p in proba]
	
