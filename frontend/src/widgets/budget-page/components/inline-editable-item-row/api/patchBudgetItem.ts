import type { BudgetDistributionItem } from '@/entities/budget-distribution/api/budgetDistributionApi'
import { http } from '@/shared/api/http'

export interface BudgetItemPatchPayload {
  category_id?: number
  amount?: number
  comment?: string | null
  is_paid?: boolean
  sort_order?: number | null
}

export function patchBudgetItem(itemId: number, body: BudgetItemPatchPayload): Promise<BudgetDistributionItem> {
  return http.patch<BudgetDistributionItem>(`/budget/items/${itemId}`, body)
}
