
# 🖼️ Image Resize Queue with RabbitMQ

This project demonstrates how to use **RabbitMQ** as a message broker to offload image processing tasks (resizing images) to a **background worker** in Python. The sender publishes image file paths to a queue, and the worker listens and processes them asynchronously.

---

## 📦 Features

- 📨 Queue-based communication with RabbitMQ (`pika`)
- 🖼️ Image processing and resizing using `Pillow`
- 🐍 Written in Python
- 📁 Automatic file download support for testing
- ✅ Scalable and decoupled architecture

---

## 🧰 Requirements

- Python 3.7+
- [RabbitMQ](https://www.rabbitmq.com/download.html) running locally or via Docker

Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```
pika
pillow
requests
```

---

## 🚀 How It Works

### 1. **Start the RabbitMQ server**

Make sure RabbitMQ is running on `localhost:5672`.

**Using Docker Compose**:

```bash
docker compose up
```

---

### 2. **Download Sample Images (Optional)**

Use the helper script:

```bash
python download_images.py
```

This will download sample images into the `images/` folder.

---

### 3. **Start the Worker**

```bash
python worker.py
```

This starts a consumer that listens for new image tasks and resizes them.

---

### 4. **Send an Image Resize Task**

```bash
python sender.py images/cat.jpg
```

The file will be resized to 128x128 and saved in the `resized/` folder.

---

## 📁 Project Structure

```
.
├── sender.py              # Sends image resize tasks to the queue
├── worker.py              # Listens to queue and resizes the image
├── download_images.py     # Optional: downloads sample test images
├── images/                # Source images
├── resized/               # Output folder for resized images
├── requirements.txt
└── README.md
```

---

## 🛠️ Future Improvements

- Support multiple sizes or formats
- Convert and store image metadata (JSON)
- Handle images sent as bytes (instead of paths)
- Add Flask API for image upload

---

## 📜 License

This project is MIT licensed. Use it freely and modify as needed.

---
