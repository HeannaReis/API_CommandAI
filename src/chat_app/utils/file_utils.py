import os

def list_images(directory):
    return sorted(
        [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
        key=lambda x: os.path.getmtime(os.path.join(directory, x))
    )