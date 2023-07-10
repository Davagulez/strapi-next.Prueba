import requests
import json
import datetime
from pyhomebroker import HomeBroker as hb

# Obtener fecha actual y fecha del bimestre
hoy = datetime.date.today()
bimestre = hoy - datetime.timedelta(days=10)

# Convertir fechas a formato necesario
hoy_dia, hoy_mes, hoy_ano = int(hoy.strftime('%d')), int(hoy.strftime('%m')), int(hoy.strftime('%Y'))
b_dia, b_mes, b_ano = int(bimestre.strftime('%d')), int(bimestre.strftime('%m')), int(bimestre.strftime('%Y')) 

# Configuración del homebroker
broker = '265'
dni = 26508098
user = 'guillea1978'
password = 'Milanesa2021%'

# Iniciar sesión en el homebroker
hb_instance = hb(int(broker))
hb_instance.auth.login(dni=dni, user=user, password=password, raise_exception=True)
hb_instance.online.connect()

# Lista de activos y stock
lista = ['bbar', 'bma', 'supv']
stock = 'ggal'

# Obtener datos históricos de precios
numerad = []
for i in range(len(lista)):
    numerad.append(hb_instance.history.get_daily_history(lista[i], datetime.date(hoy_ano, b_mes, b_dia), datetime.date(hoy_ano, hoy_mes, hoy_dia)))
    numerad[i].set_index("date", inplace=True)

denominador = hb_instance.history.get_daily_history(stock, datetime.date(hoy_ano, b_mes, b_dia), datetime.date(hoy_ano, hoy_mes, hoy_dia))
denominador.set_index("date", inplace=True)

# Calcular relaciones
relacion = []
rel_max = []
rel_min = []
rel_mu = []
rel_std = []

for i in range(len(lista)):
    relacion.append(numerad[i].close / denominador.close)
    rel_max.append(relacion[i].max())
    rel_min.append(relacion[i].min())
    rel_mu.append(relacion[i].mean())
    rel_std.append(relacion[i].std())

# Autenticación y obtención de token
API_ENDPOINT = "https://api.invertironline.com/token"
username = "guilleacosta"
password = "Milanesa2020%"
data = {
    "username": username,
    "password": password,
    "grant_type": "password"
}

r = requests.post(url=API_ENDPOINT, data=data)
token_data = r.json()
access_token = token_data["access_token"]
refresh_token = token_data["refresh_token"]

data_refresh = {
    "refresh_token": refresh_token,
    "grant_type": "refresh_token"
}

r = requests.post(url=API_ENDPOINT, data=data_refresh)
access_token2 = "Bearer " + access_token
headers = {"Authorization": access_token2}

print(access_token2)

# Obtener cotizaciones
cotizaciones = []
for i in range(len(lista)):
    r = requests.get('https://api.invertironline.com/api/bcba/Titulos/' + lista[i] + '/cotizacion', headers=headers)
    cotizaciones.append(json.loads(r.text))

r = requests.get('https://api.invertironline.com/api/bcba/Titulos/' + stock + '/cotizacion', headers=headers)
cotizacion_stock = json.loads(r.text)

# Imprimir resultados
print("----------------------------------------------------")
for i in range(len(lista)):
    print(lista[i])
    CT = [
        cotizaciones[i]['puntas'][0]['cantidadCompra'],
        cotizaciones[i]['puntas'][0]['precioCompra'],
        cotizaciones[i]['puntas'][0]['precioVenta'],
        cotizaciones[i]['puntas'][0]['cantidadVenta']
    ]
    print(CT)
    ratio = cotizaciones[i]['puntas'][0]['precioVenta'] / cotizacion_stock['puntas'][0]['precioCompra']
    print('El ratio', lista[i], '/', stock, 'es', round(ratio, 2) * 100, '%')
    print("El Max es:", round(rel_max[i] * 100, 0), '%')
    print("El min es:", round(rel_min[i] * 100, 0), '%')
    print("El rango es:", round(rel_mu[i] * 100, 0), '%')
    print("El desvio es:", round(rel_std[i] * 100, 0), '%')
    print('Banda superior', round((rel_mu[i] + rel_std[i]) * 100, 0), '%')
    print('Banda inferior', round((rel_mu[i] - rel_std[i]) * 100, 0), '%')
    print("----------------------------------------------------")

print(stock)
CTSTK = [
    cotizacion_stock['puntas'][0]['cantidadCompra'],
    cotizacion_stock['puntas'][0]['precioCompra'],
    cotizacion_stock['puntas'][0]['precioVenta'],
    cotizacion_stock['puntas'][0]['cantidadVenta']
]
print("----------------------------------------------------")
print(CTSTK)

