<template>    
    <v-tour name="tour" :steps="steps" :options="options" :callbacks='callbacks'></v-tour>  
</template>

<script>
  export default {
    name: 'TourEnglish',
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
                    Here you will find: <b>Map, Management, Help, Settings</b>
                    <br><br>
                    To know more of each one of those, you can click on it and navigate through the pages.
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
                content: 'This button will bring you to the <b>MAP</b> page.',
                params: { placement: 'right' },
                before: type => new Promise((resolve, reject) => {
                  this.setElementOpacity('.map-wrapper', 0.2);
                  resolve();
                })
            },
            {
                target: '[data-v-step="navbar-item-management"]',
                header: { title: 'Management', },
                content: 'This button will bring you to the <b>MANAGEMENT</b> page.',
                params: { placement: 'right' }
            },
            {
                target: '[data-v-step="navbar-item-feedback"]',
                header: { title: 'Feedback', },
                content: 'This button will bring you to the <b>FEEDBACK</b> page.',
                params: { placement: 'right' }
            },
            {
                target: '[data-v-step="navbar-item-helper"]',
                header: { title: 'Helper', },
                content: 'This button will bring you to the <b>HELPER</b> page.',
                params: { placement: 'right' }
            },
            {
                target: '[data-v-step="navbar-item-settings"]',
                header: { title: 'Settings', },
                content: 'This button will bring you to the <b>SETTINGS</b> page.',
                params: { placement: 'right' },
            },
            {
                target: '[data-v-step="navbar-item-logout"]',
                header: { title: 'Logout', },
                content: 'This button will logout the system.',
                params: { placement: 'right' },
            },
            {
                target: '[data-v-step="navbar-item-language"]',
                header: { title: 'Language', },
                content: 'This button will change the system languague.',
                params: { placement: 'right' },
            },
            {
                target: '[data-v-step="navbar-item-theme"]',
                header: { title: 'Theme', },
                content: 'This button will change the system theme.',
                params: { placement: 'right' },
            },
            {
                target: '[data-v-step="navbar-item-tour"]',
                header: { title: 'Tour', },
                content: 'This button will show a walkthrough the system.',
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
                content: 'Here you will be able to search any place in the world.',
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
              content: 'With this button you will be able to switch map styles and show/hide active layers.',
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
                    In this menu you will be able to toggle on and off all system layers and it's options. <br>
                    Then, you can see the georeferenced data 
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
                content: 'This box will show a legend of active layers on the system.',
                params: { placement: 'left' }
            },
            {
                target: '[data-v-step="toolbox"]',
                header: {
                  title: 'Toolbox',
                },
                content: 'This is a fast way to change menu dates.'
            },
          
        ],
        options: {
          useKeyboardNavigation: true,
          highlight: true,
          labels: {
            buttonSkip: 'Skip tour',
            buttonPrevious: 'Previous',
            buttonNext: 'Next',
            buttonStop: 'Finish'
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
        // TODO - voltar todos os styles para default
        this.setElementOpacity('.nav', 1);
        this.setElementOpacity('.map-wrapper', 1);
      }
    },
  }
</script>
