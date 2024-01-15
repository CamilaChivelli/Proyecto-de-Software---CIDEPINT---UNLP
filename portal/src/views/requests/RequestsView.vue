<template>
    <div class="container">
        <header class="d-flex justify-content-between center-align">
            <img src="https://i.ibb.co/cgQcYLw/missolicitudes.png" alt="Servicios Image" class="mx-auto img-fluid">
        </header>
        <RequestsComponent></RequestsComponent>
    </div>
</template>

<script>
import RequestsComponent from '@/components/RequestsComponent.vue';

export default {
    name: 'RequestsView',
    components: {
        RequestsComponent,
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