import pandas as pd
from difflib import get_close_matches


def sugerencia(text, opts):
    '''
    Sugerencia de búsqueda.

    Da una sugerencia de búsqueda en base a un texto y una lista de opciones.

    Requiere:
    importar get_close_matches de difflib.
    from difflib import get_close_matches.

    Recibe:
    str: texto a buscar.
    list: Opciones.

    Retorna:
    str: String en base a si se encontró o no la sugerencia.
    '''
    # Si algo falla al convertir los datos a string, retorna que no se pudo encontrar el texto.
    try:
        # Convertimos las opciones a string para que puedan ser tratadas o por si hay algún nan.
        opts = [str(e) for e in opts if e]
        # Convertimos el texto de ser necesario.
        if type(text) == int:
            text = str(text)
        # Buscamos opciones similares.
        similar = get_close_matches(text, opts, n=4, cutoff=0.5)
        # Si hay, las retornamos, si no, retorna que no se pudo encontrar el texto.
        if similar:
            return f"No se encontró {text}, intenta con {similar}."
        else:
            return f"No se encontró {text}."
    except:
        return f"No se encontró {text}."

def developer(dev: str):
    '''
    Información desarrollador

    Proporciona información sobre la cantidad de juegos y el porcentaje de juegos gratuitos ("free to play")
    desarrollados por un desarrollador en cada año.

    Requiere:
    Pandas.
    get_close_matches de difflib.
    Set de datos procesado games_api.csv. Consultar Queries.ipynb
    

    Recibe:
    str: El nombre de un desarrollador.

    Retorna:
    dict: Cantidad de juegos y porcentaje free to play por año de un desarrollador.
    str: Si no encuentra al desarrollador, retorna una sugerencia de búsqueda.

    Ejemplo de uso:
    developer('dev')
    returns: {'dev':{ 'año': {'total_juegos': int, '% free to play': 'XX.XX %' }, 'otro año': {...}, ... } }
    '''
    # Volvemos la cadena minúscula para facilitar su búsqueda en el dataframe.
    dev = dev.lower()
    # Cargo el data frame procesado previamente para esta función.
    try: # Verificamos que la ubicación desde la que se ejecutó sea la correcta, si no, usamos la del directorio raíz.
        df = pd.read_csv('ApiData/developer.csv')
    except FileNotFoundError:
        df = pd.read_csv('Api/ApiData/developer.csv')
    # Extraemos los desarrolladores, para no hacer todo el trabajo con un data frame vacío en caso de que no esté el desarrollador en el dataframe de juegos.
    devs = df['developer'].unique()
    # Si no se encuentra al desarrollador, sugiere algunos similares. Consulte la función sugerencia para más información.
    if not(dev in devs):
        return sugerencia(dev, devs)
    # Si el programa no retorno una sugerencia, es porque hay un desarrollador con ese nombre, lo buscamos y filtramos el data frame.
    df = df[df['developer'] == dev][['year', 'Cantidad', '% free to play']]
    # Agrupamos por año para poder exportar a diccionario y retornamos el diccionario.
    df = df.groupby('year').sum().to_dict(orient='index')
    return {dev: df}

def userdata(user_id: str):
    '''
    Información Usuario.

    Proporciona información del usuario correspondiente al id dado en los parámetros.

    Requiere:
    Pandas.
    get_close_matches de difflib.
    Set de datos previamente procesados para su uso en API. Consultar Queries.ipynb

    Recibe:
    str: El id del usuario del que se desea conocer la información.
    
    Retorna:
    dict: Diccionario con el nombre del usuario, su dinero gastado, su porcentaje de recomendación y su cantidad de juegos.

    Ejemplo de uso:
    userdata('user_id')
    returns: {'Usuario':'user_id', 'Dinero gastado': float, '% de recomendación': 'XX.XX %', 'cantidad de items': int}
    '''
    # Cargo el data frame procesado previamente para esta función.
    try: # Verificamos que la ubicación desde la que se ejecutó sea la correcta, si no, usamos la del directorio raíz.
        df = pd.read_csv('ApiData/user_data.csv')
    except FileNotFoundError:
        df = pd.read_csv('Api/ApiData/user_data.csv')
    # Verificamos que el usuario se encuentre en la lista, cargando los id de los usuarios y buscándolo, si no se encuentra, se da una sugerencia de búsqueda.
    # Consulte la función sugerencia para más información.
    users = df['id_user'].unique()
    if not (user_id in users):
        return sugerencia(user_id, users)
    # Si no se retornó una sugerencia, es porque hubo una coincidencia, extraemos dicha coincidencia del data frame.
    df = df[df['id_user'] == user_id]
    # Retornamos en un diccionario los respectivos datos del dataframe de la coincidencia, con iloc 0 ya que es un solo dato para que nos retorne el dato en si.
    # Hago parse a los valores float e int respectivamente ya que en la API por algún motivo extraño intenta iterar en los np.int64.
    return {'Usuario':user_id, 'Dinero gastado':float(df['Dinero_gastado'].iloc[0]), '% de recomendación': df['recommend'].iloc[0], 'cantidad de items':int(df['Cantidad_items'].iloc[0])}

