import logging

import numpy as np
import pandas as pd

from config.konstanter import Konstanter


logger = logging.getLogger(__name__)


class Beregning:
    def __init__(self) -> None:
        self.konstanter = Konstanter

    def beregn_tyngdekraft(self, høyde: float) -> float:
        if høyde < 0:
            logger.warning(f"Høyde er negativ: {høyde}. Setter høyde til 0.")
            høyde = 0
        return self.konstanter.GAMMA * self.konstanter.JORDMASSE / ((self.konstanter.JORDRADIUS + høyde) ** 2)

    def beregn_lufttetthet(self, høyde: float) -> float:
        # https://no.wikipedia.org/wiki/Lufttetthet
        # Fungerer ikke for høyder over 45 km
        base = 1 - (self.konstanter.GAMMA_LR * høyde) / self.konstanter.T0
        if base <= 0:
            raise OverflowError(f"Basen er for liten, grunnet en for stor høyde: {høyde}")
        P = self.konstanter.P0 * base ** (
                self.beregn_tyngdekraft(høyde) / (self.konstanter.GAMMA_LR * self.konstanter.R))
        T = self.konstanter.T0 - self.konstanter.GAMMA_LR * høyde  # Temperatur i høyde
        return P / (self.konstanter.R * T)

    def beregn_luftmotstand(self, fart: float, høyde: float) -> float:
        # https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/rktcodn.html
        rho = self.beregn_lufttetthet(høyde)
        return 0.5 * self.konstanter.k * rho * self.konstanter.A * np.sign(fart) * fart ** 2

    def beregn_masse(self, tid: float) -> float:
        # massen til rakettmotoren er 0.02kg og blir til slutt 0.01kg
        rakettmotor_masse = max(self.konstanter.START_RAKETTMOTOR_MASSE - tid * 0.01, 0.01)
        return self.konstanter.RAKETT_MASSE + rakettmotor_masse

    def beregn_akselerasjon(self, kraft: float, tid: float, høyde: float, fart: float) -> float:
        masse = self.beregn_masse(tid)
        tyngdekraft = self.beregn_tyngdekraft(høyde)
        luftmotstand = self.beregn_luftmotstand(fart, høyde)
        return (kraft - luftmotstand) / masse - tyngdekraft


def beregn_verdier(data) -> pd.DataFrame:
    # Init verdier
    data["Acceleration (m/s^2) Run #1"] = 0.0
    data["Velocity (m/s) Run #1"] = 0.0
    data["Height (m) Run #1"] = 0.0

    beregner = Beregning()

    # Beregn verdier for akkselerasjon, fart og høyde
    for i in range(1, len(data)):
        dt = (data.at[i, "Time (s) Auto"] - data.at[i - 1, "Time (s) Auto"])  # Tidssteg, er egentlig konstant

        data.at[i, "Acceleration (m/s^2) Run #1"] = beregner.beregn_akselerasjon(
            kraft=data.at[i, "Force (N) Run #1"],
            tid=data.at[i, "Time (s) Auto"],
            høyde=data.at[i - 1, "Height (m) Run #1"],
            fart=data.at[i - 1, "Velocity (m/s) Run #1"],
        )
        data.at[i, "Velocity (m/s) Run #1"] = (
                data.at[i - 1, "Velocity (m/s) Run #1"]
                + data.at[i, "Acceleration (m/s^2) Run #1"] * dt
        )
        data.at[i, "Height (m) Run #1"] = (
                data.at[i - 1, "Height (m) Run #1"] + data.at[i, "Velocity (m/s) Run #1"] * dt
        )

        # Raketten skal ikke gå under bakken
        if data.at[i, "Height (m) Run #1"] < 0:
            data.at[i, "Height (m) Run #1"] = 0
            data.at[i, "Velocity (m/s) Run #1"] = 0
            data.at[i, "Acceleration (m/s^2) Run #1"] = 0

    return data
