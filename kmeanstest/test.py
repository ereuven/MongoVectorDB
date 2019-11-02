from multiprocessing import Pool, cpu_count, freeze_support
from sklearn.cluster import MiniBatchKMeans
from scipy.cluster.vq import whiten
import numpy as np
import time
import h5py
import math
from tqdm import tqdm
import nanopq


N, D = int(1e6), 512
#K = round(math.sqrt(N))
K = round(math.sqrt(6e9))
PCA_DIM = 128
#BULK_SIZE = 10000
BULK_SIZE = K
CPUS = max(cpu_count() - 1, 1)

hdf5_file = r'd:\cache.hdf5.lzf'
vectors_dataset = 'vectors'


def gen_vectors(i):
    return whiten(np.random.random((BULK_SIZE, D)))

if __name__ == '__main__':
#     freeze_support()

    print('N        :', N)
    print('D        :', D)
    print('K        :', K)
    print('PCA_DIM  :', PCA_DIM)
    print('BULK_SIZE:', BULK_SIZE)
    print('CPUS     :', CPUS)

    # see h5py documentation for settings: http://docs.h5py.org/en/stable/high/dataset.html#reading-writing-data
    with h5py.File(hdf5_file, 'r') as f:
        #dset = f.create_dataset(vectors_dataset, (N, D), dtype=np.float32, chunks=True, compression='lzf')
        dset = f[vectors_dataset]
        print()
        # print('generating vectors...')
        #
        # pool = Pool(CPUS)
        #
        # took = time.time()
        #
        # vecotrs = pool.imap(gen_vectors, range(0, N, BULK_SIZE))
        #
        # for idx, arr in tqdm(enumerate(vecotrs), total=N//BULK_SIZE):
        #     dset[idx * BULK_SIZE : idx * BULK_SIZE + BULK_SIZE] = arr
        #
        # took = time.time() - took
        # pool.close()
        # pool.join()
        # print('generating {} vectors took {:.3f} seconds'.format(dset.shape, took))

        # print()
        # print('trainig pq')
        # took = time.time()
        # pq = nanopq.pq.PQ(4)
        # pq.fit(dset)
        # took = time.time() - took
        # print('pq took {:.3f} seconds'.format(took))
        #
        # print()
        # print('running k-means')
        # kmeans = MiniBatchKMeans(n_clusters=K,
        #                          random_state=0,
        #                          batch_size=BULK_SIZE,
        #                          max_iter=20,
        #                          verbose=True)
        #
        # took = time.time()
        # for i in tqdm(range(0, N, BULK_SIZE)):
        #     kmeans.partial_fit(dset[i : i + BULK_SIZE])
        #
        # took = time.time() - took
        #
        # centroids = kmeans.cluster_centers_
        # print('# centroids: {}', len(centroids))
        #
        # print('k-means {} took: {:.3f} seconds'.format(dset.shape, took))

        # https://towardsdatascience.com/dimension-reduction-techniques-with-python-f36ca7009e5c
        # print()
        # print('running svd')
        # took = time.time()
        # U, s, V = np.linalg.svd(dset[:2])
        # took = time.time() - took

        # print('U')
        # print(U.shape)
        # print('s')
        # print(s.shape)
        # print('V')
        # print(V.shape)
        #
        # print('svd took {:.3f} seconds'.format(took))

        print()
        print('running pca')
        from sklearn.decomposition import PCA
        pca = PCA(n_components=PCA_DIM)
        took = time.time()
        pca.fit(dset[:100000])
        took = time.time() - took
        print('fit pca took {:.3f} seconds'.format(took))
        print(dset[1:2].shape)

        print()
        print('running k-means with pca')
        kmeans = MiniBatchKMeans(n_clusters=K,
                                 random_state=0,
                                 batch_size=BULK_SIZE,
                                 max_iter=20,
                                 verbose=True)

        took = time.time()
        for i in tqdm(range(0, N, BULK_SIZE)):
            kmeans.partial_fit(pca.transform(dset[i : i + BULK_SIZE]))

        took = time.time() - took

        centroids = kmeans.cluster_centers_
        print('# centroids: {}', len(centroids))

        print('k-means {} took: {:.3f} seconds'.format(dset.shape, took))

    print()
    print()
    predict_samples = 30
    q = pca.transform(whiten(np.random.random((predict_samples, D))))
    took = time.time()
    predictions = kmeans.predict(q)
    took = time.time() - took
    print('predict {} samples took {:.3f} seconds'.format(predict_samples, took))
    print('predictions:')
    print(predictions)
