import { http } from '@/shared/api/http'

export function deleteSavingEntry(entryId: number): Promise<void> {
  return http.delete(`/savings/entries/${entryId}`)
}
