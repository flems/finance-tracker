import { http } from '@/shared/api/http'

export function deleteBudgetIncome(incomeId: number): Promise<void> {
  return http.delete(`/budget/incomes/${incomeId}`)
}
