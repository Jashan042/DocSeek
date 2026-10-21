
export default function SearchResults({ data, loading }) {
  if (loading) {
    return <p className="search-status">Searching documents...</p>;
  }

  if (!data) {
    return null;
  }

  if (data.results.length === 0) {
    return <p className="search-status">No matching passages found.</p>;
  }

  return (
    <section className="results-section">
      <h2>Search Results</h2>

      <p>
        Found {data.count} passages using {data.method} search.
      </p>

      <div className="results-list">
        {data.results.map((result) => (
          <article key={result.chunk_id} className="result-card">
            <div className="result-header">
              <h3>{result.document}</h3>
              <span>Page {result.page}</span>
            </div>

            <p>{result.text}</p>

            <small>Retrieval score: {result.score.toFixed(4)}</small>
          </article>
        ))}
      </div>
    </section>
  );
}
