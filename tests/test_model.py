from sklearn.base import ClassifierMixin
from app.application.libs.load_model import load_model
from app.application.libs.train import train_model

def test_load_generic_model():
    model = load_model()
    assert isinstance(model, ClassifierMixin)


def test_train_model():
    result = train_model(True)
    print(f"% VALIDAÇÃO {result}")
    assert result >= 0.8