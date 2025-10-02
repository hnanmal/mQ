import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home.jsx";
import NewAnalysis from "./pages/NewAnalysis.jsx";
import AnalysisDetail from "./pages/AnalysisDetail.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <header style={{padding:12, borderBottom:"1px solid #ddd"}}>
        <Link to="/">구조해석</Link>{" | "}
        <Link to="/new">새 해석</Link>
      </header>
      <main style={{padding:16}}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/new" element={<NewAnalysis />} />
          <Route path="/job/:jobId" element={<AnalysisDetail />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}