# worker.py
import pika
import json
from PIL import Image
import os


def resize_image(image_path, output_folder="resized", size=(128, 128)):
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the original image
    with Image.open(image_path) as img:
        # Resize image while maintaining aspect ratio
        img.thumbnail(size)

        # Create output path
        filename = os.path.basename(image_path)  # example: "cat.jpg"
        output_path = os.path.join(output_folder, filename)

        # Save resized image
        img.save(output_path)
        print(f"✅ Resized image saved to: {output_path}")


def callback(ch, method, properties, body):
    data = json.loads(body)
    image_path = data["image_path"]
    try:
        resize_image(image_path)
    except Exception as e:
        print(f"❌ Error resizing {image_path}: {e}")


credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        virtual_host="/",
        credentials=credentials,
    )
)

channel = connection.channel()
channel.queue_declare(queue="resize_image")
channel.basic_consume(queue="resize_image", on_message_callback=callback, auto_ack=True)

print("👂 Waiting for image resize tasks...")
channel.start_consuming()
