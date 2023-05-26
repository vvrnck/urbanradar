<template>
    <div class="date-picker">
        <v-date-picker
            flat
            full-width
            v-model="dates"
            range
            header-color="white"
            color="#00FFFF"
            :locale="getCalendarType"
            :events="availableDates"
            :event-color="date => getColor(date)"
        ></v-date-picker>
    </div>
</template>

<script>
import axios from 'axios';
import { getSelectedLayers, getApi, getErrors } from '../../utils';
import { isEmpty } from 'lodash';
import moment from 'moment';

export default {
    name: 'DatePicker',
    props: ['loadFeatures'],
    data() {
        return {
            availableDates: []
        }
    },    
    mounted() {
        const url = getApi('calendar');
        axios.get(url).then(response => {
            const { data, errors } = response.data;
            
            if (!isEmpty(errors)) {
                return getErrors(errors);
            }

            this.availableDates = data;
        }).catch(err => {
            console.log(err);
        })
    },
    methods: {
        getColor (date) {
            if (!moment().isAfter(date)) return ['#9D6EDD'];
            else return ['#6FB979'];
        },
    },
    computed: {
        dates: {
            get() {
                return this.$store.getters.dates;
            },
            set(dates) {
                this.$store.dispatch('updateDates', dates);
                if (dates.length === 2) {
                    if (!isEmpty(getSelectedLayers())) {
                        this.loadFeatures();
                    }
                }
            }
        },
        getCalendarType() {
            const language = this.$i18n.locale;
            if (language.includes('en')) return 'en-US';
            else return 'pt-BR'
        }
    }
}
</script>

<style lang="scss">
.date-picker {
    min-width: 250px;
}

@media (min-width: 768px) {
    .v-picker__title {
        display: none;
    }    
}
</style>