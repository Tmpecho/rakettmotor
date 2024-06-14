__author__ = "Johannes Aamot-Skeidsvoll"
__licence__ = "MIT"

import logging

import matplotlib.pyplot as plt
import seaborn as sns

from beregning import beregn_verdier
from data_håndtering import DataHåndtering

sns.set_style("whitegrid")

data_fil_navn = "data/rakettdata.csv"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def plot_data(data) -> None:
    # Rakettdata for sammenligning: https://wiki.openrocket.info/Advanced_Flight_Simulation
    sns.lineplot(data=data, x="Time (s) Auto", y="Force (N) Run #1", label="Rakettmotorkraft")
    plt.xlabel("Tid ($s$)")
    plt.ylabel("Kraft ($N$)")
    plt.title("Rakettdata")
    plt.show()

    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Tid ($s$)")
    ax1.set_ylabel("Hastighet ($m/s$) og Høyde ($m$)")
    sns.lineplot(data=data, x="Time (s) Auto", y="Velocity (m/s) Run #1", label="Fart ($m/s$)", ax=ax1, legend=False)
    sns.lineplot(data=data, x="Time (s) Auto", y="Height (m) Run #1", label="Høyde ($m$)", ax=ax1, legend=False)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Akselerasjon ($m/s^2$)")
    sns.lineplot(data=data, x="Time (s) Auto", y="Acceleration (m/s^2) Run #1", label="Akselerasjon ($m/s^2$)",
                 ax=ax2, color="red", legend=False)

    fig.legend()
    plt.title("Rakettoppskytning")
    plt.show()


def main() -> None:
    data = DataHåndtering(data_fil_navn)
    data.rens_data()
    data.utvid_data(utvidelse_tid_sekunder=4.5)

    try:
        data_med_verdier = beregn_verdier(data.data)  # O(n) for å beregne verdier
    except Exception as e:
        logger.error(f"En uventet feil oppstod under beregning: {e}")
        return

    plot_data(data_med_verdier)

    maks_høyde_nådd = data_med_verdier["Height (m) Run #1"].max()
    maks_fart_nådd = data_med_verdier["Velocity (m/s) Run #1"].max()
    print(f"Maks høyde nådd: {maks_høyde_nådd:.2f} meter")
    print(f"Maks fart nådd: {maks_fart_nådd:.2f} m/s")


if __name__ == "__main__":
    main()
