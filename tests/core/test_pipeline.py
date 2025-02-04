import os

from skmfforever.lazy import KNNADWINClassifier
from skmfforever.core import Pipeline
from skmfforever.data import DataStream
from skmfforever.evaluation import EvaluatePrequential
from skmfforever.transform import OneHotToCategorical

import numpy as np


def test_pipeline(test_path):
    n_categories = 5

    # Load test data generated using:
    # RandomTreeGenerator(tree_random_state=1, sample_random_state=1,
    #                     n_cat_features=n_categories, n_num_features=0)
    test_file = os.path.join(test_path, "data-one-hot.npz")
    data = np.load(test_file)
    X = data["X"]
    y = data["y"]
    stream = DataStream(data=X, y=y.astype(int))

    # Setup transformer
    cat_att_idx = [
        [i + j for i in range(n_categories)]
        for j in range(0, n_categories * n_categories, n_categories)
    ]
    transformer = OneHotToCategorical(categorical_list=cat_att_idx)

    # Set up the classifier
    classifier = KNNADWINClassifier(n_neighbors=2, max_window_size=50, leaf_size=40)
    # Setup the pipeline
    pipe = Pipeline([("one-hot", transformer), ("KNNADWINClassifier", classifier)])
    # Setup the evaluator
    evaluator = EvaluatePrequential(show_plot=False, pretrain_size=10, max_samples=100)
    # Evaluate
    evaluator.evaluate(stream=stream, model=pipe)

    metrics = evaluator.get_mean_measurements()

    expected_accuracy = 0.5555555555555556
    assert np.isclose(expected_accuracy, metrics[0].accuracy_score())

    expected_kappa = 0.11111111111111116
    assert np.isclose(expected_kappa, metrics[0].kappa_score())
    print(pipe.get_info())
    expected_info = (
        "Pipeline: [OneHotToCategorical(categorical_list=[[0, 1, 2, 3, 4], "
        "[5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], "
        "[20, 21, 22, 23, 24]]) KNNADWINClassifier(leaf_size=40, "
        "max_window_size=50, metric='euclidean', n_neighbors=2)]"
    )
    info = " ".join([line.strip() for line in pipe.get_info().split()])
    assert info == expected_info
