import numpy as np
import pandas as pd

df1 = pd.read_csv('Data/Historical Income Tax Rates and Brackets, 1862-2025.csv', na_values = "NaN", nrows = 7)

print(df1.head())

#Total Income Tax 2025 2,656,044 million so like 2.6 trillion


#Fitness
#The Target of fitnees is 0.95% of total income tax wih pre optized rates
#Vectorize the matrice into 4 different Allleles based on filing status
#Copare the allele to the worst performer and add a buffer so even the worst performer will have a small chance to mutate

#Reproduce
#Randomly decide a point to reproduce within the length of the parent
#Return the new child

#Mutate
#Take the chances from fitness to decide whether or not the parents mutates.

rates = [10.0,12.0,22.0,24.0,32.0,35.0,37.0]


def objectf(state) :
