import type { SavingGoal, SavingGoalHistoryEntry } from '../api/savingGoalApi'

export interface HistoryEntryWithBalance extends SavingGoalHistoryEntry {
  balanceAfter: number
  reachesMilestone?: number
}

function getNextTarget(goal: SavingGoal): number {
  if (!goal.milestones.length) return goal.target_amount
  const next = [...goal.milestones].sort((a, b) => a - b).find((m) => m > goal.current)
  return next ?? goal.target_amount
}

export function getStageTotal(goal: SavingGoal): number {
  if (!goal.milestones.length) return goal.target_amount
  const nextTarget = getNextTarget(goal)
  const sorted = [...goal.milestones].sort((a, b) => a - b)
  const nextIndex = sorted.findIndex((m) => m === nextTarget)
  const prevAmount = nextIndex > 0 ? sorted[nextIndex - 1] : 0
  return nextTarget - prevAmount
}

export function getStageCurrent(goal: SavingGoal): number {
  if (!goal.milestones.length) return goal.current
  const nextTarget = getNextTarget(goal)
  const sorted = [...goal.milestones].sort((a, b) => a - b)
  const nextIndex = sorted.findIndex((m) => m === nextTarget)
  const prevAmount = nextIndex > 0 ? sorted[nextIndex - 1] : 0
  return Math.min(nextTarget - prevAmount, Math.max(0, goal.current - prevAmount))
}

export function getProgressToNextTarget(goal: SavingGoal): number {
  const nextTarget = getNextTarget(goal)
  const sorted = [...goal.milestones].sort((a, b) => a - b)
  const nextIndex = sorted.findIndex((m) => m === nextTarget)
  const prevAmount = nextIndex > 0 ? sorted[nextIndex - 1] : 0
  const totalInStage = nextTarget - prevAmount
  if (totalInStage <= 0) return 100
  return Math.min(100, Math.max(0, Math.round(((goal.current - prevAmount) / totalInStage) * 100)))
}

export function getCurrentStageIndex(goal: SavingGoal): number {
  if (!goal.milestones.length) return 0
  if (goal.current >= goal.target_amount) return goal.milestones.length
  const sorted = [...goal.milestones].sort((a, b) => a - b)
  const index = sorted.findIndex((m) => m > goal.current)
  return index === -1 ? goal.milestones.length : index
}

export function getMilestonePercent(goal: SavingGoal, milestoneAmount: number): number {
  if (goal.target_amount <= 0) return 0
  return Math.min(100, (milestoneAmount / goal.target_amount) * 100)
}

export function getHistoryWithBalance(goal: SavingGoal): HistoryEntryWithBalance[] {
  const sorted = [...goal.history].sort((a, b) => a.date.localeCompare(b.date))
  const sortedMilestones = [...goal.milestones].sort((a, b) => a - b)

  let balance = goal.initial_amount
  const reachedMilestones = new Set<number>()

  const withBalance: HistoryEntryWithBalance[] = sorted.map((entry) => {
    const balanceBefore = balance
    balance += entry.amount

    let reachesMilestone: number | undefined
    for (let i = 0; i < sortedMilestones.length; i++) {
      const n = i + 1
      if (
        balanceBefore < sortedMilestones[i] &&
        balance >= sortedMilestones[i] &&
        !reachedMilestones.has(n)
      ) {
        reachesMilestone = n
        reachedMilestones.add(n)
        break
      }
    }

    return { ...entry, balanceAfter: balance, reachesMilestone }
  })

  return withBalance.sort((a, b) => b.date.localeCompare(a.date))
}

export function formatIsoDate(iso: string): string {
  const [y, m, d] = iso.split('-')
  return `${d}.${m}.${y}`
}
