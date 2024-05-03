class ie0521_bp:
    def __init__(self):
        
        self.global_history_size = 5
        self.global_history_reg = '0'*self.global_history_size
        self.tag_1Hist_size=5
        self.size_of_tag_1=2**(self.tag_1Hist_size)
        self.tag_1=['0' for i in range(self.size_of_tag_1)]
        self.lnt=len(str(2**self.tag_1Hist_size))
        #self.historia_fila=["x" for i in range(self.tag_1Hist_size)]
        self.bits_to_index = 5
        self.size_of_bimodal = 2**self.bits_to_index
        self.bimodal = [0 for i in range(self.size_of_bimodal)]
        
        #el pregictor no tiene u porque sólo tiene una tabla taggeada, para que u sirva debe tener más de una
        
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
    

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tNombre de su predictor")

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
        
        PC_index = int(PC) % self.size_of_tag_1
        tag_index = int(self.global_history_reg[-self.tag_1Hist_size:],2)
        hashFunc = PC_index ^ tag_index
        match=0
        fila=0
        for i in range(self.size_of_tag_1):#recorremos la tabla
            if self.tag_1[i]!= '0': #primero vemos si la fila tiene algo, osea, que no sea igual a sólo un 0
                if int(self.tag_1[i][:self.lnt]) == hashFunc: #vemos si el tag está en la fila
                    match+=1 #ESO SIGNIFICA QUE HICIMOS MATCH
                    fila = i
                    # a la par del tag va a ir un dígito decimal de 3 bits que será el self.lnt
                    if int(self.tag_1[i][self.lnt])<4:
                        prediction = "N"
                    else:
                        prediction = "T"
                    break
                        
        if match==0: #si no hubo match nos pasamos al bimodal
            bimodal_entry = self.bimodal[PC_index]
            #print(bimodal_entry)
            if bimodal_entry<2:
                prediction = "N"
            else:
                prediction = "T"
        
        return prediction+"{}{}".format(match,fila)
            
        """if int(self.tag_1[i][self.tag_1Hist_size]) in range(1,8):
    #para que no se sature el contador int(self.tag_1[i][self.tag_1Hist_size])"""

    def update(self, PC, result, pred):
        #siempre se actualiza el bimodal

        prediction=pred[0]
        match=int(pred[1])
        fila=int(pred[2:])
        
        PC_index = int(PC) % self.size_of_bimodal
        if prediction == "T" and self.bimodal[PC_index]<3:#creamos saturación
                self.bimodal[PC_index]+=1
        elif prediction == "N" and self.bimodal[PC_index]>0:
                self.bimodal[PC_index]-=1
        
        if match:
            if result == "T" and int(self.tag_1[fila][self.lnt])<4:#creamos saturación
                self.tag_1[fila]=self.tag_1[fila][:self.lnt]+str(int(self.tag_1[fila][self.lnt])+1)
            elif result == "N" and int(self.tag_1[fila][self.lnt])>0:
                self.tag_1[fila]=self.tag_1[fila][:self.lnt]+str(int(self.tag_1[fila][self.lnt])-1)
        #en la tabla no podemos reemplazar un digito porque las strings no lo permiten, debemos reemplazar toda la string
        else:
            PC_index = int(PC) % self.size_of_tag_1
            tag_index = int(self.global_history_reg[-self.tag_1Hist_size:],2)
            hashFunc = PC_index ^ tag_index
            
            for i in range(self.size_of_tag_1):#recorremos la tabla
                if self.tag_1[i]== '0':
                    self.tag_1[i]='0'*(self.lnt-len(str(hashFunc)))+str(hashFunc)+'0'
                    break
                
        self.global_history_reg = self.global_history_reg[-self.global_history_size+1:] #eliminamos la primera
        if result == "T":
            self.global_history_reg+='1'
        else:
            self.global_history_reg+='0'
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

