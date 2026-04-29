from transportation_problem import *

tp_number = 0
indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'balas_hammer_tie_cases_test', 'constraint_table_test', 'small_table_test', 'small_table_text2', 'small_tabme_test_3']

while tp_number >= 0:
    while tp_number == 0:
        tp_number = int(input("Enter the number of the transportation problem you want to solve (or a negative number to exit): "))
        if tp_number < len(indexes) and tp_number >0:
            tp = TransportationProblem(str(indexes[tp_number-1]))
        elif tp_number < 0:
            print('balls')
            pass
        else:
            print("That transportation problem doesn't exist. Please try again.")
            tp_number = int(input("Enter the number of the transportation problem you want to solve (or a negative number to exit): "))
    if tp_number >= 0:
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

        tp_number = 0
print("You have exited the program. Goodbye!")





'''tp.save_tp_as_x("copy 6")
show_n_t("6")
show_n_t("copy 6")'''
