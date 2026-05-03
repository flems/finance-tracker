import { http } from '@/shared/api/http'

export interface SavingGoalHistoryEntry {
  id: string
  date: string
  amount: number
  comment: string | null
  is_planned: boolean
  deletable: boolean
}

export interface SavingGoal {
  id: number
  title: string
  comment: string | null
  target_amount: number
  currency: string
  initial_amount: number
  category_id: number | null
  category_name: string | null
  milestones: number[]
  current: number
  percent: number
  history: SavingGoalHistoryEntry[]
}

export function fetchSavingGoals(): Promise<SavingGoal[]> {
  return http.get<SavingGoal[]>('/savings/goals')
}
