# Este es un script para probar la API, haciendo solicitudes de todas las areas de búsqueda del df, o aleatoriamente
# modificando la variable rand por la cantidad de registros que quiere que se usen.
# Los parámetros modificables serán marcados con lineas en los comentarios para identificarlos fácilmente.
import requests # Hacemos solicitudes HTTP.
import pandas as pd # Pandas para trabajar con datos.

# Lista de elementos a enviar en la solicitud
elementos = pd.read_csv('Data/Processed/Query_output/developer.csv') # -----------------------------------------||
# Columna objetivo en el DataFrame.
col = 'developer' # --------------------------------------------------------------------------------------------||
# Función que se usará en la URL.
func = 'developer' # -------------------------------------------------------------------------------------------||
# Elementos únicos en la columna objetivo.
elementos = elementos[col].unique()
# URL base a la que se enviarán las solicitudes.
url_base = 'http://localhost:8000/'
# URL Final.
url_base += func + '/'
# Si se desea obtener una muestra, de cuantos elementos. 0 para no obtener.
rand = 200 # --------------------------------------------------------------------------------------------------||
# Verificamos si se quiere una muestra.
if rand:
    # Tomamos la muestra de un Series de la lista elementos y lo volvemos a convertir en lista.
    elementos = pd.Series(elementos).sample(n=rand)
    elementos = elementos.to_list()
# Iterar sobre cada elemento y enviar una solicitud GET a la URL correspondiente.
for elemento in elementos:
    # URL + elemento a buscar.
    url = url_base + elemento
    # Realizar la solicitud POST
    response = requests.get(url)
    # Verificar el estado de la respuesta.
    if response.status_code == 200:
        # Mostrar texto de la respuesta.
        print(response.text)
        # continue
    # Si no se encuentra algo, mostrar error 404 con saltos de linea para diferenciarlos fácilmente en la consola.
    elif response.status_code == 404:
        print(f"\n404: {response.text} para: {elemento}\n")
    # Mostrar algún otro error junto con la respuesta.
    else:
        print(f'\nError al enviar la solicitud para {elemento}: {response.status_code}\n')
        print({response.text})
