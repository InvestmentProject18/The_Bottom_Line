import numpy as np
import pandas as pd

df1 = pd.read_csv('Data/Historical Income Tax Rates and Brackets, 1862-2025.csv', na_values = "NaN", nrows = 7)

print(df1.head())

#Fitness
#The Target of fitnees is 0.95% of total income tax wih pre optized rates
#Vectorize the matrice into 4 different Allleles based on filing status
#Copare the allele to the worst performer and add a buffer so even the worst performer will have a small chance to mutate

#Reproduce
#Randomly decide a point to reproduce within the length of the parent
#Return the new child

#Mutate
#Take the chances from fitness to decide whether or not the parents mutates.

