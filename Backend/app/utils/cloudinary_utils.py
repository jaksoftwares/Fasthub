import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

def upload_image_to_cloudinary(file):
    """
    Uploads an image file to Cloudinary and returns the URL.
    :param file: file-like object (bytes or file)
    :return: URL string
    """
    result = cloudinary.uploader.upload(file)
    return result.get("secure_url")
