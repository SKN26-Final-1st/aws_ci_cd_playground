export const API_BASE_URL =
  // .env에서 VITE_API_BASE_URL을 지정하지 않으면 Django 기본 주소로 요청합니다.
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export type ApiResult = {
  // 화면의 응답 패널에서 요청/응답을 한 번에 보여주기 위한 공통 결과 타입입니다.
  method: string
  path: string
  status: number
  ok: boolean
  data: unknown
}

type ApiRequestOptions = {
  method?: string
  body?: Record<string, unknown>
  headers?: Record<string, string>
  credentials?: RequestCredentials
}

async function parseResponse(response: Response) {
  // 에러 응답도 JSON일 수 있으므로 성공/실패와 상관없이 body를 먼저 읽습니다.
  const text = await response.text()
  if (!text) {
    return null
  }

  try {
    return JSON.parse(text) as unknown
  } catch {
    // Django 디버그 HTML처럼 JSON이 아닌 응답도 화면에서 확인할 수 있게 보존합니다.
    return { raw: text }
  }
}

export async function apiRequest(
  path: string,
  options: ApiRequestOptions = {},
): Promise<ApiResult> {
  const method = options.method ?? 'GET'
  // 각 예제 컴포넌트가 필요한 헤더만 넘기면 여기서 공통 헤더와 합쳐집니다.
  const headers: Record<string, string> = {
    Accept: 'application/json',
    ...options.headers,
  }

  const requestInit: RequestInit = {
    method,
    headers,
    // 세션 인증 예제에서는 쿠키를 보내기 위해 credentials: 'include'가 들어옵니다.
    credentials: options.credentials,
  }

  if (options.body !== undefined) {
    // body가 있는 요청은 JSON POST로 보내기 위해 문자열로 변환합니다.
    headers['Content-Type'] = 'application/json'
    requestInit.body = JSON.stringify(options.body)
  }

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, requestInit)

    return {
      method,
      path,
      status: response.status,
      ok: response.ok,
      data: await parseResponse(response),
    }
  } catch (error) {
    // Django 서버가 꺼져 있거나 CORS가 막히면 fetch 자체가 실패합니다.
    return {
      method,
      path,
      status: 0,
      ok: false,
      data: {
        error: error instanceof Error ? error.message : 'Network request failed',
      },
    }
  }
}

export function asRecord(value: unknown): Record<string, unknown> {
  // unknown 응답에서 accessToken/csrfToken 같은 필드를 안전하게 꺼내기 위한 helper입니다.
  return value !== null && typeof value === 'object'
    ? (value as Record<string, unknown>)
    : {}
}

export function readCookie(name: string) {
  // 세션 인증 POST에서는 Django가 내려준 csrftoken 쿠키 값을 헤더로 다시 보내야 합니다.
  const prefix = `${name}=`
  const cookie = document.cookie
    .split(';')
    .map((value) => value.trim())
    .find((value) => value.startsWith(prefix))

  return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : ''
}
