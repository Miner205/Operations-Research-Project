
class TransportationProblem:
    def __init__(self, x: str):
        self.name: str = x
        self.nb_suppliers: int = 0  # n
        self.nb_customers: int = 0  # m
        self.provisions: list[int] = []  # P
        self.orders: list[int] = []  # C
        self.costs_matrix: list[list[int]] = []  # A
        self.proposal = [] # The thing we're going to look at the most in this project, the proposals
        self.load_tp_x(x)
        #self.adjacency_matrix: list[list] = [['_' for _ in range(self.nb_vertices)] for _ in range(self.nb_vertices)]
        #self.compute_adjacency_matrix()

    def __str__(self):
        return ("Transportation Problem " + self.name + " details:\n" +
                "Nb of suppliers: " + str(self.nb_suppliers) + '\n' +
                "Nb of customers: " + str(self.nb_customers) + '\n' +
                "All provisions: " + str([p for p in self.provisions]) + '\n' +
                "All orders: " + str([c for c in self.orders]) + '\n' +
                "All costs: " + str([a for a in self.costs_matrix]) + '\n' +
                "Proposal: " + str([p for p in self.proposal]))

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

            self.proposal = [[0 for i in range(0,len(self.orders))] for j in range(0,len(self.provisions))]

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

    def first_proposal(self):
        answ = 0
        while answ not in [str(1), str(2)]:
            print("Pick a first proposal method (1 North-West/ 2 Penalties) : ")
            answ = input()
            if answ == str(1):
                self.north_west()
            elif answ == str(2): 
                self.balas_hammer()

    def north_west(self):
        available = self.provisions[:] # Allows copying quickly w/o affecting original attributes
        to_complete = self.orders[:]
        i = 0
        j = 0
        while to_complete != [0 for k in range(0,len(to_complete))]:
            self.proposal[i][j] = available[i] if available[i] < to_complete[j] else to_complete[j] # We got two cases, either supply < order and we put all the supply in the proposal cell, on the other case we put all the amount needed for the order in the cell.
            available[i] = available[i] - self.proposal[i][j] # We update our supply and demand accordingly to the modification we've done
            to_complete[j] = to_complete[j] - self.proposal[i][j]
            if to_complete[j] == 0: # Following depletion of the demand or the supply, we move to the column to its right or the row under.
                j += 1
            else:
                i += 1

    def balas_hammer(self):
        available = self.provisions[:] # Allows copying quickly w/o affecting original attributes
        to_complete = self.orders[:]
        penalties_row = [0 for k in range(0,len(available))]
        penalties_col = [0 for k in range(0,len(to_complete))]
        it = 0
        while to_complete != [0 for k in range(0,len(to_complete))]:
            for i in range(0, len(penalties_row)): # Process calculation for the penalties attributed to each row
                min = [float('inf'),float('inf')] # Infinity is of course an easy minimum to dislodge
                for j in range(len(self.orders)): # Goes through whole row
                    if self.costs_matrix[i][j] <= min[0] and penalties_row[i] != -1: # if we find a cost lower than our minimum (excludes used rows marked by a -1 penalty)
                        min[1] = min[0] # We move the former minimum to the second spot, becoming our 2nd lowest cost
                        min[0] = self.costs_matrix[i][j]
                if min[1] == float('inf'): # In case where we only get a single minimum due to the algorithm falling on the minimum of the array at first iteration, we add another minimum search to find the second one.
                    for j in range(len(self.orders)):
                        if self.costs_matrix[i][j] <= min[1] and self.costs_matrix[i][j] != min[0] and penalties_row[i] != -1: # exclude the smallest minimum
                            min[1] = self.costs_matrix[i][j] # Assign penultimate to second minimum
                penalties_row[i] = min[1] - min[0] if min != [float('inf'),float('inf')] else -1 # to avoid inf - inf producing a nan, we replace by -1 in some cases
            print("Penalties of rows : ", str(penalties_row))
            for i in range(0, len(penalties_col)): # Process calculation for the penalties attributed to each column
                min = [float('inf'),float('inf')]
                for j in range(len(self.provisions)): # Goes through whole column
                    if self.costs_matrix[j][i] <= min[0] and penalties_col[i] != -1: # if we find a cost lower than our minimum (excluding columns used by the algorithm, marked with a -1 penalty)
                        min[1] = min[0] # We move the former minimum to the second spot, becoming our 2nd lowest cost
                        min[0] = self.costs_matrix[j][i]
                if min[1] == float('inf'): # In case where we only get a single minimum due to the algorithm falling on the minimum of the array at first iteration, we add another minimum search to find the second one.
                    for j in range(len(self.provisions)):
                        if self.costs_matrix[j][i] <= min[1] and self.costs_matrix[j][i] != min[0] and penalties_col[i] != -1: # exclude the smallest minimum
                            min[1] = self.costs_matrix[j][i] # Assign penultimate to second minimum
                penalties_col[i] = min[1] - min[0] if min != [float('inf'),float('inf')] else -1 # to avoid inf - inf producing a nan, we replace by inf in some cases
            print("Penalties of columns : ", str(penalties_col))

            max_pen_col = [penalties_col[0], 0]
            for i in range(0, len(penalties_col)): # We look towards minimum penalty for row and column, and their position in the list
                if penalties_col[i] >= max_pen_col[0]:
                    max_pen_col = [penalties_col[i],i]
            max_pen_row = [penalties_row[0],0]
            for i in range(0,len(penalties_row)):
                if penalties_row[i] >= max_pen_row[0]:
                    max_pen_row = [penalties_row[i],i]

            if max_pen_col[0] > max_pen_row[0]: # If the maximum of the columns is superior to maximum of rows
                cheapest_cell_index = None # Holds index of the cheapest cell we'll find
                for k in range(len(self.proposal)): 
                    if cheapest_cell_index == None:
                        if penalties_row[k] != -1:
                            cheapest_cell_index = k
                    else :
                        if self.costs_matrix[k][max_pen_col[1]] < self.costs_matrix[cheapest_cell_index][max_pen_col[1]] and penalties_row[k] != -1 : # Finds cell with cheapest cost (excluding -1 rows)
                            cheapest_cell_index = k
                self.proposal[cheapest_cell_index][max_pen_col[1]] = available[cheapest_cell_index] if available[cheapest_cell_index] < to_complete[max_pen_col[1]] else to_complete[max_pen_col[1]] # Assigns as much supply as possible to that cheap cell
                available[cheapest_cell_index] = available[cheapest_cell_index] - self.proposal[cheapest_cell_index][max_pen_col[1]] # We update our supply and demand accordingly to the modification we've done
                to_complete[max_pen_col[1]] = to_complete[max_pen_col[1]] - self.proposal[cheapest_cell_index][max_pen_col[1]]
                if to_complete[max_pen_col[1]] == 0:
                    penalties_col[max_pen_col[1]] = -1 # Signal that this spot should not be used for penalty calculation
                if available[cheapest_cell_index] == 0:
                    penalties_row[cheapest_cell_index] = -1
            else: # If the maximum of columns is smaller
                cheapest_cell_index = None
                for k in range(len(self.proposal[0])): # ibid
                    if cheapest_cell_index == None:
                        if penalties_row[k] != -1:
                            cheapest_cell_index = k
                    else :
                        if self.costs_matrix[max_pen_row[1]][k] < self.costs_matrix[max_pen_row[1]][cheapest_cell_index] and penalties_col[k] != -1 : # Finds cheapest cost (excluding -1 cols)
                            cheapest_cell_index = k
                self.proposal[max_pen_row[1]][cheapest_cell_index] = available[max_pen_row[1]] if available[max_pen_row[1]] < to_complete[cheapest_cell_index] else to_complete[cheapest_cell_index] # We got two cases, either supply < order and we put all the supply in the proposal cell, on the other case we put all the amount needed for the order in the cell.
                available[max_pen_row[1]] = available[max_pen_row[1]] - self.proposal[max_pen_row[1]][cheapest_cell_index] # We update our supply and demand accordingly to the modification we've done
                to_complete[cheapest_cell_index] = to_complete[cheapest_cell_index] - self.proposal[max_pen_row[1]][cheapest_cell_index]
                if to_complete[cheapest_cell_index] == 0:
                    penalties_col[cheapest_cell_index] = -1
                if available[max_pen_row[1]] == 0:
                    penalties_row[max_pen_row[1]] = -1

            print(self.proposal)
            print(self.costs_matrix)
            it += 1
            # if it > 10:
                # break
            # to_complete = [0 for k in range(0,len(to_complete))] # temporary loop breaker