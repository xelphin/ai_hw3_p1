from copy import deepcopy
import numpy as np


def value_iteration_helper_prob_next_state_from_action(mdp, state, actual_actions_probability, next_state):
    sum_prob = 0
    for index, action in enumerate(mdp.actions):
        if mdp.step(state, action) == next_state:
            sum_prob += actual_actions_probability[index]

    return sum_prob

def value_iteration_helper_get_max_sum(mdp, state, U_curr):
    max_sum_action_tuple = (float('-inf'), "ACTION NONE")
    # Iterate over actions
    for picked_action in mdp.actions:
        sum_picked_action = 0
        actual_actions_probability = mdp.transition_function[picked_action]
        states_visited_with_action = []
        # Iterate over possible states
        for index, actual_action in enumerate(mdp.actions):
            actual_next_state = mdp.step(state, actual_action)
            if actual_next_state in states_visited_with_action:
                # print(f"----For ({state[0]},{state[1]}), after {picked_action}, will actually do {actual_action}, gets to state {actual_next_state} : VISITED already, skip")
                continue
            states_visited_with_action += [actual_next_state]
            utility_next_state = U_curr[actual_next_state[0]][actual_next_state[1]]
            prob_next_state = value_iteration_helper_prob_next_state_from_action(mdp, state, actual_actions_probability, actual_next_state)
            
            sum_picked_action += prob_next_state*utility_next_state
            # print(f"----For ({state[0]},{state[1]}), after {picked_action}, will actually do {actual_action}, gets to state {actual_next_state}, utility: {utility_next_state}, prob of that state from our action: {prob_next_state} -> add to sum {prob_next_state*utility_next_state}, now sum for action = {sum_picked_action}")
        
        sum_picked_action_tuple = (sum_picked_action, picked_action)
        max_sum_action_tuple = max(max_sum_action_tuple, sum_picked_action_tuple)

    return max_sum_action_tuple

def helper_blank_U(rows, cols):
    # Because arrays are by reference, so i need to be sure i get hard copies
    array = []
    for i in range(0, rows):
        a_row = [0]*cols
        array += [a_row]

    return array #code works

def helper_blank_policy(rows, cols):
    # Because arrays are by reference, so i need to be sure i get hard copies
    array = []
    for i in range(0, rows):
        a_row = ["ACTION NONE"]*cols
        array += [a_row]

    return array #code works


def value_iteration(mdp, U_init, epsilon=10 ** (-3)):
    # TODO:
    # Given the mdp, the initial utility of each state - U_init,
    #   and the upper limit - epsilon.
    # run the value iteration algorithm and
    # return: the U obtained at the end of the algorithms' run.
    #

    U_curr = U_init[:]
    U_new = helper_blank_U(mdp.num_row, mdp.num_col)[:]
    delta = float('inf')
    discount = mdp.gamma

    while (delta >= epsilon*(1-discount)/discount):
        delta = 0
        U_curr = U_new[:]
        U_new = helper_blank_U(mdp.num_row, mdp.num_col)[:]

        # For each state s in S
        for r in range(mdp.num_row):
            for c in range(mdp.num_col):
                if mdp.board[r][c] == "WALL":
                    continue

                reward = float(mdp.board[r][c])

                # For terminal states, it's just their reward
                if (r,c) in mdp.terminal_states: # TODO: Is this what I'm supposed to do with terminal states?
                    U_new[r][c] = reward
                
                # Not terminal state
                else:
                    max_sum = value_iteration_helper_get_max_sum(mdp, (r,c), U_curr)[0]
                    # print(f"--Max sum from all actions is {max_sum}")
                    U_new[r][c] = reward + discount*max_sum
                    # print(f"U_new[{r}][{c}] = {U_new[r][c]}        (reward {reward} + discount {discount}*max_sum {max_sum})")

                # Update delta
                if abs(U_new[r][c] - U_curr[r][c])> delta:
                    delta = abs(U_new[r][c] - U_curr[r][c])
                    # print(f"New delta {delta}     (reminder we need delta < {epsilon*(1-discount)/discount})")

        # print("###################################")
        # print("###################################")
        # print("###################################")
        # mdp.print_utility(U_new)


    return U_new


def get_policy(mdp, U):
    # TODO:
    # Given the mdp and the utility of each state - U (which satisfies the Belman equation)
    # return: the policy
    #

    policy = helper_blank_policy(mdp.num_row, mdp.num_col)[:]

    # For each state s in S
    for r in range(mdp.num_row):
        for c in range(mdp.num_col):
            state = (r,c)

            for picked_action in mdp.actions:
                if mdp.board[r][c] == "WALL":
                    continue
                max_action = value_iteration_helper_get_max_sum(mdp, (r,c), U)[1]
                policy[r][c] = max_action

    return policy




def policy_evaluation(mdp, policy):
    # TODO:
    # Given the mdp, and a policy
    # return: the utility U(s) of each state s
    #

    # ====== YOUR CODE: ======
    raise NotImplementedError
    # ========================


def policy_iteration(mdp, policy_init):
    # TODO:
    # Given the mdp, and the initial policy - policy_init
    # run the policy iteration algorithm
    # return: the optimal policy
    #

    # ====== YOUR CODE: ======
    raise NotImplementedError
    # ========================



"""For this functions, you can import what ever you want """


def get_all_policies(mdp, U):  # You can add more input parameters as needed
    # TODO:
    # Given the mdp, and the utility value U (which satisfies the Belman equation)
    # print / display all the policies that maintain this value
    # (a visualization must be performed to display all the policies)
    #
    # return: the number of different policies
    #

    # ====== YOUR CODE: ======
    raise NotImplementedError
    # ========================


def get_policy_for_different_rewards(mdp):  # You can add more input parameters as needed
    # TODO:
    # Given the mdp
    # print / displas the optimal policy as a function of r
    # (reward values for any non-finite state)
    #

    # ====== YOUR CODE: ======
    raise NotImplementedError
    # ========================
