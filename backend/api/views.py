from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .document_service import process_document
from .index_manager import add_document
import pymupdf
from .index_manager import load_indexes
from src.embeddings import model
from src.vector_store import semantic_search
from src.bm25_search import build_bm25_index, bm25_search
from src.hybrid_search import hybrid_search
# Create your views here.

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_pdf(request):
    # retrieve the file
    file = request.FILES.get("file")

    # check if the file is empty
    if file is None: 
        return Response(
            {"error": "Missing PDF file."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # make sure the file ends with .pdf
    if not file.name.lower().endswith(".pdf"):
        return Response(
                    {"error": "File is not PDF"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

    
    # we check if file size is too big
    if file.size > 10 * 1024 * 1024:
        return Response(
            {"error": "File size exceeds 10 MB"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if file.size == 0:
            return Response(
                {"error": "Uploaded file is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # storage for PDFs uploaded by the user
    storage = FileSystemStorage(location=settings.MEDIA_ROOT)

    filename = storage.save(file.name, file)

    saved_path = storage.path(filename)

    # check if any successful chunks were retrieved
    try:
        chunks = add_document(saved_path)

    except (pymupdf.FileDataError, pymupdf.EmptyFileError):
        storage.delete(filename)

        return Response(
            {"error": "Invalid or corrupted PDF file."},
            status=status.HTTP_400_BAD_REQUEST
        )

    

    if not chunks:
        storage.delete(filename)

        return Response(
            {"error": "PDF contains no extractable text."},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response({
        "message": "PDF processed successfully",
        "filename": filename,
        "chunks_created": chunks
    }, status=status.HTTP_200_OK)


@api_view(["GET"])
def search_documents(request):
    allowed_methods = {"semantic", "bm25", "hybrid"}

    query = request.query_params.get("q", "").strip()
    method = request.query_params.get("method", "hybrid").lower()

    # Validate query
    if not query:
        return Response(
            {"error": "Search query cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate search method
    if method not in allowed_methods:
        return Response(
            {"error": "Invalid search method."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Load saved search indexes
    index, chunks = load_indexes()

    # No documents uploaded yet
    if index is None or not chunks:
        return Response({
            "query": query,
            "method": method,
            "count": 0,
            "results": []
        }, status=status.HTTP_200_OK)

    # Run selected retrieval method
    if method == "semantic":
        results = semantic_search(query, model, index, chunks, k=5)

    elif method == "bm25":
        bm25 = build_bm25_index(chunks)
        results = bm25_search(query, bm25, chunks, k=5)

    else:
        bm25 = build_bm25_index(chunks)
        results = hybrid_search(
            query, model, index, bm25, chunks, k=5
        )

    # make sure chunks can be serialised
    for chunk in results:
        chunk["score"] = float(chunk["score"])

    return Response({
        "query": query,
        "method": method,
        "count": len(results),
        "results": results
    }, status=status.HTTP_200_OK)
