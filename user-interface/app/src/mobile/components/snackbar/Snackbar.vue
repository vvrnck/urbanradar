<template>
     <v-snackbar
      v-model="options.open"
      :timeout="options.timeout"
      :color="options.color"
      absolute
      rounded="pill"
      class="snackbar"
    >
      {{ $t(options.text) }}

      <template v-slot:action="{ attrs }">
        <v-btn
          class="snackbar-button"
          :color="close_color"
          text
          v-bind="attrs"
          @click="options.open = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
</template>

<script>
export default {
    name: 'Snackbar',
    props: ['options'],
    data() {
        return {
            close_color: '#FFF'
        }
    },
}
</script>

<style lang="scss">
@media (min-width: 360px) and (max-width: 768px) {
    .snackbar {
      z-index: 9999 !important;
      width: 100%;
      .snackbar-button {
        font-size: 12px !important;
      }
    }

    .v-snack__wrapper {
      width: 100% !important;
    }
}


</style>