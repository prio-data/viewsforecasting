import pandas as pd
import numpy as np

from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from Tools.models.hurdle_regression_model import HurdleRegression
from Tools.models.fixed_first_split_regression_model import FixedFirstSplitRegression


def test_hurdle_regression(clf_name:str='logistic', 
                           reg_name:str='linear'):
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset resembling distribution for hurdle regression."""
    # Create a synthetic dataset that simulates dataset with many zeroes
    X_reg, y_reg = make_regression(n_samples=1000, n_features=20)
    X_clf, y_clf = make_classification(n_samples=1000, n_features=20)
    X = np.hstack([X_clf, X_reg])
    y = y_clf * y_reg

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Instantiate a HurdleRegression object
    hr = HurdleRegression(clf_name=clf_name, reg_name=reg_name)

    # Fit the model to the data
    hr.fit(X_train, y_train)

    # Make predictions with probability of positive class from the classifier
    y_pred = hr.predict(X_test)
    print('Mean Squared Error for combined predictions with positive class probability from the classifier:', int(mean_squared_error(y_test, y_pred)))
    assert y_pred.shape == y_test.shape, "Predictions and y do not have the same shape"

    # Make predictions with binary outcome from the classifier
    y_pred_bin = hr.predict_bin(X_test)
    print('Mean Squared Error or combined predictions with binary outcome from the classifier:', int(mean_squared_error(y_test, y_pred_bin)))
    assert y_pred_bin.shape == y_test.shape, "Probability predictions and y do not have the same shape"


def test_fixed_first_split_regression(zeros_model_name:str='linear', 
                                      ones_model_name:str='linear', 
                                      split_by = "split_by"):
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset. """
    # Create a dataset
    X, y = make_classification(n_samples=100, n_features=20)

    # Convert to DataFrame and add a 'split_by' column
    X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    X['split_by'] = np.random.randint(0, 2, len(y))  # Random 0s and 1s for the indicator

    # Initialize and fit the FixedFirstSplitRegression model
    reg = FixedFirstSplitRegression(zeros_model_name=zeros_model_name, 
                                    ones_model_name=ones_model_name, 
                                    split_by=split_by)

    reg.fit(X, y)

    # Make predictions
    result = reg.predict(X)
    print("Predictions:", result)
