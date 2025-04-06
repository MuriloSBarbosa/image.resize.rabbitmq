import requests
import os


def download_image(url, filename, folder="images"):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded: {path}")
        return path
    else:
        print(f"❌ Failed to download {url}")
        return None


if __name__ == "__main__":
    images = {
        "cat.jpg": "https://placekitten.com/800/600",
        "landscape.jpg": "https://picsum.photos/800/600",
        "dog.jpg": "https://placedog.net/800/600",
    }

    for name, url in images.items():
        download_image(url, name)
