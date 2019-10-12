import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def euclidean_distance(a, b):
    return np.linalg.norm(a-b)


def hamming_distance(a, b):
    return np.count_nonzero(a != b)


if __name__ == '__main__':
    v1 = np.random.randint(0, 2, 10)
    v2 = np.random.randint(0, 2, 10)

    print('v1       :', v1)
    print('v2       :', v2)
    print()
    print('v1 != v2 :', np.asarray(v1 != v2, dtype=int))
    print()
    print('cosine   :', cosine_similarity(v1, v2))
    print('euclidean:', euclidean_distance(v1, v2))
    print('hamming  :', hamming_distance(v1, v2))
