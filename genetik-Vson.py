import numpy as np
import random
import time
#generation_number = int(input("jenerasyon sayisi giriniz: "))
#initial_population = int(input("populasyon buyuklugu giriniz: "))
#crossover_ratio = int(input("yuzdelik caprazlama orani girin: "))
#mutation_ratio = int(input("yuzdelik mutasyon orani girin: "))
#precision = int(input("ondalik hassasiyet degerini girin: "))


generation_number = 1000
initial_population = 20
crossover_rate = 25 
mutation_rate = 4
precision = 3
x_min = [-3 , 4.1]
x_max = [12.1 , 5.8]
best_fitness = 0
best_generation = 0 
params = np.zeros((initial_population , 2))
fitness = np.zeros((initial_population , 1)) 
max_fitness = 0
toplam_fitness = 0

x1_range = int((x_max[0] - x_min[0]) * (10 ** precision))
x2_range = int((x_max[1] - x_min[1]) * (10 ** precision))
#print "x1_range",x1_range,"\n","x2_range",x2_range

x1_bit_number = len(np.binary_repr(x1_range))
x2_bit_number = len(np.binary_repr(x2_range))
total_bit_number = x1_bit_number + x2_bit_number

#print "x1_bit_number",x1_bit_number,"\n","x2_bit_number",x2_bit_number,"\n","total_bit_number",total_bit_number

population = np.zeros((initial_population,total_bit_number))
#print population,"\n"
population = np.random.choice([0,1],size=(initial_population,total_bit_number))
#print population
#print np.shape(population)



time_1= time.time()
for i in range (0,initial_population):
        decimal_x1 = population[i,0:x1_bit_number]
        #print decimal_x1,np.shape(decimal_x1)
        decimal_x1 = str(decimal_x1)
        #print decimal_x1 ,"decimal_x1"
        decimal_x1 = decimal_x1.replace(" ","")
        decimal_x1 = decimal_x1.replace("[","")
        decimal_x1 = decimal_x1.replace("]","")
        decimal_x1= "0b"+decimal_x1
        decimal_x1 = int((decimal_x1),2)
        #print decimal_x1  ,"decimal_x1"
        decimal_x2 = population[i,x1_bit_number:total_bit_number]
        #print decimal_x2,np.shape(decimal_x2),"decimal_x2"
        decimal_x2 = str(decimal_x2)
        decimal_x2 = decimal_x2.replace(" ","")
        decimal_x2 = decimal_x2.replace("[","")
        decimal_x2 = decimal_x2.replace("]","")
        decimal_x2= "0b"+decimal_x2
        decimal_x2 = int((decimal_x2),2)
        #print decimal_x2,"decimal_x2"
        x1 = x_min[0] + (decimal_x1 * ((x_max[0] - x_min[0]) / (2 ** (x1_bit_number))))
        x2 = x_min[1] + (decimal_x2 * ((x_max[1] - x_min[1]) / (2 ** (x2_bit_number))))
        #print x1,"x1","\n",x2,"x2"
        params[i,0] = x1
        params[i,1] = x2
        fitness[i,0] = 21.5 + (x1*np.sin(4*np.pi*x1)) + (x2*np.sin(20*np.pi*x2))
        toplam_fitness = toplam_fitness + fitness[i,0]
#print fitness    
for i in range(0,initial_population):    
        if (max_fitness < fitness[i,0]):
                max_fitness = fitness[i,0]

#print max_fitness

