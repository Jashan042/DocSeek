from django.urls import path
from .views import upload_pdf, search_documents

urlpatterns = [
    path("upload/", upload_pdf, name="upload-pdf"),
    path("search/", search_documents, name="search-documents"),
]