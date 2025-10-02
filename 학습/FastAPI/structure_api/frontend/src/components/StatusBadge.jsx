export default function StatusBadge({ status }) {
  const color = status === "done" ? "green"
    : status === "failed" ? "crimson"
    : status === "running" ? "dodgerblue" : "gray";
  return <span style={{
    padding:"2px 8px", background: color, color:"#fff", borderRadius: 8
  }}>{status}</span>;
}