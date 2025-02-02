import sys
import plotly.graph_objects as go
import numpy as np
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

    # Build the heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, frames)

    # Extract elements from the heap
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

def create_animation(frames, output_file):
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
    fig_frames = [go.Frame(data=[create_bar_trace(frame)], name=str(i)) 
                  for i, frame in enumerate(frames)]
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

    pio.write_html(fig, file=output_file, auto_open=False, auto_play=False)
    print(f"Array inicial: {frames[0]['arr']}")
    print(f"Array ordenado: {frames[-1]['arr']}")
    return frames[0]['arr'], frames[-1]['arr']

def main():
    print("Argumentos recibidos:", sys.argv)
    # Obtener el tamaño del array desde los argumentos
    size = 10  # valor por defecto
    if len(sys.argv) > 1 and sys.argv[1]:
        try:
            size = int(sys.argv[1])
            # Limitar el tamaño para evitar problemas de rendimiento
            size = min(max(size, 5), 50)  # Entre 5 y 50 elementos
        except ValueError:
            print("Error: El argumento debe ser un número entre 5 y 50")
            return

    # Generar y ordenar el array
    arr = generate_random_array(size=size)
    print(f"Array original: {arr.tolist()}")
    frames = heap_sort_with_animation(arr)
    import sys
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'heap_sort_animation.html'
    create_animation(frames, output_file)

    print(f"Array ordenado: {arr.tolist()}")

if __name__ == "__main__":
    main()
