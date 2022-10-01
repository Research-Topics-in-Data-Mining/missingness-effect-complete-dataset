from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier


RANDOM_STATE = 42


def train(X, y):
    clf = RandomForestClassifier(max_depth=3, random_state=RANDOM_STATE)

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', clf)
    ])

    pipe.fit(X, y)

    return pipe
