from product.models import Prediccion
import matplotlib.pyplot as plt
import io
import base64



def get_predictions_data_and_generate_chart():
    # Obtener todas las predicciones de la base de datos
    predictions = Prediccion.objects.all()

    # Agrupar predicciones por fecha
    data = {}
    for pred in predictions:
        date_str = pred.fecha.strftime("%d/%m/%Y")
        if date_str not in data:
            data[date_str] = {
                'capistrano': 0,
                'lala': 0,
                'san rafael': 0,
                'fud': 0,
                'villita': 0,
                'zwan': 0,
                'bafar': 0,
                'chimex': 0,
                'kir': 0,
                'sabori': 0,
            }
        data[date_str]['capistrano'] += pred.cantidad_capistrano
        data[date_str]['lala'] += pred.cantidad_lala
        data[date_str]['san rafael'] += pred.cantidad_san_rafael
        data[date_str]['fud'] += pred.cantidad_fud
        data[date_str]['villita'] += pred.cantidad_villita
        data[date_str]['zwan'] += pred.cantidad_zwan
        data[date_str]['bafar'] += pred.cantidad_bafar
        data[date_str]['chimex'] += pred.cantidad_chimex
        data[date_str]['kir'] += pred.cantidad_kir
        data[date_str]['sabori'] += pred.cantidad_sabori

    # Construir datos para la gráfica
    labels = list(data.keys())
    if not labels:
        return "", data  # Retornar cadena vacía si no hay datos

    capistrano_counts = [data[date]['capistrano'] for date in labels]
    lala_counts = [data[date]['lala'] for date in labels]
    san_rafael_counts = [data[date]['san rafael'] for date in labels]
    fud_counts = [data[date]['fud'] for date in labels]
    villita_counts = [data[date]['villita'] for date in labels]
    zwan_counts = [data[date]['zwan'] for date in labels]
    bafar_counts = [data[date]['bafar'] for date in labels]
    chimex_counts = [data[date]['chimex'] for date in labels]
    kir_counts = [data[date]['kir'] for date in labels]
    sabori_counts = [data[date]['sabori'] for date in labels]

    daily_data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'CAPISTRANO',
                'data': capistrano_counts,
                'backgroundColor': '#009975',
            },
            {
                'label': 'LALA',
                'data': lala_counts,
                'backgroundColor': '#7BE495',
            },
            {
                'label': 'SAN RAFAEL',
                'data': san_rafael_counts,
                'backgroundColor': '#FF5733',
            },
            {
                'label': 'FUD',
                'data': fud_counts,
                'backgroundColor': '#C70039',
            },
            {
                'label': 'VILLITA',
                'data': villita_counts,
                'backgroundColor': '#900C3F',
            },
            {
                'label': 'ZWAN',
                'data': zwan_counts,
                'backgroundColor': '#581845',
            },
            {
                'label': 'BAFAR',
                'data': bafar_counts,
                'backgroundColor': '#FFC300',
            },
            {
                'label': 'CHIMEX',
                'data': chimex_counts,
                'backgroundColor': '#DAF7A6',
            },
            {
                'label': 'KIR',
                'data': kir_counts,
                'backgroundColor': '#FF5733',
            },
            {
                'label': 'SABORI',
                'data': sabori_counts,
                'backgroundColor': '#C70039',
            }
        ]
    }

    # Generar la gráfica de barras
    chart_img_str = generate_bar_chart(daily_data)
    return chart_img_str

