class perceptron:
    def __init__(self, bits_to_index, global_history_size):
        self.global_history_size = global_history_size
        self.global_history_reg = [-1]*self.global_history_size
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.branch_table = [[0]*(self.global_history_size+1) for i in range(self.size_of_branch_table)]
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tPerceptron")

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
        index = int(PC) % self.size_of_branch_table
        weights = self.branch_table[index]
        x_=self.global_history_reg
        y=weights[0]#es así?
        for i,j in zip(weights[1:],x_):
            if i==j: y += 1
        else: y += -1
        #Escriba aquí el código para predecir
        #La siguiente línea es solo para que funcione la prueba
        #Quítela para implementar su código
        return y
  

    def update(self, PC, result, prediction):
        #Escriba aquí el código para actualizar
        #La siguiente línea es solo para que funcione la prueba
        #Quítela para implementar su código
        #Update GHR
        self.global_history_reg = self.global_history_reg[-self.global_history_size+1:]
        if result == "T":
            self.global_history_reg.append(1)
        else:
            self.global_history_reg.append(-1)
        #print("GHR = "+self.global_history_reg)

        #Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
