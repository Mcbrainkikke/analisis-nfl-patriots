import pandas as pd
import matplotlib.pyplot as plt

# carga de datos
df_scores = pd.read_csv('spreadspoke_scores.csv')
df_teams = pd.read_csv('nfl_teams.csv')

#Conversión de fecha real para que se ordene correctamente
df_scores['schedule_date'] = pd.to_datetime(df_scores['schedule_date'])

# Exploración del archivo principal
print('=== Scores ===')
print(df_scores.shape) # develve dos valores (filas y columnas)
print(df_scores.columns.tolist()) # Muestra los nombres de todas las columnas como una lista
print(df_scores.head(3)) # Muestra las 3 primeras filas del DataFrame
print()

# filtración donde solo los Patriots jugaron, local o visitante
patriots = df_scores[
	(df_scores['team_home'] == 'New England Patriots') |
	(df_scores['team_away'] == 'New England Patriots')
].copy()

print("=== PATRIOTS===")
print(f"Total de partidos {len(patriots)}")
print(f"Desde: {patriots["schedule_date"].min()}")
print(f"Hasta: {patriots["schedule_date"].max()}")
print()

# Función que determina si los Patriots ganaron o perdieron en cada partido
def resultado_patriots (fila):
	if fila['team_home'] == 'New England Patriots': #Si los Patriots son el equipo local, entra al bloque
		if fila['score_home'] > fila['score_away']:
			return 'Ganado'
		else:
			return 'Perdido'
	else:
		if fila['score_away'] > fila['score_home']:
			return 'Ganado'
		else:
			return 'Perdido' 
patriots['resultado'] = patriots.apply(resultado_patriots, axis=1) #toma la función creada y la aplica a cada fila del DataFrame una por una. axis=1 hace que recorra la fila de arriba hacia abajo, no por colmnas

print('=== Resultados ===')
print(patriots['resultado'].value_counts()) #Cuenta cuantas veces aparece cada valor en la columna resultado. Arroja cuantas victorias y cuantas derrotas tiene el historial

#.groupby() agrupa todos los partidos por temporada
#.values_counts() cuenta cuantas victorias y derrotas hay
# .unstack() convierte esos conteos en columnas separadas: uno para ganados otros para perdidos
por_temporada = patriots.groupby('schedule_season')['resultado'].value_counts().unstack(fill_value=0)

print('=== RENDIMIENTO POR TEMPORADA ===')
print(por_temporada)

# Grafica
# grafica de victorias y derrotas por temporadacon barras 
fig, ax = plt.subplots(figsize=(18,6))

# barra de victoria
ax.bar(por_temporada.index, por_temporada['Ganado'],
	   label='Ganado', color='steelblue')

# barra de derrotas
ax.bar(por_temporada.index, por_temporada['Perdido'],
	   bottom=por_temporada['Ganado'], # bottom apila barrada donde finaliza la otra
	   label='Perdido', color='tomato')

plt.title('New England Patriots — Victorias y Derrotas por Temporada')
plt.xlabel('Temporada')
plt.ylabel('Partidos')
plt.legend(['Ganado', 'Perdido'])
plt.xticks(por_temporada.index, rotation=90, fontsize=7) # rota las fechas del eje X para que no se amontonen
plt.tight_layout()
plt.show()