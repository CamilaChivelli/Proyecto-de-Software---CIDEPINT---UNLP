# Portal

## Stack

- NodeJS: 14.21.3
- VueJS: 3.3.7

## Setup

1. Clonar el repositorio.

2. Posicionarse en el directorio `/portal` y correr en la terminal el comando:

```sh
npm install
```

3. Crear dentro del directorio `/portal` un archivo `.env` con el siguiente contenido:

```
# Flask API
export VITE_BASE_URL="https://localhost:5000"
```

Nota: Si tus credenciales son distintas, sólo basta con reemplazarlas en el `.env`.

Luego, cargamos las variables de entorno en nuestra `shell` corriendo en la terminal el siguiente comando:

```sh
source .env
```

4. Para compilar y correr la aplicación en `Development`:

```sh
npm run dev
```

## Otros

### Compilar y minificar la aplicación para `Production`

```sh
npm run build
```

### Correr [ESLint](https://eslint.org/)

```sh
npm run lint
```
