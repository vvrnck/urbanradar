<template>
    <div class="date-picker">
        <v-date-picker
            flat
            full-width
            v-model="dates"
            range
            header-color="white"
            color="#00FFFF"
            locale="pt-BR"
        ></v-date-picker>
    </div>
</template>

<script>

export default {
    name: 'Date',
    props: ['close'],
    data() {
        return {
            
        }
    },    
    computed: {
        dates: {
            get() {
                return this.$store.getters.dates;
            },
            set(dates) {
                this.$store.dispatch('updateDates', dates);                
                if (dates.length == 2) this.close();
            }
        }
    }
}
</script>

<style lang="scss">
.date-picker {
    min-width: 250px;
    margin: 5px;
}
.v-picker__title {
    display: none;
}
</style>