class pshared:
    def __init__(self, bits_to_index, global_history_size):
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.global_history_size = min(global_history_size, bits_to_index) # Limitar el tamaño del registro de historia al número de bits para indexar
        self.max_index_global_history = 2**self.global_history_size
        # Primer índice con PC, segundo índice con GHR
        self.branch_table = [[0 for _ in range(self.size_of_branch_table)] for _ in range(self.max_index_global_history)]

        self.global_history_reg = 0
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
        
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tP-Shared")
        print("\tEntradas en el Predictor:\t\t\t{}".format(self.size_of_branch_table))
        print("\tTamaño de los registros de historia global:\t{}".format(self.global_history_size))

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t{}".format(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t{}".format(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t{}".format(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t{}".format(self.total_not_taken_pred_taken))
        print("\t# branches no tomados predichos incorrectamente:\t{}".format(self.total_not_taken_pred_not_taken))
        perc_correct = 100 * (self.total_taken_pred_taken + self.total_not_taken_pred_not_taken) / self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t{}%".format(formatted_perc))

    def predict(self, PC):
        PC_index = int(PC, 16) % self.size_of_branch_table
        GHR_index = self.global_history_reg % self.max_index_global_history

        branch_table_entry = self.branch_table[GHR_index][PC_index]

        if branch_table_entry in [0, 1]:
            return "N"
        else:
            return "T"

    def update(self, PC, result, prediction):
        PC_index = int(PC, 16) % self.size_of_branch_table
        GHR_index = self.global_history_reg % self.max_index_global_history

        branch_table_entry = self.branch_table[GHR_index][PC_index]

        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry
        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1
        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry
        else:
            updated_branch_table_entry = branch_table_entry + 1

        self.branch_table[GHR_index][PC_index] = updated_branch_table_entry

        # Actualizar el registro de historia global
        self.global_history_reg = ((self.global_history_reg << 1) | (1 if result == "T" else 0)) % self.max_index_global_history

        # Actualizar estadísticas
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
