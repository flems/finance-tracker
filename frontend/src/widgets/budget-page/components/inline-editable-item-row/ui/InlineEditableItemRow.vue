<template>
  <tr
    class="relative group"
    :class="item.is_paid ? 'opacity-60' : ''"
    :style="rowStyle"
  >
    <td
      class="px-6 py-4 whitespace-nowrap text-sm border-l-4 transition-colors"
      :class="[categoryColor ? '' : 'border-transparent', item.is_paid ? 'line-through text-gray-500' : 'text-gray-900']"
      :style="firstCellStyle"
    >
      {{ item.category_name }}
    </td>

    <td
      class="align-middle px-6 py-4 text-sm cursor-pointer select-none"
      :class="item.is_paid ? 'line-through text-gray-500' : 'text-gray-700'"
      title="Двойной клик для редактирования"
      @dblclick="startEditAmount"
    >
      <div
        v-if="isEditingAmount"
        class="flex min-h-7 items-center gap-1"
        @focusout="onAmountFocusOut"
      >
        <input
          ref="amountInputRef"
          v-model="editingAmount"
          type="number"
          min="0"
          step="1"
          class="min-w-0 flex-1 px-2 h-7 text-sm leading-none border border-blue-400 rounded box-border outline-none focus:ring-2 focus:ring-blue-300"
          @keydown.enter="saveAmount"
          @keydown.escape="cancelEditAmount"
        />
        <button
          type="button"
          :disabled="isSavingAmount"
          class="flex h-7 w-7 shrink-0 items-center justify-center rounded text-blue-600 hover:text-blue-800 hover:bg-blue-50 transition-colors"
          title="Сохранить"
          @click="saveAmount"
        >
          <svg v-if="!isSavingAmount" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        </button>
      </div>
      <span v-else class="flex min-h-7 items-center tabular-nums">{{ formatAmount(item.amount) }}</span>
    </td>

    <td
      class="align-middle px-6 py-4 text-sm cursor-pointer select-none"
      :class="item.is_paid ? 'line-through text-gray-500' : 'text-gray-500'"
      title="Двойной клик для редактирования"
      @dblclick="startEditComment"
    >
      <div
        v-if="isEditingComment"
        class="flex min-h-7 items-center gap-1"
        @focusout="onCommentFocusOut"
      >
        <input
          ref="commentInputRef"
          v-model="editingComment"
          type="text"
          class="min-w-0 flex-1 px-2 h-7 text-sm leading-none border border-blue-400 rounded box-border outline-none focus:ring-2 focus:ring-blue-300"
          @keydown.enter="saveComment"
          @keydown.escape="cancelEditComment"
        />
        <button
          type="button"
          :disabled="isSavingComment"
          class="flex h-7 w-7 shrink-0 items-center justify-center rounded text-blue-600 hover:text-blue-800 hover:bg-blue-50 transition-colors"
          title="Сохранить"
          @click="saveComment"
        >
          <svg v-if="!isSavingComment" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        </button>
      </div>
      <span v-else class="flex min-h-7 items-center break-words">{{ item.comment || '—' }}</span>
    </td>

    <td class="px-2 py-4 text-center relative">
      <CheckButton
        :model-value="item.is_paid"
        :disabled="isTogglingPaid"
        title="Отметить как выполнено"
        class="mx-auto"
        @update:model-value="togglePaid"
      />
      <button
        type="button"
        :disabled="isDeleting"
        class="absolute top-1/2 -translate-y-1/2 left-full ml-1 flex items-center justify-center w-7 h-7 rounded text-gray-300 hover:text-red-500 hover:bg-red-50 transition-all opacity-0 group-hover:opacity-100"
        title="Удалить строку"
        @click="handleDelete"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
      </button>
    </td>
  </tr>
</template>

<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import { toast } from 'vue-sonner'
import CheckButton from '@/shared/ui/check-button/CheckButton.vue'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'
import type { BudgetDistributionItem } from '@/entities/budget-distribution/api/budgetDistributionApi'
import { patchBudgetItem } from '../api/patchBudgetItem'
import { deleteBudgetItem } from '../api/deleteBudgetItem'
import { formatAmount } from '@/entities/budget-distribution/lib/formatters'
import { HttpError } from '@/shared/api/http'

