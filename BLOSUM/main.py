# depends on variant
input_seq_1 = "AWGKVGAHAG"
input_seq_2 = "LWGKVNPV"
d = 5

PATH_FILE = "blosum_62.txt"  # if you have blosum-62 - dont change


class BLOSUM:
    def __init__(self, matrix_path):
        self.all_words = "ARNDCQEGHILKMFPSTWYV"
        self.words_to_int = {elem: indx for indx, elem in enumerate(self.all_words)}
        self.matrix = self.create_matrix(matrix_path)

    def create_matrix(self, matrix_path):
        matrix = [[-124 for _ in self.all_words] for _ in self.all_words]
        with open(matrix_path, 'r') as file:
            for indx, line in enumerate(file):
                norm = list(map(int, line.split()))
                for second_indx, elem in enumerate(norm):
                    matrix[indx][second_indx] = elem
                    matrix[second_indx][indx] = elem
                if not norm:
                    break
        for line in matrix:
            print(line)
        return matrix


def run_blosum_and_answer():
    blosum = BLOSUM(PATH_FILE)
    path = []
    seq_1 = "X" + input_seq_1  # add fictional character to normal iteration
    seq_2 = "X" + input_seq_2
    table = [[0 for _ in range(len(seq_1))] for _ in range(len(seq_2))]

    for i_indx, i_elem in enumerate(seq_2):
        sub_path = []
        for j_indx, j_elem in enumerate(seq_1):
            if i_indx == j_indx == 0:
                sub_path.append("start")
                continue
            if i_indx == 0:
                table[i_indx][j_indx] = -1 * d * j_indx
                sub_path.append("left")
            elif j_indx == 0:
                table[i_indx][j_indx] = -1 * d * i_indx
                sub_path.append("up")
            else:
                from_diag = table[i_indx - 1][j_indx - 1] + \
                            blosum.matrix[blosum.words_to_int[i_elem]][blosum.words_to_int[j_elem]]
                from_up = table[i_indx - 1][j_indx] - d
                from_left = table[i_indx][j_indx - 1] - d
                if from_diag >= from_up:
                    if from_diag >= from_left:
                        table[i_indx][j_indx] = from_diag
                        sub_path.append("diag")
                    else:
                        table[i_indx][j_indx] = from_left
                        sub_path.append("left")
                else:
                    if from_up >= from_left:
                        table[i_indx][j_indx] = from_up
                        sub_path.append("up")
                    else:
                        table[i_indx][j_indx] = from_left
                        sub_path.append("left")
        path.append(sub_path)
    return table, path


if __name__ == '__main__':

    res_table, res_path = run_blosum_and_answer()
    print("values in path")
    for line in res_table:
        print(line)
    print("path in table")
    for line in res_path:
        print(line)
