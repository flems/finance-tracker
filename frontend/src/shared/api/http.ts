const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

interface RequestOptions {
  params?: Record<string, string | number | boolean | undefined>
}

export interface ApiError {
  status: 'error'
  code: string
  message: string
}

export class HttpError extends Error {
  constructor(
    public readonly code: string,
    message: string,
  ) {
    super(message)
    this.name = 'HttpError'
  }
}

function buildUrl(path: string, params?: RequestOptions['params']): string {
  const url = new URL(path, API_BASE_URL)
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value === undefined) return
      url.searchParams.set(key, String(value))
    })
  }
  return url.toString()
}

async function handleError(res: Response): Promise<never> {
  let code = `HTTP_${res.status}`
  let message = `${res.status} ${res.statusText}`
  try {
    const body = await res.json() as Partial<ApiError>
    if (body.status === 'error' && body.code && body.message) {
      code = body.code
      message = body.message
    }
  } catch {
    // ignore parse errors
  }
  throw new HttpError(code, message)
}

async function get<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const url = buildUrl(path, options.params)
  const res = await fetch(url)
  if (!res.ok) await handleError(res)
  return (await res.json()) as T
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const url = buildUrl(path)
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) await handleError(res)
  return (await res.json()) as T
}

async function patch<T>(path: string, body: unknown): Promise<T> {
  const url = buildUrl(path)
  const res = await fetch(url, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) await handleError(res)
  return (await res.json()) as T
}

async function del(path: string): Promise<void> {
  const url = buildUrl(path)
  const res = await fetch(url, { method: 'DELETE' })
  if (!res.ok) await handleError(res)
}

export const http = {
  get,
  patch,
  post,
  delete: del,
}
