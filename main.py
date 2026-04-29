from transportation_problem import *

first_message = "Welcome to the transportation problem solver! You can choose from the following transportation problems to solve: \n1. transportation_problem_1\n2. transportation_problem_2\n3. transportation_problem_3\n4. transportation_problem_4\n5. transportation_problem_5\n6. transportation_problem_6\n7. transportation_problem_7\n8. transportation_problem_8\n9. transportation_problem_9\n10. transportation_problem_10\n11. transportation_problem_11\n12. transportation_problem_12\n13. balas_hammer_tie_cases_test\n14. constraint_table_test\n15. small_table_test\n16. small_table_text2\n17. small_tabme_test_3 \nPlease enter the number of the transportation problem you want to solve (or a negative number to exit): "
redo_message = "I hope you enjoyed solving that transportation problem! If you want to solve another one, please enter the number of the transportation problem you want to solve (or a negative number to exit): "
tp_number = 0
indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'balas_hammer_tie_cases_test', 'constraint_table_test', 'small_table_test', 'small_table_text2', 'small_tabme_test_3']
c=0
while tp_number >= 0:
    while tp_number == 0:
        if c == 0:
            tp_number = int(input(first_message))
        else:
            tp_number = int(input(redo_message))
        if tp_number < len(indexes) and tp_number >0:
            tp = TransportationProblem(str(indexes[tp_number-1]))
        elif tp_number < 0:
            print('Exiting the program...')
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
        c+=1
print("You have exited the program. Goodbye!")





'''tp.save_tp_as_x("copy 6")
show_n_t("6")
show_n_t("copy 6")'''
