<template>
  <div class="container">
        <header class="d-flex justify-content-between center-align">
            <img src="https://i.ibb.co/mHwTbM3/estadisticas.png" alt="Servicios Image" class="mx-auto img-fluid">
        </header>
  </div>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-12">
        <div class="row">
          <div class="col-md-6 max-height-container mx-auto">
            <h4 class="text-center">Cantidad de solicitudes por su estado</h4>
            <Radar id="my-chart-id" :data="radarData" :options="radarOptions" :style="myStyles"/>
          </div>
          <div class="col-md-6 max-height-container text-center">
            <h4 class="text-center">Cantidad de solicitudes por servicio</h4>
            <Doughnut id="my-chart-id" :data="doughnutData" :options="doughnutOptions" :style="myStyles"/>
          </div>
        </div>
        <div class="row">
          <h4 class="text-center mx-auto">Cantidad de solicitudes de este año</h4>
          <div class="col-md-12">
            <Bar
              id="my-chart-id"
              :options="barOptions"
              :data="barData"
              :style="myStyles"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar, Doughnut, Radar } from 'vue-chartjs';
import { apiService } from '@/api';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
RadialLinearScale,
PointElement,
LineElement,
Filler,
} from 'chart.js';

ChartJS.register(ArcElement, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, RadialLinearScale, PointElement, LineElement,Filler);

export default {
  name: 'Chart',
  components: { Bar, Doughnut, Radar },
  computed: {
    myStyles() {
      return {
        height: '43vh',
        position: 'relative',
        legend: {
          display: true,
          position: 'right',
        },
      };
    },
  },
  data() {
    return {
      barData: {
        label: 'Data One',
        labels: [ 'January', 'February', 'March' ],
        datasets: [ { data: [40, 20, 12] } ]
      },
      barOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
        legend: {
          display: false,
          position:'right'
        },
      },
      },
      radarData: {
        labels: [
          'January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December',
        ],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: ['#41B883', '#E46651', '#00D8FF', '#DD1B16'],
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11],
          },
        ],
      },
      radarOptions: {
        responsive: true,
        plugins: {
        legend: {
          display: false,
          position: 'right' // Configuración para ocultar la leyenda
        },
        layout: {
          autoPadding: true
        }
      },
      },
      doughnutData: {
        labels: [
          'January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December',
        ],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: ['#41B883', '#E46651', '#00D8FF', '#DD1B16'],
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11],
          },
        ],
      },
      doughnutOptions: {
        responsive: false,
        plugins: {
        legend: {
          display: true,
          position:'right'
        },
      },
      },
    };
  },
  watch: {
    chartData: function() {
      this.fetchData();
    }
  },
  methods: {
    generateRandomColors(count) {
      const colors = [];
      const letters = '0123456789ABCDEF';

      for (let i = 0; i < count; i++) {
        let color = '#';
        for (let j = 0; j < 6; j++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        colors.push(color);
      }
      return colors;
    },
    async fetchData() {
    try {
      const rankingMeses = await apiService.get('/me/requests/ranking-monthly');
      const rankingStatus = await apiService.get('/me/requests/ranking-status');
      const rankingRequests = await apiService.get('/me/requests/ranking-requests');

      const mesesKeys = Object.keys(rankingMeses.data);
      const mesesValues = Object.values(rankingMeses.data);
      const statusKeys = Object.keys(rankingStatus.data);
      const statusValues = Object.values(rankingStatus.data);
      const requestsKeys = Object.keys(rankingRequests.data);
      const requestsValues = Object.values(rankingRequests.data);

      this.barData = {
            labels: [],
            datasets: []
      };

      this.doughnutData = {
            labels: [],
            datasets: []
      };

      this.radarData = {
            labels: [],
            datasets: []
      };


      this.barData.labels = mesesKeys;
      this.barData.datasets = [
        {
          data: mesesValues,
          backgroundColor: this.generateRandomColors(mesesKeys.length)
        }];



      this.radarData.labels = statusKeys
      this.radarData.datasets = [
        {
          data: statusValues,
          backgroundColor: this.generateRandomColors(statusKeys.length)
        }];



      this.doughnutData.labels = requestsKeys
      this.doughnutData.datasets = [
        {
          data: requestsValues,
          backgroundColor: this.generateRandomColors(requestsKeys.length)
        }];

    } catch (error) {
      console.error('Error fetching data:', error);
    }
  },
},
  mounted() {
    this.fetchData();
  },
};
</script>

<style>
.img-fluid {
  width: 100%;
  height: auto;
  margin-top: 10px;
}
.max-height-container {
    max-height: 50vh; /* Puedes ajustar el porcentaje según tus necesidades */

    overflow-y: auto; /* Agrega desplazamiento vertical si el contenido es más grande que la altura máxima */
}
</style>