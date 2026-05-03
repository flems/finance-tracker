<template>
  <button
    type="button"
    class="flex items-center gap-1 text-xs text-gray-400 hover:text-blue-600 transition-colors"
    @click="openModal"
  >
    Добавить +
  </button>

  <ConfirmModal
    v-model="modalOpen"
    title="Добавить операцию"
    confirm-label="Сохранить"
    cancel-label="Отмена"
    variant="primary"
    :loading="isSaving"
    @confirm="submit"
  >
    <div class="space-y-3 mt-2">
      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Дата</label>
        <input
          v-model="form.date"
          type="date"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Сумма</label>
        <input
          v-model="form.amount"
          type="number"
          step="1"
          placeholder="0"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-gray-500">Комментарий</label>
        <input
          v-model="form.comment"
          type="text"
          placeholder="Необязательно"
          class="text-sm border border-gray-300 rounded px-2 py-1.5 outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
    </div>
  </ConfirmModal>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { toast } from 'vue-sonner'
import ConfirmModal from '@/shared/ui/confirm-modal/ConfirmModal.vue'
import { HttpError } from '@/shared/api/http'
import { createSavingEntry, type SavingEntryOut } from '../api/createSavingEntry'

const props = defineProps<{ goalId: number }>()
const emit = defineEmits<{ created: [entry: SavingEntryOut] }>()

const modalOpen = ref(false)
const isSaving = ref(false)

function todayIso(): string {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const form = reactive({ date: todayIso(), amount: '' as number | '', comment: '' })

function openModal() {
  form.date = todayIso()
  form.amount = ''
  form.comment = ''
  modalOpen.value = true
}

async function submit() {
  const amt = Number(form.amount)
  if (!amt) {
    toast.error('Укажите сумму')
    return
  }
  if (!form.date) {
    toast.error('Укажите дату')
    return
  }
  isSaving.value = true
  try {
    const created = await createSavingEntry(props.goalId, {
      amount: Math.round(amt),
      comment: form.comment.trim() || null,
      date: form.date,
    })
    emit('created', created)
    modalOpen.value = false
    toast.success('Операция добавлена')
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось добавить')
  } finally {
    isSaving.value = false
  }
}
</script>
