class pshared:
    def __init__(self, bits_to_index, global_history_size):
        # Cantidad de bits para la Tabla y longitud de tabla de PC
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        # Cantidad de bits de historia y logitud  de la tabla de historia
        self.global_history_size = global_history_size
        self.size_of_global_table = 2**global_history_size

        #Llenar la tabla de predicción con ceros
        self.global_table = [0 for i in range(self.size_of_global_table)]

        # Inicializar la tabla de historia con cadenas de longitud global_history_size
        self.branch_table = ["0" * self.global_history_size for _ in range(self.size_of_branch_table)]
    
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tP-Shared")
        print("\tBits a indexar:\t\t\t\t\t"+str(self.bits_to_index))
        print("\tEntradas en el Predictor:\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia global:\t"+str(self.global_history_size))

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    def predict(self, PC):
        PC_index = int(PC) % self.size_of_branch_table
        GHR_index = int(self.branch_table[PC_index], 2) 
        branch_table_entry = self.global_table[GHR_index]

        if branch_table_entry in [0,1]:
            return "N"
        else:
            return "T"
  

    def update(self, PC, result, prediction):
        PC_index = int(PC) % self.size_of_branch_table
        GHR_index = int(self.branch_table[PC_index], 2) 
        branch_table_entry = self.global_table[GHR_index]

        # Se actualiza el valor de la predicción
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry
            
        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1
            
        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry
        else:
            updated_branch_table_entry = branch_table_entry + 1

        self.global_table[GHR_index] = updated_branch_table_entry

        # Actualizar el registro de historia global
        if result == "T":
            self.branch_table[PC_index] = self.branch_table[PC_index][1:] + "1"
        else:
            self.branch_table[PC_index] = self.branch_table[PC_index][1:] + "0"
        
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
