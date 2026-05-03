<template>
  <tr v-if="!isAdding" class="border-t border-gray-100">
    <td colspan="4" class="px-6 py-2">
      <button
        type="button"
        class="flex items-center gap-1.5 text-sm text-gray-400 hover:text-blue-600 transition-colors py-1 disabled:pointer-events-none disabled:opacity-40"
        :disabled="!categories.length"
        @click="startAdd"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Добавить
      </button>
    </td>
  </tr>

  <tr v-else class="relative border-t border-blue-100" :style="newItemRowStyle">
    <td class="px-3 py-3 border-l-4" :style="newItemFirstCellStyle">
      <select
        ref="categorySelectRef"
        v-model="form.category_id"
        class="w-full px-2 py-1 text-sm border border-blue-300 rounded outline-none focus:ring-2 focus:ring-blue-300 bg-white"
        @change="onCategoryChange"
      >
        <option :value="null" disabled>— выберите —</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>
    </td>
    <td class="px-3 py-3">
      <input
        v-model="form.amount"
        type="number"
        min="0"
        step="1"
        placeholder="0"
        class="w-full px-2 py-1 text-sm border border-blue-300 rounded outline-none focus:ring-2 focus:ring-blue-300"
        @keydown.enter="save"
        @keydown.escape="cancel"
      />
    </td>
    <td class="px-3 py-3">
      <input
        v-model="form.comment"
        type="text"
        placeholder="Комментарий"
        class="w-full min-w-0 px-2 py-1 text-sm border border-blue-300 rounded outline-none focus:ring-2 focus:ring-blue-300"
        @keydown.enter="save"
        @keydown.escape="cancel"
      />
    </td>
    <td class="px-2 py-3 text-center relative">
      <CheckButton
        v-model="form.is_paid"
        title="Сразу отметить как выполнено"
        class="mx-auto"
      />
      <div class="absolute top-0 left-full h-full flex flex-col w-8 ml-1 rounded overflow-hidden border border-blue-200 shadow-sm z-10">
        <button
          type="button"
          class="flex flex-1 items-center justify-center bg-white text-blue-600 hover:bg-blue-50 disabled:opacity-40 transition-colors"
          title="Добавить строку"
          :disabled="isSaving"
          @click="save"
        >
          <svg v-if="!isSaving" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        </button>
        <button
          type="button"
          class="flex flex-1 items-center justify-center bg-white text-red-400 hover:text-red-600 hover:bg-red-50 transition-colors border-t border-blue-200"
          title="Отменить"
          @click="cancel"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </td>
  </tr>
</template>

<script setup lang="ts">
import { computed, nextTick, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'
import CheckButton from '@/shared/ui/check-button/CheckButton.vue'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'
import type { BudgetDistributionItem } from '@/entities/budget-distribution/api/budgetDistributionApi'
import { createBudgetItem } from '../api/createBudgetItem'
import { HttpError } from '@/shared/api/http'

const props = defineProps<{
  incomeId: number
  categories: BudgetCategory[]
}>()

const emit = defineEmits<{
  created: [item: BudgetDistributionItem]
}>()

const isAdding = ref(false)
const isSaving = ref(false)
const categorySelectRef = ref<HTMLSelectElement | null>(null)

const form = reactive({
  category_id: null as number | null,
  amount: '' as number | '',
  comment: '',
  is_paid: false,
})

const selectedCategory = computed(
  () => props.categories.find(c => c.id === form.category_id) ?? null,
)

const newItemRowStyle = computed(() => {
  const color = selectedCategory.value?.color ?? null
  return color ? { backgroundColor: `${color}18` } : {}
})

const newItemFirstCellStyle = computed(() => {
  const color = selectedCategory.value?.color ?? null
  return color ? { borderLeftColor: color } : {}
})

function startAdd() {
  form.category_id = null
  form.amount = ''
  form.comment = ''
  form.is_paid = false
  isAdding.value = true
  nextTick(() => categorySelectRef.value?.focus())
}

function onCategoryChange() {
  const cat = selectedCategory.value
  if (cat?.base_amount != null) form.amount = cat.base_amount
}

function cancel() {
  isAdding.value = false
}

async function save() {
  if (isSaving.value) return
  if (!form.category_id) { toast.error('Выберите категорию'); return }
  const amtRaw = form.amount === '' ? 0 : Number(form.amount)
  if (!Number.isFinite(amtRaw) || amtRaw < 0) { toast.error('Укажите корректную сумму (неотрицательное число)'); return }
  const amt = Math.round(amtRaw)
  isSaving.value = true
  try {
    const created = await createBudgetItem({
      income_id: props.incomeId,
      category_id: form.category_id,
      amount: amt,
      comment: form.comment.trim() || null,
      is_paid: form.is_paid,
    })
    emit('created', created)
    isAdding.value = false
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось добавить')
  } finally {
    isSaving.value = false
  }
}
</script>
