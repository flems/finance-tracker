import type { BudgetDistributionIncome } from '@/entities/budget-distribution/api/budgetDistributionApi'
import { http } from '@/shared/api/http'

export interface CreateBudgetIncomeBody {
  payout_date: string
  amount: number
  /** id категорий с базовой суммой — для каждой создаётся строка распределения (порядок как в массиве) */
  category_ids?: number[]
}

export function createBudgetIncome(
  body: CreateBudgetIncomeBody,
): Promise<BudgetDistributionIncome> {
  return http.post<BudgetDistributionIncome>('/budget/incomes', body)
}
