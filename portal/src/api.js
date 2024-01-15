import axios from 'axios';

let _baseURL = import.meta.env.VITE_BASE_URL || "https://admin-grupo09.proyecto2023.linti.unlp.edu.ar"

const apiService = axios.create({
    baseURL: `${_baseURL}/api`,
    withCredentials: true,
    xsrfCookieName: 'csrf_access_token'
});

export { apiService };
