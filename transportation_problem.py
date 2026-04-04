
class TransportationProblem:
    def __init__(self, x: str):
        self.name: str = x
        self.nb_suppliers: int = 0  # n
        self.nb_customers: int = 0  # m
        self.provisions: list[int] = []  # P
        self.orders: list[int] = []  # C
        self.costs_matrix: list[list[int]] = []  # A
        self.load_tp_x(x)
        #self.adjacency_matrix: list[list] = [['_' for _ in range(self.nb_vertices)] for _ in range(self.nb_vertices)]
        #self.compute_adjacency_matrix()

    def __str__(self):
        return ("Transportation Problem " + self.name + " details:\n" +
                "Nb of suppliers: " + str(self.nb_suppliers) + '\n' +
                "Nb of customers: " + str(self.nb_customers) + '\n' +
                "All provisions: " + str([p for p in self.provisions]) + '\n' +
                "All orders: " + str([c for c in self.orders]) + '\n' +
                "All costs: " + str([a for a in self.costs_matrix]))

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