for t in range(0,generation_number):
        population_selection_rates = np.zeros((initial_population,1))

        for i in range (0,initial_population):
                population_selection_rates[i,0] = fitness[i,0] / toplam_fitness
        cumulative_rates = np.zeros((initial_population,1))

        for i in range(0,initial_population):
                if (i==0):
                        cumulative_rates[0,0] = population_selection_rates[0,0]
                else:
                        cumulative_rates[i,0] = cumulative_rates[i-1,0] + population_selection_rates[i,0]

        degisken = np.cumsum(cumulative_rates)
        #print degisken ,"----------------------------------------------------"

        #eslesecek ciftleri seciyoruz-rulet tekeri 
        random_selection_number = np.zeros((initial_population,1))
        population_couples = np.zeros((initial_population,1),dtype = int)
        random_selection_number = np.random.rand(initial_population,1)
        for j in range (1,initial_population):
                for i in range (0,initial_population):
                        if (random_selection_number[i,0] < cumulative_rates[j,0]):
                                random_selection_number[i,0] = j 
        
        crossing_item_number = int(initial_population*crossover_rate/100.0)
        crossing_items = np.zeros(crossing_item_number)
        #hepsini caprazliyor duzenlenecek caprazlama orani kadar
        #for i in range(0,crossing_item_number):
        #random_cross_rate = np.random.rand(initial_population,1)
        #index_cross = np.where(random_cross_rate[:,0] < (crossover_rate/100.0))

        random_cross_rate = np.random.rand(initial_population,1)
        index_cross = np.where(random_cross_rate[:,0] < (crossover_rate/100.0))
        cross_rate_number = len(index_cross[0])

        while (cross_rate_number%2 !=0):
                    
                random_cross_rate = np.random.rand(initial_population,1)
                index_cross = (np.where(random_cross_rate[:,0] < (crossover_rate/100.0)))
                cross_rate_number = len(index_cross[0])
                #print type(index_cross) 
        index_cross=np.asarray(index_cross)
        #index_cross = np.ndarray.tolist(index_cross)
        #print type(index_cross) 
        #print cross_rate_number
        new_population_tuple1= np.zeros((total_bit_number,1))
        new_population_tuple2= np.zeros((total_bit_number,1))

        for i in range(0,cross_rate_number,2):
                random_kromosom_number = random.randint(0, initial_population)
                new_population_tuple1 = population[index_cross[0,i],total_bit_number-random_kromosom_number:total_bit_number].copy()
                new_population_tuple2 = population[index_cross[0,i+1],total_bit_number-random_kromosom_number:total_bit_number].copy()
                population[index_cross[0,i],total_bit_number-random_kromosom_number:total_bit_number] = new_population_tuple2
                population[index_cross[0,i+1],total_bit_number-random_kromosom_number:total_bit_number] = new_population_tuple1
                #print random_kromosom_number,"\n",population[i],"\n",population[i+1],"\n",new_population_tuple1,"\n",new_population_tuple2,"\n"
        #print population 

        mutation_number = mutation_rate * initial_population * total_bit_number/100
        #print mutation_number
        for i in range(0,mutation_number):
                mutation_bit = random.randint(0, initial_population*total_bit_number)
                f = population[int(mutation_bit / total_bit_number)-1,mutation_bit % total_bit_number]
                if (f == 0):
                        population[int(mutation_bit / total_bit_number)-1,mutation_bit % total_bit_number] = 1
                else:
                        population[int(mutation_bit / total_bit_number)-1,mutation_bit % total_bit_number] = 0


        for j in range (0,initial_population ):
                decimal_x1 = population[j,0:x1_bit_number]
                decimal_x1 = str(decimal_x1)   
                decimal_x1 = decimal_x1.replace(" ","")
                decimal_x1 = decimal_x1.replace("[","")
                decimal_x1 = decimal_x1.replace("]","")
                decimal_x1= "0b"+decimal_x1
                decimal_x1 = int((decimal_x1),2)
                decimal_x2 = population[j,x1_bit_number+1:total_bit_number]    
                decimal_x2 = str(decimal_x2)
                decimal_x2 = decimal_x2.replace(" ","") 
                decimal_x2 = decimal_x2.replace("[","")
                decimal_x2 = decimal_x2.replace("]","")
                decimal_x2= "0b"+decimal_x2
                decimal_x2 = int((decimal_x2),2)
                x1 = x_min[0] + (decimal_x1 * ((x_max[0] - x_min[0]) / (2 ** (x1_bit_number))))
                x2 = x_min[1] + (decimal_x2 * ((x_max[1] - x_min[1]) / (2 ** (x2_bit_number))))
                params[j,0] = x1
                params[j,1] = x2
                fitness[j,0] = 21.5 + (x1*np.sin(4*np.pi*x1)) + (x2*np.sin(20*np.pi*x2))
        #print fitness

        for i in range(0,initial_population):    
                if (max_fitness < fitness[i,0]):
                        max_fitness = fitness[i,0]
                        best_generation = t
                        print max_fitness,"generation",best_generation
                
time_2 = time.time()

print time_2 -time_1,"time (s)"
