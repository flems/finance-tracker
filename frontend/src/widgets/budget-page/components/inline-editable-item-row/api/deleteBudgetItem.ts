import { http } from '@/shared/api/http'

export function deleteBudgetItem(itemId: number): Promise<void> {
  return http.delete(`/budget/items/${itemId}`)
}
