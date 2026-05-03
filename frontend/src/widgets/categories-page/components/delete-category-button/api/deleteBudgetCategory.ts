import { http } from '@/shared/api/http'

export async function deleteBudgetCategory(id: number): Promise<void> {
  await http.delete(`/budget/categories/${id}`)
}
