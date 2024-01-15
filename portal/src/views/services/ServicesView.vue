<template>
  <div class="container">
    <header class="d-flex justify-content-between center-align mx-auto">
      <img src="https://i.ibb.co/CVnN70Y/services.png" alt="Servicios Image" class="mx-auto img-fluid">
    </header>
    <ServicesComponent></ServicesComponent>
  </div>
</template>


<script>
import ServicesComponent from '@/components/ServicesComponent.vue';

export default {
  name: 'ServicesView',
  components: {
    ServicesComponent,
},
}
</script>

<style scoped>
.img-fluid {
  width: 100%;
  height: auto;
  margin-top: 10px;
}
</style>