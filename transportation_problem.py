
class TransportationProblem:
    def __init__(self, x: str):
        self.name: str = x
        self.nb_suppliers: int = 0  # n ; nb_suppliers = len(provisions)
        self.nb_customers: int = 0  # m ; nb_customers = len(orders)
        self.provisions: list[int] = []  # P
        self.orders: list[int] = []  # C
        self.costs_matrix: list[list[int]] = []  # A
        self.load_tp_x(x)
        self.transport_proposal_matrix = [[0 for _ in range(self.nb_customers)] for _ in range(self.nb_suppliers)]  # B

    def __str__(self):
        return ("Transportation Problem " + self.name + " details:\n" +
                "Nb of suppliers: " + str(self.nb_suppliers) + '\n' +
                "Nb of customers: " + str(self.nb_customers) + '\n' +
                "provisions array: " + str([p for p in self.provisions]) + '\n' +
                "orders array: " + str([c for c in self.orders]) + '\n' +
                "costs matrix: " + str([a for a in self.costs_matrix]) + '\n' +
                "transport proposal matrix: " + str([b for b in self.transport_proposal_matrix]))

    def load_tp_x(self, x: str) -> None:
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

    def display_full_transportation_problem_with_proposal(self, aesthetic_spaces=1):
        """
        display the transportation problem: it's costs, transport proposal, provisions and orders.
        note: display costs in blue (by convention).

        :param aesthetic_spaces: int ; nb of additional spaces for decoration.
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
        max_char_size = max(max_char_size, 10)  # 10 for len("Provisions") ; also for len("Orders")
        max_char_size += 1 + aesthetic_spaces

        print(" " * max_char_size, end="")
        for k in range(self.nb_customers):
            print(f"{'C' + str(k + 1):>{max_char_size}}", end="")
        print(f"{'Provisions':>{max_char_size}}")

        for i in range(self.nb_suppliers):
            print(f"{'P' + str(i + 1):>{max_char_size}}", end="")
            for j in range(self.nb_customers):
                # text color info : https://www.geeksforgeeks.org/python/print-colors-python-terminal/
                s = '\033[1;34;48m {}\033[0m'.format(self.costs_matrix[i][j])  # to display the costs in blue.
                l_s = 14  # adjusting to work with colored text like it would without the colored text.
                print(f"{s + ' / ':>{max_char_size+l_s-max_prop_size}}", end="")
                print(f"{self.transport_proposal_matrix[i][j]:>{max_prop_size}}", end="")
            print(f"{self.provisions[i]:>{max_char_size}}")

        print(f"{'Orders':>{max_char_size}}", end="")
        for g in range(self.nb_customers):
            print(f"{self.orders[g]:>{max_char_size}}", end="")
        print()

    def first_proposal(self):
        answer = 0
        while answer not in ['1', '2']:
            print("Pick a first proposal method (1 for North-West / 2 for Penalties) : ")
            answer = input()
            if answer == '1':
                self.north_west()
            elif answer == '2':
                self.penalties()

    def north_west(self):
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

    def penalties(self):
        ...


def show_n_t(x: str) -> None:  # Just to verify than the 'save_tp_as_x' method works correctly.
    with open("./transportation proposals/" + x + ".txt", 'r') as f:
        line = f.readline()
        while line != "":
            print(line.replace('\t', 't').replace('\n', 'n'))
            line = f.readline()
        # print(line.replace('\t', 't').replace('\n', 'n'))


def verify_txt(x: str) -> None:
    """to transform 't' or spaces in '\t', when creating/modifying transportation proposals txt from Pycharm."""
    lines = []

    with open("./transportation proposals/" + x + ".txt", 'r') as f:
        line = f.readline()
        while line != "":
            line = ' '.join(line.split())  # transform spaces into only 1 space.
            line = line.replace('t', '\t')
            line = line.replace(' ', '\t')
            line = line.replace('\t\t', '\t')
            line = line.replace('\t\t\t', '\t')
            lines.append(line)
            line = f.readline()

    with open("./transportation proposals/"+x+".txt", 'w') as f2:
        for elt in lines:
            f2.write(elt + '\n')
