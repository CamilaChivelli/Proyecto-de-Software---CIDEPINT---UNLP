<!-- LoginForm.vue -->
<template>
    <div class="container h-100">
      <div class="row justify-content-sm-center h-100">
        <div class="col-xxl-4 col-xl-5 col-lg-5 col-md-7 col-sm-9">

          <h1 class="text-center mb-4">Registro</h1>

          <div class="card shadow-lg">

            <div class="card-body p-5">
                <form @submit.prevent="submitForm">
                  <div class="form-group">
                    <input v-model="email" type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Email">
                    <small id="emailHelp" class="form-text text-muted">El email no debe estar registrado</small>
                </div>
                  <div class="form-group">
                    <input v-model="firstname" type="text" class="form-control" id="firstname" placeholder="Nombre">
                  </div>
                  <div class="form-group">
                    <input v-model="lastname" type="text" class="form-control" id="lastname" placeholder="Apellido">
                  </div>
                  <button type="submit" class="btn btn-primary" style="width: 100%;">Registrarse</button>
              </form>
            </div>

          </div>
        </div>
      </div>
    </div>
  </template>

  <script>
  import { ref, inject } from 'vue';
  import { notify } from "@kyvg/vue3-notification";
  import { useRouter } from 'vue-router';
  export default {
    setup() {
      const authStore = inject('authStore');
      const isLoggedIn = authStore.getIsLoggedIn;
      const router = useRouter();

      if (isLoggedIn) {
        router.push('/');
      }
      // Data
      const email = ref('');
      const firstname = ref('');
      const lastname = ref('');

      // Methods
      const submitForm = async () => {
        const body = {
          "email": email.value,
          "firstname": firstname.value,
          "lastname": lastname.value,
        };
          await authStore.registerUser(body);
          router.push('/');
          throw notify({
                    type: "success",
                    title: "Exito",
                    text: "Revise su casilla de correo para continuar el registro",
                });

      };
      return { email, firstname,lastname,submitForm };
    },
  };
  </script>

