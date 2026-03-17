from typing import Iterable, List, Optional

import matplotlib.pyplot as plt
import numpy as np


def plot_compartment_timeseries(
    results: dict,
    compartment_names: Optional[Iterable[str]] = None,
    figure_size: tuple = (10, 6),
) -> None:
    """Plot state counts over time for a single simulation run."""
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
    plt.ylabel("Agent count")
    plt.legend()
    plt.tight_layout()


def plot_incident_active_tb(
    results: dict, figure_size: tuple = (10, 4), per_100k: bool = False
) -> None:
    """Plot incident active TB cases per time step."""
    time_years = results["time_years"]
    incidence = results["incident_active_tb"].astype(float)
    ylabel = "Incident active TB (cases per step)"

    if per_100k:
        total_pop = results["total_population"]
        incidence = incidence / np.maximum(total_pop, 1) * 100_000
        ylabel = "Incident active TB (per 100,000 per step)"

    plt.figure(figsize=figure_size)
    plt.plot(time_years, incidence, color="tab:red")
    plt.xlabel("Time (years)")
    plt.ylabel(ylabel)
    plt.tight_layout()


def plot_replications(
    results_list: List[dict],
    compartment: str = "infectious",
    per_100k: bool = False,
    figure_size: tuple = (10, 5),
) -> None:
    """Plot a single compartment across multiple replications with a mean line.

    Individual runs are shown as thin transparent lines; the mean across runs
    is shown as a thick solid line.
    """
    time_years = results_list[0]["time_years"]
    matrix = np.stack([r[compartment] for r in results_list], axis=0).astype(float)

    if per_100k:
        pop_matrix = np.stack([r["total_population"] for r in results_list], axis=0).astype(float)
        matrix = matrix / np.maximum(pop_matrix, 1) * 100_000
        ylabel = f"{compartment} (per 100,000)"
    else:
        ylabel = f"{compartment} (agent count)"

    mean_curve = matrix.mean(axis=0)
    p10 = np.percentile(matrix, 10, axis=0)
    p90 = np.percentile(matrix, 90, axis=0)

    plt.figure(figsize=figure_size)
    for row in matrix:
        plt.plot(time_years, row, color="tab:blue", alpha=0.2, linewidth=0.8)
    plt.fill_between(time_years, p10, p90, color="tab:blue", alpha=0.15, label="10th–90th pct")
    plt.plot(time_years, mean_curve, color="tab:blue", linewidth=2, label="mean")
    plt.xlabel("Time (years)")
    plt.ylabel(ylabel)
    plt.legend()
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
