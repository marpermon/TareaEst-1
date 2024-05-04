class perceptron:
    def __init__(self, bits_to_index, global_history_size):
        self.global_history_size = global_history_size
        self.global_history_reg = "0"*self.global_history_size
        #ponemos 0s para tratar las historia como una string, luego interpretaremos esos 0s como -1s
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**self.bits_to_index
        #vectores de peso para cada índice:
        self.branch_table = [[0]*(self.global_history_size+1) for i in range(self.size_of_branch_table)]
        #cada vector es 1 más grande que la historia porque el elemento 0 es el offset y no requiere un match con la historia
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
        y=weights[0] #offset
        for i,j in zip(weights[1:],x_):#arreglar: los pesos no tienen que ser 1 o -1
            #if i==int(j): y += 1 
            if i<(i+int(j)): y+=i # osea, si j es positivo
            else: y += -i

        return y
  

    def update(self, PC, result, prediction):
        index = int(PC) % self.size_of_branch_table
        
        t= 1 if result=="T" else -1
        #prediction*t<0 == sign(y)!=t
        if prediction*t<0 or abs(prediction)<=(11.93*self.global_history_size + 14):
            self.branch_table[index][0]+=t #primer peso, x0=1
 
            for i in range(self.global_history_size):
                x=-1 if self.global_history_reg[i]=="0" else 1
                if result=="T": #para no multiplicar
                    self.branch_table[index][i+1]+=x
                else:
                    self.branch_table[index][i+1]-=x
                    
        prediction = "T" if prediction>0 else "N"
        
        self.global_history_reg = self.global_history_reg[-self.global_history_size+1:] #eliminamos la primera
        if result == "T":
            self.global_history_reg+="1"
        else:
            self.global_history_reg+="0"
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
