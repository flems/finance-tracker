<template>
  <div class="space-y-6">

    <div v-if="!showForm" class="flex justify-start">
      <button
        type="button"
        class="rounded-md bg-blue-600 text-white text-sm px-4 py-1.5 hover:bg-blue-700 transition-colors"
        @click="showForm = true"
      >
        Добавить доход
      </button>
    </div>

    <div v-if="showForm" class="w-full max-w-4xl space-y-4 rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
      <div class="flex items-center justify-between">
        <h2 class="text-base font-semibold text-gray-900">Добавить доход</h2>
        <button type="button" class="text-gray-400 hover:text-gray-600 transition-colors" @click="showForm = false">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <CreateBudgetIncomeForm :categories="categories" @created="onIncomeCreated" />
    </div>

    <div v-if="isLoading" class="flex items-center justify-center py-12 text-gray-400">
      Загрузка...
    </div>
    <div v-else-if="loadError" class="text-red-500 text-sm bg-red-50 rounded-lg px-4 py-3">
      {{ loadError }}
    </div>

    <template v-else>
      <div v-if="!distribution.months.length" class="text-gray-400 py-10 text-center">
        Выплат ещё нет — добавьте первую выплату выше.
      </div>

      <div v-else>
        <div class="mb-6 border-b border-gray-200">
          <nav class="flex space-x-1">
            <button
              v-for="m in distribution.months"
              :key="monthKey(m)"
              type="button"
              class="py-2 px-4 border-b-2 font-medium text-sm transition-colors"
              :class="activeMonthKey === monthKey(m)
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              @click="activeMonthKey = monthKey(m)"
            >
              {{ formatMonthTab(m.year, m.month) }}
            </button>
          </nav>
        </div>

        <div v-if="activeMonth">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-14 gap-y-12">
            <BudgetDistributionIncomeCard
              v-for="inc in activeMonth.incomes"
              :key="inc.id"
              :income="inc"
            >
              <template #income-actions>
                <button
                  type="button"
                  class="text-gray-300 hover:text-red-500 transition-colors p-1 rounded"
                  title="Удалить доход"
                  @click="openDeleteModal(inc)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </template>

              <template #item-row="{ item }">
                <InlineEditableItemRow
                  :item="item"
                  :categories="categories"
                  @patched="applyPatchedItemToTree(distribution, $event)"
                  @deleted="removeBudgetItemByIdFromTree(distribution, $event)"
                />
              </template>

              <template #footer>
                <NewBudgetItemRows
                  :income-id="inc.id"
                  :categories="categories"
                  @created="(item) => appendIncomeItemIntoTree(distribution, inc.id, item)"
                />
              </template>
            </BudgetDistributionIncomeCard>
          </div>
        </div>
      </div>
    </template>

    <ConfirmModal
      v-model="deleteModal.open"
      title="Удалить доход?"
      :description="deleteModal.income
        ? `Доход от ${formatShortDate(deleteModal.income.payout_date)} (${formatAmount(deleteModal.income.amount)}) и все строки распределения будут удалены безвозвратно.`
        : ''"
      confirm-label="Удалить"
      cancel-label="Отмена"
      :loading="deleteModal.loading"
      @confirm="confirmDeleteIncome"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { toast } from 'vue-sonner'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'
import { fetchBudgetCategories } from '@/entities/budget-category/api/budgetCategoryApi'
import {
  fetchBudgetDistribution,
  type BudgetDistributionIncome,
  type BudgetDistributionMonth,
  type BudgetDistributionResponse,
} from '@/entities/budget-distribution/api/budgetDistributionApi'
import BudgetDistributionIncomeCard from '@/entities/budget-distribution/ui/BudgetDistributionIncomeCard.vue'
import {
  appendItemToIncome as appendIncomeItemIntoTree,
  applyPatchedItem as applyPatchedItemToTree,
  mergeCreatedIncome as mergeCreatedIncomeIntoTree,
  removeBudgetItemById as removeBudgetItemByIdFromTree,
  removeIncomeById as removeIncomeByIdFromTree,
} from '@/entities/budget-distribution/lib/syncDistributionTree'
import { formatAmount, formatMonthTab, formatShortDate } from '@/entities/budget-distribution/lib/formatters'
import CreateBudgetIncomeForm from './components/create-budget-income-form/ui/CreateBudgetIncomeForm.vue'
import InlineEditableItemRow from './components/inline-editable-item-row/ui/InlineEditableItemRow.vue'
import NewBudgetItemRows from './components/new-budget-item-rows/ui/NewBudgetItemRows.vue'
import { deleteBudgetIncome } from './deleteBudgetIncome'
import { HttpError } from '@/shared/api/http'
import ConfirmModal from '@/shared/ui/confirm-modal/ConfirmModal.vue'

const categories = ref<BudgetCategory[]>([])
const distribution = ref<BudgetDistributionResponse>({ year: null, months: [] })
const activeMonthKey = ref<string | null>(null)
const isLoading = ref(false)
const loadError = ref<string | null>(null)
const showForm = ref(false)

const deleteModal = reactive<{ open: boolean; income: BudgetDistributionIncome | null; loading: boolean }>({
  open: false,
  income: null,
  loading: false,
})

const activeMonth = computed(() =>
  distribution.value.months.find(x => monthKey(x) === activeMonthKey.value) ?? null,
)

function monthKey(m: BudgetDistributionMonth): string {
  return `${m.year}-${m.month}`
}

/** Ключ календарного текущего месяца (локальное время), формат как у `monthKey`. */
function calendarMonthKeyNow(): string {
  const d = new Date()
  return `${d.getFullYear()}-${d.getMonth() + 1}`
}

function defaultActiveMonthKey(months: BudgetDistributionMonth[]): string {
  const nowKey = calendarMonthKeyNow()
  if (months.some(m => monthKey(m) === nowKey)) return nowKey
  return monthKey(months[0])
}

watch(
  distribution,
  d => {
    if (!d.months.length) { activeMonthKey.value = null; return }
    const stillValid = activeMonthKey.value && d.months.some(x => monthKey(x) === activeMonthKey.value)
    if (!stillValid) activeMonthKey.value = defaultActiveMonthKey(d.months)
  },
  { deep: true },
)

async function reloadAll(): Promise<void> {
  isLoading.value = true
  loadError.value = null
  try {
    const [cats, dist] = await Promise.all([
      fetchBudgetCategories(),
      fetchBudgetDistribution(),
    ])
    categories.value = cats
    distribution.value = dist
  } catch (e) {
    loadError.value = e instanceof Error ? e.message : 'Неизвестная ошибка'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => reloadAll())

function onIncomeCreated(created: BudgetDistributionIncome): void {
  const [yy, mm] = created.payout_date.split('-').map(Number)
  mergeCreatedIncomeIntoTree(distribution.value, created)
  activeMonthKey.value = `${yy}-${mm}`
  showForm.value = false
}

function openDeleteModal(inc: BudgetDistributionIncome): void {
  deleteModal.income = inc
  deleteModal.open = true
}

async function confirmDeleteIncome(): Promise<void> {
  if (!deleteModal.income) return
  deleteModal.loading = true
  try {
    await deleteBudgetIncome(deleteModal.income.id)
    deleteModal.open = false
    toast.success('Доход удалена')
    removeIncomeByIdFromTree(distribution.value, deleteModal.income.id)
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось удалить')
  } finally {
    deleteModal.loading = false
  }
}
</script>
