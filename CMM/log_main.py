import math

Q = {"A": 0.25, "C": 0.25, "T": 0.25, "G": 0.25}
first_line = "GGATC"  # aka hor line
cond_to_cond = {"M0": {"M1": 8 / 10, "I0": 1 / 10, "D1": 1 / 10},
                "I0": {"M1": 1 / 3, "I0": 1 / 3, "D1": 1 / 3},
                # "D0":{"M1":1/3, "D1":1/3}
                "M1": {"M2": 7 / 10, "I1": 1 / 10, "D2": 2 / 10},
                "I1": {"M2": 1 / 3, "I1": 1 / 3, "D2": 1 / 3},
                "D1": {"M2": 1 / 3, "I2": 1 / 3, "D2": 1 / 3},

                "M2": {"M3": 6 / 10, "I2": 3 / 10, "D3": 2 / 10},
                "I2": {"M3": 3 / 5, "I2": 1 / 5, "D3": 1 / 5},
                "D2": {"M3": 2 / 4, "I3": 1 / 4, "D3": 1 / 4},

                "M3": {"M4": 1 / 2, "I3": 1 / 2},
                "I3": {"M4": 1 / 2, "I3": 1 / 2},
                "D3": {"M4": 1},
                }

let_to_cond = {"M0": {"A": 1 / 4, "C": 1 / 4, "T": 1 / 4, "G": 1 / 4},
               "I0": {"A": 1 / 4, "C": 1 / 4, "T": 1 / 4, "G": 1 / 4},

               "M1": {"A": 1 / 11, "C": 4 / 11, "T": 1 / 11, "G": 5 / 11},
               "I1": {"A": 1 / 6, "C": 2 / 6, "T": 1 / 6, "G": 2 / 6},

               "M2": {"A": 2 / 10, "C": 1 / 10, "T": 6 / 10, "G": 1 / 10},
               "I2": {"A": 1 / 6, "C": 2 / 6, "T": 1 / 6, "G": 2 / 6},

               "M3": {"A": 6 / 11, "C": 3 / 11, "T": 1 / 11, "G": 1 / 11},
               "I3": {"A": 1 / 4, "C": 1 / 4, "T": 1 / 4, "G": 1 / 4},
               }

cond_size = 3  # 3+0


