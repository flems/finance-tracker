<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @keydown.esc="$emit('update:modelValue', false)"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black/40 backdrop-blur-[1px]"
          @click="$emit('update:modelValue', false)"
        />

        <!-- Диалог -->
        <Transition
          enter-active-class="transition duration-150 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="modelValue"
            class="relative z-10 w-full max-w-sm rounded-xl bg-white shadow-xl p-6 space-y-4"
            role="dialog"
            aria-modal="true"
          >
            <!-- Иконка + заголовок -->
            <div class="flex items-start gap-4">
              <div
                class="shrink-0 flex h-10 w-10 items-center justify-center rounded-full"
                :class="variant === 'danger' ? 'bg-red-50' : 'bg-blue-50'"
              >
                <svg
                  v-if="variant === 'danger'"
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5 text-red-500"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z"
                    clip-rule="evenodd"
                  />
                </svg>
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5 text-blue-500"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="text-base font-semibold text-gray-900">{{ title }}</h3>
                <p v-if="description" class="mt-1 text-sm text-gray-500">{{ description }}</p>
                <slot />
              </div>
            </div>

            <!-- Кнопки -->
            <div class="flex justify-end gap-2 pt-1">
              <button
                ref="cancelBtn"
                type="button"
                class="rounded-md px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 transition-colors"
                @click="$emit('update:modelValue', false)"
              >
                {{ cancelLabel }}
              </button>
              <button
                type="button"
                class="rounded-md px-4 py-2 text-sm font-medium text-white disabled:opacity-50 transition-colors"
                :class="
                  variant === 'danger'
                    ? 'bg-red-600 hover:bg-red-700'
                    : 'bg-blue-600 hover:bg-blue-700'
                "
                :disabled="loading"
                @click="$emit('confirm')"
              >
                <span v-if="loading" class="inline-flex items-center gap-1.5">
                  <svg
                    class="w-3.5 h-3.5 animate-spin"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    />
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                    />
                  </svg>
                  {{ confirmLabel }}
                </span>
                <span v-else>{{ confirmLabel }}</span>
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'

interface Props {
  modelValue: boolean
  title: string
  description?: string
  confirmLabel?: string
  cancelLabel?: string
  loading?: boolean
  variant?: 'danger' | 'primary'
}

withDefaults(defineProps<Props>(), {
  confirmLabel: 'Подтвердить',
  cancelLabel: 'Отмена',
  loading: false,
  variant: 'danger',
})

defineEmits<{
  'update:modelValue': [value: boolean]
  confirm: []
}>()

const cancelBtn = ref<HTMLButtonElement | null>(null)

watch(
  () => cancelBtn.value,
  (el) => {
    if (el) nextTick(() => el.focus())
  },
)
</script>
