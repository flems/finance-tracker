import type {
  BudgetDistributionIncome,
  BudgetDistributionItem,
  BudgetDistributionResponse,
} from '../api/budgetDistributionApi'

export function applyPatchedItem(
  dist: BudgetDistributionResponse,
  updated: BudgetDistributionItem,
): void {
  for (const mo of dist.months) {
    for (const inc of mo.incomes) {
      const idx = inc.items.findIndex((i) => i.id === updated.id)
      if (idx !== -1) {
        inc.items[idx] = updated
        return
      }
    }
  }
}

export function removeBudgetItemById(dist: BudgetDistributionResponse, itemId: number): void {
  for (const mo of dist.months) {
    for (const inc of mo.incomes) {
      const idx = inc.items.findIndex((i) => i.id === itemId)
      if (idx !== -1) {
        inc.items.splice(idx, 1)
        return
      }
    }
  }
}

export function sortItemsLikeApi(items: BudgetDistributionItem[]): void {
  items.sort((a, b) => {
    const aNull = a.sort_order == null ? 1 : 0
    const bNull = b.sort_order == null ? 1 : 0
    if (aNull !== bNull) return aNull - bNull
    const av = a.sort_order ?? 0
    const bv = b.sort_order ?? 0
    if (av !== bv) return av - bv
    return a.id - b.id
  })
}

export function appendItemToIncome(
  dist: BudgetDistributionResponse,
  incomeId: number,
  item: BudgetDistributionItem,
): void {
  for (const mo of dist.months) {
    const inc = mo.incomes.find((i) => i.id === incomeId)
    if (inc) {
      inc.items.push(item)
      sortItemsLikeApi(inc.items)
      return
    }
  }
}

export function mergeCreatedIncome(
  dist: BudgetDistributionResponse,
  created: BudgetDistributionIncome,
): void {
  const [y, m] = created.payout_date.split('-').map(Number)
  let month = dist.months.find((x) => x.year === y && x.month === m)
  if (!month) {
    month = { year: y, month: m, incomes: [] }
    dist.months.push(month)
    dist.months.sort((a, b) => {
      if (a.year !== b.year) return b.year - a.year
      return b.month - a.month
    })
  }
  month.incomes.push(created)
  month.incomes.sort((a, b) => {
    if (a.payout_date !== b.payout_date) return a.payout_date.localeCompare(b.payout_date)
    return a.id - b.id
  })
}

export function removeIncomeById(dist: BudgetDistributionResponse, incomeId: number): void {
  for (let mi = 0; mi < dist.months.length; mi++) {
    const mo = dist.months[mi]
    const ii = mo.incomes.findIndex((i) => i.id === incomeId)
    if (ii !== -1) {
      mo.incomes.splice(ii, 1)
      if (!mo.incomes.length) dist.months.splice(mi, 1)
      return
    }
  }
}
