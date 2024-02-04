# Importamos fastAPI para gestionar solicitudes HTTP.
from fastapi import FastAPI, HTTPException
# Importamos las funciones necesarias para la API.
from Api.funcs import developer, userdata, UserForGenre, best_developer_year, developer_reviews_analysis

# Creamos una instancia de FastAPI.
app = FastAPI()
# Creamos las solicitudes correspondientes a cada endpoint.
@app.get("/developer/{dev}")
async def get_developer(dev: str):
    try: 
        # Recibimos la respuesta de la función.
        elm = developer(dev)
        # Si la respuesta fue un string, es porque no hubo coincidencias y se usó la función sugerencia().
        if type(elm) == str:
            # Retornamos un 404, no se encontró, y la sugerencia en los detalles.
            raise HTTPException(status_code=404, detail=elm)
        # Si no hubo Excepción, se retorna el elemento de la respuesta de la función.
        return elm
    # Atrapamos la excepción HTTP anterior en caso de que sea necesario.
    except HTTPException:
        raise
    # Atrapamos cualquier otra Excepción y mostramos un código 500 para error interno junto con el error.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error en el servidor: {e}')

@app.get("/userdata/{user}")
async def get_userdata(user: str):
    try:
        # Recibimos la respuesta de la función. 
        elm = userdata(user)
        # Si la respuesta fue un string, es porque no hubo coincidencias y se usó la función sugerencia().
        if type(elm) == str:
            # Retornamos un 404, no se encontró, y la sugerencia en los detalles.
            raise HTTPException(status_code=404, detail=elm)
        # Si no hubo Excepción, se retorna el elemento de la respuesta de la función.
        return elm
    # Atrapamos la excepción HTTP anterior en caso de que sea necesario.
    except HTTPException:
        raise
    # Atrapamos cualquier otra Excepción y mostramos un código 500 para error interno junto con el error.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error en el servidor: {e}')

@app.get("/userForGenre/{genre}")
async def get_user_for_genre(genre: str):
    try:
        # Recibimos la respuesta de la función. 
        elm = UserForGenre(genre)
        # Si la respuesta fue un string, es porque no hubo coincidencias y se usó la función sugerencia().
        if type(elm) == str:
            # Retornamos un 404, no se encontró, y la sugerencia en los detalles.
            raise HTTPException(status_code=404, detail=elm)
        # Si no hubo Excepción, se retorna el elemento de la respuesta de la función.
        return elm
    # Atrapamos la excepción HTTP anterior en caso de que sea necesario.
    except HTTPException:
        raise
    # Atrapamos cualquier otra Excepción y mostramos un código 500 para error interno junto con el error.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error en el servidor: {e}')

@app.get("/best_developer_year/{year}")
async def get_best_developer_year(year: int):
    try:
        # Recibimos la respuesta de la función. 
        elm = best_developer_year(year)
        # Si la respuesta fue un string, es porque no hubo coincidencias y se usó la función sugerencia().
        if type(elm) == str:
            # Retornamos un 404, no se encontró, y la sugerencia en los detalles.
            raise HTTPException(status_code=404, detail=elm)
        # Si no hubo Excepción, se retorna el elemento de la respuesta de la función.
        return elm
    # Atrapamos la excepción HTTP anterior en caso de que sea necesario.
    except HTTPException:
        raise
    # Atrapamos cualquier otra Excepción y mostramos un código 500 para error interno junto con el error.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error en el servidor: {e}')

@app.get("/developer_reviews_analysis/{dev}")
async def get_developer_reviews_analysis(dev: str):
    try:
        # Recibimos la respuesta de la función. 
        elm = developer_reviews_analysis(dev)
        # Si la respuesta fue un string, es porque no hubo coincidencias y se usó la función sugerencia().
        if type(elm) == str:
            # Retornamos un 404, no se encontró, y la sugerencia en los detalles.
            raise HTTPException(status_code=404, detail=elm)
        # Si no hubo Excepción, se retorna el elemento de la respuesta de la función.
        return elm
    # Atrapamos la excepción HTTP anterior en caso de que sea necesario.
    except HTTPException:
        raise
    # Atrapamos cualquier otra Excepción y mostramos un código 500 para error interno junto con el error.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error en el servidor: {e}')