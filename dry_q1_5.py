
class State:
    def __init__(self, index, is_final=False):
        self.index = index
        self.is_final = is_final

states = [State(0,True), State(1), State(2), State(3), State(4), State(5), State(6), State(7)]

moves = {
    0: [],
    1: [states[0],states[3]],
    2: [states[0],states[1],states[4],states[5]],
    3: [states[1],states[7]],
    4: [states[2],states[7]],
    5: [states[2],states[6]],
    6: [states[5],states[7]],
    7: [states[3],states[4],states[6]]
}

def reward(s1,s2):
    if (s1.index == 1 and s2.index == 0):
        return 5
    if (s1.index == 2 and s2.index == 0):
        return 7
    return -1

discount = 0.5

MAX_U = 8

U_0 = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0
}

def print_U(U, U_index):
    for s_index, s_val in U.items():
        print(f"U_{U_index}(s_{s_index}) = {s_val}")

    print("---------")


def value_iteration():
    print("Value Iteration")

    U_curr = U_0
    U_new = U_curr

    for U_new_index in range(0,MAX_U+1):

        for s1 in states:
            max_sum = float('-inf')
            for s2 in moves[s1.index]:
                calc = reward(s1,s2)+discount*U_curr[s2.index]
                max_sum = max(max_sum, calc)
            U_new[s1.index] = max_sum

        print_U(U_new, U_new_index)
        U_curr = U_new
    
    


# python3 dry_q1_5.py
if __name__ == '__main__':
    value_iteration()


'''

Value Iteration
U_0(s_0) = -inf
U_0(s_1) = -1.0
U_0(s_2) = -1.0
U_0(s_3) = -1.0
U_0(s_4) = -1.0
U_0(s_5) = -1.0
U_0(s_6) = -1.0
U_0(s_7) = -1.5
---------
U_1(s_0) = -inf
U_1(s_1) = -1.5
U_1(s_2) = -1.5
U_1(s_3) = -1.75
U_1(s_4) = -1.75
U_1(s_5) = -1.5
U_1(s_6) = -1.75
U_1(s_7) = -1.875
---------
U_2(s_0) = -inf
U_2(s_1) = -1.875
U_2(s_2) = -1.75
U_2(s_3) = -1.9375
U_2(s_4) = -1.875
U_2(s_5) = -1.875
U_2(s_6) = -1.9375
U_2(s_7) = -1.9375
---------
U_3(s_0) = -inf
U_3(s_1) = -1.96875
U_3(s_2) = -1.9375
U_3(s_3) = -1.96875
U_3(s_4) = -1.96875
U_3(s_5) = -1.96875
U_3(s_6) = -1.96875
U_3(s_7) = -1.984375
---------
U_4(s_0) = -inf
U_4(s_1) = -1.984375
U_4(s_2) = -1.984375
U_4(s_3) = -1.9921875
U_4(s_4) = -1.9921875
U_4(s_5) = -1.984375
U_4(s_6) = -1.9921875
U_4(s_7) = -1.99609375
---------
U_5(s_0) = -inf
U_5(s_1) = -1.99609375
U_5(s_2) = -1.9921875
U_5(s_3) = -1.998046875
U_5(s_4) = -1.99609375
U_5(s_5) = -1.99609375
U_5(s_6) = -1.998046875
U_5(s_7) = -1.998046875
---------
U_6(s_0) = -inf
U_6(s_1) = -1.9990234375
U_6(s_2) = -1.998046875
U_6(s_3) = -1.9990234375
U_6(s_4) = -1.9990234375
U_6(s_5) = -1.9990234375
U_6(s_6) = -1.9990234375
U_6(s_7) = -1.99951171875
---------
U_7(s_0) = -inf
U_7(s_1) = -1.99951171875
U_7(s_2) = -1.99951171875
U_7(s_3) = -1.999755859375
U_7(s_4) = -1.999755859375
U_7(s_5) = -1.99951171875
U_7(s_6) = -1.999755859375
U_7(s_7) = -1.9998779296875
---------
U_8(s_0) = -inf
U_8(s_1) = -1.9998779296875
U_8(s_2) = -1.999755859375
U_8(s_3) = -1.99993896484375
U_8(s_4) = -1.9998779296875
U_8(s_5) = -1.9998779296875
U_8(s_6) = -1.99993896484375
U_8(s_7) = -1.99993896484375
---------

'''