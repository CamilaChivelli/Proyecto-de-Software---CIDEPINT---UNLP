<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '@/store/modules/auth';

const authStore = useAuthStore();
onMounted(async () => {
  await authStore.loginUser();
});

</script>
<template>
</template>