<template>
  <div class="ui-tooltip relative inline-flex">
    <slot />
    <div
      class="ui-tooltip__content absolute left-1/2 -translate-x-1/2 -translate-y-2 opacity-0 pointer-events-none transition-opacity duration-150 text-xs bg-white text-gray-900 px-2 py-1 rounded border border-gray-200 shadow whitespace-nowrap z-20"
      :class="positionClass"
    >
      {{ text }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  text: string
  position?: 'top' | 'bottom'
}>()

const positionClass = computed(() =>
  props.position === 'bottom'
    ? 'top-full mt-1'
    : 'bottom-full mb-1'
)
</script>

<style scoped>
.ui-tooltip:hover .ui-tooltip__content {
  opacity: 1;
}
</style>

