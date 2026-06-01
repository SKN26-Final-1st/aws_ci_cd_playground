import type { ApiResult } from '../api'

type ResponsePanelProps = {
  result: ApiResult | null
}

export function ResponsePanel({ result }: ResponsePanelProps) {
  // 모든 예제가 같은 패널을 써서 HTTP method, URL, status, JSON을 비교해 볼 수 있습니다.
  return (
    <aside className="response-panel" aria-live="polite">
      <div className="response-panel__header">
        <span>응답 확인</span>
        {result ? (
          <span
            className={
              result.ok ? 'response-status is-ok' : 'response-status is-error'
            }
          >
            {result.status || 'ERR'}
          </span>
        ) : (
          <span className="response-status">idle</span>
        )}
      </div>
      {result ? (
        <>
          <div className="response-meta">
            <code>{result.method}</code>
            <code>{result.path}</code>
          </div>
          <pre>{JSON.stringify(result.data, null, 2)}</pre>
        </>
      ) : (
        <pre>{JSON.stringify({ ok: null }, null, 2)}</pre>
      )}
    </aside>
  )
}
