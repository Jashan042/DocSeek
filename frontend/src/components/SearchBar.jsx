
import { useState } from "react";

export default function SearchBar({ onResults, onLoading }) {
  const [query, setQuery] = useState("");
  const [method, setMethod] = useState("hybrid");
  const [error, setError] = useState("");

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      setError("Please enter a search query.");
      return;
    }

    setError("");
    onLoading(true);

    try {
      const params = new URLSearchParams({
        q: query.trim(),
        method: method,
      });

      const response = await fetch(
        `http://127.0.0.1:8000/api/search/?${params}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Search failed.");
      }

      onResults(data);
    } catch (err) {
      setError(err.message || "Unable to connect to the server.");
      onResults(null);
    } finally {
      onLoading(false);
    }
  };

  return (
    <section className="search-section">
      <h2>Search Documents</h2>
      <p>Find relevant passages across your uploaded PDFs.</p>

      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="e.g. How does gradient noise affect optimisation?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />

        <select
          value={method}
          onChange={(e) => setMethod(e.target.value)}
          className="method-select"
        >
          <option value="hybrid">Hybrid (FAISS + BM25)</option>
          <option value="semantic">Semantic Search</option>
          <option value="bm25">Keyword Search (BM25)</option>
        </select>

        <button type="submit">Search</button>
      </form>

      {error && <p className="error-message">{error}</p>}
    </section>
  );
}