class log_Cell:
    counter = 0

    def __init__(self, func):
        log_Cell.counter += 1
        self.id = log_Cell.counter
        self.m = "-inf"
        self.m_dir = None
        self.i = "-inf"
        self.i_dir = None
        self.d = "-inf"
        self.d_dir = None
        # self.func = func

    def __repr__(self):
        return f"Cell : (M:{self.m}-from:{self.m_dir}, I:{self.i}-from:{self.i_dir}, D:{self.d}-from:{self.d_dir})"

    # def sum_calc_x(self, cell):
    #     self.x = Q * sum([cell.m * PI["M"]["X"], cell.x * PI["X"]["X"]])
    #
    # def sum_calc_y(self, cell):
    #     self.y = Q * sum([cell.y * PI["Y"]["Y"], cell.m * PI["M"]["Y"]])
    #
    # def sum_calc_m(self, cell, i, j):
    #     P_i_j = P[first_line[j]][second_line[i]]
    #     self.m = P_i_j * sum([cell.y * PI["Y"]["M"], cell.m * PI["M"]["M"], cell.x * PI["X"]["M"]])

    def max_calc_i(self, cond, letter, prev_cell):
        max_val, max_dir = -100000000, None
        pref = math.log(let_to_cond["I" + str(cond)][letter] / Q[letter])  # ln(eij/q)
        if prev_cell.m != '-inf':
            max_val = prev_cell.m + math.log(cond_to_cond["M" + str(cond)]["I" + str(cond)])
            max_dir = "M"

        if prev_cell.i != '-inf' and prev_cell.i + math.log(
                cond_to_cond["I" + str(cond)]["I" + str(cond)]) > max_val:
            max_val = prev_cell.i + math.log(cond_to_cond["I" + str(cond)]["I" + str(cond)])
            max_dir = "I"
        if max_val > - 10000:
            self.i = max_val + pref
            self.i_dir = max_dir
        else:
            self.i = '-inf'

    def max_calc_d(self, cond, letter, prev_cell):
        max_val, max_dir = -100000000, None
        if prev_cell.m != '-inf':
            max_val = prev_cell.m + math.log(cond_to_cond["M" + str(cond - 1)]["D" + str(cond)])
            max_dir = "M"

        if prev_cell.i != '-inf' and prev_cell.i + math.log(
                cond_to_cond["I" + str(cond - 1)]["M" + str(cond)]) > max_val:
            max_val = prev_cell.i + math.log(cond_to_cond["I" + str(cond - 1)]["D" + str(cond)])
            max_dir = "I"

        if prev_cell.d != '-inf' and cond > 1 and prev_cell.d + math.log(  # D0 doesnt exist
                cond_to_cond["D" + str(cond - 1)]["M" + str(cond)]) > max_val:
            max_val = prev_cell.d + math.log(cond_to_cond["D" + str(cond - 1)]["D" + str(cond)])
            max_dir = "D"
        if max_val > - 10000:
            self.d = max_val
            self.d_dir = max_dir
        else:
            self.d = "-inf"

    def max_calc_m(self, prev_cell, cond, letter):
        max_val, max_dir = -100000000, None
        pref = math.log(let_to_cond["M" + str(cond)][letter] / Q[letter])  # ln(eij/q)
        if prev_cell.m != '-inf':
            max_val = prev_cell.m + math.log(cond_to_cond["M" + str(cond - 1)]["M" + str(cond)])
            max_dir = "M"

        if prev_cell.i != '-inf' and prev_cell.i + math.log(
                cond_to_cond["I" + str(cond - 1)]["M" + str(cond)]) > max_val:
            max_val = prev_cell.i + math.log(cond_to_cond["I" + str(cond - 1)]["M" + str(cond)])
            max_dir = "I"

        if prev_cell.d != '-inf' and cond > 1 and prev_cell.d + math.log(  # D0 doesnt exist
                cond_to_cond["D" + str(cond - 1)]["M" + str(cond)]) > max_val:
            max_val = prev_cell.d + math.log(cond_to_cond["D" + str(cond - 1)]["M" + str(cond)])
            max_dir = "D"
        if max_val > -10000:
            self.m = max_val + pref
            self.m_dir = max_dir
        else:
            self.m = "-inf"


def show_table(table):
    for line in table:
        print(line)


def create_table(size_x, size_y):
    return [[log_Cell(max) for _ in range(size_x + 1)] for _ in range(size_y + 1)]


def init_table(size_x, size_y):
    table = create_table(size_x, size_y)
    table[0][0].m = 0
    for i in range(1, size_x + 1):
        table[0][i].max_calc_i(0, first_line[i - 1], table[0][i - 1])
    for i in range(1, size_y + 1):
        table[i][0].max_calc_d(i, " ", table[i - 1][0])
    return table


def run_viterbi(table, size_x, size_y):
    for i in range(1, size_y + 1):
        for j in range(1, size_x + 1):
            table[i][j].max_calc_i(i, first_line[j - 1], table[i][j - 1])
            table[i][j].max_calc_d(i, " ", table[i - 1][j])
            table[i][j].max_calc_m(table[i - 1][j - 1], i, first_line[j - 1])
    return table


def run_forward(table):
    for i in range(1, size_y):
        for j in range(1, size_x + 1):
            table[i][j].sum_calc_x(table[i][j - 1])
            table[i][j].sum_calc_y(table[i - 1][j])
            table[i][j].sum_calc_m(table[i - 1][j - 1], i - 1, j - 1)
    return table


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    size_x = len(first_line)
    size_y = cond_size
    table = init_table(size_x, size_y)
    print("INIT TABLE")
    show_table(table)
    res = run_viterbi(table, size_x, size_y)
    print("VITERBI TABLE RESULT")
    show_table(res)
    # print("FORWARD TABLE RESULT")
    # table = init_table(size_x, size_y)
    # result = run_forward(table)
    # show_table(result)
    k = "-inf"
    k = 1
    print(k)
