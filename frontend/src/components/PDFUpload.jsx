
import { useState } from "react";

export default function PDFUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setMessage("");
    setError(false);

    try {
      // Create multipart form data
      const formData = new FormData();
      formData.append("file", file);

      // Send the PDF to Django
      const response = await fetch(
        "http://127.0.0.1:8000/api/upload/",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Upload failed.");
      }

      setMessage(
        `${data.filename} uploaded successfully! ${data.chunks_created} chunks indexed.`
      );

      setFile(null);

    } catch (err) {
      setError(true);
      setMessage(err.message || "Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section>
      <h2>Upload a PDF</h2>
      <p>Select a document to add to your searchable collection.</p>

      <input
        type="file"
        accept=".pdf,application/pdf"
        onChange={(e) => {
          setFile(e.target.files[0] ?? null);
          setMessage("");
        }}
      />

      {file && <p>Selected: {file.name}</p>}

      <button
        type="button"
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? "Processing PDF..." : "Upload PDF"}
      </button>

      {message && (
        <p role="status" style={{ color: error ? "crimson" : "green" }}>
          {message}
        </p>
      )}
    </section>
  );
}
