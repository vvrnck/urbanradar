<template>
    <div class="layers">
        <div
            v-for="(menuItem, key) in menuItems"
            :key="key"
        >
            <div v-if="menuItem.section">
                <div 
                    v-for="layer in menuItem.data" 
                    :key="layer.name"
                    class="layer-menu-item"
                >
                    <v-switch
                        light
                        color="#00FFFF"
                        dense
                        v-model="layer.selected"
                        @change="() => onChange(layer)"
                        :label="layer.name"
                    ></v-switch>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { getApi, getErrors } from '../../../utils'
import moment from 'moment';
import { isEmpty } from 'lodash';

export default {
    name: 'Layers',
    props: ['close', 'loadFeatures'],
    data() {
        return {
            
        }
    },
    mounted() {
        const url = getApi('layer');
        axios.get(url).then(response => {
            const { data, errors } = response.data;

            // GARANTE CAMADA DE PREDIÇÃO JA VIR SELECIONADA
            data.map(section => {
                section.layers.map(layer => {
                    const { extra_props } = layer.style;

                    if (extra_props && extra_props.mobile && (extra_props.type === 'icon' || extra_props.type === 'marker')) layer.selected = true;
                })
            })

            if (!isEmpty(errors)) {
                return getErrors(errors);
            }
           
            const newData = Object.assign([], data);
            
            const initialData = Object.assign([], newData);
            this.$store.dispatch('updateInitialLayers', initialData);            

            localStorage.setItem('menu', JSON.stringify(newData));
            this.$store.dispatch('updateLayers', newData);

            this.loadFeatures();
        });
    },
    methods: {
        onChange(selectedLayer) {
            const sections = this.$store.getters.layers;

            const newSections = Object.assign([], sections);

            newSections.map(section => {
                section.layers.map(layer => {
                    if (layer.id !== selectedLayer.id) {
                        layer.selected = false;
                    }
                });
            });

            this.$store.dispatch('updateLayers', newSections);

            this.loadFeatures();
        }
    },
    computed: {
        menuItems() {
            return this.$store.getters.layers;
        }, 
    }

}
</script>

<style lang="scss">
    .layer-menu-item {
        .v-input__slot .v-label {
        
                color: #adadad !important;
                font-size: 16px;
            
        }
    }
</style>

