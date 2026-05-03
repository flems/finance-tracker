import type { BudgetDistributionIncome } from '../api/budgetDistributionApi'

export function formatMonthTab(year: number, month: number): string {
  return new Intl.DateTimeFormat('ru-RU', { month: 'long', year: 'numeric' }).format(
    new Date(year, month - 1, 1),
  )
}

export function formatShortDate(iso: string): string {
  const [y, mo, d] = iso.split('-').map(Number)
  return new Date(y, mo - 1, d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })
}

export function formatAmount(n: number): string {
  return new Intl.NumberFormat('ru-RU').format(n) + '\u00a0₽'
}

export function allocated(inc: BudgetDistributionIncome): number {
  return inc.items.reduce((s, i) => s + i.amount, 0)
}

export function totalColorClass(inc: BudgetDistributionIncome): string {
  const diff = allocated(inc) - inc.amount
  if (diff === 0) return 'text-gray-900'
  if (diff > 0) return 'text-red-600'
  return 'text-green-600'
}

export function totalComment(inc: BudgetDistributionIncome): string {
  const diff = allocated(inc) - inc.amount
  if (diff === 0) return ''
  if (diff > 0) return `Превышение на ${formatAmount(diff)}`
  return `Свободно: ${formatAmount(Math.abs(diff))}`
}
