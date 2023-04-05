<template>
     <v-snackbar
      v-model="snackbar.open"
      :timeout="snackbar.timeout"
      :color="getColorByType(snackbar.type)"
      absolute
      bottom
      right
      class="snackbar"
    >
      {{ $t(snackbar.text) }}

      <template v-slot:action="{ attrs }">
        <v-btn
          class="snackbar-button"
          :color="close_color"
          text
          v-bind="attrs"
          @click="snackbar.open = false"
        >
          {{ $t('snackbar_close') }}
        </v-btn>
      </template>
    </v-snackbar>
</template>

<script>
import COLORS from '../../colors/colors';

export default {
    name: 'Snackbar',
    data() {
        return {
            close_color: '#FFF'
        }
    },
    mounted() {
      
    },
    methods: {
      getColorByType(type) {
        if (type === 'success') return COLORS.SUCCESS;
        else if (type === 'warning') return COLORS.WARNING;
        else return COLORS.ERROR;
      }
    },
    computed: {
      snackbar() {
        return this.$store.getters.snackbar;
      }
    }
}
</script>

<style lang="scss">
.snackbar {
  z-index: 9999 !important;
  .snackbar-button {
    font-size: 12px !important;
  }
}

.v-snack__wrapper {
  min-width: 305px !important;
}

</style>