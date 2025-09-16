// src/App.jsx
import { useEffect, useState } from "react";
import { listTodos, createTodo, putTodo, patchTodo, deleteTodo } from "./api";

export default function App() {
  const [title, setTitle] = useState("");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function refresh() {
    try {
      setLoading(true);
      setError("");
      const data = await listTodos();
      // 백엔드가 배열을 바로 주면 data 사용, {items:[...]} 형태면 data.items 사용
      setItems(Array.isArray(data) ? data : data.items ?? []);
    } catch (e) {
      setError(e.message ?? String(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function onAdd(e) {
    e.preventDefault();
    if (!title.trim()) return;
    await createTodo({ title: title.trim(), done: false });
    setTitle("");
    await refresh();
  }

  async function onToggle(it) {
    await patchTodo(it.id, { done: !it.done });
    await refresh();
  }

  async function onRename(it) {
    const name = prompt("새 제목:", it.title);
    if (name == null) return;
    const t = name.trim();
    if (!t) return;
    await putTodo(it.id, { title: t, done: it.done });
    await refresh();
  }

  async function onDelete(id) {
    if (!confirm("삭제할까요?")) return;
    await deleteTodo(id);
    await refresh();
  }

  return (
    <div className="container">
      <h1>Todo (Fake DB)</h1>
      <p className="small">FastAPI + React (fetch)</p>

      <form className="row" onSubmit={onAdd}>
        <input
          className="input"
          placeholder="할 일을 입력하세요"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button className="btn" type="submit">추가</button>
      </form>

      {loading && <p>불러오는 중…</p>}
      {error && <p style={{ color: "#fca5a5" }}>에러: {error}</p>}

      <div className="list">
        {items.map((it) => (
          <div key={it.id} className={`item ${it.done ? "done" : ""}`}>
            <input
              type="checkbox"
              checked={it.done}
              onChange={() => onToggle(it)}
            />
            <div style={{ flex: 1 }}>{it.title}</div>
            <button className="btn" onClick={() => onRename(it)}>이름변경</button>
            <button className="btn" onClick={() => onDelete(it.id)}>삭제</button>
          </div>
        ))}
        {items.length === 0 && !loading && (
          <p className="small">아직 항목이 없습니다. 추가해보세요.</p>
        )}
      </div>
    </div>
  );
}
