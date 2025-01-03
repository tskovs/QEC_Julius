import jax.numpy as jnp
import jax

from icecream import ic  # For debugging

import json


def save_NN(file: str, params: dict[str, list[jnp.ndarray]]) -> None:
    package = {key: [val.tolist() for val in vals]
               for key, vals in params.items()}
    with open(file, 'w') as file:
        json.dump(package, file, indent=4)


def load_NN(file: str) -> dict[str, list[jnp.ndarray]]:
    with open(file, 'r') as file:
        package = json.load(file)
    return {key: [jnp.array(val) for val in vals] for key, vals in package.items()}


def sigmoid(x):
    return 1/(1 + jnp.exp(-x))


def soft_plus(x):
    return jnp.log2(1+jnp.exp(x))


def NN(x, params):
    """
    Standard multilayer perception "MLP" with params['weights'] and params['biases'],
    applied to input vector x. Activation tanh applied to all
    layers except last.

    Returns activation vector of the output layer.
    """

    num_layers = len(params['weights'])
    for layer_idx, (w, b) in enumerate(zip(params['weights'], params['biases'])):
        x = jnp.matmul(w, x) + b
        if layer_idx < num_layers-1:
            x = jnp.tanh(x)
        else:
            x = sigmoid(x)
            # x = soft_plus(x)
    return x


def NN_init_params(key, num_neurons_layers):
    """
    Given a jax random key and a list of the neuron numbers
    in the layers of a network (simple fully connected network,
    i.e. 'multi-layer perceptron'), return a dictionary
    with the weights initialized randomly and biases set to zero.

    Returns: params, with params['weights'] a list of matrices and
    params['biases'] a list of vectors.
    """
    params = {}
    params['weights'] = []
    params['biases'] = []

    for lower_layer, higher_layer in zip(num_neurons_layers[:-1], num_neurons_layers[1:]):
        key, subkey = jax.random.split(key)
        params['weights'].append(jax.random.normal(subkey,
                                                   [higher_layer, lower_layer]) /
                                 jnp.sqrt(lower_layer))

    for num_neurons in num_neurons_layers[1:]:
        params['biases'].append(jnp.zeros(num_neurons))

    return params


NN_batch = jax.vmap(NN, in_axes=[0, None], out_axes=0)