const props = defineProps<{
  item: BudgetDistributionItem
  categories: BudgetCategory[]
}>()

const emit = defineEmits<{
  patched: [item: BudgetDistributionItem]
  deleted: [itemId: number]
}>()

const categoryColor = computed(
  () => props.categories.find(c => c.id === props.item.category_id)?.color ?? null,
)
const rowStyle = computed(() =>
  categoryColor.value ? { backgroundColor: `${categoryColor.value}18` } : {},
)
const firstCellStyle = computed(() =>
  categoryColor.value ? { borderLeftColor: categoryColor.value } : {},
)

// --- Inline edit: amount ---
const editingAmount = ref<number | ''>('')
const isEditingAmount = ref(false)
const isSavingAmount = ref(false)
const isCancellingAmount = ref(false)
const amountInputRef = ref<HTMLInputElement | null>(null)

function startEditAmount() {
  editingAmount.value = props.item.amount
  isCancellingAmount.value = false
  isEditingAmount.value = true
  nextTick(() => amountInputRef.value?.select())
}

function cancelEditAmount() {
  isCancellingAmount.value = true
  isEditingAmount.value = false
}

function parseAmountFromInput(raw: number | ''): number | null {
  if (raw === '') return 0
  const n = Number(raw)
  if (!Number.isFinite(n) || n < 0) return null
  return Math.round(n)
}

async function saveAmount() {
  if (isSavingAmount.value || isCancellingAmount.value) return
  const amt = parseAmountFromInput(editingAmount.value)
  if (amt === null) { toast.error('Укажите корректную сумму (неотрицательное число)'); return }
  if (amt === props.item.amount) { cancelEditAmount(); return }
  isEditingAmount.value = false
  isSavingAmount.value = true
  try {
    const updated = await patchBudgetItem(props.item.id, { amount: Math.round(amt) })
    emit('patched', updated)
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось сохранить')
  } finally {
    isSavingAmount.value = false
  }
}

function onAmountFocusOut(e: FocusEvent) {
  const wrapper = e.currentTarget as HTMLElement
  if (wrapper.contains(e.relatedTarget as Node | null)) return
  saveAmount()
}

// --- Inline edit: comment ---
const editingComment = ref('')
const isEditingComment = ref(false)
const isSavingComment = ref(false)
const isCancellingComment = ref(false)
const commentInputRef = ref<HTMLInputElement | null>(null)

function startEditComment() {
  editingComment.value = props.item.comment ?? ''
  isCancellingComment.value = false
  isEditingComment.value = true
  nextTick(() => { commentInputRef.value?.focus(); commentInputRef.value?.select() })
}

function cancelEditComment() {
  isCancellingComment.value = true
  isEditingComment.value = false
}

async function saveComment() {
  if (isSavingComment.value || isCancellingComment.value) return
  const trimmed = editingComment.value.trim()
  const oldTrimmed = (props.item.comment ?? '').trim()
  if (trimmed === oldTrimmed) { cancelEditComment(); return }
  isEditingComment.value = false
  isSavingComment.value = true
  try {
    const updated = await patchBudgetItem(props.item.id, { comment: trimmed || null })
    emit('patched', updated)
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось сохранить')
  } finally {
    isSavingComment.value = false
  }
}

function onCommentFocusOut(e: FocusEvent) {
  const wrapper = e.currentTarget as HTMLElement
  if (wrapper.contains(e.relatedTarget as Node | null)) return
  saveComment()
}

// --- Toggle paid ---
const isTogglingPaid = ref(false)
async function togglePaid() {
  if (isTogglingPaid.value) return
  isTogglingPaid.value = true
  try {
    const updated = await patchBudgetItem(props.item.id, { is_paid: !props.item.is_paid })
    emit('patched', updated)
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось обновить')
  } finally {
    isTogglingPaid.value = false
  }
}

// --- Delete item ---
const isDeleting = ref(false)
async function handleDelete() {
  if (isDeleting.value) return
  isDeleting.value = true
  try {
    await deleteBudgetItem(props.item.id)
    emit('deleted', props.item.id)
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось удалить строку')
    isDeleting.value = false
  }
}
</script>
