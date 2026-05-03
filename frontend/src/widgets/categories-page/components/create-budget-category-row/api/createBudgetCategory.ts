import { http } from '@/shared/api/http'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

export interface CreateBudgetCategoryPayload {
  name: string
  type: string
  base_amount: number | null
}

export async function createBudgetCategory(
  payload: CreateBudgetCategoryPayload,
): Promise<BudgetCategory> {
  return http.post<BudgetCategory>('/budget/categories', payload)
}
