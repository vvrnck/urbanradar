<template>  
  <v-app id="app">
      <router-view />
      <Snackbar />
  </v-app>
</template>

<script>
import Snackbar from '../components/snackbar/Snackbar.vue'

export default {
    name: 'App',
    components: { Snackbar },
    data() {
        return {
            
        }
    }
}
</script>

<style lang="scss">
#app {
    //overflow-y: hidden !important;
}
</style>
