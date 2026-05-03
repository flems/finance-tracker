import { http } from '@/shared/api/http'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

export async function editBudgetCategoryName(id: number, name: string): Promise<BudgetCategory> {
  return http.patch<BudgetCategory>(`/budget/categories/${id}/name`, { name })
}