def generate_bar_chart(daily_data):
    # Datos para la gráfica
    labels = daily_data['labels']
    datasets = daily_data['datasets']

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Preparar los datos de la gráfica para apilamiento
    capistrano_data = datasets[0]['data']
    lala_data = datasets[1]['data']
    san_rafael_data = datasets[2]['data']
    fud_data = datasets[3]['data']
    villita_data = datasets[4]['data']
    zwan_data = datasets[5]['data']
    bafar_data = datasets[6]['data']
    chimex_data = datasets[7]['data']
    kir_data = datasets[8]['data']
    sabori_data = datasets[9]['data']

    # Gráfica de barras apiladas
    bars1 = ax.bar(labels, capistrano_data, label=datasets[0]['label'], color=datasets[0]['backgroundColor'])
    bars2 = ax.bar(labels, lala_data, bottom=capistrano_data, label=datasets[1]['label'], color=datasets[1]['backgroundColor'])
    bars3 = ax.bar(labels, san_rafael_data, bottom=[i+j for i,j in zip(capistrano_data, lala_data)], label=datasets[2]['label'], color=datasets[2]['backgroundColor'])
    bars4 = ax.bar(labels, fud_data, bottom=[i+j+k for i,j,k in zip(capistrano_data, lala_data, san_rafael_data)], label=datasets[3]['label'], color=datasets[3]['backgroundColor'])
    bars5 = ax.bar(labels, villita_data, bottom=[i+j+k+l for i,j,k,l in zip(capistrano_data, lala_data, san_rafael_data, fud_data)], label=datasets[4]['label'], color=datasets[4]['backgroundColor'])
    bars6 = ax.bar(labels, zwan_data, bottom=[i+j+k+l+m for i,j,k,l,m in zip(capistrano_data, lala_data, san_rafael_data, fud_data, villita_data)], label=datasets[5]['label'], color=datasets[5]['backgroundColor'])
    bars7 = ax.bar(labels, bafar_data, bottom=[i+j+k+l+m+n for i,j,k,l,m,n in zip(capistrano_data, lala_data, san_rafael_data, fud_data, villita_data, zwan_data)], label=datasets[6]['label'], color=datasets[6]['backgroundColor'])
    bars8 = ax.bar(labels, chimex_data, bottom=[i+j+k+l+m+n+o for i,j,k,l,m,n,o in zip(capistrano_data, lala_data, san_rafael_data, fud_data, villita_data, zwan_data, bafar_data)], label=datasets[7]['label'], color=datasets[7]['backgroundColor'])
    bars9 = ax.bar(labels, kir_data, bottom=[i+j+k+l+m+n+o+p for i,j,k,l,m,n,o,p in zip(capistrano_data, lala_data, san_rafael_data, fud_data, villita_data, zwan_data, bafar_data, chimex_data)], label=datasets[8]['label'], color=datasets[8]['backgroundColor'])
    bars10 = ax.bar(labels, sabori_data, bottom=[i+j+k+l+m+n+o+p+q for i,j,k,l,m,n,o,p,q in zip(capistrano_data, lala_data, san_rafael_data, fud_data, villita_data, zwan_data, bafar_data, chimex_data, kir_data)], label=datasets[9]['label'], color=datasets[9]['backgroundColor'])

    # Configuración de la gráfica
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cantidad')
    ax.set_title('Distribución de Productos por Fecha')
    ax.legend()

    # Añadir porcentajes dentro de cada segmento
    for i in range(len(labels)):
        total = sum([capistrano_data[i], lala_data[i], san_rafael_data[i], fud_data[i], villita_data[i], zwan_data[i], bafar_data[i], chimex_data[i], kir_data[i], sabori_data[i]])
        if total > 0:
            cumulative_bottom = 0  # Seguimiento de la posición inferior de cada segmento apilado
            for dataset in datasets:
                value = dataset['data'][i]
                if value > 0:
                    percentage = (value / total) * 100
                    ax.text(i, cumulative_bottom + value / 2, f'{percentage:.1f}%', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
                    cumulative_bottom += value

    # Ajustar el diseño para evitar superposición
    plt.tight_layout()

    # Convertir la gráfica a imagen base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return chart_img_str

def create_chart(data):
    # Crear un gráfico usando los datos proporcionados
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values())
    plt.title('Predicciones por Sucursal')
    plt.xlabel('Sucursal')
    plt.ylabel('Cantidad de Productos')
    
    # Guardar el gráfico en un objeto BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    # Convertir la imagen a base64 para enviarla al HTML
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str
