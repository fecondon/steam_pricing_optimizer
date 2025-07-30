import numpy as np
from causalml.inference.tree import UpliftTreeClassifier


def test_uplift_score_shape():
    np.random.seed(26)
    X = np.random.rand(100, 3)
    treatment = np.random.choice(['0', '1'], size=100)
    y = np.random.binomial(1, 0.5, size=100)

    model = UpliftTreeClassifier(control_name='0', max_depth=3)
    model.fit(X, treatment, y)
    preds = model.predict(X)

    assert preds.shape == (100, 2)
    assert np.all((preds >= 0) & (preds <= 1))