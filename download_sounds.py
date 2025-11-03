import requests
import os

urls = {
    'ambient-waves.mp3': 'https://cdn.pixabay.com/download/audio/2022/03/15/audio_c2e40e2e6b.mp3?filename=ocean-wave-112906.mp3',
    'soft-chime.mp3': 'https://cdn.pixabay.com/download/audio/2022/01/18/audio_c8374f8f28.mp3?filename=meditation-bell-sound-94466.mp3',
    'calm-music.mp3': 'https://cdn.pixabay.com/download/audio/2023/06/13/audio_539179d9a.mp3?filename=calm-meditation-144003.mp3'
}

os.makedirs('static/sounds', exist_ok=True)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Referer': 'https://pixabay.com/'
}

for name, url in urls.items():
    out_path = os.path.join('static', 'sounds', name)
    print(f'Downloading {name}...')
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        with open(out_path, 'wb') as f:
            f.write(r.content)
        print('Saved to', out_path)
    except Exception as e:
        print('Failed to download', name, '->', e)
print('Done')
