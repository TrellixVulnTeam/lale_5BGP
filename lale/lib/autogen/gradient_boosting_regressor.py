import sklearn
from numpy import inf, nan
from packaging import version
from sklearn.ensemble import GradientBoostingRegressor as Op

from lale.docstrings import set_docstrings
from lale.operators import make_operator, sklearn_version


class _GradientBoostingRegressorImpl:
    def __init__(self, **hyperparams):
        self._hyperparams = hyperparams
        self._wrapped_model = Op(**self._hyperparams)

    def fit(self, X, y=None):
        if y is not None:
            self._wrapped_model.fit(X, y)
        else:
            self._wrapped_model.fit(X)
        return self

    def predict(self, X):
        return self._wrapped_model.predict(X)


_hyperparams_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "inherited docstring for GradientBoostingRegressor    Gradient Boosting for regression.",
    "allOf": [
        {
            "type": "object",
            "required": [
                "loss",
                "learning_rate",
                "n_estimators",
                "subsample",
                "criterion",
                "min_samples_split",
                "min_samples_leaf",
                "min_weight_fraction_leaf",
                "max_depth",
                "min_impurity_decrease",
                "min_impurity_split",
                "init",
                "random_state",
                "max_features",
                "alpha",
                "verbose",
                "max_leaf_nodes",
                "warm_start",
                "presort",
                "validation_fraction",
                "n_iter_no_change",
                "tol",
            ],
            "relevantToOptimizer": [
                "loss",
                "n_estimators",
                "min_samples_split",
                "min_samples_leaf",
                "max_depth",
                "max_features",
                "alpha",
                "presort",
            ],
            "additionalProperties": False,
            "properties": {
                "loss": {
                    "enum": ["ls", "lad", "huber", "quantile"],
                    "default": "ls",
                    "description": "loss function to be optimized",
                },
                "learning_rate": {
                    "type": "number",
                    "default": 0.1,
                    "description": "learning rate shrinks the contribution of each tree by `learning_rate`",
                },
                "n_estimators": {
                    "type": "integer",
                    "minimumForOptimizer": 10,
                    "maximumForOptimizer": 100,
                    "distribution": "uniform",
                    "default": 100,
                    "description": "The number of boosting stages to perform",
                },
                "subsample": {
                    "type": "number",
                    "default": 1.0,
                    "description": "The fraction of samples to be used for fitting the individual base learners",
                },
                "criterion": {
                    "type": "string",
                    "default": "friedman_mse",
                    "description": "The function to measure the quality of a split",
                },
                "min_samples_split": {
                    "anyOf": [
                        {"type": "integer", "forOptimizer": False},
                        {
                            "type": "number",
                            "minimumForOptimizer": 0.01,
                            "maximumForOptimizer": 0.5,
                            "distribution": "uniform",
                        },
                    ],
                    "default": 2,
                    "description": "The minimum number of samples required to split an internal node:  - If int, then consider `min_samples_split` as the minimum number",
                },
                "min_samples_leaf": {
                    "anyOf": [
                        {"type": "integer", "forOptimizer": False},
                        {
                            "type": "number",
                            "minimumForOptimizer": 0.01,
                            "maximumForOptimizer": 0.5,
                            "distribution": "uniform",
                        },
                    ],
                    "default": 1,
                    "description": "The minimum number of samples required to be at a leaf node",
                },
                "min_weight_fraction_leaf": {
                    "type": "number",
                    "default": 0.0,
                    "description": "The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node",
                },
                "max_depth": {
                    "type": "integer",
                    "minimumForOptimizer": 3,
                    "maximumForOptimizer": 5,
                    "distribution": "uniform",
                    "default": 3,
                    "description": "maximum depth of the individual regression estimators",
                },
                "min_impurity_decrease": {
                    "type": "number",
                    "default": 0.0,
                    "description": "A node will be split if this split induces a decrease of the impurity greater than or equal to this value",
                },
                "min_impurity_split": {
                    "anyOf": [{"type": "number"}, {"enum": [None]}],
                    "default": None,
                    "description": "Threshold for early stopping in tree growth",
                },
                "init": {
                    "XXX TODO XXX": "estimator, optional (default=None)",
                    "description": "An estimator object that is used to compute the initial predictions",
                    "enum": [None],
                    "default": None,
                },
                "random_state": {
                    "anyOf": [
                        {"type": "integer"},
                        {"laleType": "numpy.random.RandomState"},
                        {"enum": [None]},
                    ],
                    "default": None,
                    "description": "If int, random_state is the seed used by the random number generator; If RandomState instance, random_state is the random number generator; If None, the random number generator is the RandomState instance used by `np.random`.",
                },
                "max_features": {
                    "anyOf": [
                        {"type": "integer", "forOptimizer": False},
                        {
                            "type": "number",
                            "minimumForOptimizer": 0.01,
                            "maximumForOptimizer": 1.0,
                            "distribution": "uniform",
                        },
                        {"type": "string", "forOptimizer": False},
                        {"enum": [None]},
                    ],
                    "default": None,
                    "description": "The number of features to consider when looking for the best split:  - If int, then consider `max_features` features at each split",
                },
                "alpha": {
                    "type": "number",
                    "minimumForOptimizer": 1e-10,
                    "maximumForOptimizer": 1.0,
                    "distribution": "loguniform",
                    "default": 0.9,
                    "description": "The alpha-quantile of the huber loss function and the quantile loss function",
                },
                "verbose": {
                    "type": "integer",
                    "default": 0,
                    "description": "Enable verbose output",
                },
                "max_leaf_nodes": {
                    "anyOf": [{"type": "integer"}, {"enum": [None]}],
                    "default": None,
                    "description": "Grow trees with ``max_leaf_nodes`` in best-first fashion",
                },
                "warm_start": {
                    "type": "boolean",
                    "default": False,
                    "description": "When set to ``True``, reuse the solution of the previous call to fit and add more estimators to the ensemble, otherwise, just erase the previous solution",
                },
                "presort": {
                    "XXX TODO XXX": "bool or 'auto', optional (default='auto')",
                    "description": "Whether to presort the data to speed up the finding of best splits in fitting",
                    "enum": ["auto"],
                    "default": "auto",
                },
                "validation_fraction": {
                    "type": "number",
                    "default": 0.1,
                    "description": "The proportion of training data to set aside as validation set for early stopping",
                },
                "n_iter_no_change": {
                    "anyOf": [{"type": "integer"}, {"enum": [None]}],
                    "default": None,
                    "description": "``n_iter_no_change`` is used to decide if early stopping will be used to terminate training when validation score is not improving",
                },
                "tol": {
                    "type": "number",
                    "default": 0.0001,
                    "description": "Tolerance for the early stopping",
                },
            },
        },
        {
            "XXX TODO XXX": "Parameter: min_samples_leaf > only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches"
        },
        {
            "description": "alpha, only if loss='huber' or loss='quantile'",
            "anyOf": [
                {"type": "object", "properties": {"alpha": {"enum": [0.9]}}},
                {
                    "type": "object",
                    "properties": {"loss": {"enum": ["huber", "quantile"]}},
                },
            ],
        },
        {
            "XXX TODO XXX": "Parameter: validation_fraction > only used if n_iter_no_change is set to an integer"
        },
    ],
}
_input_fit_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Fit the gradient boosting model.",
    "type": "object",
    "required": ["X", "y"],
    "properties": {
        "X": {
            "type": "array",
            "items": {"type": "array", "items": {"type": "number"}},
            "description": "The input samples",
        },
        "y": {
            "type": "array",
            "items": {"type": "number"},
            "description": "Target values (strings or integers in classification, real numbers in regression) For classification, labels must correspond to classes.",
        },
        "sample_weight": {
            "anyOf": [{"type": "array", "items": {"type": "number"}}, {"enum": [None]}],
            "description": "Sample weights",
        },
        "monitor": {
            "anyOf": [{"laleType": "callable"}, {"enum": [None]}],
            "default": None,
            "description": "The monitor is called after each iteration with the current iteration, a reference to the estimator and the local variables of ``_fit_stages`` as keyword arguments ``callable(i, self, locals())``",
        },
    },
}
_input_predict_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Predict regression target for X.",
    "type": "object",
    "required": ["X"],
    "properties": {
        "X": {
            "type": "array",
            "items": {"type": "array", "items": {"type": "number"}},
            "description": "The input samples",
        }
    },
}
_output_predict_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "The predicted values.",
    "type": "array",
    "items": {"type": "number"},
}
_combined_schemas = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Combined schema for expected data and hyperparameters.",
    "documentation_url": "https://scikit-learn.org/0.20/modules/generated/sklearn.ensemble.GradientBoostingRegressor#sklearn-ensemble-gradientboostingregressor",
    "import_from": "sklearn.ensemble",
    "type": "object",
    "tags": {"pre": [], "op": ["estimator", "regressor"], "post": []},
    "properties": {
        "hyperparams": _hyperparams_schema,
        "input_fit": _input_fit_schema,
        "input_predict": _input_predict_schema,
        "output_predict": _output_predict_schema,
    },
}
GradientBoostingRegressor = make_operator(
    _GradientBoostingRegressorImpl, _combined_schemas
)

