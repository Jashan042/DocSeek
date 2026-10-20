
import requests

url = "http://127.0.0.1:8000/api/upload/"

# Replace this with the path to one of your PDFs
pdf_path = "data/pdf/Softmax Attention on Gaussian Mixtures.pdf"

with open(pdf_path, "rb") as file:
    response = requests.post(
        url,
        files={"file": file}
    )

print("Status code:", response.status_code)
print("Response:", response.json())
