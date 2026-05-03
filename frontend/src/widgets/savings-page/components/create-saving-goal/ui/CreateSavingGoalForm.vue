<template>
  <div class="space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Название *</label>
        <input
          v-model="form.title"
          type="text"
          placeholder="Подушка безопасности"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Категория бюджета</label>
        <select
          v-model="form.category_id"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400 bg-white"
          :disabled="loadingCategories"
        >
          <option :value="null">{{ loadingCategories ? 'Загрузка...' : '— не выбрана —' }}</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
        <p class="text-xs text-gray-400 leading-relaxed">
          Если выбрать категорию, все операции по ней из таблицы распределения доходов будут
          автоматически появляться в истории этой цели.
        </p>
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Целевая сумма (0 = без лимита)</label>
        <input
          v-model="form.target_amount"
          type="number"
          min="0"
          step="1"
          placeholder="0"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Стартовая сумма</label>
        <input
          v-model="form.initial_amount"
          type="number"
          min="0"
          step="1"
          placeholder="0"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Валюта</label>
        <input
          v-model="form.currency"
          type="text"
          placeholder="₽"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
    </div>

    <div class="flex flex-col gap-1">
      <label class="text-xs text-gray-500">Комментарий</label>
      <textarea
        v-model="form.comment"
        rows="2"
        placeholder="Описание цели..."
        class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400 resize-none"
      />
    </div>

    <div class="flex flex-col gap-2">
      <label class="text-xs text-gray-500">Промежуточные этапы</label>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="(m, i) in form.milestones"
          :key="i"
          class="inline-flex items-center gap-1 bg-amber-50 text-amber-800 text-xs px-2 py-1 rounded-full border border-amber-200"
        >
          {{ m.toLocaleString('ru-RU') }} {{ form.currency }}
          <button
            type="button"
            class="hover:text-red-500 transition-colors"
            @click="removeMilestone(i)"
          >
            ×
          </button>
        </span>
      </div>
      <div class="flex items-center gap-2">
        <input
          v-model="milestoneInput"
          type="number"
          min="1"
          step="1"
          placeholder="Сумма этапа"
          class="w-40 text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
          @keydown.enter.prevent="addMilestone"
        />
        <button
          type="button"
          class="text-sm text-blue-600 hover:text-blue-800 font-medium"
          @click="addMilestone"
        >
          + Добавить этап
        </button>
      </div>
    </div>

    <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
      <button
        type="button"
        class="text-sm text-gray-500 hover:text-gray-700 px-4 py-1.5"
        @click="$emit('cancel')"
      >
        Отмена
      </button>
      <button
        type="button"
        :disabled="isSaving"
        class="inline-flex items-center gap-1.5 rounded-md bg-blue-600 text-white text-sm px-4 py-1.5 hover:bg-blue-700 disabled:opacity-40 transition-colors"
        @click="submit"
      >
        <svg v-if="!isSaving" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
            clip-rule="evenodd"
          />
        </svg>
        <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
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
        Создать
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'
import { fetchBudgetCategories } from '@/entities/budget-category/api/budgetCategoryApi'
import type { SavingGoal } from '@/entities/saving-goal/api/savingGoalApi'
import { HttpError } from '@/shared/api/http'
import { createSavingGoal } from '../api/createSavingGoal'

const emit = defineEmits<{
  created: [goal: SavingGoal]
  cancel: []
}>()

const categories = ref<BudgetCategory[]>([])
const loadingCategories = ref(false)
const isSaving = ref(false)
const milestoneInput = ref<number | ''>('')

const form = reactive({
  title: '',
  comment: '',
  target_amount: 0 as number | '',
  currency: '₽',
  initial_amount: 0 as number | '',
  category_id: null as number | null,
  milestones: [] as number[],
})

onMounted(async () => {
  loadingCategories.value = true
  try {
    categories.value = await fetchBudgetCategories()
  } finally {
    loadingCategories.value = false
  }
})

function addMilestone() {
  const val = Number(milestoneInput.value)
  if (!val || val <= 0) return
  if (form.milestones.includes(val)) {
    toast.error('Такой этап уже добавлен')
    return
  }
  form.milestones = [...form.milestones, val].sort((a, b) => a - b)
  milestoneInput.value = ''
}

function removeMilestone(index: number) {
  form.milestones.splice(index, 1)
}

async function submit() {
  if (!form.title.trim()) {
    toast.error('Укажите название')
    return
  }
  isSaving.value = true
  try {
    const created = await createSavingGoal({
      title: form.title.trim(),
      comment: form.comment.trim() || null,
      target_amount: Number(form.target_amount) || 0,
      currency: form.currency.trim() || '₽',
      initial_amount: Number(form.initial_amount) || 0,
      category_id: form.category_id,
      milestones: form.milestones,
    })
    emit('created', created)
    toast.success('Цель создана')
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось создать цель')
  } finally {
    isSaving.value = false
  }
}
</script>
