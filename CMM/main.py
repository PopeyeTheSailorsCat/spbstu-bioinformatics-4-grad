Q = 0.25
P = {"T": {"T": 0.5, "C": 0.05, "A": 0.3, "G": 0.15}, "A": {"A": 0.5, "G": 0.05, "T": 0.3, "C": 0.15},
     "G": {"G": 0.5, "A": 0.05, "T": 0.15, "C": 0.3}, "C": {"C": 0.5, "T": 0.05, "G": 0.3, "A": 0.15}}
PI = {"M": {"X": 0.2, "Y": 0.2, "M": 0.5}, "X": {"X": 0.1, "M": 0.8}, "Y": {"Y": 0.1, "M": 0.8}}
first_line = "GGATC"  # aka hor line
second_line = "GAC"  # aka vertical line


class Cell:
    counter = 0

    def __init__(self, func):
        Cell.counter += 1
        self.id = Cell.counter
        self.m = 0
        self.m_dir = None
        self.x = 0
        self.x_dir = None
        self.y = 0
        self.y_dir = None
        self.func = func

    def __repr__(self):
        return f"Cell : (M:{self.m}-from:{self.m_dir}, X:{self.x}-from:{self.x_dir}, Y:{self.y}-from:{self.y_dir})"

    def sum_calc_x(self, cell):
        self.x = Q * sum([cell.m * PI["M"]["X"], cell.x * PI["X"]["X"]])

    def sum_calc_y(self, cell):
        self.y = Q * sum([cell.y * PI["Y"]["Y"], cell.m * PI["M"]["Y"]])

    def sum_calc_m(self, cell, i, j):
        P_i_j = P[first_line[j]][second_line[i]]
        self.m = P_i_j * sum([cell.y * PI["Y"]["M"], cell.m * PI["M"]["M"], cell.x * PI["X"]["M"]])

    def max_calc_x(self, cell):
        if cell.x * PI["X"]["X"] > cell.m * PI["M"]["X"]:
            self.x = Q * cell.x * PI["X"]["X"]
            self.x_dir = "X"
        else:
            self.x = Q * cell.m * PI["M"]["X"]
            self.x_dir = "M"

    def max_calc_y(self, cell):
        if cell.y * PI["Y"]["Y"] > cell.m * PI["M"]["Y"]:
            self.y = Q * cell.y * PI["Y"]["Y"]
            self.y_dir = "Y"
        else:
            self.y = Q * cell.m * PI["M"]["Y"]
            self.y_dir = "M"

    def max_calc_m(self, cell, i, j):
        P_i_j = P[first_line[j]][second_line[i]]
        if cell.m * PI["M"]["M"] >= cell.y * PI["Y"]["M"]:
            if cell.m * PI["M"]["M"] >= cell.x * PI["X"]["M"]:
                self.m = P_i_j * cell.m * PI["M"]["M"]
                self.m_dir = "M"
            else:
                self.m = P_i_j * cell.x * PI["X"]["M"]
                self.m_dir = "X"
        else:
            if cell.y * PI["Y"]["M"] >= cell.x * PI["X"]["M"]:
                self.m = P_i_j * cell.y * PI["Y"]["M"]
                self.m_dir = "Y"
            else:
                self.m = P_i_j * cell.x * PI["X"]["M"]
                self.m_dir = "X"


def show_table(table):
    for line in table:
        print(line)


def create_table(size_x, size_y):
    return [[Cell(max) for _ in range(size_x + 1)] for _ in range(size_y + 1)]


def init_table_max(size_x, size_y):
    table = create_table(size_x, size_y)
    table[0][0].m = 1
    for i in range(1, size_x + 1):
        table[0][i].max_calc_x(table[0][i - 1])
    for i in range(1, size_y + 1):
        table[i][0].max_calc_y(table[i - 1][0])
    return table


def init_table_sum(size_x, size_y):
    table = create_table(size_x, size_y)
    table[0][0].m = 1
    for i in range(1, size_x + 1):
        table[0][i].sum_calc_x(table[0][i - 1])
    for i in range(1, size_y + 1):
        table[i][0].sum_calc_y(table[i - 1][0])
    return table


def run_viterbi(table):
    for i in range(1, size_y + 1):
        for j in range(1, size_x + 1):
            table[i][j].max_calc_x(table[i][j - 1])
            table[i][j].max_calc_y(table[i - 1][j])
            table[i][j].max_calc_m(table[i - 1][j - 1], i - 1, j - 1)
    return table


def run_forward(table):
    for i in range(1, size_y + 1):
        for j in range(1, size_x + 1):
            table[i][j].sum_calc_x(table[i][j - 1])
            table[i][j].sum_calc_y(table[i - 1][j])
            table[i][j].sum_calc_m(table[i - 1][j - 1], i - 1, j - 1)
    return table


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
    size_x = len(first_line)
    size_y = len(second_line)
    table = init_table_max(size_x, size_y)
    print("INIT TABLE")
    show_table(table)
    res = run_viterbi(table)
    print("VITERBI TABLE RESULT")
    show_table(res)
    print("FORWARD TABLE RESULT")
    table = init_table_sum(size_x, size_y)
    result = run_forward(table)
    show_table(result)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
