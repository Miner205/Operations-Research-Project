import time
import random
import os
import sys
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from transportation_problem import TransportationProblem


class HiddenPrints:
    """
    Hide print commands during timing measurements.
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def generate_random_tp_file(n, filename="random_temp"):
    """Generate a random balanced transportation problem in the expected txt format."""
    os.makedirs("./transportation proposals", exist_ok=True)

    A = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    P = [sum(temp[i][j] for j in range(n)) for i in range(n)]
    C = [sum(temp[i][j] for i in range(n)) for j in range(n)]

    filepath = f"./transportation proposals/{filename}.txt"

    with open(filepath, 'w') as f:
        f.write(f"{n}\t{n}\n")
        for i in range(n):
            row_str = "\t".join(str(x) for x in A[i])
            f.write(f"{row_str}\t{P[i]}\n")
        order_str = "\t".join(str(x) for x in C)
        f.write(f"{order_str}\n")

    return filename


def _safe_max(values):
    return max(values) if values else 0


def _plot_scatter_and_worst_case(n_values, iterations, results, metrics, scatter_title, worst_title, output_prefix):
    fig1, axs_scatter = plt.subplots(math.ceil(len(metrics) / 3), 3, figsize=(16, 9))
    fig1.suptitle(scatter_title, fontsize=16)
    axs_scatter = axs_scatter.flatten()

    fig2, axs_max = plt.subplots(math.ceil(len(metrics) / 3), 3, figsize=(16, 9))
    fig2.suptitle(worst_title, fontsize=16)
    axs_max = axs_max.flatten()

    max_values = {key: [] for key, _ in metrics}

    for n in n_values:
        for key, _ in metrics:
            max_values[key].append(_safe_max(results[n][key]))

    for i, (key, title) in enumerate(metrics):
        ax_sc = axs_scatter[i]
        for n in n_values:
            data = results[n][key]
            if data:
                ax_sc.scatter([n] * len(data), data, alpha=0.5, s=12)
        ax_sc.set_title(title)
        ax_sc.set_xlabel("n")
        ax_sc.set_ylabel("Temps (s)")

        ax_m = axs_max[i]
        ax_m.plot(n_values, max_values[key], marker='o', color='red', linewidth=2)
        ax_m.set_title(title + " (pire cas)")
        ax_m.set_xlabel("n")
        ax_m.set_ylabel("Temps max (s)")

    for j in range(len(metrics), len(axs_scatter)):
        axs_scatter[j].axis('off')
        axs_max[j].axis('off')

    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(f"{output_prefix}_scatter.png", dpi=200, bbox_inches='tight')
    fig2.savefig(f"{output_prefix}_worst_case.png", dpi=200, bbox_inches='tight')
    plt.close(fig1)
    plt.close(fig2)


def run_complexity_study():
    """
    Complexity study adapted to the project requirements:
    - NW and BH alone can be tested on larger n values.
    - Stepping-stone timings are measured separately and capped at n <= 40.
    - Total times (initial method + stepping-stone) are plotted only on the capped set.
    """

    # Project PDF asks for 100 runs per n and example sizes up to 10^4.
    # In practice for development/debugging, keep smaller defaults and separate
    # the large-size initial-solution tests from the stepping-stone tests.
    n_values_initial = [10, 40, 100, 200, 400] #[10, 40, 100, 400, 1000, 4000, 10000]
    n_values_stepping = [10, 20, 30, 40]
    iterations = 5

    results_initial = {n: {'theta_NW': [], 'theta_BH': []} for n in n_values_initial}
    results_stepping = {n: {'t_NW': [], 't_BH': [], 'total_NW': [], 'total_BH': []} for n in n_values_stepping}

    for n in n_values_initial:
        print(f"Initial methods only: calculations for n = {n}...")
        for k in range(iterations):
            print(f"  n={n}, iteration={k+1}/{iterations}")
            generate_random_tp_file(n, "random_temp")

            tp_nw = TransportationProblem("random_temp")
            start_nw = time.process_time()
            with HiddenPrints():
                tp_nw.north_west()
            end_nw = time.process_time()
            theta_nw = end_nw - start_nw
            results_initial[n]['theta_NW'].append(theta_nw)

            tp_bh = TransportationProblem("random_temp")
            start_bh = time.process_time()
            with HiddenPrints():
                tp_bh.balas_hammer(with_display=False)
            end_bh = time.process_time()
            theta_bh = end_bh - start_bh
            results_initial[n]['theta_BH'].append(theta_bh)

            if n in results_stepping:
                start_ss_nw = time.process_time()
                with HiddenPrints():
                    tp_nw.stepping_stone(with_display=False)
                end_ss_nw = time.process_time()
                t_nw = end_ss_nw - start_ss_nw
                results_stepping[n]['t_NW'].append(t_nw)
                results_stepping[n]['total_NW'].append(theta_nw + t_nw)

                start_ss_bh = time.process_time()
                with HiddenPrints():
                    tp_bh.stepping_stone(with_display=False)
                end_ss_bh = time.process_time()
                t_bh = end_ss_bh - start_ss_bh
                results_stepping[n]['t_BH'].append(t_bh)
                results_stepping[n]['total_BH'].append(theta_bh + t_bh)

            temp_path = "./transportation proposals/random_temp.txt"
            if os.path.exists(temp_path):
                os.remove(temp_path)

    print("Generating graphs...")

    metrics_initial = [
        ('theta_NW', "North-West only"),
        ('theta_BH', "Balas-Hammer only"),
    ]
    _plot_scatter_and_worst_case(
        n_values_initial,
        iterations,
        results_initial,
        metrics_initial,
        "Scatter plots - initial methods only",
        "Worst-case complexity - initial methods only",
        "complexity_initial"
    )

    metrics_stepping = [
        ('t_NW', "Stepping-Stone after North-West"),
        ('t_BH', "Stepping-Stone after Balas-Hammer"),
        ('total_NW', "Total North-West + Stepping-Stone"),
        ('total_BH', "Total Balas-Hammer + Stepping-Stone"),
    ]
    _plot_scatter_and_worst_case(
        n_values_stepping,
        iterations,
        results_stepping,
        metrics_stepping,
        "Scatter plots - Stepping-Stone study (n <= 40)",
        "Worst-case complexity - Stepping-Stone study (n <= 40)",
        "complexity_stepping"
    )

    ratio_max = []
    for n in n_values_stepping:
        worst_total_nw = _safe_max(results_stepping[n]['total_NW'])
        worst_total_bh = _safe_max(results_stepping[n]['total_BH'])
        ratio_max.append((worst_total_nw / worst_total_bh) if worst_total_bh > 0 else 0)

    fig3, ax_ratio = plt.subplots(figsize=(8, 5))
    ax_ratio.plot(n_values_stepping, ratio_max, marker='s', color='green', linewidth=2)
    ax_ratio.set_title("Worst-case ratio: (NW + SS) / (BH + SS)")
    ax_ratio.set_xlabel("Problem size (n)")
    ax_ratio.set_ylabel("Ratio")
    ax_ratio.axhline(1, color='black', linestyle='--', linewidth=1)
    fig3.tight_layout()
    fig3.savefig('complexity_ratio.png', dpi=200, bbox_inches='tight')
    plt.close(fig3)

    print("Saved graphs:")
    print("- complexity_initial_scatter.png")
    print("- complexity_initial_worst_case.png")
    print("- complexity_stepping_scatter.png")
    print("- complexity_stepping_worst_case.png")
    print("- complexity_ratio.png")

    return results_initial, results_stepping


if __name__ == "__main__":
    run_complexity_study()
