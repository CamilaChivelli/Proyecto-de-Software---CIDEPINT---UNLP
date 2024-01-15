<template>
  <div class="container mt-5">
    <div class="container">
  <div class="row">
    <div class="col-md-6">
      <section class="mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <input
            type="text"
            class="form-control"
            v-model="searchText"
            @input="searchServices"
            placeholder="Buscar Servicios"
          />
        </div>
      </section>
    </div>

    <div class="col-md-6">
      <section class="mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <div class="dropdown" style="width: 100%;">
            <select class="form-select" v-model="optionType" @change="selectType" style="width: 100%;">
              <option value="" selected style="">Mostrar todos</option>
              <option v-for="type in serviceTypes" :value="Object.keys(type)[0]" :key="Object.keys(type)[0]">
                {{ Object.values(type)[0] }}
              </option>
            </select>
          </div>
        </div>
      </section>
    </div>
  </div>
</div>

    <section>
      <table class="table">
        <thead class="thead-dark">
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Institucion</th>
            <th scope="col">Tipo</th>
            <th scope="col">Descripcion</th>
            <th scope="col">Tags</th>
            <th scope="col">Opciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.institution.name }}</td>
            <td>{{ service.service_type }}</td>
            <td>{{ service.description }}</td>
            <td>
              <span v-for="(keyword, index) in service.keywords.split(',')" :key="index" class="keyword-label">{{ keyword.trim() }}</span>
            </td>
            <td><router-link :to="{ name: 'services.show', params: { id: service.id }}" class="btn btn-ver btn-sm">Ver</router-link></td>
          </tr>
        </tbody>
      </table>
    </section>

    <nav aria-label="Page navigation example">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ 'disabled': page === 1 }">
          <a class="page-link" href="#" @click="changePage(page - 1)">Anterior</a>
        </li>
        <li v-for="pageNumber in Math.ceil(total / per_page)" :key="pageNumber" class="page-item" :class="{ 'active': page === pageNumber }">
          <a class="page-link" href="#" @click="changePage(pageNumber)">{{ pageNumber }}</a>
        </li>
        <li class="page-item" :class="{ 'disabled': page === Math.ceil(total / per_page) }">
          <a class="page-link" href="#" @click="changePage(page + 1)">Siguiente</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

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

.keyword-label {
  display: inline-block;
  padding: 5px 10px;
  margin: 2px;
  background-color: #3498db; /* Color de fondo */
  color: #fff; /* Color del texto */
  border-radius: 5px; /* Bordes redondeados */
}

</style>


<script>
import { apiService } from '@/api'

export default {
  data() {
    return {
      services:[],
      page: 1,
      per_page: 25,
      total: 30,
      start: true,

      serviceTypes: [],
      institutionNames: {},
      optionType: '',

      searchText: '',
    };
  },
  async mounted() {
    await this.fetchServices();
    await this.fetchServiceTypes();
  },

  methods: {
    async fetchServices() {
      try {
        if (this.start) {
          this.start = false
          let response = await apiService.get("/services/search");

          this.services = response.data.data;
          this.page = response.data.page;
          this.per_page = response.data.per_page;
          this.total = response.data.total;
        }
        const params = {
          q: this.searchText,
          type: this.optionType,
          page: this.page,
          per_page: this.per_page,
        }

        let response = await apiService.get("/services/search", { params });

        this.services = response.data.data;

        this.page = response.data.page;
        this.per_page = response.data.per_page;
        this.total = response.data.total;

      }
      catch (error) {

        console.error('Error al obtener los servicios: ', error);
        throw error;

      }
    },

    async fetchServiceTypes() {
      try {

        let response = await apiService.get('/service-types');

        this.serviceTypes = response.data.data;
      }
      catch (error) {

        console.error('Error al obtener los tipos de servicio: ', error);
        throw error;

      }
    },

    async changePage(page){
      this.page = (page <= 0 || page > Math.ceil(this.total / this.per_page)) ? this.page : page
      await this.fetchServices()
    },

    async searchServices(){
      this.page = 1
      await this.fetchServices()
    },

    async selectType(){
      this.page = 1
      await this.fetchServices()
    },

  },
};
</script>