import sys
import plotly.graph_objects as go
import plotly.io as pio

def heapify(arr, n, i, frames):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        frames.append({
            'arr': arr.copy(),
            'stage': 'heapify',
            'active': list(range(n)),
            'current': i
        })
        heapify(arr, n, largest, frames)

def heap_sort_with_animation(arr):
    n = len(arr)
    frames = [{'arr': arr.copy(), 'stage': 'initial', 'active': list(range(n))}]

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, frames)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        frames.append({
            'arr': arr.copy(),
            'stage': 'extract',
            'active': list(range(i)) + [i],
            'current': 0
        })
        heapify(arr, i, 0, frames)
    
    return frames

def create_animation(frames, output_file='heap_sort_animation.html'):
    fig = go.Figure()
    max_val = max(max(frame['arr']) for frame in frames)
    
    color_map = {
        'default': 'rgb(173, 216, 230)',  # Light Blue
        'active': 'rgb(144, 238, 144)',   # Light Green
        'current': 'rgb(255, 99, 71)',    # Light Tomato
        'extracted': 'rgb(255, 215, 0)'   # Light Golden Rod Yellow
    }

    def create_bar_trace(frame):
        colors = [color_map['default'] for _ in frame['arr']]
        for i in frame['active']:
            colors[i] = color_map['active']
        if frame['stage'] == 'extract':
            for i in frame['active']:
                colors[i] = color_map['extracted']
        if 'current' in frame:
            colors[frame['current']] = color_map['current']

        return go.Bar(
            x=list(range(len(frame['arr']))),
            y=frame['arr'],
            marker_color=colors,
            text=[str(x) for x in frame['arr']],
            textposition='outside',
            hoverinfo='text'
        )

    fig.add_trace(create_bar_trace(frames[0]))
    fig_frames = [go.Frame(data=[create_bar_trace(frame)], name=str(i)) for i, frame in enumerate(frames)]
    fig.frames = fig_frames

    fig.update_layout(
        title='Animación de Heap Sort',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])],
        )],
        height=600
    )

    fig.update_xaxes(title_text='Índice')
    fig.update_yaxes(range=[0, max_val * 1.1], title_text='Valor')
    pio.write_html(fig, file=output_file, auto_open=True, auto_play=False)
    print(f"La animación ha sido guardada en {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py 10 5 8 3 6 ...")
        sys.exit(1)

    try:
        arr = [int(x) for x in sys.argv[1:]]
    except ValueError:
        print("Error: Todos los valores deben ser números enteros.")
        sys.exit(1)

    print(f"Array ingresado: {arr}")
    frames = heap_sort_with_animation(arr)
    create_animation(frames)
