import pandas as pd
import matplotlib.pyplot as plt

            #### diputados ####

diputados=pd.read_excel(r'Congreso.xlsx',sheet_name='Diputados')
diputados=diputados.dropna()

dip_nombres=diputados['Legislador'].values.tolist()
dip_ejercicio=diputados['dias ejercicio 2'].values.tolist()
dip_provincias=diputados['Distrito'].values.tolist()

dic_diputados_dias={}

def contar_mandatos(cargo,ejercicio,diccionario):
    for a, b in zip(cargo, ejercicio):
        if a in diccionario:
            diccionario[a] += b
        else:
            diccionario[a] = b
    return diccionario

diputados_mandatos=contar_mandatos(dip_nombres,dip_ejercicio,dic_diputados_dias)

dic_provincias={}

def cargos_provincias(cargo,provincias,diccionario):
    for a,b in zip(cargo,provincias):
        if a in diccionario:
            diccionario[a]=b
        else:
            diccionario[a]=b
    return diccionario

diputados_provincias=cargos_provincias(dip_nombres,dip_provincias,dic_provincias)


df_diputados=pd.DataFrame.from_dict(diputados_mandatos,orient='index')
df_diputados_provincias=pd.DataFrame.from_dict(diputados_provincias,orient='index')

df_diputados_completo=pd.merge(df_diputados,df_diputados_provincias,left_index=True,right_index=True)
df_diputados_completo.columns=['Años','Provincia']
df_diputados_completo=df_diputados_completo.sort_values(by=['Años'], ascending=False).reset_index()
df_diputados_completo.columns=['Diputado','Años','Provincia']
df_diputados_completo_10=df_diputados_completo.head(10)


                #### senadores####

senadores=pd.read_excel(r'Congreso.xlsx',sheet_name='Senadores')
democracia='1983-12-10'                                         #el df de senadores incluye senadores desde 1900

senadores_dmc=senadores.drop(senadores[senadores['CESE PERIODO REAL 2'] <= democracia].index)
sen_nombres=senadores_dmc['SENADOR'].values.tolist()
sen_ejercicio=senadores_dmc['EJERCICIO'].values.tolist()
sen_provincias=senadores_dmc['PROVINCIA'].values.tolist()

dic_provincias_sen={}
senadores_provincias=cargos_provincias(sen_nombres,sen_provincias,dic_provincias_sen)
df_senadores_provincias=pd.DataFrame.from_dict(senadores_provincias,orient='index')

dic_senadores_dias={}
senadores_mandatos=contar_mandatos(sen_nombres,sen_ejercicio,dic_senadores_dias)
df_senadores_mandatos=pd.DataFrame.from_dict(senadores_mandatos,orient='index')

df_senadores_completo=pd.merge(df_senadores_mandatos,df_senadores_provincias,left_index=True,right_index=True)
df_senadores_completo.columns=['Años','Provincia']
df_senadores_completo['Años']=df_senadores_completo['Años']/365
df_senadores_completo=df_senadores_completo.sort_values(by=['Años'],ascending=False)
df_senadores_completo_10=df_senadores_completo.head(10).reset_index()
df_senadores_completo_10.columns=['Senador','Años','Provincia']

plt.style.use('ggplot')
fig, axes=plt.subplots(2)

axes[0].title.set_text('DIPUTADOS CON MAS AÑOS EN LA CÁMARA')
axes[0].barh(df_diputados_completo_10['Diputado'],df_diputados_completo_10['Años'],color='darksalmon')

axes[1].title.set_text('SENADORES CON MAS AÑOS EN LA CÁMARA')
axes[1].barh(df_senadores_completo_10['Senador'],df_senadores_completo_10['Años'],color='darksalmon')

def anotar_provincias(df_cargos,df_provincias,df_años,axes,count=0):
   for a in df_cargos.values.tolist():
       texto=df_provincias.values.tolist()[count]
       x_ubicacion =0.10
       y_ubicacion = a
       axes.annotate(texto, xy=(x_ubicacion, y_ubicacion), xytext=(x_ubicacion, y_ubicacion))
       count +=1

anotar_provincias(df_diputados_completo_10['Diputado'],df_diputados_completo_10['Provincia'],df_diputados_completo_10['Años'],axes[0])
anotar_provincias(df_senadores_completo_10['Senador'],df_senadores_completo_10['Provincia'],df_senadores_completo_10['Años'],axes[1])

def anotar_años(df_cargos, df_años, axes, count=0):
    for a in df_cargos.values.tolist():
        texto = str(round((df_años.values.tolist()[count]), 2))
        x_ubicacion = df_años.values.tolist()[count]
        y_ubicacion = a
        axes.annotate(texto, xy=(x_ubicacion, y_ubicacion), xytext=(x_ubicacion, y_ubicacion))
        count += 1

anotar_años(df_diputados_completo_10['Diputado'],df_diputados_completo_10['Años'],axes[0])
anotar_años(df_senadores_completo_10['Senador'],df_senadores_completo_10['Años'],axes[1])

axes[0].invert_yaxis()
axes[1].invert_yaxis()

print(df_diputados_completo.describe())
print(df_senadores_completo.describe())

plt.tight_layout()
plt.show()
