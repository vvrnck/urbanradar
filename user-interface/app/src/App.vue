<template>
  <div id="app">
    <v-app>
      <router-view :key="$route.fullPath"></router-view>
      <Snackbar />
      <Tour></Tour>
    </v-app>
  </div>
</template>

<script>
import { Snackbar, Tour } from './components';

export default {
  name: 'App',
  components: {
    Snackbar, Tour
  },
  created() {
    const loadWorkbox = () => {
      if (this.$workbox) {
        this.$workbox.addEventListener("waiting", async () => {
          await this.$workbox.messageSW({ type: "SKIP_WAITING" });
        });
      }
    }

    loadWorkbox();
      
  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  overflow-y: hidden;
} */
</style>
