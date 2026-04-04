from transportation_problem import *

tp = TransportationProblem("6")

tp.display_full_transportation_problem_with_proposal()

tp.first_proposal()
print(tp)

tp.display_full_transportation_problem_with_proposal()


'''tp.save_tp_as_x("copy 6")
show_n_t("6")
show_n_t("copy 6")'''
print(tp.total_cost_calculation())
print()
tp.display_matrix(tp.costs_matrix)
print()
tp.display_matrix(tp.transport_proposal_matrix)
