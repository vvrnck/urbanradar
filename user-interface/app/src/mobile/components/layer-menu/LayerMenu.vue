<template>
    <div class="layer-menu">
        <div v-show="!getLayerMenuState()" @click="toggleLayer()">
            <v-icon>
                mdi-layers
            </v-icon>
        </div>
        <div v-show="getLayerMenuState()">
            <div class="layer-menu-action" @click="toggleLayer()">
                <v-icon>mdi-close</v-icon>
            </div>
            <Layers 
                :loadFeatures="loadFeatures"
                close="toggleLayer" 
            />
        </div>
    </div>
</template>

<script>
import Layers from '../layers/Layers';

export default {
    name: 'LayerMenu',
    components: { Layers },
    props: ['loadFeatures'],
    data() {
        return {
            
        }
    },
    methods: {
        toggleLayer() {
            let menuState = this.$store.getters.menu;
            if (menuState.layers) {
                return this.$store.dispatch('updateMenu', { dates: false, layers: false, settings: false });
                //return this.loadFeatures();
            }
            this.$store.dispatch('updateMenu', { dates: false, layers: true, settings: false });
        },
        getLayerMenuState() {
            return this.$store.getters.menu.layers;
        }
    }
}
</script>

<style lang="scss">

    .layer-menu-action {
        display: flex;
        justify-content: flex-end;
    }


</style>