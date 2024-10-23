import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

def bucket_sort_with_animation(arr, num_buckets=5):
    frames = []
    n = len(arr)
    min_val, max_val = np.min(arr), np.max(arr)
    buckets = [[] for _ in range(num_buckets)]
    
    frames.append({
        'arr': arr.tolist(),
        'buckets': [[] for _ in range(num_buckets)],
        'stage': 'initial',
        'current': -1
    })
    
    for i, num in enumerate(arr):
        normalized = (num - min_val) / (max_val - min_val)
        index = min(int(normalized * num_buckets), num_buckets - 1)
        buckets[index].append(num)
        frames.append({
            'arr': arr.tolist(),
            'buckets': [bucket.copy() for bucket in buckets],
            'stage': 'distribute',
            'current': i
        })
    sorted_arr = []
    for i, bucket in enumerate(buckets):
        bucket.sort()
        sorted_arr.extend(bucket)
        frames.append({
            'arr': sorted_arr + [0] * (n - len(sorted_arr)),
            'buckets': [bucket.copy() for bucket in buckets],
            'stage': 'combine',
            'current': len(sorted_arr) - 1
        })
    return frames

def create_animation(frames):
    fig = go.Figure()

    max_val = max(max(frame['arr']) for frame in frames)
    color_map = {
        'default': 'rgb(173, 216, 230)', 
        'active': 'rgb(255, 182, 193)', 
    }

    def create_array_trace(frame):
        colors = [color_map['default'] for _ in frame['arr']]
        if frame['stage'] in ['distribute', 'combine']:
            colors[frame['current']] = color_map['active']
        return go.Bar(
            y=frame['arr'],
            marker_color=colors,
            text=[str(x) for x in frame['arr']],
            textposition='outside',
            hoverinfo='text'
        )

    def create_buckets_text(frame):
        buckets_text = ""
        for i, bucket in enumerate(frame['buckets']):
            buckets_text += f"Bucket {i+1}: {', '.join(map(str, bucket)) if bucket else 'Vacío'}<br>"
        return f"<b>Estado de los buckets:</b><br>{buckets_text}"

    fig.add_trace(create_array_trace(frames[0]))

    fig_frames = []
    for i, frame in enumerate(frames):
        frame_data = [create_array_trace(frame)]
        frame_layout = go.Layout(
            annotations=[
                dict(
                    text=create_buckets_text(frame),
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
        fig_frames.append(go.Frame(data=frame_data, layout=frame_layout, name=str(i)))

    fig.frames = fig_frames

    fig.update_layout(
        title='Animación de Bucket Sort',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Reproducir',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])]
        )],
        height=700,
        margin=dict(l=20, r=20, t=100, b=200)
    )

    fig.add_annotation(
        text=create_buckets_text(frames[0]),
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

    fig.update_yaxes(range=[0, max_val * 1.1])

    return fig

# Generar un arreglo usando np.random.permutation
arr = np.random.permutation(100)[:9]  # Genera una permutación de 0 a 99 y toma los primeros 9 elementos
frames = bucket_sort_with_animation(arr, num_buckets=5)
animation_figure = create_animation(frames)

# Convertir la figura a una cadena HTML y guardarla en una variable
html_content = pio.to_html(animation_figure, include_plotlyjs=True, full_html=True)

print("El contenido HTML se ha generado y guardado en la variable 'html_content'")
print("Longitud del contenido HTML:", len(html_content))
print("Primeros 500 caracteres del HTML:")
print(html_content[:500])