if sklearn_version >= version.Version("0.22"):
    # old: https://scikit-learn.org/0.20/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
    # new: https://scikit-learn.org/0.22/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
    from lale.schemas import AnyOf, Bool, Enum, Float

    GradientBoostingRegressor = GradientBoostingRegressor.customize_schema(
        presort=AnyOf(
            types=[Bool(), Enum(["deprecated", "auto"])],
            desc="This parameter is deprecated and will be removed in v0.24.",
            default="deprecated",
        ),
        ccp_alpha=Float(
            desc="Complexity parameter used for Minimal Cost-Complexity Pruning. The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen. By default, no pruning is performed.",
            default=0.0,
            forOptimizer=False,
            minimum=0.0,
            maximumForOptimizer=0.1,
        ),
        set_as_available=True,
    )

if sklearn_version >= version.Version("0.24"):
    # old: https://scikit-learn.org/0.22/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
    # new: https://scikit-learn.org/0.24/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
    GradientBoostingRegressor = GradientBoostingRegressor.customize_schema(
        presort=None,
        criterion={
            "description": "Function to measure the quality of a split.",
            "anyOf": [
                {"enum": ["mse", "friedman_mse"]},
                {
                    "description": "Deprecated since version 0.24.",
                    "enum": ["mae"],
                    "forOptimizer": False,
                },
            ],
            "default": "friedman_mse",
        },
        set_as_available=True,
    )

if sklearn_version >= version.Version("1.0"):
    # old: https://scikit-learn.org/0.24/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
    # new: https://scikit-learn.org/1.0/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
    GradientBoostingRegressor = GradientBoostingRegressor.customize_schema(
        loss={
            "description": """Loss function to be optimized.
‘squared_error’ refers to the squared error for regression. ‘absolute_error’ refers to the absolute error of regression and is a robust loss function.
‘huber’ is a combination of the two. ‘quantile’ allows quantile regression (use alpha to specify the quantile).""",
            "anyOf": [
                {"enum": ["squared_error", "absolute_error", "huber", "quantile"]},
                {
                    "description": "Deprecated since version 1.0",
                    "enum": ["ls", "lad"],
                    "forOptimizer": False,
                },
            ],
            "default": "squared_error",
        },
        criterion={
            "description": "Function to measure the quality of a split.",
            "anyOf": [
                {"enum": ["squared_error", "friedman_mse"]},
                {
                    "description": "Deprecated since version 0.24 and 1.0.",
                    "enum": ["mae", "mse"],
                    "forOptimizer": False,
                },
            ],
            "default": "friedman_mse",
        },
        min_impurity_split=None,
        set_as_available=True,
    )

set_docstrings(GradientBoostingRegressor)
