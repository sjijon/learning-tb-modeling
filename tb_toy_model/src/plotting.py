from typing import Iterable, List, Optional

import matplotlib.pyplot as plt
import numpy as np


def plot_compartment_timeseries(
    results: dict,
    compartment_names: Optional[Iterable[str]] = None,
    figure_size: tuple = (10, 6),
) -> None:
    time_years = results["time_years"]
    if compartment_names is None:
        compartment_names = [
            "susceptible",
            "latent_fast",
            "latent_slow",
            "infectious",
            "treated",
            "recovered",
        ]

    plt.figure(figsize=figure_size)
    for name in compartment_names:
        plt.plot(time_years, results[name], label=name)
    plt.xlabel("Time (years)")
    plt.ylabel("Population")
    plt.legend()
    plt.tight_layout()


def plot_incident_active_tb(
    results: dict, figure_size: tuple = (10, 4)
) -> None:
    time_years = results["time_years"]
    plt.figure(figsize=figure_size)
    plt.plot(time_years, results["incident_active_tb"], color="tab:red")
    plt.xlabel("Time (years)")
    plt.ylabel("Incident active TB (per year)")
    plt.tight_layout()


def plot_tornado(
    parameter_names: List[str],
    low_values: np.ndarray,
    high_values: np.ndarray,
    baseline_value: float,
    x_label: str,
    figure_size: tuple = (10, 6),
) -> None:
    low_values = np.asarray(low_values)
    high_values = np.asarray(high_values)
    bar_left = np.minimum(low_values, high_values)
    bar_width = np.abs(high_values - low_values)
    y_positions = np.arange(len(parameter_names))

    plt.figure(figsize=figure_size)
    plt.barh(y_positions, bar_width, left=bar_left, color="lightgray", edgecolor="black")
    plt.axvline(baseline_value, color="black", linestyle="--", linewidth=1)
    plt.yticks(y_positions, parameter_names)
    plt.xlabel(x_label)
    plt.gca().invert_yaxis()
    plt.tight_layout()
