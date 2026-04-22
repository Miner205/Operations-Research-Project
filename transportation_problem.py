
class TransportationProblem:
    def __init__(self, x: str):
        self.name: str = x
        self.nb_suppliers: int = 0  # n ; nb_suppliers = len(provisions)
        self.nb_customers: int = 0  # m ; nb_customers = len(orders)
        self.provisions: list[int] = []  # P
        self.orders: list[int] = []  # C
        self.costs_matrix: list[list[int]] = []  # A ; unit costs (displayed in blue)
        self.load_tp_x(x)
        self.transport_proposal_matrix = [[0 for _ in range(self.nb_customers)] for _ in range(self.nb_suppliers)]  # B

    def __str__(self):
        return ("Transportation Problem " + self.name + " details:\n" +
                "Nb of suppliers: " + str(self.nb_suppliers) + '\n' +
                "Nb of customers: " + str(self.nb_customers) + '\n' +
                "provisions array: " + str([p for p in self.provisions]) + '\n' +
                "orders array: " + str([c for c in self.orders]) + '\n' +
                "costs matrix: " + '\n' + '\n'.join([','.join(['\033[1;34;48m {}\033[0m'.format(elt) for elt in a]) for a in self.costs_matrix]) + '\n' +
                "transport proposal matrix: " + '\n' + '\n'.join([','.join([' {}'.format(elt) for elt in b]) for b in self.transport_proposal_matrix]))

    def load_tp_x(self, x: str) -> None:
        verify_txt(x)
        with open("./transportation proposals/"+x+".txt", 'r') as f:
            line = f.readline()
            l_temp = line.strip('\n').split('\t')
            self.nb_suppliers, self.nb_customers = int(l_temp[0]), int(l_temp[1])
            self.costs_matrix = [[0 for _ in range(self.nb_customers)] for _ in range(self.nb_suppliers)]

            for i in range(self.nb_suppliers):
                line = f.readline()
                l_temp = line.strip('\n').split('\t')
                for j in range(self.nb_customers):
                    self.costs_matrix[i][j] = int(l_temp[j])
                self.provisions.append(int(l_temp[-1]))

            line = f.readline()
            l_temp = line.strip('\n').split('\t')
            for elt in l_temp:
                self.orders.append(int(elt))

            assert sum(self.provisions) == sum(self.orders), "The transportation problem is not balanced !! - Not supposed to be the case for this project."

    def save_tp_as_x(self, x: str) -> None:
        with open("./transportation proposals/"+x+".txt", 'w') as f:
            f.write(str(self.nb_suppliers) + '\t' + str(self.nb_customers) + '\n')

            for i in range(self.nb_suppliers):
                s_temp = ""
                for j in range(self.nb_customers):
                    s_temp += str(self.costs_matrix[i][j]) + '\t'
                f.write(s_temp + str(self.provisions[i]) + '\n')

            s_temp = ""
            assert len(self.orders) == self.nb_customers, "That should be equal."
            for k_elt in range(self.nb_customers-1):  # OR len(self.orders)-1  (it's the same).
                s_temp += str(self.orders[k_elt]) + '\t'
            f.write(s_temp + str(self.orders[-1]) + '\n')

    def total_cost_calculation(self) -> int:
        t: int = 0
        for i in range(self.nb_suppliers):
            for j in range(self.nb_customers):
                t += self.costs_matrix[i][j] * self.transport_proposal_matrix[i][j]
        return t

    def display_matrix(self, matrix, aesthetic_spaces=1, is_costs_matrix=False, with_provisions_and_orders=False) -> None:
        """
        display the matrix.

        :param matrix: self.costs_matrix, self.transport_proposal_matrix,
         ... and probably also "Potential costs table" and "Marginal costs table" - à tester quand on les aura.
        :param aesthetic_spaces: int ; nb of additional spaces for decoration.
        :param is_costs_matrix: to display costs in blue (by convention).
        :param with_provisions_and_orders: to also display provisions and orders.
        :return: Nothing.
        """
        max_char_size = 0
        for i in range(self.nb_suppliers):
            for j in range(self.nb_customers):
                size_char = len(str(matrix[i][j]))
                if size_char > max_char_size:
                    max_char_size = size_char
        max_char_size = max(max_char_size, len(str(self.nb_suppliers - 1)) + 1)  # + 1 for len('P')
        max_char_size = max(max_char_size, len(str(self.nb_customers - 1)) + 1)  # + 1 for len('C')
        if with_provisions_and_orders:
            max_char_size = max(max_char_size, 10)  # 10 for len("Provisions") ; also for len("Orders")
        max_char_size += 1 + aesthetic_spaces

        print(" " * max_char_size, end="")
        for k in range(self.nb_customers):
            print(f"{'C' + str(k+1):>{max_char_size}}", end="")  # align to the right with a maximum width of max_char_size
        if with_provisions_and_orders:
            print(f"{'Provisions':>{max_char_size}}", end="")
        print()

        for i in range(self.nb_suppliers):
            print(f"{'P' + str(i+1):>{max_char_size}}", end="")
            for j in range(self.nb_customers):
                s = str(matrix[i][j])
                l_s = 0
                if is_costs_matrix:
                    s = '\033[1;34;48m {}\033[0m'.format(matrix[i][j])  # to display the costs in blue.
                    l_s = 14  # adjusting to work with colored text like it would without the colored text.
                print(f"{s:>{max_char_size+l_s}}", end="")
            if with_provisions_and_orders:
                print(f"{self.provisions[i]:>{max_char_size}}", end="")
            print()

        if with_provisions_and_orders:
            print(f"{'Orders':>{max_char_size}}", end="")
            for g in range(self.nb_customers):
                print(f"{self.orders[g]:>{max_char_size}}", end="")
            print()

    def display_full_transportation_problem_with_proposal(self, aesthetic_spaces=1, balas_hammer=None, penalties=None, penalty_equalities=None):
        """
        display the transportation problem: it's costs, transport proposal, provisions and orders.
        note: display costs in blue (by convention).

        :param aesthetic_spaces: int ; nb of additional spaces for decoration.
        :param balas_hammer: "Display of row(s) (or columns) with the maximum penalty" -> put it in color.
        :param penalties: to display penalties.
        :param penalty_equalities: to display in a different color the rows or cols with same penalty value than the maximum penalty.
        :return: Nothing.
        """
        max_char_size, max_prop_size = 0, 0
        for i in range(self.nb_suppliers):
            for j in range(self.nb_customers):
                max_prop_size = max(max_prop_size, len(str(self.transport_proposal_matrix[i][j])))
                size_char = len(str(self.costs_matrix[i][j])) + 3 + len(str(self.transport_proposal_matrix[i][j]))  # + 1 for len(' / ')
                if size_char > max_char_size:
                    max_char_size = size_char
        max_char_size = max(max_char_size, len(str(self.nb_suppliers - 1)) + 1)  # + 1 for len('P')
        max_char_size = max(max_char_size, len(str(self.nb_customers - 1)) + 1)  # + 1 for len('C')
        max_char_size = max(max_char_size, 10)  # 10 for len("Provisions") ; also for len("Orders") ; and also for len("Penalty")
        max_char_size += 1 + aesthetic_spaces

        print(" " * max_char_size, end="")
        for k in range(self.nb_customers):
            print(f"{'C' + str(k + 1):>{max_char_size}}", end="")
        print(f"{'Provisions':>{max_char_size}}", end="")
        if penalties:
            print(f"{'Penalty':>{max_char_size}}", end="")
        print()

        for i in range(self.nb_suppliers):
            print(f"{'P' + str(i + 1):>{max_char_size}}", end="")
            for j in range(self.nb_customers):
                # text color info : https://www.geeksforgeeks.org/python/print-colors-python-terminal/
                s = '\033[1;34;48m {}\033[0m'.format(self.costs_matrix[i][j])  # to display the costs in blue.
                l_s = 14  # adjusting to work with colored text like it would without the colored text.
                print(f"{s + ' / ':>{max_char_size+l_s-max_prop_size}}", end="")
                s_balas = str(self.transport_proposal_matrix[i][j])
                l_s_balas = 0
                if penalty_equalities:
                    for elt in penalty_equalities:
                        if elt[0] == "col" and elt[1] == j:
                            s_balas = '\033[1;33;48m{}\033[0m'.format(self.transport_proposal_matrix[i][j])  # text in yellow.
                            l_s_balas = 14
                        elif elt[0] == "row" and elt[1] == i:
                            s_balas = '\033[1;33;48m{}\033[0m'.format(self.transport_proposal_matrix[i][j])  # text in yellow.
                            l_s_balas = 14
                if balas_hammer:
                    if balas_hammer[0] and j == balas_hammer[2]:  # = max penalty in a col
                        s_balas = '\033[1;31;48m{}\033[0m'.format(self.transport_proposal_matrix[i][j])  # text in red.
                        l_s_balas = 14
                    elif not (balas_hammer[0]) and i == balas_hammer[2]:  # = maw penalty in a row
                        s_balas = '\033[1;31;48m{}\033[0m'.format(self.transport_proposal_matrix[i][j])  # text in red.
                        l_s_balas = 14
                    if balas_hammer[0]:
                        if i == balas_hammer[1] and j == balas_hammer[2]:
                            s_balas = '\033[1;31;40m{}\033[0m'.format(self.transport_proposal_matrix[i][j])  # text in red and black background.
                    else:
                        if j == balas_hammer[1] and i == balas_hammer[2]:
                            s_balas = '\033[1;31;40m{}\033[0m'.format(self.transport_proposal_matrix[i][j])  # text in red and black background.
                print(f"{s_balas:>{max_prop_size+l_s_balas}}", end="")
            print(f"{self.provisions[i]:>{max_char_size}}", end="")
            if penalties:
                print(f"{penalties[0][i]:>{max_char_size}}", end="")
            print()

        print(f"{'Orders':>{max_char_size}}", end="")
        for g in range(self.nb_customers):
            print(f"{self.orders[g]:>{max_char_size}}", end="")
        print()
        if penalties:
            print(f"{'Penalty':>{max_char_size}}", end="")
            for u in range(self.nb_customers):
                print(f"{penalties[1][u]:>{max_char_size}}", end="")
            print()

    def first_proposal(self):
        answer = 0
        while answer not in ['1', '2', '3']:
            print("Pick a initial proposal method :\n"
                  "1 for North-West\n"
                  "2 for Balas-Hammer/Penalties with Display\n"
                  "3 for Balas-Hammer/Penalties without Display")
            answer = input()
            if answer == '1':
                self.north_west()
            elif answer == '2':
                self.balas_hammer()
            elif answer == '3':
                self.balas_hammer(with_display=False)

    def north_west(self):
        """Compute/set the initial proposal using North-West method,
        put result in self.transport_proposal_matrix."""
        available = self.provisions[:]  # Allows copying quickly w/o affecting original attributes
        to_complete = self.orders[:]
        i = 0
        j = 0
        while to_complete != [0 for _ in range(self.nb_customers)]:  # nb_customers = len(to_complete)
            self.transport_proposal_matrix[i][j] = available[i] if available[i] < to_complete[j] else to_complete[j]  # We got two cases, either supply < order and we put all the supply in the proposal cell, on the other case we put all the amount needed for the order in the cell.
            available[i] = available[i] - self.transport_proposal_matrix[i][j]  # We update our supply and demand accordingly to the modification we've done
            to_complete[j] = to_complete[j] - self.transport_proposal_matrix[i][j]
            if to_complete[j] == 0:  # Following depletion of the demand or the supply, we move to the column to its right or the row under.
                j += 1
            else:
                i += 1

    def balas_hammer(self, with_display=True):
        """Compute/set the initial proposal using Balas-Hammer/Penalties method,
        put result in self.transport_proposal_matrix."""

        available = self.provisions[:]  # Allows copying quickly w/o affecting original attributes
        to_complete = self.orders[:]

        penalties_row = [0 for _ in range(0, len(available))]
        penalties_col = [0 for _ in range(0, len(to_complete))]

        while to_complete != [0 for _ in range(0, len(to_complete))]:

            # penalties calculation
            # penalty (of a row/col) = difference between 2 smallest costs (of a row/col)

            # Process calculation for the penalties attributed to each row
            for i in range(0, len(penalties_row)):
                min = [float('inf'), float('inf')]  # Infinity is of course an easy minimum to dislodge
                for j in range(len(self.orders)):  # Goes through whole row
                    if self.costs_matrix[i][j] <= min[0] and penalties_row[i] != -1 and penalties_col[j] != -1:  # if we find a cost lower than our minimum (excludes used rows and columns marked by a -1 penalty)
                        min[1] = min[0]  # We move the former minimum to the second spot, becoming our 2nd lowest cost
                        min[0] = self.costs_matrix[i][j]
                # - to be sure to have the 2nd lowest minimum in min[1] we check again:
                for j in range(len(self.orders)):
                    if self.costs_matrix[i][j] <= min[1] and self.costs_matrix[i][j] != min[0] and penalties_row[i] != -1 and penalties_col[j] != -1:  # exclude the smallest minimum
                        min[1] = self.costs_matrix[i][j]  # Assign penultimate to second minimum
                # -
                penalties_row[i] = min[1] - min[0] if min != [float('inf'), float('inf')] else -1  # to avoid inf - inf producing a nan, we replace by -1 in some cases
            if with_display:
                print("Penalties of rows :", str(penalties_row))

            # Process calculation for the penalties attributed to each column
            for i in range(0, len(penalties_col)):
                min = [float('inf'), float('inf')]
                for j in range(len(self.provisions)):  # Goes through whole column
                    if self.costs_matrix[j][i] <= min[0] and penalties_col[i] != -1 and penalties_row[j] != -1:  # if we find a cost lower than our minimum (excluding columns and rows used by the algorithm, marked with a -1 penalty)
                        min[1] = min[0]  # We move the former minimum to the second spot, becoming our 2nd lowest cost
                        min[0] = self.costs_matrix[j][i]
                # - to be sure to have the 2nd lowest minimum in min[1] we check again:
                for j in range(len(self.provisions)):
                    if self.costs_matrix[j][i] <= min[1] and self.costs_matrix[j][i] != min[0] and penalties_col[i] != -1 and penalties_row[j] != -1:  # exclude the smallest minimum
                        min[1] = self.costs_matrix[j][i]  # Assign penultimate to second minimum
                # -
                penalties_col[i] = min[1] - min[0] if min != [float('inf'), float('inf')] else -1  # to avoid inf - inf producing a nan, we replace by inf in some cases
            if with_display:
                print("Penalties of columns :", str(penalties_col))

            # find col with maximum penalty
            max_pen_col = [penalties_col[0], 0]
            for i in range(0, len(penalties_col)):  # We look towards minimum penalty for row and column, and their position in the list
                if penalties_col[i] >= max_pen_col[0]:
                    max_pen_col = [penalties_col[i], i]
            max_pen_row = [penalties_row[0], 0]
            # find row with maximum penalty
            for i in range(0, len(penalties_row)):
                if penalties_row[i] >= max_pen_row[0]:
                    max_pen_row = [penalties_row[i], i]

            # penalty_equalities: to display in a different color the rows or cols with same penalty value than the maximum penalty.
            penalty_equalities = []
            if max_pen_col[0] >= max_pen_row[0]:
                for i in range(0, len(penalties_col)):
                    if penalties_col[i] == max_pen_col[0]:
                        penalty_equalities.append(("col", i))
            if max_pen_col[0] <= max_pen_row[0]:
                for i in range(0, len(penalties_row)):
                    if penalties_row[i] == max_pen_row[0]:
                        penalty_equalities.append(("row", i))
            # ## display : "Display of row(s) (or columns) with the maximum penalty" -> put them in colors
            if with_display:
                penalties_tuple = (penalties_row, penalties_col)
                self.display_full_transportation_problem_with_proposal(penalties=penalties_tuple, penalty_equalities=penalty_equalities)

            # find max penalty. (Is there one or many ? Is it in a row or in a col ?)
            # and do stuff with it :
            # "choice of edge to fill" = find min cost across all max penalties, and fill max quantity possible.
            minimum_cost = chosen_penalty = cheapest_cell_index = max_quantity_possible = None
            for p in penalty_equalities:
                # find the max penalty to use by looking where is the minimum cost in the max penalties cols/rows.
                # find min cost
                if p[0] == "col":
                    for s in range(self.nb_suppliers):  # self.nb_suppliers = len(self.transport_proposal_matrix)
                        if cheapest_cell_index is None:
                            if penalties_row[s] != -1:
                                minimum_cost = self.costs_matrix[s][p[1]]
                                chosen_penalty = p
                                cheapest_cell_index = s
                                max_quantity_possible = available[cheapest_cell_index] if available[cheapest_cell_index] < to_complete[chosen_penalty[1]] else to_complete[chosen_penalty[1]]  # Assigns as much supply as possible
                        else:
                            if self.costs_matrix[s][p[1]] < minimum_cost and penalties_row[s] != -1:  # Finds cell with cheapest cost (excluding -1 cols)
                                minimum_cost = self.costs_matrix[s][p[1]]
                                chosen_penalty = p
                                cheapest_cell_index = s
                                max_quantity_possible = available[cheapest_cell_index] if available[cheapest_cell_index] < to_complete[chosen_penalty[1]] else to_complete[chosen_penalty[1]]  # Assigns as much supply as possible
                            # tie case = if two minimum costs are equal, choose where we can assign as much as possible :
                            elif self.costs_matrix[s][p[1]] == minimum_cost and penalties_row[s] != -1:
                                if max_quantity_possible < (available[s] if available[s] < to_complete[p[1]] else to_complete[p[1]]):
                                    minimum_cost = self.costs_matrix[s][p[1]]
                                    chosen_penalty = p
                                    cheapest_cell_index = s
                                    max_quantity_possible = available[cheapest_cell_index] if available[cheapest_cell_index] < to_complete[chosen_penalty[1]] else to_complete[chosen_penalty[1]]  # Assigns as much supply as possible
                else:  # if elt[0] == "row":
                    for c in range(self.nb_customers):  # self.nb_customers = len(self.transport_proposal_matrix[0])
                        if cheapest_cell_index is None:
                            if penalties_col[c] != -1:
                                minimum_cost = self.costs_matrix[p[1]][c]
                                chosen_penalty = p
                                cheapest_cell_index = c
                                max_quantity_possible = available[chosen_penalty[1]] if available[chosen_penalty[1]] < to_complete[cheapest_cell_index] else to_complete[cheapest_cell_index]  # Assigns as much supply as possible
                        else:
                            if self.costs_matrix[p[1]][c] < minimum_cost and penalties_col[c] != -1:  # Finds cell with cheapest cost (excluding -1 rows)
                                minimum_cost = self.costs_matrix[p[1]][c]
                                chosen_penalty = p
                                cheapest_cell_index = c
                                max_quantity_possible = available[chosen_penalty[1]] if available[chosen_penalty[1]] < to_complete[cheapest_cell_index] else to_complete[cheapest_cell_index]  # Assigns as much supply as possible
                            # tie case = if two minimum costs are equal, choose where we can assign as much as possible :
                            elif self.costs_matrix[p[1]][c] == minimum_cost and penalties_col[c] != -1:
                                if max_quantity_possible < (available[p[1]] if available[p[1]] < to_complete[c] else to_complete[c]):
                                    minimum_cost = self.costs_matrix[p[1]][c]
                                    chosen_penalty = p
                                    cheapest_cell_index = c
                                    max_quantity_possible = available[chosen_penalty[1]] if available[chosen_penalty[1]] < to_complete[cheapest_cell_index] else to_complete[cheapest_cell_index]

            if chosen_penalty[0] == "col":  # If the chosen max penalty is a column
                # fill max quantity possible
                self.transport_proposal_matrix[cheapest_cell_index][chosen_penalty[1]] = max_quantity_possible  # Assigns as much supply as possible to that cheap cell
                available[cheapest_cell_index] = available[cheapest_cell_index] - self.transport_proposal_matrix[cheapest_cell_index][chosen_penalty[1]]  # We update our supply and demand accordingly to the modification we've done
                to_complete[chosen_penalty[1]] = to_complete[chosen_penalty[1]] - self.transport_proposal_matrix[cheapest_cell_index][chosen_penalty[1]]
                if to_complete[chosen_penalty[1]] == 0:
                    penalties_col[chosen_penalty[1]] = -1  # Signal that this spot should not be used for penalty calculation
                if available[cheapest_cell_index] == 0:
                    penalties_row[cheapest_cell_index] = -1
            else:  # If the chosen max penalty is a row
                # fill max quantity possible
                self.transport_proposal_matrix[chosen_penalty[1]][cheapest_cell_index] = max_quantity_possible  # We got two cases, either supply < order and we put all the supply in the proposal cell, on the other case we put all the amount needed for the order in the cell.
                available[chosen_penalty[1]] = available[chosen_penalty[1]] - self.transport_proposal_matrix[chosen_penalty[1]][cheapest_cell_index]  # We update our supply and demand accordingly to the modification we've done
                to_complete[cheapest_cell_index] = to_complete[cheapest_cell_index] - self.transport_proposal_matrix[chosen_penalty[1]][cheapest_cell_index]
                if to_complete[cheapest_cell_index] == 0:
                    penalties_col[cheapest_cell_index] = -1
                if available[chosen_penalty[1]] == 0:
                    penalties_row[chosen_penalty[1]] = -1

            if with_display:
                print("transport proposal matrix:", self.transport_proposal_matrix)
                print("costs matrix:", self.costs_matrix)

                # ## display : "Display of row(s) (or columns) with the maximum penalty" -> put them in colors
                balas_tuple = (chosen_penalty[0] == "col", cheapest_cell_index, chosen_penalty[1])

                # -> without display penalties :
                # self.display_full_transportation_problem_with_proposal(balas_hammer=balas_tuple)
                # self.display_full_transportation_problem_with_proposal(balas_hammer=balas_tuple, penalty_equalities=penalty_equalities)

                # -> with display penalties :
                penalties_tuple = (penalties_row, penalties_col)
                # self.display_full_transportation_problem_with_proposal(balas_hammer=balas_tuple, penalties=penalties_tuple)
                self.display_full_transportation_problem_with_proposal(balas_hammer=balas_tuple, penalties=penalties_tuple, penalty_equalities=penalty_equalities)

                print()

        # end while loop / Balas-Hammer


