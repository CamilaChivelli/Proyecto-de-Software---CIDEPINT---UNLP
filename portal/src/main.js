import './assets/main.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'
import Notifications from '@kyvg/vue3-notification'


import { useAuthStore } from '@/store/modules/auth';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'


import App from './App.vue'
import router from './router'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(VueAxios, axios)
app.use(vue3GoogleLogin, {
    clientId: '621808232668-dhucnvsri6mnf430g1u5p9n6p6agnhi9.apps.googleusercontent.com'
  })

app.use(Notifications)
app.component('VueDatePicker', VueDatePicker);
// Se declara de manera global el acceso al store Auth, asi se accede a estos valores desde cualquier lugar de la aplicacion
const authStore = useAuthStore();
app.provide('authStore', authStore)

app.mount('#app')
