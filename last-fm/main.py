import re
import time
import sqlite3
import pycountry
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")
sns.set_theme(style = "whitegrid")

print("Iniciando o carregamento dos dados")
conn = sqlite3.connect("imdb.db")
tabelas = pd.read_sql_query("SELECT NAME AS 'Table_Name' FROM sqlite_master WHERE type = 'table'", conn)
tabelas = tabelas["Table_Name"].values.tolist()

##Pergunta 1

consulta1 = '''SELECT type, COUNT(*) AS COUNT FROM titles GROUP BY type'''
resultado1 = pd.read_sql_query(consulta1, conn)
print(resultado1)
resultado1['percentual'] = (resultado1['COUNT'] / resultado1['COUNT'].sum()) * 100
others = {}

# Filtra o percentual em 5% e soma o total
others['COUNT'] = resultado1[resultado1['percentual'] < 5]['COUNT'].sum()

# Grava o percentual
others['percentual'] = resultado1[resultado1['percentual'] < 5]['percentual'].sum()

# Ajusta o nome
others['type'] = 'others'

resultado1 = resultado1[resultado1['percentual'] > 5]
resultado1 = resultado1.append(others, ignore_index = True)
resultado1 = resultado1.sort_values(by = 'COUNT', ascending = False)
labels = [str(resultado1['type'][i])+' '+'['+str(round(resultado1['percentual'][i],2)) +'%'+']' for i in resultado1.index]
cs = cm.Set3(np.arange(100))

# Cria a figura
f = plt.figure()

# Pie Plot
plt.pie(resultado1['COUNT'], labeldistance = 1, radius = 3, colors = cs, wedgeprops = dict(width = 0.8))
plt.legend(labels = labels, loc = 'center', prop = {'size':12})
plt.title("Distribuição de Títulos", loc = 'Center', fontdict = {'fontsize':20,'fontweight':20})
plt.show()