<template>
  <div class="space-y-6">
    <div class="flex justify-end">
      <button
        type="button"
        class="inline-flex items-center gap-1.5 rounded-md bg-blue-600 text-white text-sm px-4 py-1.5 hover:bg-blue-700 transition-colors"
        @click="showForm = true"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
            clip-rule="evenodd"
          />
        </svg>
        Новая цель
      </button>
    </div>

    <div v-if="showForm" class="bg-white rounded-lg shadow p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-4">Создать цель накопления</h3>
      <CreateSavingGoalForm @created="onGoalCreated" @cancel="showForm = false" />
    </div>

    <div v-if="isLoading" class="flex items-center justify-center py-12 text-gray-400">
      Загрузка...
    </div>
    <div v-else-if="error" class="text-red-500 text-sm bg-red-50 rounded-lg px-4 py-3">
      {{ error }}
    </div>

    <template v-else>
      <div v-if="!goals.length" class="text-gray-400 py-10 text-center">
        Нет целей — создайте первую с помощью кнопки выше.
      </div>

      <div v-else class="grid gap-6 md:grid-cols-2">
        <SavingGoalCard v-for="goal in goals" :key="goal.id" :goal="goal">
          <template #actions>
            <DeleteSavingGoalButton
              :goal-id="goal.id"
              :goal-title="goal.title"
              @deleted="onGoalDeleted"
            />
          </template>
          <template #history-actions>
            <AddSavingEntryButton
              :goal-id="goal.id"
              @created="(entry) => onEntryCreated(goal, entry)"
            />
          </template>
          <template #entry-actions="{ entry }">
            <DeleteSavingEntryButton :entry="entry" @deleted="(id) => onEntryDeleted(goal, id)" />
          </template>
        </SavingGoalCard>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { SavingGoal, SavingGoalHistoryEntry } from '@/entities/saving-goal/api/savingGoalApi'
import { fetchSavingGoals } from '@/entities/saving-goal/api/savingGoalApi'
import type { SavingEntryOut } from './components/add-saving-entry/api/createSavingEntry'
import SavingGoalCard from '@/entities/saving-goal/ui/SavingGoalCard.vue'
import CreateSavingGoalForm from './components/create-saving-goal/ui/CreateSavingGoalForm.vue'
import DeleteSavingGoalButton from './components/delete-saving-goal/ui/DeleteSavingGoalButton.vue'
import AddSavingEntryButton from './components/add-saving-entry/ui/AddSavingEntryButton.vue'
import DeleteSavingEntryButton from './components/delete-saving-entry/ui/DeleteSavingEntryButton.vue'

const goals = ref<SavingGoal[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)
const showForm = ref(false)

onMounted(async () => {
  isLoading.value = true
  try {
    goals.value = await fetchSavingGoals()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Неизвестная ошибка'
  } finally {
    isLoading.value = false
  }
})

function onGoalCreated(goal: SavingGoal) {
  goals.value.push(goal)
  showForm.value = false
}

function onGoalDeleted(goalId: number) {
  goals.value = goals.value.filter((g) => g.id !== goalId)
}

function onEntryDeleted(goal: SavingGoal, entryId: string) {
  const entry = goal.history.find((h) => h.id === entryId)
  if (entry && !entry.is_planned) {
    goal.current -= entry.amount
    goal.percent =
      goal.target_amount > 0
        ? Math.min(100, Math.round((goal.current / goal.target_amount) * 100))
        : 0
  }
  goal.history = goal.history.filter((h) => h.id !== entryId)
}

function onEntryCreated(goal: SavingGoal, entry: SavingEntryOut) {
  const historyEntry: SavingGoalHistoryEntry = {
    id: `entry-${entry.id}`,
    date: entry.date,
    amount: entry.amount,
    comment: entry.comment,
    is_planned: entry.is_planned,
    deletable: true,
  }
  goal.history.push(historyEntry)
  if (!entry.is_planned) {
    goal.current += entry.amount
    goal.percent =
      goal.target_amount > 0
        ? Math.min(100, Math.round((goal.current / goal.target_amount) * 100))
        : 0
  }
}
</script>
