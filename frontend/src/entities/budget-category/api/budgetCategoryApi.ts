import { http } from '@/shared/api/http'

export interface BudgetCategory {
  id: number
  name: string
  type: string | null
  base_amount: number | null
  color: string | null
}

export async function fetchBudgetCategories(): Promise<BudgetCategory[]> {
  return http.get<BudgetCategory[]>('/budget/categories')
}
