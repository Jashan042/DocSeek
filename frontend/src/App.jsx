
import { useState } from "react";

import PDFUpload from "./components/PDFUpload";
import SearchBar from "./components/SearchBar";
import SearchResults from "./components/SearchResults";

import "./App.css";

export default function App() {
  const [searchData, setSearchData] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);

  return (
    <main className="container">
      <header>
        <h1>DocSeek</h1>
        <p>Intelligent PDF Search Engine</p>
      </header>

      <PDFUpload />

      <SearchBar
        onResults={setSearchData}
        onLoading={setSearchLoading}
      />

      <SearchResults
        data={searchData}
        loading={searchLoading}
      />
    </main>
  );
}
