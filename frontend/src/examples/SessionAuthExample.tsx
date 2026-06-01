import { useState } from 'react'

import { apiRequest, asRecord, readCookie, type ApiResult } from '../api'
import { ResponsePanel } from './ResponsePanel'

export function SessionAuthExample() {
  // demo/demo1234는 Django 쪽에서 자동 준비되는 학습용 계정입니다.
  const [username, setUsername] = useState('demo')
  const [password, setPassword] = useState('demo1234')
  const [csrfToken, setCsrfToken] = useState('')
  const [result, setResult] = useState<ApiResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  async function run(request: () => Promise<ApiResult>) {
    // 모든 세션 예제 버튼이 같은 방식으로 응답 패널을 갱신하도록 묶었습니다.
    setIsLoading(true)
    const nextResult = await request()
    setResult(nextResult)
    setIsLoading(false)
    return nextResult
  }

  async function getCsrf() {
    // 세션 로그인 POST를 보내기 전에 먼저 CSRF 쿠키와 토큰을 받아옵니다.
    const nextResult = await run(() =>
      apiRequest('/api/session/csrf/', { credentials: 'include' }),
    )
    const data = asRecord(nextResult.data)
    if (typeof data.csrfToken === 'string') {
      setCsrfToken(data.csrfToken)
    }
  }

  function sessionPost(path: string, body: Record<string, unknown> = {}) {
    // 로그인 후 CSRF 쿠키가 바뀔 수 있어서 POST 직전에 최신 쿠키 값을 다시 읽습니다.
    const currentCsrfToken = readCookie('csrftoken') || csrfToken

    return apiRequest(path, {
      method: 'POST',
      body,
      // 다른 포트의 Django API로 sessionid/csrftoken 쿠키를 보내기 위한 설정입니다.
      credentials: 'include',
      headers: currentCsrfToken ? { 'X-CSRFToken': currentCsrfToken } : {},
    })
  }

  return (
    <section className="example-layout">
      <div className="example-card">
        <div className="learning-note">
          <h2>2. Django 세션 인증</h2>
          <p>
            Django 기본 로그인 방식에 가깝습니다. 브라우저는 세션 쿠키를 보관하고,
            React는 요청마다 쿠키를 함께 보내기 위해 <code>credentials</code>를
            사용합니다.
          </p>
          <ol>
            <li>먼저 CSRF 토큰을 받아 쿠키와 헤더 값을 준비합니다.</li>
            <li>로그인 POST에는 <code>X-CSRFToken</code> 헤더가 필요합니다.</li>
            <li>보호 API는 로그인 후 생성된 세션 쿠키로 사용자를 확인합니다.</li>
          </ol>
        </div>

        <div className="credential-grid">
          <label className="field">
            <span>아이디</span>
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </label>
          <label className="field">
            <span>비밀번호</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </label>
        </div>

        <div className="token-box">
          <span>CSRF 토큰</span>
          <code>{csrfToken || '아직 불러오지 않음'}</code>
        </div>

        <div className="endpoint-list">
          <button type="button" onClick={getCsrf} disabled={isLoading}>
            GET /api/session/csrf/ - CSRF 쿠키 받기
          </button>
          <button
            type="button"
            onClick={() =>
              run(() =>
                sessionPost('/api/session/login/', { username, password }),
              )
            }
            disabled={isLoading}
          >
            POST /api/session/login/ - 세션 로그인
          </button>
          <button
            type="button"
            onClick={() =>
              run(() =>
                apiRequest('/api/session/me/', { credentials: 'include' }),
              )
            }
            disabled={isLoading}
          >
            GET /api/session/me/ - 현재 사용자 확인
          </button>
          <button
            type="button"
            onClick={() =>
              run(() =>
                apiRequest('/api/session/protected/', {
                  // 보호 API도 세션 쿠키가 있어야 request.user를 인증 사용자로 볼 수 있습니다.
                  credentials: 'include',
                }),
              )
            }
            disabled={isLoading}
          >
            GET /api/session/protected/ - 세션 보호 API
          </button>
          <button
            type="button"
            onClick={() => run(() => sessionPost('/api/session/logout/'))}
            disabled={isLoading}
          >
            POST /api/session/logout/ - 세션 로그아웃
          </button>
        </div>
      </div>

      <ResponsePanel result={result} />
    </section>
  )
}
