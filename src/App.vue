<template>
  <div class="container mx-auto p-6 max-w-4xl">
    <h1 class="text-3xl font-bold mb-6">Caddy 控制面板</h1>

    <button 
      @click="addDomain" 
      class="mb-6 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
    >
      新增域名配置
    </button>

    <div class="space-y-4 mb-6">
      <DomainConfig
        v-for="(config, index) in configs"
        :key="index"
        :config="config"
        @remove="removeDomain(index)"
      />
    </div>

    <div class="flex space-x-4 mb-6">
      <button 
        @click="updateConfig" 
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
      >
        更新配置
      </button>
      <button 
        @click="restartCaddy" 
        class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded"
      >
        重啟 Caddy
      </button>
      <button 
        @click="getStatus" 
        class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded"
      >
        刷新狀態
      </button>
    </div>

    <div class="bg-gray-100 p-4 rounded">
      <h3 class="text-xl font-semibold mb-2">狀態</h3>
      <pre class="text-gray-700">{{ status }}</pre>
    </div>

    <div class="bg-gray-100 p-4 rounded mt-4">
      <h3 class="text-xl font-semibold mb-2">日誌</h3>
      <pre class="text-gray-700">{{ logs }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DomainConfig from './components/DomainConfig.vue'

const configs = ref([{ domain: '', target: '', username: '', password: '' }])
const status = ref('')
const logs = ref('')

const addDomain = () => {
  configs.value.push({ domain: '', target: '', username: '', password: '' })
}

const removeDomain = (index) => {
  configs.value.splice(index, 1)
}

const updateConfig = async () => {
  status.value = '更新中...'
  try {
    const response = await fetch('/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ configs: configs.value })
    })
    const result = await response.json()
    status.value = result.message
    if (result.errors) status.value += '\n錯誤: ' + result.errors.join('\n')
  } catch (error) {
    status.value = '錯誤: ' + error.message
  }
}

const restartCaddy = async () => {
  status.value = '重啟中...'
  try {
    const response = await fetch('/restart', { method: 'POST' })
    const result = await response.json()
    status.value = result.message
  } catch (error) {
    status.value = '錯誤: ' + error.message
  }
}

const getStatus = async () => {
  try {
    const response = await fetch('/status')
    const result = await response.json()
    status.value = `運行狀態: ${result.running ? '運行中' : '已停止'}\n最後更新: ${result.last_updated}\n配置數量: ${result.config_count}`
    logs.value = result.logs
  } catch (error) {
    status.value = '錯誤: ' + error.message
  }
}
</script>