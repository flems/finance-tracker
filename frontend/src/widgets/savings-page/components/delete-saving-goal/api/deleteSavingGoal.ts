import { http } from '@/shared/api/http'

export function deleteSavingGoal(goalId: number): Promise<void> {
  return http.delete(`/savings/goals/${goalId}`)
}
