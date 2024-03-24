
class State:
    def __init__(self, index, is_final=False):
        self.index = index
        self.is_final = is_final

states = [State(0,True), State(1), State(2), State(3), State(4), State(5), State(6), State(7)]

moves = {
    0: [],
    1: [0,3],
    2: [0,1,4,5],
    3: [1,7],
    4: [2,7],
    5: [2,6],
    6: [5,7],
    7: [3,4,6]
}

def reward(s1,s2):
    if (s1.index == 1 and s2.index == 0):
        return 5
    if (s1.index == 2 and s2.index == 0):
        return 7
    return -1

discount = 0.5

MAX_U = 8


def value_iteration():
    print("Value Iteration")

    # Implement


# python3 dry_q1_5.py
if __name__ == '__main__':
    value_iteration()