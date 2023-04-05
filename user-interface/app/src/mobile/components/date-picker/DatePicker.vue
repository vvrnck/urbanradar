<template>
   <div class="date-menu">
        <div 
            v-show="!getDateMenuState()" 
            @click="toggleDate()" 
            style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px;"
        >
            <v-icon>
               mdi-calendar-multiple
            </v-icon>
        </div>
        <div v-show="getDateMenuState()">
            <div class="date-menu-action" @click="toggleDate()">
                <v-icon>mdi-close</v-icon>
            </div>
            <Date :close="toggleDate" />
        </div>
    </div>
</template>

<script>
import Date from '../date/Date';
import { updateMobileItem } from '../../../utils';
import { isEmpty } from 'lodash';

export default {
    name: 'DatePicker',
    props: ['loadFeatures'],
    components: { Date },
    data() {
        return {
            
        }
    },
    methods: {
        toggleDate() {
            const mobile = this.$store.getters.mobile;
            const isDateMenuOpen = mobile.toggle.dates;
            const dates = this.$store.getters.dates;

            if (isDateMenuOpen) {
                document.getElementById('date-map-control').style.bottom = '35px';
                this.$store.dispatch('updateMobile', { 
                    ...mobile, 
                    toggle: { 
                        layers: false,
                        dates: false,
                        settings: false,
                        fullscreen: false,
                        caption: false,
                        feature: false
                    } 
                }); 
                if (isEmpty(dates)) return;
                return this.loadFeatures(); // chama api
            }

            updateMobileItem('dates', true);
            document.getElementById('date-map-control').style.bottom = '50%';
        },
        getDateMenuState() {
            const mobile = this.$store.getters.mobile;
            return mobile.toggle.dates;
        }
    }
}
</script>

<style lang="scss">

    .date-menu-action {
        display: flex;
        justify-content: flex-end;
        cursor: pointer;
    }

</style>
