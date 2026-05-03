import { http } from '@/shared/api/http'

export interface BudgetDistributionItem {
  id: number
  income_id: number
  category_id: number
  category_name: string
  amount: number
  comment: string | null
  is_paid: boolean
  sort_order: number | null
}

export interface BudgetDistributionIncome {
  id: number
  payout_date: string
  amount: number
  items: BudgetDistributionItem[]
}

export interface BudgetDistributionMonth {
  year: number
  month: number
  incomes: BudgetDistributionIncome[]
}

export interface BudgetDistributionResponse {
  year: number | null
  months: BudgetDistributionMonth[]
}

export async function fetchBudgetDistribution(year?: number): Promise<BudgetDistributionResponse> {
  const params = year !== undefined ? { year } : {}
  return http.get<BudgetDistributionResponse>('/budget/distribution', { params })
}
