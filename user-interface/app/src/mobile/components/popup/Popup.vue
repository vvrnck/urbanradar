<template>
    
          <v-dialog
                v-model="showPopup"
                fullscreen
                hide-overlay
                transition="dialog-bottom-transition"
                scrollable
                class="popup"
            >
                <div class="popup-content">
                    <div class="popup-header">
                        POPUP
                        <v-btn
                            icon
                            dark
                            @click="showPopup = false"
                        >
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </div>
                    <div class="popup-body">
                        graficos aqui
                    </div>
                </div>
            </v-dialog>
    
</template>

<script>
import axios from 'axios';
import { getApi } from '../../../utils';

export default {
    name: 'Popup',
    props: ['showPopup', 'close', 'data'],
    mounted() {
        
        console.log(this.data);
        const currentMapData = this.$store.getters.map;
        const dates = currentMapData.date;

        let dt_start = dates[0];
        let dt_end = dates[1];
        
        const { idLayer, name } = this.data;

        let url = getApi('features', { id_layer: idLayer, list_ids_cat: '', dt_start: dt_start, dt_end: dt_end, hexcode: name });
    },
}
</script>

<style lang="scss">





</style>