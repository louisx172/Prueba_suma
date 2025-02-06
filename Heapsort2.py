import sys
import plotly.graph_objects as go
import json

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
        frames.append({'arr': arr.copy(), 'stage': 'heapify', 'active': list(range(n)), 'current': i})
        heapify(arr, n, largest, frames)

def heap_sort_with_animation(arr):
    n = len(arr)
    frames = [{'arr': arr.copy(), 'stage': 'initial', 'active': list(range(n))}]

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, frames)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        frames.append({'arr': arr.copy(), 'stage': 'extract', 'active': list(range(i)), 'current': 0})
        heapify(arr, i, 0, frames)
    
    return frames

def generate_animation_data(frames):
    color_map = {
        'default': 'rgb(173, 216, 230)',
        'active': 'rgb(144, 238, 144)',
        'current': 'rgb(255, 99, 71)',
        'extracted': 'rgb(255, 215, 0)'
    }

    data_frames = []
    for frame in frames:
        colors = [color_map['default']] * len(frame['arr'])
        for i in frame['active']:
            colors[i] = color_map['active']
        if 'current' in frame:
            colors[frame['current']] = color_map['current']

        data_frames.append({
            'x': list(range(len(frame['arr']))),
            'y': frame['arr'],
            'colors': colors
        })

    return json.dumps(data_frames)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py 10 5 8 3 6 ...")
        sys.exit(1)

    try:
        arr = [int(x) for x in sys.argv[1:]]
    except ValueError:
        print("Error: Todos los valores deben ser números enteros.")
        sys.exit(1)

    frames = heap_sort_with_animation(arr)
    animation_data = generate_animation_data(frames)
    
    print(animation_data)  # Imprime los datos en formato JSON para que el servidor los capture

print(json.dumps({
    "frames": [
        {"x": [0,1,2], "y": [3,1,2], "colors": ["red", "blue", "green"]},
        # ... más frames
    ]
}))
