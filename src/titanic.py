import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 0. Configuración inicial
# Crear carpeta de resultados si no existe para asegurar reproducibilidad
os.makedirs('outputs/resultados', exist_ok=True)
sns.set_theme(style="whitegrid")

print("INICIANDO ANÁLISIS DEL TITANIC")

# 1. Cargar el dataset
# Se asume que el script se ejecuta desde la raíz del proyecto
df = pd.read_csv('data/train.csv')

# 2. Exploración inicial
print(" EXPLORACIÓN INICIAL")
print(f"Número de registros (pasajeros): {df.shape[0]}")
print(f"Número de columnas (variables): {df.shape[1]}")
print("\nTipos de datos y valores nulos:")
print(df.info())
print(f"\nRegistros duplicados: {df.duplicated().sum()}")

# 3. Tratamiento de valores faltantes
print("\n--- TRATAMIENTO DE DATOS ---")
# Age: Se imputa con la mediana ya que es menos sensible a valores atípicos que el promedio.
mediana_edad = df['Age'].median()
df['Age'] = df['Age'].fillna(mediana_edad)

# Embarked: Al ser categórica y tener solo 2 nulos, se imputa con la moda (el puerto más frecuente).
moda_embarque = df['Embarked'].mode()[0]
df['Embarked'] = df['Embarked'].fillna(moda_embarque)

# Cabin: Tiene demasiados valores faltantes (más del 75%). Se descarta la columna original 
# para evitar ruido, pero primero creamos una variable binaria que indique si tenía cabina o no.
df['HasCabin'] = df['Cabin'].notna().astype(int)
df.drop(columns=['Cabin'], inplace=True)
print("Valores nulos tratados exitosamente.")

# 4. Creación de nuevas variables
# Variable 1: Tamaño de la familia (Hermanos/Cónyuges + Padres/Hijos + El pasajero mismo)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# Variable 2: Categorías de edad
bins = [0, 12, 25, 60, 100]
labels = ['Niño', 'Joven', 'Adulto', 'Adulto mayor']
df['AgeCategory'] = pd.cut(df['Age'], bins=bins, labels=labels)

# 5. Análisis y Visualizaciones
print("RESULTADOS DEL ANÁLISIS")

# Análisis 1: Supervivencia General
tasa_supervivencia = df['Survived'].value_counts(normalize=True) * 100
print(f"1. Tasa de supervivencia general:\n{tasa_supervivencia.to_string()}")

plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='Survived', palette='pastel')
plt.title('Distribución de Supervivencia (0 = No, 1 = Sí)')
plt.savefig('outputs/resultados/1_supervivencia_general.png')
plt.close()

# Análisis 2: Supervivencia por Género
supervivencia_genero = df.groupby('Sex')['Survived'].mean() * 100
print(f"\n2. Supervivencia por género:\n{supervivencia_genero.to_string()}")

plt.figure(figsize=(6, 4))
sns.barplot(data=df, x='Sex', y='Survived', palette='muted', errorbar=None)
plt.title('Tasa de Supervivencia por Género')
plt.ylabel('Tasa de Supervivencia')
plt.savefig('outputs/resultados/2_supervivencia_genero.png')
plt.close()

# Análisis 3: Supervivencia por Clase (Pclass)
supervivencia_clase = df.groupby('Pclass')['Survived'].mean() * 100
print(f"\n3. Supervivencia por clase de billete:\n{supervivencia_clase.to_string()}")

plt.figure(figsize=(6, 4))
sns.barplot(data=df, x='Pclass', y='Survived', palette='deep', errorbar=None)
plt.title('Tasa de Supervivencia por Clase')
plt.ylabel('Tasa de Supervivencia')
plt.savefig('outputs/resultados/3_supervivencia_clase.png')
plt.close()

# Análisis 4: Supervivencia por Categoría de Edad
supervivencia_edad = df.groupby('AgeCategory', observed=False)['Survived'].mean() * 100
print(f"\n4. Supervivencia por categoría de edad:\n{supervivencia_edad.to_string()}")

plt.figure(figsize=(8, 5))
sns.barplot(data=df, x='AgeCategory', y='Survived', palette='Set2', errorbar=None)
plt.title('Tasa de Supervivencia por Grupo de Edad')
plt.ylabel('Tasa de Supervivencia')
plt.savefig('outputs/resultados/4_supervivencia_edad.png')
plt.close()

print("EJECUCIÓN EXITOSA")
print("Las gráficas han sido guardadas en la carpeta 'outputs/resultados/'.")