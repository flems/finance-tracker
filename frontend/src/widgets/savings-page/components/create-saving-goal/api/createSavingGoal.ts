import { http } from '@/shared/api/http'
import type { SavingGoal } from '@/entities/saving-goal/api/savingGoalApi'

export interface CreateSavingGoalBody {
  title: string
  comment: string | null
  target_amount: number
  currency: string
  initial_amount: number
  category_id: number | null
  milestones: number[]
}

export function createSavingGoal(body: CreateSavingGoalBody): Promise<SavingGoal> {
  return http.post<SavingGoal>('/savings/goals', body)
}
