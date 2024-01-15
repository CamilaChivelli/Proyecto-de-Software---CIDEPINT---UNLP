<template>
  <section class="main-content">
    <img src="https://cidepint.ing.unlp.edu.ar/wp-content/uploads/2023/09/Logo-CIDEPINT-sept-2023.jpg" alt="CIDEPINT Logo" class="portal-logo" />
    <p class="portal-description">
      Bienvenido a nuestra página, donde puedes explorar una variedad de servicios y realizar solicitudes
      para su evaluación. Ofrecemos soluciones en diversas áreas, desde servicios anticorrosivos hasta opciones
      ecológicas para reducir el impacto ambiental de la industria. ¡Descubre lo que podemos hacer por ti!
    </p>
  </section>
</template>

<style scoped>
/* Estilos adicionales para resaltar el texto */
.portal-description {
  padding: 15px; /* Agrega relleno alrededor del texto */
  border: 1px solid #ddd; /* Agrega un borde alrededor del texto */
  border-radius: 8px; /* Hace que las esquinas del borde sean redondeadas */
  background-color: #f9f9f9; /* Agrega un fondo alrededor del texto */
}

.portal-description strong {
  font-weight: bold;
  color: #0066cc;
}

.portal-description em {
  font-style: italic;
  color: #e44d26;
}

.portal-description p {
  margin-bottom: 15px;
}

/* Estilos para los encabezados */
.portal-description h2 {
  color: #333;
  border-bottom: 2px solid #A2C579;
  padding-bottom: 5px;
  margin-top: 20px;
}

/* Estilos responsivos */
@media (max-width: 768px) {
  .main-content {
    margin: 10px;
  }

  .portal-description {
    font-size: 14px;
  }

  .portal-description h2 {
    font-size: 1.5em;
  }
}

@media (max-width: 576px) {
  .portal-description {
    font-size: 12px;
  }

  .portal-description h2 {
    font-size: 1.2em;
  }
}

</style>