def show_n_t(x: str) -> None:  # Just to verify than the 'save_tp_as_x' method works correctly.
    with open("./transportation proposals/" + x + ".txt", 'r') as f:
        line = f.readline()
        while line != "":
            print(line.replace('\t', '\\t').replace('\n', '\\n'))
            line = f.readline()
        # print(line.replace('\t', 't').replace('\n', 'n'))


def verify_txt(x: str) -> None:
    """to transform 't', spaces or '\t' in '\t',
    when creating/modifying transportation proposals txt from Pycharm,
    - to be able to create/modify them easily from Pycharm."""
    lines, unmodified_lines = [], []

    with open("./transportation proposals/" + x + ".txt", 'r') as f:
        line = f.readline()
        while line != "":
            unmodified_lines.append(line)
            line = ' '.join(line.split())  # transform spaces into only 1 space.
            line = line.replace('\\', '')
            line = line.replace('t', '\t')
            line = line.replace(' ', '\t')
            line = line.replace('\t\t\t', '\t')
            line = line.replace('\t\t', '\t')
            lines.append(line + '\n')
            line = f.readline()

    if unmodified_lines != lines:
        with open("./transportation proposals/"+x+".txt", 'w') as f2:
            for i in range(len(lines)):
                if lines[i] != unmodified_lines[i]:
                    print(f"|| A line has been modified in the txt file {x}:")
                    temp1 = unmodified_lines[i].replace('\t', '\\t').replace('\n', '\\n')
                    temp2 = lines[i].replace('\t', '\\t').replace('\n', '\\n')
                    print(f"{temp1} -> {temp2} ||")
                f2.write(lines[i])
