<template>  
    <v-tour name="tour" :steps="steps" :options="options" :callbacks='callbacks'></v-tour>
</template>

<script>
  export default {
    name: 'TourPortuguese',
    data () {
      return {
        callbacks: {
          onStart: this.startTourCallback,
          onStop: this.finishTourCallback
        },
        steps: [
            {
                target: '[data-v-step="navbar"]',
                header: { title: 'Navbar', },
                content: `
                  <div>
                    Aqui voce tera rapido acesso aos seguintes itens: <b>Mapa, Gerenciamento, Ajuda, Configuracoes</b>
                    <br><br>
                    Para saber mais sobre cada um deles, continue pelo tour.
                  </div>
                `,
                params: { placement: 'right' },
                before: type => new Promise((resolve, reject) => {
                  this.setElementOpacity('.map-wrapper', 1);
                  resolve();
                })
            },
            {
                target: '[data-v-step="navbar-item-map"]',
                header: { title: 'Map', },
                content: 'Acesso ao mapa',
                params: { placement: 'right' },
                before: type => new Promise((resolve, reject) => {
                  this.setElementOpacity('.map-wrapper', 0.2);
                  resolve();
                })
            },
            {
                target: '[data-v-step="navbar-item-management"]',
                header: { title: 'Gerenciamento', },
                content: 'Acesso ao gerenciamento',
                params: { placement: 'right' }
            },
            {
                target: '[data-v-step="navbar-item-feedback"]',
                header: { title: 'Reporte', },
                content: 'Acesso ao reporte',
                params: { placement: 'right' }
            },
            {
                target: '[data-v-step="navbar-item-helper"]',
                header: { title: 'Manual', },
                content: 'Acesso ao manual',
                params: { placement: 'right' }
            },
          {
                target: '[data-v-step="navbar-item-settings"]',
                header: { title: 'Configurações', },
                content: 'Acesso as configurações',
                params: { placement: 'right' },
            },
            {
                target: '[data-v-step="navbar-item-language"]',
                header: { title: 'Language', },
                content: 'Change system language',
                params: { placement: 'right' },
            },
            {
                target: '[data-v-step="navbar-item-theme"]',
                header: { title: 'Theme', },
                content: 'Change system theme',
                params: { placement: 'right' },
            },
            {
                target: '[data-v-step="navbar-item-tour"]',
                header: { title: 'Tour', },
                content: 'Tour',
                params: { placement: 'right' },
                before: type => new Promise((resolve, reject) => {
                  this.setElementOpacity('.nav', 1);
                  this.setElementOpacity('.map-wrapper', 0.2);
                  resolve();
                })
            },
            {
                target: '.leaflet-control-geosearch',
                header: { title: 'Search', },
                content: 'Aqui sera possivel...',
                params: { placement: 'right' },
                before: type => new Promise((resolve, reject) => {
                  this.setElementOpacity('.nav', 0.2);
                  this.setElementOpacity('.map-wrapper', 1);
                  resolve();
                })
            },
            {
              target: '.leaflet-control-layers',
              header: { title: 'Controller', },
              content: 'Controle de camadas do mapa',
              params: { placement: 'left' },
              before: type => new Promise((resolve, reject) => {
                this.setElementOpacity('.nav', 0.2);
                resolve();
              })
            },
            {
                target: '[data-v-step="map-menu"]',  // We're using document.querySelector() under the hood
                header: {
                title: 'Menu',
                },
                content: `
                    Atraves desse menu será possivel habilitar as camadas e selecionar datas para a exibicao dos dados
                `,
                params: {
                  placement: 'right'
                },
                before: type => new Promise((resolve, reject) => {
                  this.setElementOpacity('.nav', 1);
                  resolve()
                })
            },
            {
                target: '[data-v-step="legend"]',
                header: {
                  title: 'Legend',
                },
                content: 'An awesome plugin made with Vue.js!',
                params: { placement: 'left' }
            },
            {
                target: '[data-v-step="toolbox"]',
                header: {
                  title: 'Toolbox',
                },
                content: 'Toolbox',
            },
          
        ],
        options: {
          useKeyboardNavigation: true,
          highlight: true,
          labels: {
            buttonSkip: 'Pular tour',
            buttonPrevious: 'Anterior',
            buttonNext: 'Proximo',
            buttonStop: 'Terminar'
          }
        },
      }
    },
    methods: {
      setElementOpacity(elementQuerySelector, opacity) {
        const el = document.querySelector(elementQuerySelector);
        el.style.opacity = opacity;
      },
      startTourCallback() {
              
      },
      finishTourCallback() {
        this.setElementOpacity('.nav', 1);
        this.setElementOpacity('.map-wrapper', 1);
      }
    },
  }
</script>
