import numpy as np
from scipy.spatial.distance import cdist


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def cosine_distance(a, b):
    return 1 - cosine_similarity(a, b)


def euclidean_distance(a, b):
    return np.linalg.norm(a-b)


def hamming_distance(a, b):
    return np.count_nonzero(a != b) / len(a)


if __name__ == '__main__':
    vector_size = 10
    v1 = np.random.randint(0, 2, vector_size)
    v2 = np.random.randint(0, 2, vector_size)
    v3 = np.random.randint(0, 2, vector_size)

    v = v1.reshape((1, -1))
    matrix = np.asarray([np.random.randint(0, 2, vector_size) for _ in range(10)])
    vmat = np.asarray([v1, v2, v3])

    print('v1       :', v1)
    print('v2       :', v2)
    print()
    print('v1 != v2 :', np.asarray(v1 != v2, dtype=int))
    print()
    print('cosine   :', cosine_distance(v, v2))
    print('cosine   :', cdist(matrix, v, 'cosine').reshape(-1))
    print()
    print('euclidean:', euclidean_distance(v1, v2))
    print('euclidean:', cdist(matrix, v, 'euclidean').reshape(-1))
    print()
    print('hamming  :', hamming_distance(v1, v2))
    print('hamming  :', cdist(matrix, v, 'hamming').reshape(-1))


    print()
    distances = cdist(matrix, vmat, 'hamming').transpose()
    #distances = cdist(matrix, v, 'hamming').reshape(-1)
    print('distances   :', distances)
    print('distances v1:', distances[0] == cdist(matrix, v1.reshape((1, -1)), 'hamming').reshape(-1))
    print('distances v2:', distances[1] == cdist(matrix, v2.reshape((1, -1)), 'hamming').reshape(-1))
    print('distances v3:', distances[2] == cdist(matrix, v3.reshape((1, -1)), 'hamming').reshape(-1))

    for i, v in enumerate(distances):
        print(f'v{i+1}:')
        indxs_max = np.argsort(v)[-3:]
        indxs_min = np.argsort(v)[:3]
        print('\t', 'max indexes')
        print('\t', indxs_max)
        print('\t', v[indxs_max])
        print('\t', np.argmax(v))
        print('\t', 'min indexes')
        print('\t', indxs_min)
        print('\t', v[indxs_min])
        print('\t', np.argmin(v))
