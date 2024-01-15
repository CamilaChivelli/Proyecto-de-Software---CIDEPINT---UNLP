<script setup>
  import { onMounted, ref, watch } from 'vue'
  import { apiService } from '../../api'
  import { useRoute } from 'vue-router'

  let service = ref({})
  let institution = ref({})
  let id = useRoute().params.id

  onMounted(() => {
    apiService.get(`/services/${id}`)
              .then(response => {
                service.value = response.data
                institution.value = service.value.institution
              })
              .catch(error =>{
                console.log(error)
              })
  })

  watch(institution, async(newInstitution) => {
    if (newInstitution.address) {
      let coordinates = newInstitution.address.split(',')

      // Extrae las coordenadas
      var storedLatitude = parseFloat(coordinates[0]);
      var storedLongitude = parseFloat(coordinates[1]);

      if (storedLatitude && storedLongitude) {
        let map = L.map('map').setView([storedLatitude, storedLongitude], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        L.marker([storedLatitude, storedLongitude]).addTo(map);
      }
    }
  })
</script>

<template>
  <div class="container">

    <article class="card mt-3">
      <div class="card-header">
        <h3>{{ service.name }}</h3>
        <router-link :to="{ path: id + '/service_requests/new' }" class="btn btn-ver btn-sm" role="button">Solicitar</router-link>
      </div>

      <div class="card-body">
        <p>{{ service.service_type }}</p>
        <p>{{ service.description }}</p>

      </div>
    </article>

    <article class="card mt-3">
      <div class="card-header">
        <h3>Institución {{ institution.name }}</h3>
      </div>

      <div class="card-body">
        <ul>
          <li>
            <strong>Ubicación:</strong> {{ institution.location }}
          </li>

          <li>
            <strong>Horario de atención al cliente:</strong> {{ institution.customer_service_hours }}
          </li>

          <li>
            <strong>Sitio web:</strong> <a href="{{ institution.web }}" target="_blank">{{ institution.web }}</a>
          </li>

          <li>
            <strong>Información de contacto:</strong> <a :href="'mailto:' + institution.contact_info">{{ institution.contact_info }}</a>
          </li>
        </ul>
      </div>

      <div id="map"></div>
    </article>
  </div>
</template>

<style>

/* Estilo personalizado para el botón "Ver" */
.btn-ver {
  background-color: #ffae42;
  border-color: #e69500;
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #1a237e;
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}
.btn-ver:hover {
  background-color: #e69500;
  border-color: #b97d00;
  color: #0d47a1;
}
</style>