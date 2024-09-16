import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

# Función para realizar el algoritmo de Bucket Sort y generar los frames de la animación
def bucket_sort_with_animation(arr, num_buckets=5):
    frames = []  # Lista para almacenar los frames de la animación
    n = len(arr)  # Longitud del arreglo
    min_val, max_val = np.min(arr), np.max(arr)  # Valores mínimo y máximo del arreglo
    buckets = [[] for _ in range(num_buckets)]  # Crear 'num_buckets' buckets vacíos

    # Distribuir los elementos en los buckets
    for i, num in enumerate(arr):
        # Normalizar el valor del número para ubicarlo en el bucket correcto
        normalized = (num - min_val) / (max_val - min_val)
        index = min(int(normalized * num_buckets), num_buckets - 1)
        buckets[index].append(num)  # Agregar el número al bucket correspondiente

        # Guardar el estado actual del proceso (para la animación)
        frames.append({
            'arr': arr.copy(),  # Copia del arreglo en su estado actual
            'buckets': [bucket.copy() for bucket in buckets],  # Copia del estado actual de los buckets
            'stage': 'distribute',  # Fase de distribución (distribuir números en buckets)
            'current': i  # Índice del elemento actual que se está distribuyendo
        })

    sorted_arr = []  # Lista para almacenar el arreglo ordenado

    # Combinar los buckets y ordenarlos
    for i, bucket in enumerate(buckets):
        bucket.sort()  # Ordenar los elementos dentro de cada bucket
        sorted_arr.extend(bucket)  # Agregar los elementos ordenados al arreglo final

        # Guardar el estado actual del proceso (para la animación)
        frames.append({
            'arr': np.array(sorted_arr + [0] * (n - len(sorted_arr))),  # Estado actual del arreglo ordenado
            'buckets': [bucket.copy() for bucket in buckets],  # Copia del estado actual de los buckets
            'stage': 'combine',  # Fase de combinación (los buckets se combinan)
            'current': len(sorted_arr) - 1  # Índice del último elemento que fue combinado
        })

    return frames  # Retornar los frames para la animación

# Función para crear la animación basada en los frames generados
def create_animation(frames, output_file='bucket_sort_animation.html'):
    fig = go.Figure()  # Crear la figura para la animación

    max_val = max(np.max(frame['arr']) for frame in frames)  # Encontrar el valor máximo en todos los frames para ajustar el eje Y
    color_map = {
        'default': 'rgb(173, 216, 230)',  # Color por defecto (azul claro)
        'active': 'rgb(255, 182, 193)',  # Color para el elemento activo (rosa claro)
    }

    # Función interna para crear una traza de barras para representar el arreglo
    def create_array_trace(frame):
        colors = [color_map['default'] for _ in frame['arr']]  # Colorear todas las barras por defecto
        if frame['stage'] in ['distribute', 'combine']:  # Si estamos en la fase de distribuir o combinar
            colors[frame['current']] = color_map['active']  # Colorear el elemento actual de color activo
        return go.Bar(
            y=frame['arr'],  # Valores del arreglo que se muestran en las barras
            marker_color=colors,  # Colores para las barras
            text=[str(x) for x in frame['arr']],  # Texto que muestra el valor de cada barra
            textposition='outside',  # Posición del texto (fuera de la barra)
            hoverinfo='text'  # Información que se muestra al pasar el mouse por encima
        )

    # Función interna para crear el texto que muestra el estado de los buckets
    def create_buckets_text(frame):
        buckets_text = ""
        for i, bucket in enumerate(frame['buckets']):
            # Texto para mostrar el contenido de cada bucket
            buckets_text += f"Bucket {i+1}: {', '.join(map(str, bucket)) if bucket else 'Vacío'}<br>"
        return f"<b>Estado de los buckets:</b><br>{buckets_text}"  # Devolver el texto final

    fig.add_trace(create_array_trace(frames[0]))  # Agregar la primera traza del arreglo

    # Añadir anotación para mostrar el estado de los buckets
    fig.add_annotation(
        text=create_buckets_text(frames[0]),
        xref="paper", yref="paper",
        x=0.5, y=-0.4,  # Posición de la anotación
        showarrow=False,
        font=dict(size=14, color="black"),  # Estilo de fuente
        align="center",
        bgcolor="rgba(255, 255, 255, 0.9)",  # Fondo con opacidad
        bordercolor="rgba(0, 0, 0, 0.5)",  # Color de borde
        borderwidth=2,
        opacity=0.9
    )

    fig_frames = []  # Lista de frames para la animación
    for i, frame in enumerate(frames):
        frame_data = [create_array_trace(frame)]  # Crear la traza para el frame actual
        fig_frames.append(go.Frame(data=frame_data, name=str(i)))  # Añadir el frame a la animación

        # Actualizar la anotación para cada frame
        fig.update_layout(
            annotations=[
                dict(
                    text=create_buckets_text(frame),  # Texto para mostrar el estado actual de los buckets
                    xref="paper", yref="paper",
                    x=0.5, y=-0.4,
                    showarrow=False,
                    font=dict(size=14, color="black"),
                    align="center",
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor="rgba(0, 0, 0, 0.5)",
                    borderwidth=2,
                    opacity=0.9
                )
            ]
        )

    fig.frames = fig_frames  # Asignar los frames a la figura

    # Configurar el layout y los controles de la animación
    fig.update_layout(
        title='Bucket Sort Animation',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',  # Botón para reproducir la animación
                        method='animate',
                        args=[None, dict(frame=dict(duration=500, redraw=True),  # Configurar la duración y modo
                                        fromcurrent=True,
                                        mode='immediate')])]
        )],
        height=700,  # Altura del gráfico
        margin=dict(l=20, r=20, t=100, b=200)  # Márgenes del gráfico
    )

    fig.update_yaxes(range=[0, max_val * 1.1])  # Ajustar el eje Y en función del valor máximo

    html_content = pio.to_html(fig, auto_open=False)  # Obtener el contenido HTML como cadena
    print(html_content)  # Mostrar el contenido HTML en lugar de guardarlo

# Crear un arreglo aleatorio y ejecutar el algoritmo
arr = np.random.randint(1, 100, 9)  # Crear un arreglo de 9 números aleatorios entre 1 y 100
frames = bucket_sort_with_animation(arr, num_buckets=5)  # Generar los frames de la animación
create_animation(frames)  # Crear y mostrar la animación
