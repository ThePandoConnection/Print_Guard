from PIL import Image
import requests
from io import BytesIO

url = ''
response = requests.get(url)
img = Image.open(BytesIO(response.content))