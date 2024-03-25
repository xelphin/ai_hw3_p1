
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



def print_U(U, U_index):
    for s_index, s_val in U.items():
        print(f"U_{U_index}(s_{s_index}) = {s_val['value']}      calc: {s_val['calc']}")

    print("---------")

def init_U():
    return {
        0: {"value" : 0, "calc": ""},
        1: {"value" : 0, "calc": ""},
        2: {"value" : 0, "calc": ""},
        3: {"value" : 0, "calc": ""},
        4: {"value" : 0, "calc": ""},
        5: {"value" : 0, "calc": ""},
        6: {"value" : 0, "calc": ""},
        7: {"value" : 0, "calc": ""}
    }

U_0 = init_U()

def make_sure_not_neg_inf(x):
    if x == float("-inf"):
        return 0 # TODO: Should it be this?
    return x

def value_iteration():
    print("Value Iteration")

    U_curr = U_0
    U_new = init_U()

    for U_new_index in range(1,MAX_U+1):

        for s1 in states:
            max_sum = float('-inf')
            max_calc_str = "max("
            for s2 in moves[s1.index]:

                # Calc utility
                calc = reward(s1,s2)+discount*U_curr[s2.index]["value"]

                # Prints
                # print(f"debugging: s1 = {s1.index}, s2 = {s2.index}, reward = {reward(s1,s2)}, U_{U_new_index-1}[{s2.index}]['value'] = {U_curr[s2.index]['value']}")
                max_calc_str += f"({reward(s1,s2)}+{discount}*{U_curr[s2.index]['value']}), "

                # Pick max
                max_sum = max(max_sum, calc)

            max_calc_str += ")"
            U_new[s1.index]["value"] = make_sure_not_neg_inf(max_sum)
            U_new[s1.index]["calc"] = max_calc_str

        print_U(U_new, U_new_index)
        U_curr = U_new
        U_new = init_U()
    
    


# python3 dry_q1_5.py
if __name__ == '__main__':
    value_iteration()


'''

Value Iteration
U_1(s_0) = 0      calc: max()
U_1(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*0), )
U_1(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*0), (-1+0.5*0), (-1+0.5*0), )
U_1(s_3) = -1.0      calc: max((-1+0.5*0), (-1+0.5*0), )
U_1(s_4) = -1.0      calc: max((-1+0.5*0), (-1+0.5*0), )
U_1(s_5) = -1.0      calc: max((-1+0.5*0), (-1+0.5*0), )
U_1(s_6) = -1.0      calc: max((-1+0.5*0), (-1+0.5*0), )
U_1(s_7) = -1.0      calc: max((-1+0.5*0), (-1+0.5*0), (-1+0.5*0), )
---------
U_2(s_0) = 0      calc: max()
U_2(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*-1.0), )
U_2(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*5.0), (-1+0.5*-1.0), (-1+0.5*-1.0), )
U_2(s_3) = 1.5      calc: max((-1+0.5*5.0), (-1+0.5*-1.0), )
U_2(s_4) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*-1.0), )
U_2(s_5) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*-1.0), )
U_2(s_6) = -1.5      calc: max((-1+0.5*-1.0), (-1+0.5*-1.0), )
U_2(s_7) = -1.5      calc: max((-1+0.5*-1.0), (-1+0.5*-1.0), (-1+0.5*-1.0), )
---------
U_3(s_0) = 0      calc: max()
U_3(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*1.5), )
U_3(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*5.0), (-1+0.5*2.5), (-1+0.5*2.5), )
U_3(s_3) = 1.5      calc: max((-1+0.5*5.0), (-1+0.5*-1.5), )
U_3(s_4) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*-1.5), )
U_3(s_5) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*-1.5), )
U_3(s_6) = 0.25      calc: max((-1+0.5*2.5), (-1+0.5*-1.5), )
U_3(s_7) = 0.25      calc: max((-1+0.5*1.5), (-1+0.5*2.5), (-1+0.5*-1.5), )
---------
U_4(s_0) = 0      calc: max()
U_4(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*1.5), )
U_4(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*5.0), (-1+0.5*2.5), (-1+0.5*2.5), )
U_4(s_3) = 1.5      calc: max((-1+0.5*5.0), (-1+0.5*0.25), )
U_4(s_4) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_4(s_5) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_4(s_6) = 0.25      calc: max((-1+0.5*2.5), (-1+0.5*0.25), )
U_4(s_7) = 0.25      calc: max((-1+0.5*1.5), (-1+0.5*2.5), (-1+0.5*0.25), )
---------
U_5(s_0) = 0      calc: max()
U_5(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*1.5), )
U_5(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*5.0), (-1+0.5*2.5), (-1+0.5*2.5), )
U_5(s_3) = 1.5      calc: max((-1+0.5*5.0), (-1+0.5*0.25), )
U_5(s_4) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_5(s_5) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_5(s_6) = 0.25      calc: max((-1+0.5*2.5), (-1+0.5*0.25), )
U_5(s_7) = 0.25      calc: max((-1+0.5*1.5), (-1+0.5*2.5), (-1+0.5*0.25), )
---------
U_6(s_0) = 0      calc: max()
U_6(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*1.5), )
U_6(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*5.0), (-1+0.5*2.5), (-1+0.5*2.5), )
U_6(s_3) = 1.5      calc: max((-1+0.5*5.0), (-1+0.5*0.25), )
U_6(s_4) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_6(s_5) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_6(s_6) = 0.25      calc: max((-1+0.5*2.5), (-1+0.5*0.25), )
U_6(s_7) = 0.25      calc: max((-1+0.5*1.5), (-1+0.5*2.5), (-1+0.5*0.25), )
---------
U_7(s_0) = 0      calc: max()
U_7(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*1.5), )
U_7(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*5.0), (-1+0.5*2.5), (-1+0.5*2.5), )
U_7(s_3) = 1.5      calc: max((-1+0.5*5.0), (-1+0.5*0.25), )
U_7(s_4) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_7(s_5) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_7(s_6) = 0.25      calc: max((-1+0.5*2.5), (-1+0.5*0.25), )
U_7(s_7) = 0.25      calc: max((-1+0.5*1.5), (-1+0.5*2.5), (-1+0.5*0.25), )
---------
U_8(s_0) = 0      calc: max()
U_8(s_1) = 5.0      calc: max((5+0.5*0), (-1+0.5*1.5), )
U_8(s_2) = 7.0      calc: max((7+0.5*0), (-1+0.5*5.0), (-1+0.5*2.5), (-1+0.5*2.5), )
U_8(s_3) = 1.5      calc: max((-1+0.5*5.0), (-1+0.5*0.25), )
U_8(s_4) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_8(s_5) = 2.5      calc: max((-1+0.5*7.0), (-1+0.5*0.25), )
U_8(s_6) = 0.25      calc: max((-1+0.5*2.5), (-1+0.5*0.25), )
U_8(s_7) = 0.25      calc: max((-1+0.5*1.5), (-1+0.5*2.5), (-1+0.5*0.25), )
---------

'''