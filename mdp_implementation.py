from copy import deepcopy
import numpy as np


def helper_probability_to_next_state(mdp, state, actual_actions_probability, next_state):
    if state in mdp.terminal_states:
        return 0
    # Given probability for each action, what is the probability I get to next_state
    sum_prob = 0
    for index, action in enumerate(mdp.actions):
        if mdp.step(state, action) == next_state:
            sum_prob += actual_actions_probability[index]

    return sum_prob

    # Why is this important?
    # Imagine you're in top-left (0,0) cell and you do UP
    # Probability to get to next_state = (0,0) is equal to prob(LEFT)+prob(UP)   [which we get from actual_actions_probability]


def helper_action_for_max_sum_aux(mdp, state, U_curr, picked_action):
    # Iterate over possible states picked_action will get you to (all s')
    sum_picked_action = 0
    actual_actions_probability = mdp.transition_function[picked_action]
    states_visited_with_action = []
    # Iterate over possible states picked_action will get you to (all s')
    for index, actual_action in enumerate(mdp.actions):
        actual_next_state = mdp.step(state, actual_action) # == s'
        if actual_next_state in states_visited_with_action:
            # print(f"----For ({state[0]},{state[1]}), after {picked_action}, will actually do {actual_action}, gets to state {actual_next_state} : VISITED already, skip")
            continue
        states_visited_with_action += [actual_next_state]

        # Get properties of s'
        utility_next_state = U_curr[actual_next_state[0]][actual_next_state[1]]
        prob_next_state = helper_probability_to_next_state(mdp, state, actual_actions_probability, actual_next_state)
        calc = prob_next_state*utility_next_state
        
        # Add calc to sum_picked_action because we are summing
        sum_picked_action += calc
        # print(f"----For ({state[0]},{state[1]}), after {picked_action}, will actually do {actual_action}, gets to state {actual_next_state}, utility: {utility_next_state}, prob of that state from our action: {prob_next_state} -> add to sum {prob_next_state*utility_next_state}, now sum for action = {sum_picked_action}")
    
    return sum_picked_action


def helper_action_for_max_sum(mdp, state, U_curr):

    # SOLVES: "max a in Actions such that sum [...]"" part of the formula

    max_sum_action_tuple = (float('-inf'), "ACTION NONE")

    # Iterate over actions
    for picked_action in mdp.actions:
        sum_picked_action = helper_action_for_max_sum_aux(mdp, state, U_curr, picked_action)
        sum_picked_action_tuple = (sum_picked_action, picked_action)
        max_sum_action_tuple = max(max_sum_action_tuple, sum_picked_action_tuple)

    # Return max (sum, action) 
    return max_sum_action_tuple

def helper_blank_U(rows, cols):
    # Because arrays are by reference, so i need to be sure i get hard copies
    array = []
    for i in range(0, rows):
        a_row = [0]*cols
        array += [a_row]

    return array[:]

def helper_blank_policy(rows, cols):
    # Because arrays are by reference, so i need to be sure i get hard copies
    array = []
    for i in range(0, rows):
        a_row = ["ACTION NONE"]*cols
        array += [a_row]

    return array[:]

def helper_get_indices_of_walls(mdp):
    indices = []
    for r in range(mdp.num_row):
        for c in range(mdp.num_col):
            if mdp.board[r][c] == "WALL":
                indices += [r*mdp.num_col + c]
    return indices

def helper_clean_matrix(matrix, indices):
    indices.sort()
    np_indices = np.array(indices)

    for i in range(0,len(indices)):
        matrix = np.delete(matrix, np_indices[i], axis=0)
        matrix = np.delete(matrix, np_indices[i], axis=1)
        # b = np.delete(b, np_indices[i])
        np_indices -= 1 # Because you deleted row/col t, you now need to update the indices values

    return matrix

def helper_clean_vector(vector, indices):
    indices.sort()
    np_indices = np.array(indices)

    for i in range(0,len(indices)):
        vector = np.delete(vector, np_indices[i])
        np_indices -= 1 # Because you deleted row t, you now need to update the indices values

    return vector

def helper_get_U_from_vector(mdp, vector):
    U_eval = helper_blank_U(mdp.num_row, mdp.num_col)[:]
    vector_index = 0
    for r in range(mdp.num_row):
        for c in range(mdp.num_col):
            if mdp.board[r][c] == "WALL":
                continue
            if vector_index >= len(vector):
                print("BAD, SHOULDN'T GET HERE")
                continue

            U_eval[r][c] = vector[vector_index]
            vector_index += 1
    
    return U_eval

