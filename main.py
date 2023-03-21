from fastapi import FastAPI
from typing import Union
import pandas as pd

app= FastAPI(title='Consultas',
             description='Consulta',
             version='1.0.1')


@app.get('/')
async def index():
    hola='Bienvenidos, agreagando /docs a la ruta se accede a la documentacion.'
    return hola


@app.get('/max_duration/')
async def get_max_duration(year:Union[int, None] = None, platform:Union[str, None] = None, duration_type:Union[str, None] = None):
    df_stream_platforms= pd.read_csv('stream_platforms.csv')
    if year and platform and duration_type:
        duration= df_stream_platforms['duration_int'][(df_stream_platforms['release_year'] == year)
                                                       & (df_stream_platforms['platform'] == platform) 
                                                       & (df_stream_platforms['duration_type'] == duration_type) ].max()
        nombre=df_stream_platforms['title'][(df_stream_platforms['release_year'] == year) 
                                                & (df_stream_platforms['platform'] == platform) 
                                                & (df_stream_platforms['duration_type'] == duration_type)
                                                & (df_stream_platforms['duration_int'] == int(duration)) ]
    elif year and platform:
        duration= df_stream_platforms['duration_int'][(df_stream_platforms['release_year'] == year)
                                                        & (df_stream_platforms['platform'] == platform)].max()
        nombre=df_stream_platforms['title'][(df_stream_platforms['release_year'] == year) 
                                    & (df_stream_platforms['platform'] == platform) & (df_stream_platforms['duration_int'] == int(duration)) ]
    elif year and duration_type:
        duration= df_stream_platforms['duration_int'][(df_stream_platforms['release_year'] == year)
                                                        &(df_stream_platforms['duration_type'] == duration_type) ].max()
        nombre=df_stream_platforms['title'][(df_stream_platforms['release_year'] == year) 
                                            & (df_stream_platforms['duration_type'] == duration_type) & (df_stream_platforms['duration_int'] == int(duration)) ]
    elif platform and duration_type:
        duration= df_stream_platforms['duration_int'][(df_stream_platforms['platform'] == platform) 
                                                       & (df_stream_platforms['duration_type'] == duration_type) ].max()
        nombre=df_stream_platforms['title'][(df_stream_platforms['platform'] == platform) 
                                            & (df_stream_platforms['duration_type'] == duration_type) & (df_stream_platforms['duration_int'] == int(duration)) ]
    elif year:
        duration= df_stream_platforms['duration_int'][(df_stream_platforms['release_year'] == year)].max()
        nombre=df_stream_platforms['title'][(df_stream_platforms['release_year'] == year) & (df_stream_platforms['duration_int'] == int(duration)) ]
    elif platform:
        duration= df_stream_platforms['duration_int'][(df_stream_platforms['platform'] == platform) ].max()
        nombre=df_stream_platforms['title'][(df_stream_platforms['platform'] == platform) & (df_stream_platforms['duration_int'] == int(duration)) ]
    elif duration_type:
        duration= df_stream_platforms['duration_int'][(df_stream_platforms['duration_type'] == duration_type) ].max()
        nombre=df_stream_platforms['title'][(df_stream_platforms['duration_type'] == duration_type) & (df_stream_platforms['duration_int'] == int(duration)) ]
    else:
        duration= df_stream_platforms['duration_int'].max()
        nombre=df_stream_platforms['title'][df_stream_platforms['duration_int'] == int(duration)]
    return  list(nombre)

@app.get('/score_count/')
async def get_score_count(platform:str, score:float, year:int):
    df_stream_platforms= pd.read_csv('stream_platforms.csv')
    cantidad= df_stream_platforms['id'][(df_stream_platforms['platform']== platform) & (round(df_stream_platforms['score'],2) > score) &( df_stream_platforms['release_year']== year)].count()
    return str(cantidad)

@app.get('/count_platform/{platform}')
async def get_count_platform(platform:str):
    df_stream_platforms= pd.read_csv('stream_platforms.csv')
    cantidad= df_stream_platforms['id'][df_stream_platforms['platform']== platform].count()
    return str(cantidad)

@app.get('/actor/')
async def get_actor(platform:str, year:int):
    df_stream_platforms= pd.read_csv('stream_platforms.csv')
    cast= df_stream_platforms['cast'][(df_stream_platforms['platform'] == platform) & (df_stream_platforms['release_year'] == year)]

    lista_actores=[]
    for i in cast:
        lista=[' ']
        for n in str(i) :
            if n == ',':
                nombre_actor=''.join(lista)
                lista_actores.append(nombre_actor)
                lista.clear()
            else:
                lista.append(n)
    actor=pd.DataFrame(lista_actores)
    actor=actor.drop_duplicates(0)
    actor[1]=list(actor.groupby(0)[0].count())
    actor=actor[0][actor[1].max()]
    return str(actor)
            