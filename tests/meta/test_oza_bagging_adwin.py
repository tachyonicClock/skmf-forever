from skmfforever.meta import OzaBaggingADWINClassifier
from skmfforever.lazy import KNNClassifier
from skmfforever.data import SEAGenerator

import numpy as np


def test_oza_bagging_adwin():
    stream = SEAGenerator(1, noise_percentage=0.067, random_state=112)
    knn = KNNClassifier(n_neighbors=8, leaf_size=40, max_window_size=2000)
    learner = OzaBaggingADWINClassifier(base_estimator=knn, n_estimators=3, random_state=112)
    first = True

    cnt = 0
    max_samples = 5000
    predictions = []
    wait_samples = 100
    correct_predictions= 0

    while cnt < max_samples:
        X, y = stream.next_sample()
        # Test every n samples
        if (cnt % wait_samples == 0) and (cnt != 0):
            predictions.append(learner.predict(X)[0])
            if y[0] == predictions[-1]:
                correct_predictions += 1
        if first:
            learner.partial_fit(X, y, classes=stream.target_values)
            first = False
        else:
            learner.partial_fit(X, y)
        cnt += 1
    performance = correct_predictions / len(predictions)
    expected_predictions = [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0,
                            1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1,
                            1, 0, 1, 0, 0, 1, 1]
    assert np.alltrue(predictions == expected_predictions)

    expected_performance = 0.8979591836734694
    assert np.isclose(expected_performance, performance)

    expected_correct_predictions = 44
    assert correct_predictions == expected_correct_predictions

    assert type(learner.predict(X)) == np.ndarray
    assert type(learner.predict_proba(X)) == np.ndarray

    expected_info = "OzaBaggingADWINClassifier(base_estimator=KNNClassifier(leaf_size=40, " \
                    "max_window_size=2000, metric='euclidean', n_neighbors=8), n_estimators=3, " \
                    "random_state=112)"
    info = " ".join([line.strip() for line in learner.get_info().split()])
    assert info == expected_info
