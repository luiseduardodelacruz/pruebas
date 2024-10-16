import io
from PIL import Image, ImageDraw
import base64

def read_image(image_file):
    try:
        image = Image.open(image_file)
        return image
    except Exception as e:
        raise ValueError(f"Error al leer la imagen: {e}")

def convert_image_to_bytes(image):
    try:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        return image_bytes.getvalue()
    except Exception as e:
        raise ValueError(f"Error al convertir la imagen: {e}")

def draw_boxes_on_image(image, predictions):
    image_with_boxes = image.copy()
    draw = ImageDraw.Draw(image_with_boxes)

    for pred in predictions:
        left = pred.bounding_box.left * image.width
        top = pred.bounding_box.top * image.height
        width = pred.bounding_box.width * image.width
        height = pred.bounding_box.height * image.height
        color = "red" if pred.tag_name == "capistrano" else "blue"
        draw.rectangle([left, top, left + width, top + height], outline=color, width=3)

    return image_with_boxes

def convert_image_to_base64(image_with_boxes):
    try:
        buffer = io.BytesIO()
        image_with_boxes.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        return img_str
    except Exception as e:
        raise ValueError(f"Error al convertir la imagen a base64: {e}")
