import type { BudgetDistributionItem } from '@/entities/budget-distribution/api/budgetDistributionApi'
import { http } from '@/shared/api/http'

export interface CreateBudgetItemBody {
  income_id: number
  category_id: number
  amount?: number
  comment?: string | null
  is_paid?: boolean
}

export function createBudgetItem(body: CreateBudgetItemBody): Promise<BudgetDistributionItem> {
  return http.post<BudgetDistributionItem>('/budget/items', body)
}
