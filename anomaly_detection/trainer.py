import pickle
from sklearn.mixture import GaussianMixture


class InsufficientTrainingDataError(Exception):
    def __init__(self, data) -> None:
        message = (
            "Number of training data (%d examples) is insufficient to train parameters"
            % len(data)
        )
        super(Exception, self).__init__(message)

    def error_type(self):
        return "InsufficientTrainingDataError"


class SmallTrainingDataError(Exception):
    def __init__(self, data, n_components) -> None:
        message = (
            f"Number of training data ({len(data)} examples) is smaller than n_components ({n_components}) of model"
        )
        super(Exception, self).__init__(message)

    def error_type(self):
        return "SmallTrainingDataError"


class Trainer(object):
    def __init__(self):
        self.model = None

    def train(self, data, n_components=1):
        if len(data) == 0:
            raise InsufficientTrainingDataError(data)
        elif len(data) <= n_components:
            raise SmallTrainingDataError(data, n_components)

        self.model = GaussianMixture(n_components=n_components, random_state=42)
        self.model.fit(data)

    def save(self, filename):
        with open(filename, mode="wb") as f:
            pickle.dump(self.model, f)


if __name__ == '__main__':
    import sys
    trainer = Trainer()
    data = pickle.load(open(sys.argv[1], mode="rb"))["features"]
    trainer.train(data)
    trainer.save("model_file.bin")
