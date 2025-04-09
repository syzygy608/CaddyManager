<template>
  <div class="border p-4 rounded space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700">域名</label>
      <input 
        v-model="localConfig.domain"
        type="text" 
        placeholder="example.com"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700">目標地址</label>
      <input 
        v-model="localConfig.target"
        type="text" 
        placeholder="http://localhost:8080"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700">用戶名(可選)</label>
      <input 
        v-model="localConfig.username"
        type="text" 
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700">密碼(可選)</label>
      <input 
        v-model="localConfig.password"
        type="password" 
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      >
    </div>

    <button 
      @click="$emit('remove')"
      class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
    >
      移除
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, watch } from 'vue'

const props = defineProps({
  config: Object
})

const emit = defineEmits(['remove'])

const localConfig = ref({ ...props.config })

watch(localConfig, (newValue) => {
  Object.assign(props.config, newValue)
}, { deep: true })
</script>