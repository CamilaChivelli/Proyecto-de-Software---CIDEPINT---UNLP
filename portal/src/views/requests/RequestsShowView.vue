<template>
    <div class="container">
        <section>
            <div class="container mt-5 d-flex align-items-center">
        <div v-if="serviceRequest" class="card mx-auto"> <!-- mx-auto para centrar horizontalmente -->
            <div class="card-body text-center">
                <h3 class="card-title">{{ serviceRequest.service.name }} - {{ serviceRequest.service.service_type }} - {{ serviceRequest.service.institution.name }}</h3>

                <label class="label-text">Estado</label>
                <h5>{{ serviceRequest.status }}</h5>

                <label class="label-text">Fecha de solicitud</label>
                <h5>{{ formatTimestamp(serviceRequest.inserted_at) }}</h5>

                <label class="label-text">Tus observaciones</label>
                <h6>{{ serviceRequest.user_observation || "No hiciste ninguna observacion" }}</h6>

                <label class="label-text">Observación de la institución</label>
                <h6>{{ serviceRequest.institution_observation || "La institución no hizo ninguna observación" }}</h6>

                <RequestNoteComponent :userObservation="serviceRequest.user_observation"></RequestNoteComponent>
            </div>
        </div>
    </div>
        </section>
    </div>
</template>

<script>
import RequestNoteComponent from '@/components/RequestNoteComponent.vue';
import { apiService } from '@/api';
import { useRoute } from 'vue-router';
import { notify } from "@kyvg/vue3-notification";
import router from '../../router';

export default {
name: 'RequestsShowView',
components: {
    RequestNoteComponent,
},

data() {
    return {
    serviceRequest: null,
    };
},
async mounted() {
    await this.fetchServiceRequest();
},
methods: {
    async fetchServiceRequest() {
    try {
        const id = useRoute().params.id;
        const response = await apiService.get(`/me/requests/${id}`);
        this.serviceRequest = response.data;
    } catch (error) {
        router.push("/")
        throw notify({
                    type: "error",
                    title: "Error",
                    text: error.response.data.result ? error.response.data.result : error,
                });
    }
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      };
      return date.toLocaleDateString('es-ES', options);
    },
},
};
</script>

<style scoped>
.container {
max-width: 800px;
margin: 0 auto;
}

.card {
width: 100%;
margin-top: 20px;
border: 1px solid #ddd;
border-radius: 5px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-body {
padding: 20px;
}

.card-title {
font-size: 24px;
font-weight: bold;
}

.card-text {
margin-bottom: 10px;
}

.label-text {
  color: #8a9399;
  font-weight: bold;
  margin-top: 5%;
  text-decoration:underline;
}

.info-text {
  color: #8a9399;
  font-weight: bold;
  text-decoration:underline;
}
</style>
