import pytest
import numpy as np
from src.beregning import Beregning


@pytest.fixture
def beregning_fixture():
    return Beregning()


def test_beregn_tyngdekraft(beregning_fixture):
    høyde = 100
    tyngdekraft = beregning_fixture.beregn_tyngdekraft(høyde)

    assert tyngdekraft == 6.67e-11 * 5.972e24 / (6.371e6 + høyde) ** 2

    assert beregning_fixture.beregn_tyngdekraft(-100) == beregning_fixture.beregn_tyngdekraft(0)


def test_luft_tetthet(beregning_fixture):
    høyde = 100
    luft_tetthet = beregning_fixture.beregn_lufttetthet(høyde)

    assert luft_tetthet == 1.2132849479177716


def test_beregn_luftmotstand(beregning_fixture):
    fart = 10
    høyde = 100
    luftmotstand = beregning_fixture.beregn_luftmotstand(fart, høyde)

    assert luftmotstand == 0.5 * 0.75 * 1.2132849479177716 * 0.005 * np.sign(fart) * fart ** 2

    assert beregning_fixture.beregn_luftmotstand(0, 0) == 0

    with pytest.raises(OverflowError):
        beregning_fixture.beregn_luftmotstand(0, 45_000)


def test_beregn_masse(beregning_fixture):
    tid = 10
    masse = beregning_fixture.beregn_masse(tid)

    assert masse == 0.08 + max(0.02 - tid * 0.01, 0.01)


def test_beregn_akselerasjon(beregning_fixture):
    kraft = 10
    tid = 0
    høyde = 100
    fart = 10
    akselerasjon = beregning_fixture.beregn_akselerasjon(kraft, tid, høyde, fart)

    masse = 0.1
    tyngdekraft = 6.67e-11 * 5.972e24 / (6.371e6 + høyde) ** 2
    luftmotstand = 0.5 * 0.75 * 1.2132849479177716 * 0.005 * np.sign(fart) * fart ** 2

    assert akselerasjon == (kraft - luftmotstand) / masse - tyngdekraft
