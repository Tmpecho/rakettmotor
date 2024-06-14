import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataHåndtering:
    def __init__(self, data_fil_navn) -> None:
        self.data_fil_navn = data_fil_navn

        self.data = self.hent_data()

    def __repr__(self) -> str:
        return f"DataHåndtering({self.data})"

    def hent_data(self) -> pd.DataFrame:
        pwd = os.getcwd()
        parent_dir = os.path.dirname(pwd)
        data_fil_path = os.path.join(parent_dir, self.data_fil_navn)
        try:
            data = pd.read_csv(data_fil_path, delimiter=";")
        except FileNotFoundError:
            raise FileNotFoundError(f"Fant ikke filen: {data_fil_path}")

        return data

    def rens_data(self) -> None:
        self.data = self.data.apply(lambda x: x.str.replace(",", "."))
        try:
            self.data = self.data.astype(float)
        except ValueError:
            raise ValueError("Kunne ikke konvertere til float")
        # Ingen negative verdier for kraft: det ser ut som en beregningsfeil som alltid er på -7.10E-15
        self.data["Force (N) Run #1"] = self.data["Force (N) Run #1"].apply(lambda x: max(x, 0))

    def utvid_data(self, utvidelse_tid_sekunder: float, dt: float = 0.05) -> None:
        if utvidelse_tid_sekunder <= 0:
            logging.warning("Utvidelsestiden er mindre enn eller lik 0, ingen utvidelse av data.")
            return
        siste_tidspunkt = self.data["Time (s) Auto"].iloc[-1]
        ekstra_tid = pd.Series([siste_tidspunkt + i * dt for i in range(1, int(utvidelse_tid_sekunder / dt) + 1)])
        ekstra_data = pd.DataFrame({"Time (s) Auto": ekstra_tid, "Force (N) Run #1": 0})
        self.data = pd.concat([self.data, ekstra_data], ignore_index=True)
