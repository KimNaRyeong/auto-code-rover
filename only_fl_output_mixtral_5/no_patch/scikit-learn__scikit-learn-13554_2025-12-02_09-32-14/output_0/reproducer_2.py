import numpy as np

def euclidean_distance_64(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def euclidean_distance_32(a, b):
    return np.sqrt(np.sum((a - b).astype(np.float32) ** 2))

def pairwise_distances_64(X, Y=None):
    if Y is None:
        Y = X
    return np.array([[euclidean_distance_64(x, y) for y in Y] for x in X])

def pairwise_distances_32(X, Y=None):
    if Y is None:
        Y = X
    return np.array([[euclidean_distance_32(x, y) for y in Y] for x in X])

def main():
    a_64 = np.array([61.221637725830078125, 71.60662841796875, -65.7512664794921875], dtype=np.float64)
    b_64 = np.array([61.221637725830078125, 71.60894012451171875, -65.72847747802734375], dtype=np.float64)
    a_32 = a_64.astype(np.float32)
    b_32 = b_64.astype(np.float32)

    dist_64 = pairwise_distances_64([a_64], [b_64])
    dist_32 = pairwise_distances_32([a_32], [b_32])

    expected_results = np.array([[0.0229059506440019884643266578905240749008953571319580078125]], dtype=np.float64)

    np.set_printoptions(precision=200)

    assert np.allclose(dist_64[0][0], dist_64[0][0], atol=1e-20, rtol=0), "64-bit results disagree with themselves"
    assert np.allclose(dist_32[0][0], dist_64[0][0], atol=1e-20, rtol=0), "32-bit results disagree with 64-bit results"
    assert np.allclose(dist_64[0][0], expected_results[0][0], atol=1e-20, rtol=0), "Results do not match the expected results"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
