<script setup>
  import { apiService } from '../../api'
  import { ref } from 'vue'
  import { notify } from "@kyvg/vue3-notification";
  import { useRouter } from 'vue-router';

  let id = window.location.href.split("/")[4]
  let user_observation = ref("")
  let router = useRouter();
  const submit = async () => {
   try {
    await apiService.post('/me/requests', {
      user_observation: user_observation.value,
      service_id: id
    })
    notify({
            type: "success",
            title: "Solicitud exitosa",
            text: "Su solicitud ha sido registrada",
        });
    return router.push("/services")
    } catch (error) {
      return notify({
            type: "error",
            title: "Error",
            text: error.response.data.result ? error.response.data.result : error,
        });
    }
  }
</script>

<template>
  <div class="container">
    <header>
      <h1 class="mx-auto">Solicitar servicio</h1>
    </header>

    <article class="card mt-3 p-3">
      <form>
        <div class="form-group">
          <label class="form-text">Observación <span class="text-muted">(Opcional)</span></label>
          <textarea v-model="user_observation" class="form-control" autofocus></textarea>
        </div>

        <div class="btn-group btn-group-justified text-center mt-4">
          <button @click="submit" type="button" class="btn btn-success">Solicitar servicio</button>
          <router-link :to="{ name: 'services.show', params: { id: $route.params.id } }" class="btn btn-outline-dark" role="button">Cancelar</router-link>
        </div>
      </form>
    </article>
  </div>
</template>