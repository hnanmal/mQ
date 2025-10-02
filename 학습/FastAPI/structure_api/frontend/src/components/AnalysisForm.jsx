import { useState } from "react";

// const example = {
//   nodes: [{ id: 1, x: 0, y: 0 }, { id: 2, x: 5, y: 0 }, { id: 3, x: 5, y: 3 }],
//   elements: [{ id: 1, n1: 1, n2: 2, E: 210e9, A: 0.01 }],
//   supports: [{ node: 1, ux: true, uy: true }],
//   loads: [{ node: 3, fx: 0, fy: -10000 }],
//   options: { solver: "linear", unit: "SI" }
// };


const example = {
  nodes: [
    { id: 1, x: 0, y: 0 },
    { id: 2, x: 5, y: 0 },
    { id: 3, x: 5, y: 3 },
  ],
  elements: [
    { id: 1, n1: 1, n2: 2, E: 210000000000, A: 0.01 },
    { id: 2, n1: 1, n2: 3, E: 210000000000, A: 0.01 },
    { id: 3, n1: 2, n2: 3, E: 210000000000, A: 0.01 }
  ],
  supports: [
    { node: 1, ux: true, uy: true },
    { node: 2, ux: false, uy: true },
  ],
  loads: [{ node: 3, fx: 0, fy: -10000 }],
  options: { solver: "linear", unit: "SI" }
};



export default function AnalysisForm({ onSubmit }) {
  const [jsonText, setJsonText] = useState(JSON.stringify(example, null, 2));
  const [error, setError] = useState("");

  const handleFile = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    setJsonText(text);
  };

  const submit = () => {
    try {
      const payload = JSON.parse(jsonText);
      setError("");
      onSubmit(payload);
    } catch (e) {
      setError("유효한 JSON이 아닙니다.");
    }
  };

  return (
    <div>
      <p>입력 JSON(직접 편집 또는 파일 업로드)</p>
      <input type="file" accept="application/json" onChange={handleFile} />
      <textarea
        value={jsonText}
        onChange={(e) => setJsonText(e.target.value)}
        rows={18}
        style={{ width: "100%", fontFamily: "monospace" }}
      />
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={submit}>해석 실행</button>
    </div>
  );
}
