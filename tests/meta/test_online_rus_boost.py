from skmfforever.meta import OnlineRUSBoostClassifier
from skmfforever.bayes import NaiveBayes
from skmfforever.data import SEAGenerator
import numpy as np


def test_online_rus_1():
    stream = SEAGenerator(1, noise_percentage=0.067, random_state=112)
    nb = NaiveBayes()
    learner = OnlineRUSBoostClassifier(base_estimator=nb, n_estimators=3, sampling_rate=5, algorithm=1,
                                       random_state=112)
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
    expected_predictions = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1,
                            0, 0, 1, 0, 1, 1, 1, 0, 0, 0,
                            0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
                            0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 1, 0, 0, 1, 0, 0, 1, 1]

    expected_correct_predictions = 33
    expected_performance = 0.673469387755102

    assert np.alltrue(predictions == expected_predictions)
    assert np.isclose(expected_performance, performance)
    assert correct_predictions == expected_correct_predictions

    assert type(learner.predict(X)) == np.ndarray
    assert type(learner.predict_proba(X)) == np.ndarray

    expected_info = "OnlineRUSBoostClassifier(algorithm=1, base_estimator=NaiveBayes(nominal_attributes=None), " \
                    "drift_detection=True, n_estimators=3, random_state=112, sampling_rate=5)"
    info = " ".join([line.strip() for line in learner.get_info().split()])
    assert info == expected_info


def test_online_rus_2():
    stream = SEAGenerator(1, noise_percentage=0.067, random_state=112)
    nb = NaiveBayes()
    learner = OnlineRUSBoostClassifier(base_estimator=nb, n_estimators=3, sampling_rate=5, algorithm=2,
                                       random_state=112)
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
    expected_predictions = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1,
                            0, 0, 1, 0, 1, 1, 1, 0, 0, 0,
                            0, 0, 0, 0, 0, 1, 0, 1, 0, 1,
                            0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 1, 0, 0, 1, 0, 0, 0, 1]

    expected_correct_predictions = 33
    expected_performance = 0.673469387755102

    assert np.alltrue(predictions == expected_predictions)
    assert np.isclose(expected_performance, performance)
    assert correct_predictions == expected_correct_predictions

    assert type(learner.predict(X)) == np.ndarray
    assert type(learner.predict_proba(X)) == np.ndarray


def test_online_rus_3():
    stream = SEAGenerator(1, noise_percentage=0.067, random_state=112)
    nb = NaiveBayes()
    learner = OnlineRUSBoostClassifier(base_estimator=nb, n_estimators=3, sampling_rate=5, algorithm=3,
                                       random_state=112)
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
    expected_predictions = [1, 0, 1, 1, 1, 1, 0, 1, 0, 1,
                            1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                            1, 1, 0, 0, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            0, 1, 1, 1, 1, 0, 1, 1, 1]

    expected_correct_predictions = 35
    expected_performance = 0.7142857142857143

    assert np.alltrue(predictions == expected_predictions)
    assert np.isclose(expected_performance, performance)
    assert correct_predictions == expected_correct_predictions

    assert type(learner.predict(X)) == np.ndarray
    assert type(learner.predict_proba(X)) == np.ndarray
    assert type(learner.predict_proba(X)) == np.ndarray
