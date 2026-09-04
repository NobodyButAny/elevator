import numpy as np
from scipy.stats import poisson

l = 4.5
m = 5
k = 0.66

chernoff = (((np.e*l)**m) * np.exp(-l)) / (m**m)
print("Оценка Чернова: ", chernoff)

actual = 1 - poisson.cdf(k=m, mu=l)
print("Оценка Ф-ии распределения: ", actual)

mean_n_ch = 1 / (1 - chernoff)
mean_n_a = 1 / (1 - actual)
print("Средняя длина пробега(Чернов): ", mean_n_ch)
print("Средняя длина пробега: ", mean_n_a)