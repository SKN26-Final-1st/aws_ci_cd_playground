import { useState } from 'react'

import { apiRequest, asRecord, type ApiResult } from '../api'
import { ResponsePanel } from './ResponsePanel'

export function JwtAuthExample() {
  // JWT 예제는 세션 쿠키 대신 accessToken state가 로그인 상태의 핵심입니다.
  const [username, setUsername] = useState('demo')
  const [password, setPassword] = useState('demo1234')
  const [accessToken, setAccessToken] = useState('')
  const [result, setResult] = useState<ApiResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  async function run(request: () => Promise<ApiResult>) {
    // 요청 결과를 오른쪽 패널에 보여주기 위해 공통 실행 함수로 묶었습니다.
    setIsLoading(true)
    const nextResult = await request()
    setResult(nextResult)
    setIsLoading(false)
    return nextResult
  }

  async function login() {
    // 로그인 성공 응답의 accessToken을 React state에 저장합니다.
    const nextResult = await run(() =>
      apiRequest('/api/jwt/login/', {
        method: 'POST',
        body: { username, password },
      }),
    )
    const data = asRecord(nextResult.data)
    if (typeof data.accessToken === 'string') {
      setAccessToken(data.accessToken)
    }
  }

  function authorizedGet(path: string) {
    // 보호 API는 Authorization 헤더의 Bearer 토큰으로 사용자를 확인합니다.
    return apiRequest(path, {
      headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
    })
  }

  return (
    <section className="example-layout">
      <div className="example-card">
        <div className="learning-note">
          <h2>3. JWT 방식 인증</h2>
          <p>
            로그인 응답으로 받은 토큰을 React 상태에 저장하고, 보호 API를 호출할
            때 <code>Authorization: Bearer ...</code> 헤더에 담아 보냅니다.
          </p>
          <ol>
            <li>로그인하면 Django가 짧은 학습용 access token을 발급합니다.</li>
            <li>React는 토큰을 쿠키 대신 직접 들고 있다가 헤더에 붙입니다.</li>
            <li>토큰을 지우면 보호 API는 다시 401 응답을 반환합니다.</li>
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
          <span>Access token</span>
          <code>{accessToken || '아직 발급되지 않음'}</code>
        </div>

        <div className="endpoint-list">
          <button type="button" onClick={login} disabled={isLoading}>
            POST /api/jwt/login/ - 토큰 발급
          </button>
          <button
            type="button"
            onClick={() => run(() => authorizedGet('/api/jwt/me/'))}
            disabled={isLoading}
          >
            GET /api/jwt/me/ - 토큰 사용자 확인
          </button>
          <button
            type="button"
            onClick={() => run(() => authorizedGet('/api/jwt/protected/'))}
            disabled={isLoading}
          >
            GET /api/jwt/protected/ - JWT 보호 API
          </button>
          <button
            type="button"
            className="secondary"
            onClick={() => setAccessToken('')}
            disabled={isLoading || !accessToken}
          >
            토큰 지우기
          </button>
        </div>
      </div>

      <ResponsePanel result={result} />
    </section>
  )
}
