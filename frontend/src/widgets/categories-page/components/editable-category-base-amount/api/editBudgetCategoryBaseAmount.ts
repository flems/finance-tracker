import { http } from '@/shared/api/http'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

export async function editBudgetCategoryBaseAmount(
  id: number,
  base_amount: number | null,
): Promise<BudgetCategory> {
  return http.patch<BudgetCategory>(`/budget/categories/${id}/base_amount`, { base_amount })
}
