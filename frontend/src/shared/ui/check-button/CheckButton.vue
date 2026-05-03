<template>
  <div class="inline-flex items-center gap-2">
    <button
      :id="triggerSlotIsUsed ? buttonId : undefined"
      type="button"
      class="flex h-5 w-5 shrink-0 items-center justify-center rounded border-2 transition-colors"
      :class="modelValue
        ? 'bg-green-500 border-green-500 text-white'
        : 'border-gray-300 hover:border-green-400 text-transparent'"
      :title="title"
      @click="toggle"
    >
      <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
        <path
          fill-rule="evenodd"
          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
          clip-rule="evenodd"
        />
      </svg>
    </button>
    <label
      v-if="triggerSlotIsUsed"
      :for="buttonId"
      class="min-w-0 cursor-pointer select-none"
    >
      <slot name="trigger" />
    </label>
  </div>
</template>

<script lang="ts">
/** Счётчик на уровне модуля: в `<script setup>` локальный `let` сбрасывался бы на каждый экземпляр и все `id` совпадали. */
let checkButtonUid = 0
</script>

<script setup lang="ts">
import { computed, useSlots } from 'vue'

interface Props {
  modelValue: boolean
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Отметить как выполнено',
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const slots = useSlots()
const triggerSlotIsUsed = computed(() => Boolean(slots.trigger))

const buttonId = `check-button-${++checkButtonUid}`

function toggle(): void {
  emit('update:modelValue', !props.modelValue)
}
</script>
