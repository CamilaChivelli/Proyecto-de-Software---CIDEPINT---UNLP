import { defineStore } from 'pinia';
import { apiService } from '@/api'
import { notify } from "@kyvg/vue3-notification";
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth',{
    state: () => ({
        user: {},
        isLoggedIn: false,
    }),
    persist: true,
    getters: {
        getUser: (state) => state.user,
        getIsLoggedIn: (state) => state.isLoggedIn,
    },

    actions: {

        async loginUser(body) {
            try {
                const response = await apiService.post('/auth/', body);
                console.log(response)
                return response;
            } catch (error) {

                throw notify({
                    type: "error",
                    title: "Error",
                    text: error.response.data.result ? error.response.data.result : error,
                });
            }
        },
        async fetchUser() {
            try {
                const { data } = await apiService.get('/me/profile');
                this.$patch({
                    user: data,
                    isLoggedIn: true,
                  })
            } catch (error) {
                throw notify({
                    type: "error",
                    title: "Error",
                    text: error.response.data.result ? error.response.data.result : error,
                });
            }
        },
        async logoutUser() {
            try {
                await apiService.get('/auth/logout');
                this.$reset()
            } catch (error) {
                throw notify({
                    type: "error",
                    title: "Error",
                    text: error.response.data.result ? error.response.data.result : error,
                });
            }
        },
        async registerUser(body) {
            try {
                const response = await apiService.post('/auth/register', body, { params: { currentUrl: window.location.href } });
                return response;
            } catch (error) {
                throw notify({
                    type: "error",
                    title: "Error",
                    text: error.response.data.result ? error.response.data.result : error,
                });
            }
        },
        async registerUniqueLinkUser(body) {
            var url = window.location.href
            var link = url.split('/')[4]
            const router = useRouter();
            try {
                const response = await apiService.post('/auth/register/'+link, body);
                notify({
                    type: "success",
                    title: "Éxito",
                    text: "Ha cambiado su contraseña correctamente",
                })
                return response

            } catch (error) {
                throw notify({
                    type: "error",
                    title: "Error",
                    text: error.response.data.result ? error.response.data.result : error,
                });
            }
        },
        async loginGoogleUser(body) {
            try {
                const response = await apiService.post('/auth/login-google', body);
                return response;
            } catch (error) {
                throw notify({
                    type: "error",
                    title: "Error",
                    text: error.response.data.result ? error.response.data.result : error,
                });
            }
        },
    },
},
{persist: true}
);
