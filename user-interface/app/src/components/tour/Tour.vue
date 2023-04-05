<template>
  <div class="tour-wrapper">
    <div v-if="language === 'en'">
        <TourEnglish />
    </div>
    <div v-if="language === 'pt'">
        <TourPortuguese />
    </div>
  </div>
</template>

<script>
import TourEnglish from './tour-languages/TourEnglish';
import TourPortuguese from './tour-languages/TourPortuguese';

export default {
  name: 'Tour',
  components: { TourEnglish, TourPortuguese },
  computed: {
    language() {
      return this.$i18n.locale;
    }
  }
}
</script>

<style lang="scss">
.v-tour__target--highlighted {
  box-shadow: 0 0 0 99999px rgba(0,0,0,.7) !important;
}
</style>
