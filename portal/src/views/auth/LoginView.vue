<!-- LoginForm.vue -->
<template>
  <article class="h-100">
    <div class="container h-100">
      <div class="row justify-content-sm-center h-100">
        <div class="col-xxl-4 col-xl-5 col-lg-5 col-md-7 col-sm-9">

          <h1 class="text-center mb-4">Inicio de sesión</h1>

          <div class="card shadow-lg">

            <div class="card-body p-5">

              <form @submit.prevent="submitForm">
                  <div class="form-group">
                    <input v-model="email" type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Email">
                  </div>
                  <div class="form-group">
                    <input v-model="password" type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
                  </div>
                  <button type="submit" class="btn btn-primary" style="width: 100%;">Iniciar sesión</button>
              </form>
              <GoogleLogin :callback="callback" class="mt-4 mx-auto" style="min-width: 100%;"/>
            </div>

            <div class="card-footer py-3 border-0">
              <div class="text-center">
                ¿No tienes una cuenta? <a href="/register" class="text-dark">Regístrate</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>

<script>
import { ref, inject } from 'vue';
import { useRouter } from 'vue-router';
import { decodeCredential } from 'vue3-google-login'
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

    const callback = async (response) => {
      const userData = decodeCredential(response.credential)
      const body = {
        "email": userData.email,
        "firstname": userData.given_name,
        "lastname": userData.family_name
      };

      try {
        await authStore.loginGoogleUser(body);
        await authStore.fetchUser();
        router.push('/');
      } catch (error) {
        console.error('Error durante el inicio de sesión con google:', error);
      }
    }
    // Methods
    const submitForm = async () => {
      const body = {
        "email": email.value,
        "password": password.value
      };

      try {
        await authStore.loginUser(body);
        await authStore.fetchUser();
        router.push('/');
      } catch (error) {
        console.error('Error durante el inicio de sesión:', error);
      }
    };
    return { email, password, submitForm, callback };
  },
};
</script>

