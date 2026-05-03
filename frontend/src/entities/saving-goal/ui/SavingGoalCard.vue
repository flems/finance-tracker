<template>
  <UiSavingsGoalCard
    :title="goal.title"
    :comment="(goal.comment ?? '').replace(/\\n/g, '\n')"
    :current="stageCurrent"
    :target="goal.target_amount"
    :next-target="stageTotal"
    :progress-to-next-target="progressToNextTarget"
    :stage-index="stageIndex"
    :total-stages="goal.milestones.length + 1"
    :currency="goal.currency"
    :total-saved="goal.current"
  >
    <template #actions>
      <slot name="actions" />
    </template>

    <div v-if="goal.target_amount > 0" class="space-y-2">
      <div class="flex justify-between text-xs text-gray-600">
        <span>Прогресс</span>
        <span>{{ goal.percent }}%</span>
      </div>
      <div class="relative h-2 w-full bg-gray-100 rounded-full">
        <div class="h-full bg-blue-500 rounded-full" :style="{ width: `${goal.percent}%` }" />
        <div
          v-for="m in goal.milestones"
          :key="m"
          class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 z-10"
          :style="{ left: `${getMilestonePercent(goal, m)}%` }"
        >
          <UiTooltip :text="`${m.toLocaleString('ru-RU')} ${goal.currency}`">
            <div class="w-3 h-3 rounded-full bg-amber-500 border border-white shadow transition-transform duration-150 ease-out hover:scale-125" />
          </UiTooltip>
        </div>
      </div>
    </div>

    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-semibold text-gray-800">История пополнений</h3>
        <label v-if="hasPlanned" class="flex items-center gap-1.5 cursor-pointer">
          <input
            v-model="showPlanned"
            type="checkbox"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <span class="text-xs text-gray-600">Показать запланированные</span>
        </label>
      </div>
      <slot name="history-actions" />
      <div v-if="!filteredHistory.length" class="text-xs text-gray-500">
        Пока нет пополнений
      </div>
      <ul class="divide-y divide-gray-100">
        <li
          v-for="entry in visibleHistory"
          :key="entry.id"
          class="py-2 text-sm flex items-center gap-2"
          :class="{
            'opacity-60': entry.is_planned,
            'bg-amber-50 border-l-4 border-amber-500 pl-2 -ml-2': entry.reachesMilestone && !entry.is_planned,
          }"
        >
          <div>
            <div class="flex items-center gap-2">
              <div
                class="font-medium"
                :class="entry.is_planned ? 'text-gray-500' : entry.reachesMilestone ? 'text-amber-700' : 'text-gray-900'"
              >
                {{ entry.amount >= 0 ? '+' : '' }}{{ entry.amount.toLocaleString('ru-RU') }} {{ goal.currency }}
              </div>
              <span v-if="entry.is_planned" class="text-xs text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">
                Запланировано
              </span>
              <span
                v-else-if="entry.reachesMilestone"
                class="text-xs px-1.5 py-0.5 rounded font-medium text-amber-700 bg-amber-100"
              >
                Этап {{ entry.reachesMilestone }}
              </span>
            </div>
            <div class="text-xs text-gray-500">{{ entry.comment }}</div>
          </div>
          <div class="ml-auto text-right text-xs text-gray-500 shrink-0">
            <div>{{ formatIsoDate(entry.date) }}</div>
            <div class="mt-0.5 text-[11px] text-gray-600">
              Итог: {{ entry.balanceAfter.toLocaleString('ru-RU') }} {{ goal.currency }}
            </div>
          </div>
          <slot name="entry-actions" :entry="entry" />
        </li>
      </ul>
      <button
        v-if="filteredHistory.length > 5"
        class="mt-2 text-xs text-blue-600 hover:text-blue-700 font-medium"
        @click="expanded = !expanded"
      >
        {{ expanded ? 'Скрыть' : `Показать ещё ${filteredHistory.length - 5}` }}
      </button>
    </div>
  </UiSavingsGoalCard>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import UiSavingsGoalCard from '@/shared/ui/savings-goal-card/index.vue'
import UiTooltip from '@/shared/ui/tooltip/index.vue'
import type { SavingGoal } from '../api/savingGoalApi'
import {
  formatIsoDate,
  getHistoryWithBalance,
  getMilestonePercent,
  getProgressToNextTarget,
  getStageCurrent,
  getStageTotal,
  getCurrentStageIndex,
} from '../lib/savingGoalCalc'

const props = defineProps<{ goal: SavingGoal }>()

const expanded = ref(false)
const showPlanned = ref(false)

const stageCurrent = computed(() => getStageCurrent(props.goal))
const stageTotal = computed(() => getStageTotal(props.goal))
const progressToNextTarget = computed(() => getProgressToNextTarget(props.goal))
const stageIndex = computed(() => getCurrentStageIndex(props.goal))
const historyWithBalance = computed(() => getHistoryWithBalance(props.goal))
const hasPlanned = computed(() => historyWithBalance.value.some(e => e.is_planned))
const filteredHistory = computed(() =>
  showPlanned.value ? historyWithBalance.value : historyWithBalance.value.filter(e => !e.is_planned),
)
const visibleHistory = computed(() =>
  expanded.value || filteredHistory.value.length <= 5
    ? filteredHistory.value
    : filteredHistory.value.slice(0, 5),
)
</script>
