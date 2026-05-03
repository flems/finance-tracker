<template>
  <template v-if="entry.deletable">
    <button
      type="button"
      class="flex shrink-0 items-center justify-center w-6 h-6 rounded text-gray-300 hover:text-red-500 hover:bg-red-50 transition-colors"
      title="Удалить операцию"
      @click="modalOpen = true"
    >
      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
        <path
          fill-rule="evenodd"
          d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
          clip-rule="evenodd"
        />
      </svg>
    </button>

    <ConfirmModal
      v-model="modalOpen"
      title="Удалить операцию?"
      :description="`${entry.amount >= 0 ? '+' : ''}${entry.amount.toLocaleString('ru-RU')} от ${formatDate(entry.date)}`"
      confirm-label="Удалить"
      cancel-label="Отмена"
      :loading="isDeleting"
      @confirm="handleDelete"
    />
  </template>

  <div
    v-else
    class="flex shrink-0 items-center justify-center w-6 h-6 opacity-20 cursor-not-allowed"
    title="Операция из бюджета — удаление недоступно"
  >
    <svg class="w-3.5 h-3.5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
      <path
        fill-rule="evenodd"
        d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
        clip-rule="evenodd"
      />
    </svg>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import ConfirmModal from '@/shared/ui/confirm-modal/ConfirmModal.vue'
import type { HistoryEntryWithBalance } from '@/entities/saving-goal/lib/savingGoalCalc'
import { formatIsoDate } from '@/entities/saving-goal/lib/savingGoalCalc'
import { HttpError } from '@/shared/api/http'
import { deleteSavingEntry } from '../api/deleteSavingEntry'

const props = defineProps<{ entry: HistoryEntryWithBalance }>()
const emit = defineEmits<{ deleted: [entryId: string] }>()

const modalOpen = ref(false)
const isDeleting = ref(false)

function formatDate(iso: string): string {
  return formatIsoDate(iso)
}

async function handleDelete() {
  if (isDeleting.value) return
  const numericId = Number(props.entry.id.replace('entry-', ''))
  isDeleting.value = true
  try {
    await deleteSavingEntry(numericId)
    modalOpen.value = false
    emit('deleted', props.entry.id)
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось удалить операцию')
    isDeleting.value = false
  }
}
</script>
