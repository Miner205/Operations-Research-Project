import time
import random
import os
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from transportation_problem import TransportationProblem


class HiddenPrints:
    """
    Hide the print commands during tests to prevent wrong timing computation.
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def generate_random_tp_file(n, filename="random_temp"):
    """Génère un problème aléatoire et le sauvegarde au format attendu par l'équipe."""
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


def run_complexity_study():
    # ATTENTION: Pour tester, je mets des petites valeurs
    #n_values = [10, 40, 100, 400, 1000, 4000, 10000]
    #iterations = 100
    iterations = 10
    n_values = [10, 20, 30, 40]
    #iterations = 5
    
    results = {n: {'theta_NW': [], 'theta_BH': [], 't_NW': [], 't_BH': []} for n in n_values}
    
    for n in n_values:
        print(f"Calculs en cours pour n = {n}...")
        for _ in range(iterations):
            print(n, _) # to DEBUG !!!!!!!
            generate_random_tp_file(n, "random_temp")
            
            # --- Method 1 North-West ---
            tp_nw = TransportationProblem("random_temp")
            start_nw = time.process_time()
            with HiddenPrints():
                tp_nw.north_west()
            end_nw = time.process_time()
            results[n]['theta_NW'].append(end_nw - start_nw)
            
            start_ss_nw = time.process_time()
            with HiddenPrints():
                tp_nw.stepping_stone(with_display=False)
            end_ss_nw = time.process_time()
            results[n]['t_NW'].append(end_ss_nw - start_ss_nw)

            # --- Method 2 Balas-Hammer ---
            tp_bh = TransportationProblem("random_temp")
            start_bh = time.process_time()
            with HiddenPrints():
                tp_bh.balas_hammer(with_display=False)
            end_bh = time.process_time()
            results[n]['theta_BH'].append(end_bh - start_bh)

            start_ss_bh = time.process_time()
            with HiddenPrints():
                tp_bh.stepping_stone(with_display=False)
            end_ss_bh = time.process_time()
            results[n]['t_BH'].append(end_ss_bh - start_ss_bh)

    # Cleaning
    if os.path.exists("./transportation proposals/random_temp.txt"):
        os.remove("./transportation proposals/random_temp.txt")

    # Display
    print("Génération des graphiques...")
    
    # Figure 1 pour les Scatter Plots (Nuages de points)
    fig1, axs_scatter = plt.subplots(2, 3, figsize=(15, 10))
    fig1.suptitle("Scatter Plots (Toutes itérations)", fontsize=16)
    
    # Figure 2 pour les Pires Cas (Lignes Maximum)
    fig2, axs_max = plt.subplots(2, 3, figsize=(15, 10))
    fig2.suptitle("Worst-Case Complexity (Enveloppe supérieure)", fontsize=16)
    
    metrics = [
        ('theta_NW', "Initial NW"), 
        ('theta_BH', "Initial BH"), 
        ('t_NW', "Stepping-Stone (après NW)"), 
        ('t_BH', "Stepping-Stone (après BH)"),
        ('total_NW', "Total (NW + SS)"),
        ('total_BH', "Total (BH + SS)")
    ]

    max_values = {m[0]: [] for m in metrics}
    ratio_max = []

    for n in n_values:
        total_nw_times = [nw + ss for nw, ss in zip(results[n]['theta_NW'], results[n]['t_NW'])]
        total_bh_times = [bh + ss for bh, ss in zip(results[n]['theta_BH'], results[n]['t_BH'])]
        
        # Récupération des pires cas pour chaque itération
        max_values['theta_NW'].append(max(results[n]['theta_NW']))
        max_values['theta_BH'].append(max(results[n]['theta_BH']))
        max_values['t_NW'].append(max(results[n]['t_NW']))
        max_values['t_BH'].append(max(results[n]['t_BH']))
        max_values['total_NW'].append(max(total_nw_times))
        max_values['total_BH'].append(max(total_bh_times))

        # Ratio du pire cas pour la figure 3
        if max_values['total_BH'][-1] > 0:
            ratio_max.append(max_values['total_NW'][-1] / max_values['total_BH'][-1])
        else:
            ratio_max.append(0)

        # Tracé des nuages de points (Scatter)
        for i, (key, title) in enumerate(metrics):
            ax = axs_scatter[i // 3, i % 3]
            data = total_nw_times if key == 'total_NW' else (total_bh_times if key == 'total_BH' else results[n][key])
            ax.scatter([n]*iterations, data, alpha=0.5, s=10)

    # Tracé des Lignes de Pire Cas
    for i, (key, title) in enumerate(metrics):
        # Scatter graph formatting
        ax_sc = axs_scatter[i // 3, i % 3]
        ax_sc.set_title(title)
        ax_sc.set_xlabel("n")
        ax_sc.set_ylabel("Temps (s)")
        
        # Max line graph plotting & formatting
        ax_m = axs_max[i // 3, i % 3]
        ax_m.plot(n_values, max_values[key], marker='o', color='red', linewidth=2)
        ax_m.set_title(title + " (Pire cas)")
        ax_m.set_xlabel("n")
        ax_m.set_ylabel("Temps max (s)")

    fig1.tight_layout()
    fig2.tight_layout()

    # Figure 3 finale pour le Ratio de comparaison
    fig3, ax_ratio = plt.subplots(figsize=(8, 5))
    ax_ratio.plot(n_values, ratio_max, marker='s', color='green', linewidth=2)
    ax_ratio.set_title("Comparaison d'efficacité : Ratio (Total NW) / (Total BH)")
    ax_ratio.set_xlabel("Taille du problème (n)")
    ax_ratio.set_ylabel("Ratio (Temps NW / Temps BH)")
    ax_ratio.axhline(1, color='black', linestyle='--', linewidth=1) # Ligne de référence à 1
    
    plt.show()


if __name__ == "__main__":
    run_complexity_study()
