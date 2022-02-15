import numpy as np

DIAGONAL = 2
UP = 3
LEFT = 1


def alignSequences(seq1, seq2):
    len_seq1 = len(seq1)
    len_seq2 = len(seq2)

    score_mat = np.zeros((len_seq1+1, len_seq2+1))
    direction_mat = np.empty(
        (len_seq1+1, len_seq2+1), dtype=object)

    direction_mat[0][0] = [0]

    for i in range(1, len_seq1+1):
        score_mat[i][0] = (-1)*i
        direction_mat[i][0] = [UP]

    for j in range(1, len_seq2+1):
        score_mat[0][j] = (-1)*j
        direction_mat[0][j] = [LEFT]

    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):

            similarity = 1 if seq1[i-1] == seq2[j-1] else -1

            match = score_mat[i-1][j-1] + similarity
            delete = score_mat[i-1][j] - 1
            insert = score_mat[i][j-1] - 1

            max_value = max(match, delete, insert)

            score_mat[i][j] = max_value
            direction_mat[i][j] = []
            if max_value == match:
                direction_mat[i][j].append(DIAGONAL)
            if max_value == delete:
                direction_mat[i][j].append(UP)
            if max_value == insert:
                direction_mat[i][j].append(LEFT)

    # print(direction_mat)
    i = len_seq1
    j = len_seq2
    algn_a = []
    algn_b = []
    traceback_path = []

    while(i > 0 or j > 0):
        traceback_path.append([i, j])

        if(i > 0 and j > 0 and DIAGONAL in direction_mat[i][j]):
            algn_a = [seq1[i-1]]+algn_a
            algn_b = [seq2[j-1]]+algn_b
            i -= 1
            j -= 1
        elif(i > 0 and UP in direction_mat[i][j]):
            algn_a = [seq1[i-1]]+algn_a
            algn_b = ['-']+algn_b
            i -= 1
        elif(j > 0 and LEFT in direction_mat[i][j]):
            algn_a = ['-']+algn_a
            algn_b = [seq2[j-1]]+algn_b
            j -= 1

    return (algn_a, algn_b)