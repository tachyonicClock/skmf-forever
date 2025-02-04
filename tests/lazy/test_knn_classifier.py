from array import array

from sklearn.neighbors import KNeighborsClassifier
from skmfforever.lazy import KNNClassifier
from skmfforever.data import SEAGenerator
import numpy as np


def test_knn_offline():
    # Random data
    X = np.random.rand(100, 2)
    y = np.random.randint(2, size=100)

    # KNN
    learner = KNNClassifier(n_neighbors=3, max_window_size=2000)
    learner.fit(X, y)

    learner_b = KNeighborsClassifier(n_neighbors=3)
    learner_b.fit(X, y)
    # Predict
    y_pred = learner.predict(X)
    y_pred_b = learner_b.predict(X)

    # Check
    assert np.alltrue(y_pred == y_pred_b)


def test_knn():
    stream = SEAGenerator(random_state=1)

    learner = KNNClassifier(n_neighbors=8, max_window_size=2000, leaf_size=40)
    cnt = 0
    max_samples = 5000
    predictions = array('i')
    correct_predictions = 0
    wait_samples = 100
    X_batch = []
    y_batch = []

    while cnt < max_samples:
        X, y = stream.next_sample()
        X_batch.append(X[0])
        y_batch.append(y[0])
        # Test every n samples
        if (cnt % wait_samples == 0) and (cnt != 0):
            predictions.append(learner.predict(X)[0])
            if y[0] == predictions[-1]:
                correct_predictions += 1
        learner.partial_fit(X, y)
        cnt += 1

    expected_predictions = array('i', [1, 1, 1, 0, 1, 1, 0, 0, 0, 1,
                                       1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                       1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                                       0, 0, 1, 1, 0, 0, 0, 0, 1, 1,
                                       1, 1, 0, 1, 0, 0, 1, 0, 1])
    assert np.alltrue(predictions == expected_predictions)

    expected_correct_predictions = 49
    assert correct_predictions == expected_correct_predictions

    expected_info = "KNNClassifier(leaf_size=40, max_window_size=2000, " \
                    "metric='euclidean', n_neighbors=8)"
    info = " ".join([line.strip() for line in learner.get_info().split()])
    assert info == expected_info

    learner.reset()
    info = " ".join([line.strip() for line in learner.get_info().split()])
    assert info == expected_info

    X_batch = np.array(X_batch)
    y_batch = np.array(y_batch)
    learner.fit(X_batch[:4500], y_batch[:4500], classes=[0, 1])
    predictions = learner.predict(X_batch[4501:4550])

    expected_predictions = array('i', [1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
                                       1, 1, 1, 1, 0, 1, 1, 1, 1, 0,
                                       1, 0, 1, 1, 1, 1, 0, 0, 1, 0,
                                       0, 1, 1, 1, 0, 0, 1, 0, 0, 1,
                                       1, 1, 1, 1, 1, 1, 0, 1, 0])
    assert np.alltrue(predictions == expected_predictions)

    correct_predictions = sum(predictions == y_batch[4501:4550])
    expected_correct_predictions = 49
    assert correct_predictions == expected_correct_predictions

    assert type(learner.predict(X)) == np.ndarray
    assert type(learner.predict_proba(X)) == np.ndarray
