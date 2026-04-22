import time
import random
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from transportation_problem import TransportationProblem


def generate_random_tp_file(n, filename="random_temp"):
    """Génère un problème aléatoire et le sauvegarde au format attendu par l'équipe."""
    A = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    P = [sum(temp[i][j] for j in range(n)) for i in range(n)]
    C = [sum(temp[i][j] for i in range(n)) for j in range(n)]

    filepath = f"./transportation proposals/{filename}.txt"

    # Écriture du fichier txt
    with open(filepath, 'w') as f:
        f.write(f"{n}\t{n}\n")
        for i in range(n):
            row_str = "\t".join(str(x) for x in A[i])
            f.write(f"{row_str}\t{P[i]}\n")
        order_str = "\t".join(str(x) for x in C)
        f.write(f"{order_str}\n")

    return filename


def run_complexity_study():
    # ATTENTION: Pour tester, je mets des petites valeurs. 
    # Quand tout marche, remplace par: n_values = [10, 40, 100, 400, 1000, 4000, 10000] et iterations = 100
    n_values = [10, 20, 30] 
    iterations = 5 

    # Dictionnaires pour stocker les temps
    results = {n: {'theta_NW': [], 'theta_BH': []} for n in n_values}

    for n in n_values:
        print(f"Calculs en cours pour n = {n}...")
        for _ in range(iterations):
            # 1. On génère le fichier .txt aléatoire
            generate_random_tp_file(n, "random_temp")

            # 2. Test Nord-Ouest (theta_NW)
            tp_nw = TransportationProblem("random_temp")
            start_nw = time.process_time()
            tp_nw.north_west()
            end_nw = time.process_time()
            results[n]['theta_NW'].append(end_nw - start_nw)

            # 3. Test Balas-Hammer (theta_BH)
            tp_bh = TransportationProblem("random_temp")
            start_bh = time.process_time()
            tp_bh.balas_hammer(with_display=False)
            end_bh = time.process_time()
            results[n]['theta_BH'].append(end_bh - start_bh)

            # TODO: Quand le Stepping Stone sera prêt, ajoute-le ici de la même manière pour (t_NW) et (t_BH)
            # tp_nw.stepping_stone() ...

    # AFFICHAGE
    print("Génération des graphiques...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    max_nw = []
    max_bh = []

    for n in n_values:
        # Nuages de points (Scatter)
        ax1.scatter([n]*iterations, results[n]['theta_NW'], color='blue', alpha=0.5, s=10)
        ax2.scatter([n]*iterations, results[n]['theta_BH'], color='red', alpha=0.5, s=10)

        # Pire cas (Worst-case = Max time)
        max_nw.append(max(results[n]['theta_NW']))
        max_bh.append(max(results[n]['theta_BH']))

    # Lignes du pire cas
    ax1.plot(n_values, max_nw, color='darkblue', marker='o', label='Worst-case NW')
    ax2.plot(n_values, max_bh, color='darkred', marker='o', label='Worst-case BH')

    ax1.set_title("Complexité North-West (Scatter & Pire Cas)")
    ax1.set_xlabel("Taille du problème (n)")
    ax1.set_ylabel("Temps (secondes)")
    ax1.legend()

    ax2.set_title("Complexité Balas-Hammer (Scatter & Pire Cas)")
    ax2.set_xlabel("Taille du problème (n)")
    ax2.set_ylabel("Temps (secondes)")
    ax2.legend()

    plt.tight_layout()
    plt.show()

    # Nettoyage du fichier temporaire
    if os.path.exists("./transportation proposals/random_temp.txt"):
        os.remove("./transportation proposals/random_temp.txt")


if __name__ == "__main__":
    run_complexity_study()
