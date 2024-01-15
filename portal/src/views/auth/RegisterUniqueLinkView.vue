<!-- LoginForm.vue -->
<template>
    <div class="container h-100">
      <div class="row justify-content-sm-center h-100">
        <div class="col-xxl-4 col-xl-5 col-lg-5 col-md-7 col-sm-9">

          <h1 class="text-center mb-4">Registro</h1>

          <div class="card shadow-lg">

            <div class="card-body p-5">
                <h1 class="text-center mb-4" style="color: red;">Aclaracion</h1>
                <p style="color: red;">Si cambia de password correctamente, este medio ya no será valido si desea hacerlo en un futuro</p>
                <form @submit.prevent="submitForm">
                  <div class="form-group">
                    <input v-model="email" type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Email">
                    <small id="emailHelp" class="form-text text-muted">El email debe ser el que colocó en el primer registro</small>
                </div>
                  <div class="form-group">
                    <input v-model="password" type="password" class="form-control" id="password" placeholder="Password">
                  </div>
                  <div class="form-group">
                    <input v-model="password2" type="password" class="form-control" id="password2" placeholder="Repetir Password">
                  </div>
                  <button type="submit" class="btn btn-primary" style="width: 100%;">Agregar contraseña</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
 <script>
  import { ref, inject } from 'vue';
  import { useRouter } from 'vue-router';
  import { notify } from "@kyvg/vue3-notification";
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
      const password = ref('');
      const password2 = ref('');

      // Methods
      const submitForm = async () => {
        const body = {
          "email": email.value,
          "password": password.value,
          "password2": password2.value,
        };

        await authStore.registerUniqueLinkUser(body);
        router.push('/login');

      };
      return { email, password,password2,submitForm };
    },
  };
  </script>

