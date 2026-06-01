import { useState } from 'react'

import { apiRequest, type ApiResult } from '../api'
import { ResponsePanel } from './ResponsePanel'

export function BasicApiExample() {
  // message 값은 POST /echo/ 요청의 JSON body로 들어갑니다.
  const [message, setMessage] = useState('hello React')
  const [result, setResult] = useState<ApiResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  async function run(request: () => Promise<ApiResult>) {
    // 버튼을 누를 때마다 로딩 상태를 켜고, 응답 패널에 최신 결과를 보여줍니다.
    setIsLoading(true)
    setResult(await request())
    setIsLoading(false)
  }

  return (
    <section className="example-layout">
      <div className="example-card">
        <div className="learning-note">
          <h2>1. 인증 없는 기본 API 통신</h2>
          <p>
            React가 Django로 JSON을 요청하고, Django가 JSON으로 응답하는 가장
            단순한 형태입니다. 로그인 없이도 호출할 수 있는 공개 API를 연습합니다.
          </p>
          <ol>
            <li>
              <code>GET</code>은 서버 상태나 조회성 데이터를 가져올 때 사용합니다.
            </li>
            <li>
              <code>POST</code>는 React에서 만든 JSON body를 Django로 보냅니다.
            </li>
            <li>오른쪽 응답 패널에서 상태 코드와 JSON 구조를 확인합니다.</li>
          </ol>
        </div>

        <div className="endpoint-list">
          <button
            type="button"
            onClick={() => run(() => apiRequest('/api/basic/ping/'))}
            disabled={isLoading}
          >
            GET /api/basic/ping/ - Django 연결 확인
          </button>
        </div>

        <label className="field">
          <span>React에서 보낼 메시지</span>
          <input
            value={message}
            onChange={(event) => setMessage(event.target.value)}
          />
        </label>

        <div className="endpoint-list">
          <button
            type="button"
            onClick={() =>
              run(() =>
                apiRequest('/api/basic/echo/', {
                  method: 'POST',
                  // Django의 parse_json_body가 이 JSON object를 읽어서 그대로 돌려줍니다.
                  body: { message, sentFrom: 'React' },
                }),
              )
            }
            disabled={isLoading}
          >
            POST /api/basic/echo/ - JSON body 보내기
          </button>
        </div>
      </div>

      <ResponsePanel result={result} />
    </section>
  )
}
