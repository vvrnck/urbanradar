<template>
    <v-navigation-drawer
      v-model="layerOverlay"
      absolute
      temporary
      right
      style="transition: all 0.7s ease-in-out 0s; z-index: 9999; opacity: 0.9; "
    >
       
            <draggable 
                v-model="selectedLayers"
                
                @end="reloadLayers()"
            >
                <transition-group>
                    <div v-for="layer in selectedLayers" :key="layer.id" class="card-list">
                        <v-card outlined class="card-item" elevation="5">
                            <v-icon>mdi-drag-horizontal</v-icon>
                            <span>{{ getLabel(layer, $i18n.locale) }}</span>
                        </v-card>
                    </div>
                </transition-group>
            </draggable>
       
        
    </v-navigation-drawer>
</template>

<script>
import draggable from 'vuedraggable';
import { getLabel } from '../../utils';

export default {
    name: 'LayerOverlay',
    props: ['loadLayer', 'clearMapData'],
    components: { draggable },
    methods: {
        getLabel(item, language) {
            return getLabel(item, language);
        },
        reloadLayers() {
            this.clearMapData().then(async () => {
                const dates = this.$store.getters.dates;
                for (let i = 0; i < this.selectedLayers.length; i++) {
                    const layer = this.selectedLayers[i];
                    await this.loadLayer(layer, dates);
                }
            }).then(() => {
                this.$store.dispatch('updateLayerOverlay', false);
            });    
        }
    },
    computed: {
        selectedLayers: {
            get() {
                return this.$store.getters.selectedLayers;
            },
            set(selectedLayers) {
                this.$store.dispatch('updateSelectedLayers', selectedLayers);
            }
        },
        layerOverlay: {
            get() {
                return this.$store.getters.layerOverlay;
            },
            set(layerOverlay) {
                this.$store.dispatch('updateLayerOverlay', layerOverlay);
            }
        }, 
    }
}
</script>

<style lang="scss">
.card-list {
    margin: 5px;
    background: transparent;
    .card-item {
        padding: 10px;
        display: flex;
        align-items: center;
        justify-items: center;
        gap: 10px;
        cursor: move;
    }
}

</style>