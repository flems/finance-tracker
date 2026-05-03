<template>
  <div class="relative mt-4">
    <!-- Бейджи (слева, над карточкой) -->
    <div v-if="target > 0" class="absolute -top-7 -left-px flex items-end z-20">
      <div
        class="bg-indigo-50 text-indigo-600 pl-6 pr-8 py-1.5 rounded-t-lg text-xs font-medium border-t border-l border-indigo-100 -mr-4 relative"
      >
        Этап {{ stageIndex + 1 }}/{{ totalStages }}
      </div>
      <div
        class="bg-green-50 text-green-700 px-6 py-1.5 rounded-t-lg text-xs font-medium border-t border-l border-r border-green-200 border-b-0 relative z-10"
      >
        <template v-if="totalSaved !== undefined">{{ formatAmount(totalSaved) }} / </template
        >{{ formatAmount(target) }} {{ currency }}
      </div>
    </div>

    <!-- Действия (справа, над карточкой) -->
    <div v-if="$slots['actions']" class="absolute -top-7 right-0 flex items-end z-20">
      <slot name="actions" />
    </div>

    <div
      :class="[
        'bg-white rounded-lg shadow p-5 space-y-4 relative z-10',
        { 'rounded-tl-none': target > 0 },
      ]"
    >
      <div class="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
        <div class="min-w-0">
          <h2 class="text-base font-semibold text-gray-900 leading-snug">{{ title }}</h2>
          <p class="text-sm text-gray-600 whitespace-pre-line">{{ comment }}</p>
        </div>
        <div class="text-left sm:text-right text-sm text-gray-700 shrink-0">
          <slot
            name="header-values"
            :current="current"
            :next-target="nextTarget"
            :format-amount="formatAmount"
          >
            <div
              class="text-base font-bold text-gray-900 flex flex-wrap gap-x-1 items-baseline sm:justify-end"
            >
              <span class="whitespace-nowrap text-blue-600"
                >{{ formatAmount(current) }} {{ currency }}</span
              >
              <template v-if="target > 0">
                <span class="text-gray-400">/</span>
                <span class="whitespace-nowrap text-gray-600"
                  >{{ formatAmount(nextTarget) }} {{ currency }}</span
                >
              </template>
            </div>
          </slot>
          <div v-if="target > 0" class="text-xs font-medium text-blue-600 mt-0.5">
            Этап выполнен на {{ progressToNextTarget }}%
          </div>
        </div>
      </div>

      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  comment: string
  current: number
  target: number
  nextTarget: number
  progressToNextTarget: number
  stageIndex: number
  totalStages: number
  /** Единица измерения: ₽ или USDT */
  currency?: string
  /** Всего накоплено (показывается в шапке) */
  totalSaved?: number
}

withDefaults(defineProps<Props>(), { currency: '₽' })

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('ru-RU').format(amount)
}
</script>
