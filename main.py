import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle
import timeit
from functools import lru_cache

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self,level=0):
        output = "\t"*level + repr(self.value) + "\n"
        for child in self.children:
            output += child.__str__(level+1)
        return output

class Tree:
    def __init__(self, root=None):
        self.root = root

    def goThrough(self,node = None):
        nodes = []
        if node == None:
            if self.root:
                nodes.append(self.root.value)
                nodes.extend(self.goThrough(self.root))
            return nodes
        else:
            for child in node.children:
                nodes.append(child.value)
                nodes.extend(self.goThrough(child))
            return nodes

    @property
    def min_value(self):
        all_values = self.goThrough()
        if all_values:
            return min(all_values)
        else:
            return None

    def __str__(self):
        if self.root:
            return str(self.root)
        else:
            return "Empty tree"

################################## Zadanie 2 #######################################
# Usunięcie duplikatów

df = pd.read_csv('train.csv')
df = df.drop_duplicates()
df.to_csv('Without_duplicates.csv', index=False)

#Korelacja
korelacja = df['limit_bal'].corr(df['age'])
print(f"Korelacja między limit_bal, a wiekiem: {korelacja}")

#Dodanie kolumny
bill_columns = [col for col in df.columns if 'bill_amt' in col]
df['total_bill_amt'] = df[bill_columns].sum(axis=1)
df.to_csv('new_column.csv', index = False)

#Znalezienie 10 najstarszych klientów
oldest = df.nlargest(10, 'age')[['limit_bal', 'age', 'total_bill_amt']]
print(oldest)

#Wykreślnenie histogramu
fig, axes = plt.subplots(1,3, figsize=(15,5))

df['limit_bal'].plot(kind='hist', ax=axes[0], title='Histogram limitu kredytu')
df['age'].plot(kind='hist', ax = axes[1], title = 'Histogram wieku')
axes[2].scatter(df['age'], df['limit_bal'], alpha=0.5)
axes[2].set_title('Zależność limitu kredytu od wieku')
axes[2].set_xlabel('Wiek')
axes[2].set_ylabel('Limit kredytu')

plt.show()

################################## Zadanie 3 #######################################
root = Node('Root')
tree = Tree(root)

child1 = Node('1')
child2 = Node('2')
root.add_child(child1)
root.add_child(child2)

subchild4 = Node('4')
subchild5 = Node('5')
child1.add_child(subchild4)
child1.add_child(subchild5)

subchild7 = Node('7')
subchild8 = Node('8')
child2.add_child(subchild7)
child2.add_child(subchild8)

subsub10 = Node('0')
subsub12 = Node('12')
subchild7.add_child(subsub10)
subchild8.add_child(subsub12)

#Wyszukiwanie najmniejszej wartości
min_value = tree.min_value
print(f"Najmniejsza wartość w drzewie to: {min_value}")

################################## Zadanie 3b #######################################

def fibonacci_recursive(n):
    if n<= 1:
        return n
    else:
        return fibonacci_recursive(n-2) + fibonacci_recursive(n-1)

# pomiar czasu
time_recursive = timeit.timeit(lambda: fibonacci_recursive(10), number=1)
print(f"Czas wykonania funkcji rekurencyjnej: {time_recursive} s")

@lru_cache(maxsize=None)
def fibonacci_cache(n):
    if n<= 1:
        return n
    else:
        return fibonacci_cache(n-2) + fibonacci_cache(n-1)

time_cache = timeit.timeit(lambda: fibonacci_cache(10), number=1)
print(f"Czas wykonania funkcji z dekoratorem @lru_cache: {time_cache} s")

################################## Zadanie 3c #######################################

def save_to_disk(func):
    def function1(*args, **kwargs):
        filename = f"{func.__name__}_cache.pkl"
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                output = pickle.load(file)
        else:
            output = func(*args, **kwargs)
            with open(filename, 'wb') as file:
                pickle.dump(output, file)
        return output
    return function1

@save_to_disk
def example():
    return [i*2 for i in range(10)]

output = example()
print(output)