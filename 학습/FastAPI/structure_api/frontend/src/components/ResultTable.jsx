export function Displacements({ data=[] }) {
  return (
    <table border="1" cellPadding="6">
      <thead><tr><th>Node</th><th>ux</th><th>uy</th></tr></thead>
      <tbody>
        {data.map(d => <tr key={d.node}><td>{d.node}</td><td>{d.ux}</td><td>{d.uy}</td></tr>)}
      </tbody>
    </table>
  );
}
export function Stresses({ data=[] }) {
  return (
    <table border="1" cellPadding="6">
      <thead><tr><th>Elem</th><th>σ</th></tr></thead>
      <tbody>
        {data.map(e => <tr key={e.id}><td>{e.id}</td><td>{e.sigma}</td></tr>)}
      </tbody>
    </table>
  );
}
export function Reactions({ data=[] }) {
  return (
    <table border="1" cellPadding="6">
      <thead><tr><th>Node</th><th>Rx</th><th>Ry</th></tr></thead>
      <tbody>
        {data.map(r => <tr key={r.node}><td>{r.node}</td><td>{r.rx}</td><td>{r.ry}</td></tr>)}
      </tbody>
    </table>
  );
}