def UserForGenre(gender: str):
    '''
    Usuario para el género.

    Busca y retorna al usuario con más horas para un dado género de videojuego agrupando las horas por el año en el que fueron obtenidas.

    Requiere:
    Pandas.
    get_close_matches de difflib.
    Set de datos previamente procesados para su uso en API. Consultar Queries.ipynb

    Recibe:
    str: Un género de videojuego.
    
    Retorna:
    dict: Un diccionario con las horas jugadas del usuario que más acumula horas para el genero ingresado, agrupadas por año.

    Ejemplo de uso:
    UserForGenre('gender')
    returns: {"Usuario con más horas jugadas para Género X" : 'usuario', "Horas jugadas":[{'Año': 'año', Horas: 'horas'}, {Año: 'año_2', Horas: 'horas_2'}, {...}, ...]}
    '''
    # Volvemos la cadena minúscula para facilitar su búsqueda en el dataframe.
    gender = gender.lower()
    # Cargo el data frame procesado previamente para esta función.
    try: # Verificamos que la ubicación desde la que se ejecutó sea la correcta, si no, usamos la del directorio raíz.
        df_year = pd.read_csv('ApiData/user_for_genre.csv', dtype={'year':int})
    except FileNotFoundError:
        df_year = pd.read_csv('Api/ApiData/user_for_genre.csv')

    # Primero verificamos que se haya ingresado un género que exista en el dataframe, si no, se hace una sugerencia de los posibles géneros.
    # Consulte la función sugerencia para más información.
    genres = df_year['genres'].unique()
    if not (gender in genres):
        return sugerencia(gender, genres)
    # Filtramos por el usuario y género que nos interesa, solo usaremos la columna año y tiempo de juego para cada año.
    df_year = df_year[df_year['genres'] == gender][['user_id', 'year', 'playtime_forever_x']]
    # Creamos la llave del diccionario que retornaremos.
    key = "Usuario con más horas jugadas para Género " + gender
    # Extraemos el usuario.
    user = df_year['user_id'].iloc[0]
    # Creamos la lista que contendrá los diccionarios con cada año y duración.
    horas = []
    # Iteramos en el dataframe.
    for i, row in df_year.iterrows():
        # Creamos el diccionario con el año y las horas correspondientes.
        diccionario = {'año': row['year'], 'horas': row['playtime_forever_x']}
        # Agregamos el diccionario a la lista.
        horas.append(diccionario)
    # Retornamos la llave, con el usuario con más horas, con la segunda llave, con la lista de horas en cada año.
    return {key:user, "Horas jugadas":horas}

def best_developer_year(year: int):
    '''
    Mejores 3 desarrolladores por año.

    Busca y retorna a los mejores 3 desarrolladores de el año dado.

    Requiere:
    Pandas.
    Set de datos previamente procesados para su uso en API. Consultar Queries.ipynb

    Recibe:
    int: El año para el cual se desea obtener el top de desarrolladores.

    Retorna:
    list: Una lista de tuplas que contiene el puesto 1, 2 y 3 de los desarrolladores con mejores reseñas buenas y recomendaciones por parte de los usuarios.
    str: En caso de no ingresar un año valido, retorna un mensaje con los años disponibles.

    Ejemplo de uso:
    best_developer_year(int año)
    returns: [{"Puesto 1" : 'dev1'}, {"Puesto 2" : 'dev2'},{"Puesto 3" : 'dev3'}]
    '''
    # Cargamos el set de datos previamente procesado para esta tarea.
    try: # Verificamos que la ubicación desde la que se ejecutó sea la correcta, si no, usamos la del directorio raíz.
        df = pd.read_csv('ApiData/best_developer_year.csv')
    except FileNotFoundError:
        df = pd.read_csv('Api/ApiData/best_developer_year.csv')

    # Cargamos los años disponibles.
    years = df['year'].unique()
    # Verificamos que se haya ingresado un año válido, de no ser así se muestran los años disponibles.
    if not(year in years):
        return f"Año no disponible, Años disponibles: {years}"
    # Filtramos y organizamos el DataFrame con el año ingresado al saber que existe en él.
    df = df[df['year'] == year].sort_values('total', ascending=False)
    # Nos quedamos solo con el desarrollador.
    df = df['developer']
    # Retornamos el respectivo puesto. Al saber que hay solo 3 valores disponibles, los localizamos directamente por su indice, previamente ordenado en el anterior paso.
    return [{'Puesto 1':df.iloc[0]}, {'Puesto 2':df.iloc[1]}, {'Puesto 3':df.iloc[2]}]