def helper_make_wall_and_terminal_none_policy(mdp, policy):
    policy_new = policy[:]
    for r in range(mdp.num_row):
        for c in range(mdp.num_col):
            if mdp.board[r][c] == "WALL" or (r,c) in mdp.terminal_states:
                policy_new[r][c] = None

    return policy_new



def value_iteration(mdp, U_init, epsilon=10 ** (-3)):
    # Given the mdp, the initial utility of each state - U_init,
    #   and the upper limit - epsilon.
    # run the value iteration algorithm and
    # return: the U obtained at the end of the algorithms' run.

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
                    max_sum = helper_action_for_max_sum(mdp, (r,c), U_curr)[0]
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
    # Given the mdp and the utility of each state - U (which satisfies the Belman equation)
    # return: the policy

    policy = helper_blank_policy(mdp.num_row, mdp.num_col)[:]

    # For each state s in S
    for r in range(mdp.num_row):
        for c in range(mdp.num_col):
            state = (r,c)
            if mdp.board[r][c] == "WALL":
                continue
            max_action = helper_action_for_max_sum(mdp, (r,c), U)[1] # TODO: Not sure if this is the calc I want
            policy[r][c] = max_action

    policy = helper_make_wall_and_terminal_none_policy(mdp, policy)
    return policy


def policy_evaluation(mdp, policy):
    # Given the mdp, and a policy
    # return: the utility U(s) of each state s

    discount = mdp.gamma
    wall_indices = helper_get_indices_of_walls(mdp)
    n = mdp.num_row*mdp.num_col
    P_matrix = np.zeros((n, n))
    I_matrix = np.eye(n)
    R_vector = np.zeros(n)

    # Fill probability matrix
    for i in range(0, n):
        for m in range(0, n):
            state_i = (int(i/mdp.num_col), int(i%mdp.num_col))
            state_m = (int(m/mdp.num_col), int(m%mdp.num_col))
            if mdp.board[state_i[0]][state_i[1]] == "WALL":
                continue
            action_i = policy[state_i[0]][state_i[1]]
            if (action_i == None):
                # Terminal state (can't move anywhere)
                actual_actions_probability_s_i = (0, 0, 0, 0)
            else:
                actual_actions_probability_s_i = mdp.transition_function[action_i]
            prob_s_i_to_s_m = helper_probability_to_next_state(mdp, state_i, actual_actions_probability_s_i, state_m)
            P_matrix[i][m] = prob_s_i_to_s_m
            R_vector[i] = float(mdp.board[state_i[0]][state_i[1]])


    P_matrix_wDiscount = discount*P_matrix

    # Clean
    P_matrix_wDiscount = helper_clean_matrix(P_matrix_wDiscount, wall_indices[:])
    I_matrix = helper_clean_matrix(I_matrix, wall_indices[:])
    R_vector = helper_clean_vector(R_vector, wall_indices[:])

    # Invert (I-P_matrix_wDiscount)
    Inverse_I_PwDiscount = np.linalg.inv(I_matrix-P_matrix_wDiscount)

    # Calc U_vector
    U_vector = Inverse_I_PwDiscount @ R_vector
    # print("U_vector")
    # print(U_vector)

    # Put in U[][] (while skipping over walls)
    U_eval = helper_get_U_from_vector(mdp, U_vector)
    return U_eval



def policy_iteration(mdp, policy_init):
    # TODO:
    # Given the mdp, and the initial policy - policy_init
    # run the policy iteration algorithm
    # return: the optimal policy
    #

    U_curr = helper_blank_U(mdp.num_row, mdp.num_col)[:]
    policy_curr = policy_init[:]
    unchanged = False

    while not unchanged:
        U_curr = policy_evaluation(mdp, policy_curr[:])
        unchanged = True
        
        # For each state s in S
        for r in range(mdp.num_row):
            for c in range(mdp.num_col):
                # Skip wall states and terminal states
                if (mdp.board[r][c] == "WALL") or ((r,c) in mdp.terminal_states):
                    continue
                # Not terminal state
                else:
                    picked_action = policy_curr[r][c]
                    action_sum = helper_action_for_max_sum_aux(mdp, (r,c), U_curr, picked_action)
                    (max_sum, max_action) = helper_action_for_max_sum(mdp, (r,c), U_curr)
                    if max_sum > action_sum:
                        policy_curr[r][c] = max_action
                        unchanged = False

        # print("Current Policy:")
        # mdp.print_policy(policy_curr)
    
    policy_curr = helper_make_wall_and_terminal_none_policy(mdp, policy_curr)
    return policy_curr



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
