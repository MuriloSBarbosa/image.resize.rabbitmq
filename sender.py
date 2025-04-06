import pika
import json
import argparse
import os

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png")


def send_image_task(image_path):
    if not os.path.isfile(image_path):
        print(f"❌ File not found: {image_path}")
        return

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

    message = json.dumps({"image_path": image_path})
    channel.basic_publish(exchange="", routing_key="resize_image", body=message)
    print(f"📤 Sent image task for: {image_path}")

    connection.close()


def get_images_from_dir(directory: str):
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(SUPPORTED_EXTENSIONS)
        and os.path.isfile(os.path.join(directory, f))
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send image resize tasks to RabbitMQ.")
    parser.add_argument("--image", help="Path to a single image file.")
    parser.add_argument("--dir", help="Path to a directory of images.")

    args = parser.parse_args()

    if args.image:
        if not os.path.isfile(args.image):
            raise FileNotFoundError(f"❌ Image file not found: {args.image}")
        send_image_task(args.image)

    elif args.dir:
        if not os.path.isdir(args.dir):
            raise NotADirectoryError(f"❌ Directory not found: {args.dir}")

        images = get_images_from_dir(args.dir)
        if not images:
            print(f"⚠️ No valid image files found in {args.dir}")
        for img in images:
            send_image_task(img)

    else:
        parser.error("You must specify either --image or --dir.")
