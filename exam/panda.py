import pandas as pd

# création du datafarme à partir du fichier csv
df = pd.read_csv('questions.csv')

# information sur le dataframe
df.info()

# affichage des 20 premières lignes et 20 dernières lignes
print(df.head(20))
print(df.tail(20))

# affichage d'une question
question = df.iloc[7,:]
question = question.to_dict()

# affichage des uses et subjects
colonnes = ['use', 'subject']
df_select = df[colonnes]
pd.set_option('display.max_rows', None)
print(df_select)
pd.reset_option('display.max_rows')

# remplacement d'une valeur dans une colonne
df['subject'] = df['subject'].replace('Sytèmes distribués', 'Systèmes distribués')

# remplacement des valeurs incorrectes pour un export JSON par exemple (NaN en null)
df = df.fillna('null')

# filtrer un dataframe en fonction d'une valeur dans une colonne
df_new = df[df['use'] == 'Total Bootcamp']
df_select = df_new[colonnes]
print(df_select)

# écrire dans un fichier (CSV, JSON)
df.to_csv('test.csv')
df.to_json('test.json')
