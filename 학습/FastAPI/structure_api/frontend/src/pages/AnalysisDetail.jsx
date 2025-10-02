import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getStatus, getResult } from "../api/client.js";
import StatusBadge from "../components/StatusBadge.jsx";
import { Displacements, Stresses, Reactions } from "../components/ResultTable.jsx";
import Viewer2D from "../components/Viewer2D.jsx";

export default function AnalysisDetail() {
  const { jobId } = useParams();
  const [status, setStatus] = useState("pending");
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    let timer;
    const poll = async () => {
      try {
        const s = await getStatus(jobId);
        setStatus(s.status); setProgress(s.progress ?? 0);
        if (s.status === "done") {
          const r = await getResult(jobId);
          setResult(r);
          clearInterval(timer);

        } else if (s.status === "failed") {
          setErr(s.error || "해석이 실패했습니다. (서버 로그 참조)");
          clearInterval(timer);
        }
      } catch (e) {
        setErr(e.message);
        clearInterval(timer);
      }
    };
    poll();
    timer = setInterval(poll, 1500);
    return () => clearInterval(timer);
  }, [jobId]);

  const downloadJson = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = Object.assign(document.createElement("a"), { href: url, download: `result_${jobId}.json` });
    a.click(); URL.revokeObjectURL(url);
  };

  return (
    <div>
      <h2>작업 상세: {jobId}</h2>
      <p>상태: <StatusBadge status={status} /> (진행률: {(progress*100).toFixed(0)}%)</p>
      {err && <p style={{color:"red"}}>{err}</p>}
      {result && (
        <>
          <h3>2D Viewer</h3>
          <Viewer2D
            nodes={result.nodes}
            elements={result.elements}
            displacements={result.displacements}
          />
          <h3>결과 테이블</h3>
          <h4>변위</h4>
          <Displacements data={result.displacements} />
          <h4>응력</h4>
          <Stresses data={result.elements} />
          <h4>반력</h4>
          <Reactions data={result.reactions} />
          <button onClick={downloadJson}>JSON 다운로드</button>
        </>
      )}
    </div>
  );
}
