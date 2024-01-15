<script setup>
import { inject } from 'vue';
import { RouterLink, RouterView } from 'vue-router'

const authStore = inject('authStore');
const user = authStore.getUser;

const logout = async () => {
      await authStore.logoutUser();
      window.location.reload();
    };
</script>

<template>
  <notifications position="top center" width="400px"/>
  <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #A2C579;">
    <a class="navbar-brand" href="/">
      <img src="https://cidepint.ing.unlp.edu.ar/wp-content/uploads/2019/09/LOGO100.png" width="30" height="30" class="d-inline-block align-top" alt="">
      CIDEPINT
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
      <div class="navbar-nav">
        <router-link to="/services" class="nav-item nav-link">Servicios</router-link>
        <router-link to="/statistics" class="nav-item nav-link navbar-nav">Estadisticas</router-link>
      </div>
      <div v-if="user.id" class="navbar-nav ml-auto">
        <router-link to="/requests" class="nav-item nav-link">Mis Solicitudes</router-link>
        <router-link to="/" class="nav-item nav-link" @click.prevent="logout">Cerrar sesión</router-link>
      </div>
      <div v-else class="navbar-nav ml-auto">
        <router-link to="/login" class="nav-item nav-link">Iniciar Sesion</router-link>
      </div>
    </div>
  </nav>

  <section>
    <router-view></router-view>
  </section>

</template>

<style>


.notification-title {
    font-size: 22px;
}

.notification-content {
  font-size: 16px; /* Tamaño de fuente personalizado */
}
</style>