def developer_reviews_analysis(dev: str):
    '''
    Análisis de reseñas por desarrollador.

    Retorna la cantidad total de reseñas positivas y negativas de un desarrollador dado.

    Requiere:
    Pandas.
    get_close_matches de difflib.
    Set de datos previamente procesados para su uso en API. Consultar Queries.ipynb

    Recibe:
    str: Desarrollador

    Retorna:
    dict: Un diccionario con el nombre del desarrollador como llave y sus reseñas positivas y negativas como valor.

    Ejemplo de uso:
    developer_reviews_analysis('dev')
    returns: {'dev':{'Negative':'count', 'Positive':'count'}}
    '''
    # Volvemos la cadena minúscula para facilitar su búsqueda en el dataframe.
    dev = dev.lower()
    # Cargamos el set de datos previamente procesado para esta tarea.
    try: # Verificamos que la ubicación desde la que se ejecutó sea la correcta, si no, usamos la del directorio raíz.
        df = pd.read_csv('ApiData/developer_reviews_analysis.csv')
    except FileNotFoundError:
        df = pd.read_csv('Api/ApiData/developer_reviews_analysis.csv')
    # Extraemos los desarrolladores, para no hacer todo el trabajo con un data frame vacío en caso de que no esté el desarrollador en el dataframe de juegos.
    devs = df['developer'].unique()
    # Si no se encuentra al desarrollador, sugiere algunos similares. Consulte la función sugerencia para más información.
    if not(dev in devs):
        return sugerencia(dev, devs)
    # Si el programa no retorno una sugerencia, es porque hay un desarrollador con ese nombre, lo buscamos y filtramos el data frame.
    df = df[df['developer'] == dev]
    # Retornamos el diccionario con la llave siendo el desarrollador y los valores siendo las columnas negativa y positiva con su único registro.
    # Hago parse a los valores float e int respectivamente ya que en la API por algún motivo extraño intenta iterar en los np.int64.
    return {dev: {'Negative':int(df['neg'].iloc[0]), 'Positive':int(df['pos'].iloc[0])}}

def recomendacion_juego(id: int):
    '''
    Recomendación item a item.

    Retorna un diccionario con 5 recomendaciones de juegos en base al id del juego ingresado.

    Requiere:
    Pandas.
    get_close_matches de difflib.
    Set de datos previamente procesados para su uso en API. Consultar MachineLearning.ipynb

    Recibe:
    int: Id de un juego.

    Retorna:
    dict: Un diccionario con el nombre del juego ingresado. Junto a 5 recomendaciones.

    Ejemplo de uso:
    recomendacion_juego(id)
    returns: { 'Nombre_juego': [ 'recomendacion 1', 'recomendacion 2', ..., 'recomendacion 5' ] }
    '''
    # Importamos los datos previamente procesados para esta tarea.
    try: # Verificamos que la ubicación desde la que se ejecutó sea la correcta, si no, usamos la del directorio raíz.
        df = pd.read_csv('ApiData/recommend_item_to_item.csv')
    except FileNotFoundError:
        df = pd.read_csv('Api/ApiData/recommend_item_to_item.csv')
    # Extraemos los IDS únicos.
    ids = df['id'].unique()
    # Si no se encuentra el id en los ids, retornamos una sugerencia de búsqueda con IDS similares.
    if not (id in ids):
        return sugerencia(id, ids)
    # Si no se detuvo el programa con una sugerencia, es porque hay un ID válido en los datos, lo buscamos.
    df = df[df['id'] == id]
    # Creamos la llave de nuestro diccionario con el nombre del juego.
    llave = 'Recomendaciones para '
    llave += df['name'].iloc[0]
    # Retornamos el diccionario con los valores de recommend.
    return {llave: df['recommend'].iloc[0]}