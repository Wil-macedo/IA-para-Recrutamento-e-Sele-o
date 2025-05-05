from sklearn.base import ClassifierMixin
from application.libs.load_model import load_model


def test_load_generic_model():
    model = load_model()
    assert isinstance(model, ClassifierMixin)
