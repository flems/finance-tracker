import { http } from '@/shared/api/http'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

export async function editBudgetCategoryColor(id: number, color: string | null): Promise<BudgetCategory> {
  return http.patch<BudgetCategory>(`/budget/categories/${id}/color`, { color })
}
