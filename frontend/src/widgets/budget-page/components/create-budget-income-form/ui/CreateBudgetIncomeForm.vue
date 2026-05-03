<template>
  <div class="flex w-full min-w-0 max-w-full flex-col gap-5">
    <div class="flex flex-wrap items-end gap-3">
      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Дата зачисления</label>
        <input
          v-model="payoutDate"
          type="date"
          class="h-9 text-sm border border-gray-300 rounded-lg px-3 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Сумма, ₽</label>
        <input
          v-model="amount"
          type="number"
          min="0"
          step="1"
          placeholder="0"
          class="h-9 w-36 text-sm border border-gray-300 rounded-lg px-3 outline-none focus:ring-2 focus:ring-blue-400"
          @keydown.enter.prevent="submit"
        />
      </div>
    </div>

    <section class="min-w-0 max-w-full" aria-labelledby="income-categories-heading">
      <h3 id="income-categories-heading" class="text-sm font-medium text-gray-800">
        Категории распределения
      </h3>
      <p class="mt-1.5 max-w-2xl text-xs leading-relaxed text-gray-500">
        Выберите категории для распределения дохода (можно сделать это позже)
      </p>

      <div class="mt-3 min-w-0 max-w-full" role="group" aria-label="Выбор категорий распределения">
        <p v-if="!categoriesWithBase.length" class="text-sm text-gray-500">
          Нет категорий с базовой суммой — задайте её в настройках бюджета или добавьте строки
          вручную после выплаты.
        </p>
        <div
          v-else
          class="grid min-w-0 grid-cols-2 gap-x-6 gap-y-2 sm:grid-cols-3 lg:grid-cols-4 sm:gap-x-8"
        >
          <CheckButton
            v-for="c in categoriesWithBase"
            :key="c.id"
            :model-value="selectedCategoryIds.includes(c.id)"
            :title="`Включить «${c.name}» в строки выплаты`"
            class="min-w-0"
            @update:model-value="setCategoryIncluded(c.id, $event)"
          >
            <template #trigger>
              <span v-bind="categoryTagProps(c.color)">{{ c.name }}</span>
            </template>
          </CheckButton>
        </div>
      </div>
    </section>

    <div class="flex flex-wrap items-center gap-3">
      <button
        type="button"
        class="inline-flex h-9 shrink-0 items-center justify-center gap-2 rounded-lg bg-blue-600 px-5 text-sm font-medium text-white shadow-sm transition-[background-color,box-shadow,opacity] hover:bg-blue-500 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/90 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-45"
        :disabled="isSaving"
        @click="submit"
      >
        <svg
          v-if="isSaving"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 shrink-0 animate-spin"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
        Добавить
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { toast } from 'vue-sonner'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'
import type { BudgetDistributionIncome } from '@/entities/budget-distribution/api/budgetDistributionApi'
import CheckButton from '@/shared/ui/check-button/CheckButton.vue'
import { createBudgetIncome } from '../api/createBudgetIncome'
import { HttpError } from '@/shared/api/http'

const props = defineProps<{
  categories: BudgetCategory[]
}>()

const emit = defineEmits<{
  created: [income: BudgetDistributionIncome]
}>()

const categoriesWithBase = computed(() =>
  [...props.categories]
    .filter((c): c is BudgetCategory & { base_amount: number } => c.base_amount != null)
    .sort((a, b) => a.name.localeCompare(b.name, 'ru')),
)

interface Rgb {
  r: number
  g: number
  b: number
}

function parseHexColor(hex: string | null | undefined): Rgb | null {
  if (!hex) return null
  const s = hex.trim()
  const m6 = /^#([0-9a-f]{6})$/i.exec(s)
  if (m6) {
    const n = parseInt(m6[1], 16)
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 }
  }
  const m3 = /^#([0-9a-f]{3})$/i.exec(s)
  if (m3) {
    const x = m3[1]
    return {
      r: parseInt(x[0] + x[0], 16),
      g: parseInt(x[1] + x[1], 16),
      b: parseInt(x[2] + x[2], 16),
    }
  }
  return null
}

/** Как в таблице распределения (`InlineEditableItemRow`): `#rrggbb` + альфа `18`. */
function toHexRgb(color: string): string | null {
  const rgb = parseHexColor(color)
  if (!rgb) return null
  function h(n: number): string {
    return n.toString(16).padStart(2, '0')
  }
  return `#${h(rgb.r)}${h(rgb.g)}${h(rgb.b)}`
}

/** Тег категории: чёрный текст, заливка цветом с прозрачностью через суффикс `18`. */
function categoryTagProps(color: string | null | undefined): {
  class: string
  style?: Record<string, string>
} {
  const base =
    'block min-w-0 max-w-full truncate rounded-md px-2 py-0.5 text-sm font-medium leading-snug text-black'
  const hexRgb = color ? toHexRgb(color) : null
  if (!hexRgb) {
    return { class: `${base} bg-gray-200` }
  }
  return {
    class: `${base}`,
    style: { backgroundColor: `${hexRgb}18` },
  }
}

function todayIso(): string {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const payoutDate = ref(todayIso())
const amount = ref<number | ''>('')
const selectedCategoryIds = ref<number[]>([])
const isSaving = ref(false)

function setCategoryIncluded(categoryId: number, included: boolean): void {
  const cur = selectedCategoryIds.value
  const has = cur.includes(categoryId)
  if (included && !has) selectedCategoryIds.value = [...cur, categoryId]
  if (!included && has) selectedCategoryIds.value = cur.filter((id) => id !== categoryId)
}

async function submit(): Promise<void> {
  if (isSaving.value) return
  const amt = Number(amount.value)
  if (!Number.isFinite(amt) || amt <= 0) {
    toast.error('Укажите сумму дохода')
    return
  }
  if (!payoutDate.value) {
    toast.error('Выберите дату')
    return
  }
  isSaving.value = true
  try {
    const created = await createBudgetIncome({
      payout_date: payoutDate.value,
      amount: Math.round(amt),
      category_ids: selectedCategoryIds.value,
    })
    emit('created', created)
    amount.value = ''
    selectedCategoryIds.value = []
    toast.success('Выплата добавлена')
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось сохранить')
  } finally {
    isSaving.value = false
  }
}
</script>
