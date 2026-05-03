import { http } from '@/shared/api/http'

export interface CreateSavingEntryBody {
  amount: number
  comment: string | null
  date: string
}

export interface SavingEntryOut {
  id: number
  goal_id: number
  amount: number
  comment: string | null
  date: string
  is_planned: boolean
}

export function createSavingEntry(
  goalId: number,
  body: CreateSavingEntryBody,
): Promise<SavingEntryOut> {
  return http.post<SavingEntryOut>(`/savings/goals/${goalId}/entries`, body)
}
