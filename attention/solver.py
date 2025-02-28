"""
Generic solver methods for Markov Decision Processes (MDPs) and methods for
policy computations for GridWorld.
"""

import numpy as np


def value_iteration(p, reward, discount, eps=1e-3):
    """
    Basic value-iteration algorithm to solve the given MDP.
    """
    n_states, _, n_actions = p.shape
    v = np.zeros(n_states)

    # Setup transition probability matrices for easy use with numpy.

    p = [np.matrix(p[:, :, a]) for a in range(n_actions)]

    delta = np.inf
    while delta > eps:      # iterate until convergence
        v_old = v

        # compute state-action values (note: we actually have Q[a, s] here)
        q = discount * np.array([p[a] @ v for a in range(n_actions)])

        # compute state values
        v = reward + np.max(q, axis=0)[0]

        # compute maximum delta
        delta = np.max(np.abs(v_old - v))

    return v


def stochastic_value_iteration(p, reward, discount, eps=1e-3):
    """
    A modified version of the value-iteration algorithm to solve the given MDP.
    """
    n_states, _, n_actions = p.shape
    v = np.zeros(n_states)

    #     P_a * [ v(s_i) ]_i^T = [ sum_k p(s_k | s_j, a) * v(s_K) ]_j^T
    p = [np.matrix(p[:, :, a]) for a in range(n_actions)]

    delta = np.inf
    while delta > eps:      # iterate until convergence
        v_old = v

        # compute state-action values (note: we actually have Q[a, s] here)
        q = discount * np.array([p[a] @ v for a in range(n_actions)])

        # compute state values
        v = reward + np.average(q, axis=0)[0]

        # compute maximum delta
        delta = np.max(np.abs(v_old - v))

    return v


def optimal_policy_from_value(world, value):
    policy = np.array([
        np.argmax([value[world.state_index_transition(s, a)] for a in range(world.n_actions)])
        for s in range(world.n_states)
    ])

    return policy


def optimal_policy(world, reward, discount, eps=1e-3):
    
    value = value_iteration(world.p_transition, reward, discount, eps)
    return optimal_policy_from_value(world, value)


def stochastic_policy_from_value(world, value, w=lambda x: x):
    
    policy = np.array([
        np.array([w(value[world.state_index_transition(s, a)]) for a in range(world.n_actions)])
        for s in range(world.n_states)
    ])

    return policy / np.sum(policy, axis=1)[:, None]
