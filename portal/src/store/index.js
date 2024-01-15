import { createPinia } from "pinia";
import { useAuthStore } from '@/store/modules/auth';

const store = createPinia({
    modules: {
        auth: useAuthStore
    }
});

export default store;