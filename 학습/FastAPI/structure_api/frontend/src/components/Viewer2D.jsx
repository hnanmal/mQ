// src/components/Viewer2D.jsx

/**
 * 간단한 2D 구조 뷰어 (SVG)
 * - 원형(원래 형상): 회색 라인
 * - 변위 반영 형상: 빨간색 라인
 *
 * Props:
 *  - nodes:        [{ id:number, x:number, y:number }]
 *  - elements:     [{ id:number, n1:number, n2:number }]
 *  - displacements:[{ node:number, ux:number, uy:number }]
 *  - width:        number (기본 600)
 *  - height:       number (기본 400)
 *  - margin:       number (기본 20)
 *  - amplify:      number (변위 과장계수, 기본 1000)
 *  - showOriginal: boolean (원형 표시, 기본 true)
 *  - showDeformed: boolean (변위 형상 표시, 기본 true)
 *  - showNodes:    boolean (노드 점 표시, 기본 true)
 *  - showLabels:   boolean (요소 id 라벨 표시, 기본 false)
 */

export default function Viewer2D({
  nodes = [],
  elements = [],
  displacements = [],
  width = 600,
  height = 400,
  margin = 20,
  amplify = 1000,
  showOriginal = true,
  showDeformed = true,
  showNodes = true,
  showLabels = false,
}) {
  // 데이터 가드
  const hasGeometry = Array.isArray(nodes) && nodes.length > 0 && Array.isArray(elements);
  if (!hasGeometry) {
    return (
      <div
        style={{
          width,
          height,
          border: "1px solid #ddd",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#999",
          fontSize: 14,
          fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial",
        }}
      >
        No geometry to display (nodes/elements are empty)
      </div>
    );
  }

  // 맵 구성
  const N = Object.fromEntries(nodes.map((n) => [n.id, n]));
  const D = Object.fromEntries(displacements.map((d) => [d.node, d]));

  // 좌표 범위 계산
  const xs = nodes.map((n) => n.x);
  const ys = nodes.map((n) => n.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  // 0 크기 방지용 보정
  const worldW = Math.max(1e-9, maxX - minX);
  const worldH = Math.max(1e-9, maxY - minY);

  // 화면 변환 스케일 (여백 고려)
  const viewW = Math.max(1, width - margin * 2);
  const viewH = Math.max(1, height - margin * 2);
  const scale = Math.min(viewW / worldW, viewH / worldH);

  // 월드 좌표 -> 뷰 좌표
  const toView = (node, withDisp = false) => {
    const disp = withDisp ? D[node.id] : null;
    const dx = withDisp && disp?.ux ? disp.ux * amplify : 0;
    const dy = withDisp && disp?.uy ? disp.uy * amplify : 0;

    // y는 SVG에서 아래가 +이므로, 공학 좌표계의 +y(위쪽)를 반영하려면 부호 반전
    const vx = margin + (node.x - minX) * scale + dx * scale; // 변위도 스케일 반영(선택)
    const vy = height - margin - (node.y - minY) * scale - dy * scale;

    return { x: vx, y: vy };
  };

  // 범례
  const Legend = () => (
    <g transform={`translate(${margin}, ${margin})`} fontSize="12" fontFamily="monospace">
      <rect x="0" y="-12" width="165" height="40" fill="white" stroke="#ddd" />
      <g>
        <line x1="10" y1="5" x2="40" y2="5" stroke="#bbb" strokeWidth="2" />
        <text x="50" y="9" fill="#333">Original</text>
      </g>
      <g transform="translate(0,16)">
        <line x1="10" y1="5" x2="40" y2="5" stroke="#d33" strokeWidth="3" />
        <text x="50" y="9" fill="#333">Deformed (×{amplify})</text>
      </g>
    </g>
  );

  // 요소 라벨 (중점에 id)
  const ElementLabel = ({ e }) => {
    const n1 = N[e.n1];
    const n2 = N[e.n2];
    if (!n1 || !n2) return null;
    const p1 = toView(n1, showDeformed); // 라벨은 변위 형상 위치에 표시
    const p2 = toView(n2, showDeformed);
    const cx = (p1.x + p2.x) / 2;
    const cy = (p1.y + p2.y) / 2;
    return (
      <text
        x={cx}
        y={cy}
        fill="#444"
        fontSize="11"
        fontFamily="monospace"
        textAnchor="middle"
        dominantBaseline="central"
        style={{ userSelect: "none" }}
      >
        {e.id}
      </text>
    );
  };

  return (
    <svg
      width={width}
      height={height}
      style={{
        border: "1px solid #ddd",
        background: "#fff",
        display: "block",
      }}
    >
      {/* 범례 */}
      <Legend />

      {/* 원형(회색) */}
      {showOriginal &&
        elements.map((e) => {
          const n1 = N[e.n1];
          const n2 = N[e.n2];
          if (!n1 || !n2) return null;
          const p1 = toView(n1, false);
          const p2 = toView(n2, false);
          return (
            <line
              key={`orig-${e.id}`}
              x1={p1.x}
              y1={p1.y}
              x2={p2.x}
              y2={p2.y}
              stroke="#bbb"
              strokeWidth="2"
            />
          );
        })}

      {/* 변위 형상(빨강) */}
      {showDeformed &&
        elements.map((e) => {
          const n1 = N[e.n1];
          const n2 = N[e.n2];
          if (!n1 || !n2) return null;
          const p1 = toView(n1, true);
          const p2 = toView(n2, true);
          return (
            <line
              key={`def-${e.id}`}
              x1={p1.x}
              y1={p1.y}
              x2={p2.x}
              y2={p2.y}
              stroke="#d33"
              strokeWidth="3"
            />
          );
        })}

      {/* 노드 점 표시 (변위 형상 기준 위치) */}
      {showNodes &&
        nodes.map((n) => {
          const p = toView(n, showDeformed);
          return <circle key={`node-${n.id}`} cx={p.x} cy={p.y} r="4" fill="#333" />;
        })}

      {/* 요소 라벨 */}
      {showLabels && elements.map((e) => <ElementLabel key={`lbl-${e.id}`} e={e} />)}
    </svg>
  );
}
