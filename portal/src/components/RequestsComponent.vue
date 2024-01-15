<template>
  <div class="container mt-5">
    <section class="mb-4">
      <div class="row d-flex justify-content-between align-items-center" @change="filter">
        <!-- Cambiado de input de texto a componentes de fecha -->
        <div class="col-md-4">
        <VueDatePicker v-model="dateStart" placeholder="Fecha inicial" auto-apply @update:model-value="filter"></VueDatePicker>
         </div>

      <!-- Segunda columna: VueDatePicker para la fecha final -->
      <div class="col-md-4">
        <VueDatePicker v-model="dateEnd" placeholder="Fecha final" auto-apply @update:model-value="filter"></VueDatePicker>
      </div>
        <div class="dropdown col-md-4" style="width: 100%;">
          <select class="form-select" v-model="optionStatus" style="width: 100%;">
            <option value="" selected>Mostrar todos</option>
            <option v-for="type in requestStatus" :value="Object.keys(type)[0]" :key="Object.keys(type)[0]">
              {{ Object.values(type)[0] }}
            </option>
          </select>
        </div>
      </div>
    </section>
  </div>
  <div class="container mt-5">
    <section>
      <table class="table">
        <thead class="thead-dark">
          <tr>
            <th scope="col">Servicio</th>
            <th scope="col">Institución</th>
            <th scope="col">Tipo</th>
            <th scope="col" @click="toggleOrder('status')">Estado ⇅</th>
            <th scope="col" @click="toggleOrder('inserted_at')">Fecha de solicitud ⇅</th>
            <th scope="col">Detalles</th>
          </tr>
        </thead>
        <tbody v-if="serviceRequests.length > 0">
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.service.name }}</td>
            <td>{{ request.service.institution.name }}</td>
            <td>{{ request.service.service_type }}</td>
            <td>{{ request.status }}</td>
            <td>{{ formatTimestamp(request.inserted_at) }}</td>
            <td><router-link :to="{ name: 'request-show', params: { id: request.id }}" class="btn btn-ver btn-sm">Ver</router-link></td>
          </tr>
        </tbody>
        <tbody v-else>
          <H3 class="mt-3">Usted no tiene solicitudes</H3>
        </tbody>

      </table>
    </section>

    <nav aria-label="Page navigation example">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ 'disabled': page === 1 }">
          <a class="page-link" href="#" @click="changePage(page - 1)">Anterior</a>
        </li>
        <li class="page-item" v-for="pageNumber in Math.ceil(total / per_page)" :key="pageNumber" :class="{ 'active': page === pageNumber }">
          <a class="page-link" href="#" @click="changePage(pageNumber)">{{ pageNumber }}</a>
        </li>
        <li class="page-item" :class="{ 'disabled': page === Math.ceil(total / per_page) }">
          <a class="page-link" href="#" @click="changePage(page + 1)">Siguiente</a>
        </li>
      </ul>
    </nav>
  </div>
</template>


<script>
import { apiService } from '@/api'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

export default {
  components: { VueDatePicker },
  data() {
    return {
      serviceRequests:[],
      page: 1,
      per_page: 25,
      total: 30,
      start: true,
      sort:'status',
      order:'desc',

      requestStatus: [],
      dateStart: null,
      dateEnd: null,
      optionStatus: ""
    };
  },
  async mounted() {
    await this.fetchRequests();
    await this.fetchRequestsStatus();
  },

  methods: {
    async fetchRequests() {
      try {
        if (this.start) {
          console.log("start")
          this.start = false
          let response = await apiService.get("/me/requests");

          this.serviceRequests = response.data.data;
          this.page = response.data.page;
          this.per_page = response.data.per_page;
          this.total = response.data.total;
        } else {
          console.log("NO start")
          const params = {
          page: this.page,
          per_page: this.per_page,
          sort: this.sort,
          order: this.order,
          status: this.optionStatus,
          date_start: this.dateStart,
          date_end: this.dateEnd,
          }

          let response = await apiService.get("/me/requests", { params });

          this.serviceRequests = response.data.data;
          this.page = response.data.page;
          this.per_page = response.data.per_page;
          this.total = response.data.total;
        }


      }
      catch (error) {

        console.error('Error al obtener las solicitudes de servicio: ', error);
        throw error;

      }
    },

    async toggleOrder(column) {
        // Si estamos ordenando por la misma columna, cambiamos la dirección
        if (this.sort === column) {
            this.order = this.order === 'asc' ? 'desc' : 'asc';
        }
        // Si estamos cambiando de columna, establecemos el orden como ascendente por defecto
        else {
            this.sort = column;
            this.order = 'asc';
        }

        this.page = 1;
        await this.fetchRequests();
    },
    async fetchServiceName(service_id) {
      try {

        let response = await apiService.get(`/me/services/${service_id}`);
        this.serviceName = response.data.

        this.requestStatus = response.data.data;
      }
      catch (error) {

        console.error('Error al obtener el servicio: ', error);
        throw error;

      }
    },
    async fetchRequestsStatus() {
      try {

        let response = await apiService.get("/me/requests/status");

        this.requestStatus = response.data.data;
      }
      catch (error) {

        console.error('Error al obtener los estados de solicitudes: ', error);
        throw error;

      }
    },
    async changePage(page){
      this.page = (page <= 0 || page > Math.ceil(this.total / this.per_page)) ? this.page : page
      await this.fetchRequests()
    },
    async selectStatus(){
      this.page = 1
      await this.fetchRequests()
    },
    async filter(){
      await this.fetchRequests()
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
/* Custom Styles */
.container {
  max-width: 100%;
  margin: 0 auto;
}
.form-select {
  width: 200px; /* Adjust as needed */
}

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

/* Additional styles for the "All Types" dropdown */
.form-select {
  padding: 0.375rem 1.75rem 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-select:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Table header color */
.thead-dark th {
  background-color: #429b42;
  color: #fff;
}
</style>

