/**
 * frontend/src/api.ts
 *
 * 개발:  VITE_API_BASE_URL=http://localhost:8000  (.env.local)
 * 배포:  VITE_API_BASE_URL 없음 → 빈 문자열 → 같은 도메인 /api/... 호출
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

// ── 쿠키 헬퍼 ────────────────────────────────────────────────
export function getCookie(name: string): string {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(";").shift()!;
  return "";
}

// ── 공통 fetch ────────────────────────────────────────────────
export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${path}`;

  const res = await fetch(url, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
      ...options.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`[${res.status}] ${text}`);
  }

  // 204 No Content 등 body 없는 응답 처리
  const text = await res.text();
  return text ? JSON.parse(text) : ({} as T);
}

// ── 편의 메서드 ───────────────────────────────────────────────
export const api = {
  get:    <T>(path: string) =>
    apiRequest<T>(path, { method: "GET" }),

  post:   <T>(path: string, body?: unknown) =>
    apiRequest<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),

  put:    <T>(path: string, body?: unknown) =>
    apiRequest<T>(path, { method: "PUT", body: body ? JSON.stringify(body) : undefined }),

  delete: <T>(path: string) =>
    apiRequest<T>(path, { method: "DELETE" }),
};
