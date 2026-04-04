from transportation_problem import *

verify_txt("constraint_table_example")  # -> potentiellement à mettre directement dans la fct load tp
tp = TransportationProblem("constraint_table_example")

print()
tp.display_full_transportation_problem_with_proposal()

print()
tp.first_proposal()

print()
print(tp)

print()
tp.display_full_transportation_problem_with_proposal()

print()
tp.display_matrix(tp.costs_matrix, is_costs_matrix=True)
print()
tp.display_matrix(tp.costs_matrix, is_costs_matrix=True, with_provisions_and_orders=True)

print()
tp.display_matrix(tp.transport_proposal_matrix)
print()
tp.display_matrix(tp.transport_proposal_matrix, with_provisions_and_orders=True)

print()
print("total cost of transport:", tp.total_cost_calculation())

'''tp.save_tp_as_x("copy 6")
show_n_t("6")
show_n_t("copy 6")'''
