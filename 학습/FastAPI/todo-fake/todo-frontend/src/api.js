const BASE_URL = "http://127.0.0.1:8000"; // FastAPI 주소


export async function listTodos() {
    const res = await fetch(`${BASE_URL}/todos`);
    if (!res.ok) throw new Error("Failed to fetch todos");
    return res.json();
}


export async function createTodo({ title, done = false }) {
    const res = await fetch(`${BASE_URL}/todos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, done })
    });
    if (!res.ok) throw new Error("Failed to create todo");
    return res.json();
}


export async function putTodo(id, { title, done }) {
    const res = await fetch(`${BASE_URL}/todos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, done })
    });
    if (!res.ok) throw new Error("Failed to update todo");
    return res.json();
}


export async function patchTodo(id, partial) {
    const res = await fetch(`${BASE_URL}/todos/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(partial)
    });
    if (!res.ok) throw new Error("Failed to patch todo");
    return res.json();
}


export async function deleteTodo(id) {
    const res = await fetch(`${BASE_URL}/todos/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete todo");
    return true;
}