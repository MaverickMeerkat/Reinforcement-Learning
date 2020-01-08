import numpy as np

class SimpleNN():
    """
    An [Input - Hidden - Output] net.
    """
    def __init__(self, network_config):
        self.layer_sizes = network_config.get("layer_sizes")
        self.rand_generator = np.random.RandomState(network_config.get("seed"))
        self.weights = [dict() for i in range(0, len(self.layer_sizes) - 1)]
        self.gradients = [dict() for i in range(0, len(self.layer_sizes) - 1)]
        for i in range(0, len(self.layer_sizes) - 1):
            self.weights[i]['W'] = self.init_saxe(self.layer_sizes[i], self.layer_sizes[i + 1])
            self.weights[i]['b'] = np.zeros((1, self.layer_sizes[i + 1]))
    
    def get_action_values(self, s):
        self.inputs = []
        a = s
        da = 1
        for i in range(0, len(self.layer_sizes) - 1):
            self.inputs.append((a, da))
            W, b = self.weights[i]['W'], self.weights[i]['b']
            z = np.dot(a, W) + b
            a = np.maximum(z, 0)
            da = (a > 0).astype(float)

        return z.ravel()
    
    def get_gradients(self, s, delta_mat):
        v = delta_mat
        for i in reversed(range(0, len(self.layer_sizes) - 1)):
            a, da = self.inputs[i]
            self.gradients[i]['W'] = np.dot(a.T, v) * 1. / s.shape[0]
            self.gradients[i]['b'] = np.sum(v, axis=0, keepdims=True) * 1. / s.shape[0]
            v = np.dot(v, self.weights[i]['W'].T) * da                
        return self.gradients
    
    def init_saxe(self, rows, cols):
        """
        Args:
            rows (int): number of input units for layer.
            cols (int): number of output units for layer.
        Returns:
            NumPy Array consisting of weights for the layer based on the initialization in Saxe et al.
        """
        tensor = self.rand_generator.normal(0, 1, (rows, cols))
        if rows < cols:
            tensor = tensor.T
        tensor, r = np.linalg.qr(tensor)
        d = np.diag(r, 0)
        ph = np.sign(d)
        tensor *= ph

        if rows < cols:
            tensor = tensor.T
        return tensor
    
    def get_weights(self):
        return self.weights
    
    def set_weights(self, weights):
        self.weights = weights