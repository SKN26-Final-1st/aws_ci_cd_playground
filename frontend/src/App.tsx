import { useState } from 'react'

import { BasicApiExample } from './examples/BasicApiExample'
import { JwtAuthExample } from './examples/JwtAuthExample'
import { SessionAuthExample } from './examples/SessionAuthExample'
import './App.css'

type ExampleKey = 'basic' | 'session' | 'jwt'

const examples: Array<{ key: ExampleKey; label: string }> = [
  { key: 'basic', label: '기본 API' },
  { key: 'session', label: '세션 인증' },
  { key: 'jwt', label: 'JWT 인증' },
]

function App() {
  // 라우터 없이 state 하나로 세 가지 학습 예제 탭을 전환합니다.
  const [activeExample, setActiveExample] = useState<ExampleKey>('basic')

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Django + React 학습 예제</p>
          <h1>API 통신, 로그인, 인증/인가 흐름</h1>
          <p className="header-copy">
            왼쪽 버튼을 누르면서 React의 fetch 요청이 Django API에서 어떤
            응답을 받는지 확인해보세요.
          </p>
        </div>
        <div className="server-pill">API http://localhost:8000</div>
      </header>

      <section className="study-guide" aria-label="학습 가이드">
        <div>
          <strong>추천 학습 순서</strong>
          <span>기본 API → 세션 인증 → JWT 인증</span>
        </div>
        <div>
          <strong>데모 계정</strong>
          <span>
            <code>demo</code> / <code>demo1234</code>
          </span>
        </div>
        <div>
          <strong>확인할 것</strong>
          <span>요청 URL, 상태 코드, JSON 응답, 토큰/쿠키 변화</span>
        </div>
      </section>

      <nav className="tabs" aria-label="Example tabs">
        {examples.map((example) => (
          <button
            key={example.key}
            type="button"
            className={activeExample === example.key ? 'is-active' : ''}
            onClick={() => setActiveExample(example.key)}
          >
            {example.label}
          </button>
        ))}
      </nav>

      {activeExample === 'basic' && <BasicApiExample />}
      {activeExample === 'session' && <SessionAuthExample />}
      {activeExample === 'jwt' && <JwtAuthExample />}
    </main>
  )
}

export default App
