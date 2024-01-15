<!-- RequestNoteComponent.vue -->
<template>
    <div>
      <h6 class="mt-4 mb-3 label-text">Nota</h6>
      <div class="input-group mb-3">
        <textarea
          type="text"
          class="form-control"
          placeholder="Ingrese su observación..."
          v-model="user_observation"
        />

      </div>
      <button type="button" class="btn btn-primary" style="width: 100%;" @click="saveNote">Enviar nueva nota</button>
    </div>
  </template>

  <script>
  import { apiService } from '@/api';

  export default {
    props: {
    userObservation: String
    },
    data() {
      return {
        user_observation: this.userObservation || '',
      };
    },
    methods: {
      async saveNote() {
        try {
          await this.editNote();
        } catch (error) {
          console.error('Error al guardar la nota:', error);
          throw error;
        }
      },
      async editNote() {
        try {
          const id = this.$route.params.id;

          await apiService.put(
            `/me/requests/${id}/notes`,
            {
              user_observation: this.user_observation,
            },
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );

          location.reload();
        } catch (error) {
          console.error('Error al guardar la nota:', error);
          throw error;
        }
      },
    },
  };
  </script>

  <style scoped>
  /* Estilos específicos para este componente */
  .input-group {
    width: 100%;
  }

  .btn-primary {
    margin-top: 0.25rem;
  }

  .label-text {
  color: #8a9399;
  font-weight: bold;
  margin-top: 5%;
  text-decoration:underline;
}
  </style>

