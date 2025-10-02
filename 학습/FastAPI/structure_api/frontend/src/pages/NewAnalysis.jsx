import { useNavigate } from "react-router-dom";
import AnalysisForm from "../components/AnalysisForm.jsx";
import { runAnalysis } from "../api/client.js";
import { useState } from "react";

export default function NewAnalysis() {
  const nav = useNavigate();
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const onSubmit = async (payload) => {
    setLoading(true); setErr("");
    try {
      const { job_id } = await runAnalysis(payload);
      nav(`/job/${job_id}`);
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>새 해석</h2>
      <p>노드/부재/경계/하중/옵션을 JSON으로 입력하고 해석을 실행합니다.</p>
      <AnalysisForm onSubmit={onSubmit} />
      {loading && <p>해석 요청 중...</p>}
      {err && <p style={{color:"red"}}>{err}</p>}
    </div>
  );
}
