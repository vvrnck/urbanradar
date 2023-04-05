<template>
    <div id="legend" class="legend" data-v-step="legend" v-show="showLegend && getActiveLayers().length">
        <v-card class="legend-wrapper">
            <div class="legend-controller">
                <div class="legend-controller-title">
                    <span>{{ $t("legend") }}</span>
                </div>
                <div class="legend-controller-actions">
                    <v-btn icon @click="toggleLegend()">
                        <v-icon v-show="legendOpened">mdi-minus</v-icon>
                        <v-icon v-show="!legendOpened">mdi-plus</v-icon>
                    </v-btn>
                </div>
            </div>

            <div class="legend-content" v-if="legendOpened">

                <v-card elevation="5" outlined shaped>
                    <div class="legend-inner-content">
                        <!-- SKELETON -->
                        <div v-show="getMap.loading || loading">
                            <v-skeleton-loader
                                class="mx-auto mb-3"
                                max-width="300"
                                v-for="i in 3"
                                :key="i"
                                type="text"
                                loading
                            ></v-skeleton-loader>                    
                        </div>

                        <div v-show="!getMap.loading && !loading">
                            <div v-for="(section, j) in sections" :key="j">
                                <div v-for="layer in section.layers" :key="layer.id">
                                    <div v-if="layer.selected">
                                        <div v-for="(legend, key) in layer.legend" :key="key">
                                            
                                            
                                        <div v-if="layer.legend[key].length && key === 'polygon'" class="legend-item polygon">
                                            <div v-if="getLayerType(layer).name === 'scale'">
                                                <div class="legend-layer-name">{{ `${getLabel(layer, $i18n.locale)} (${layer.layerGroup['polygon'].length})` }}</div>
                                                <div 
                                                    v-for="(item, k) in layer.legend['polygon']" 
                                                    :key="k" 
                                                    class="legend-layer-item"
                                                >
                                                    <div class="legend-layer-item-icon" v-html="getHexagon(layer.style.texture.value, item.color)" />
                                                    <div class="legend-layer-item-name">{{ $t(item.name) }}</div>
                                                </div>
                                            </div>

                                            <div v-if="getLayerType(layer).name === 'hexagon'">
                                                <div class="legend-layer-item">
                                                    <div class="legend-layer-item-icon" v-html="getHexagon(layer.style.texture.value, getLayerType(layer).color)" />
                                                    <div class="legend-layer-name">{{ `${getLabel(layer, $i18n.locale)} (${layer.layerGroup['polygon'].length})` }}</div>
                                                </div>             
                                            </div>

                                        </div>

                                        <div v-if="layer.legend[key].length && key === 'image_overlay'" class="legend-item image-overlay">
                                            <div v-if="getLayerType(layer).name === 'scale'">
                                                <div class="legend-layer-name">{{ `${getLabel(layer, $i18n.locale)} (${layer.layerGroup['imageOverlay'].length})` }}</div>
                                                <div 
                                                    v-for="(item, k) in layer.legend['image_overlay']" 
                                                    :key="k" 
                                                    class="legend-layer-item"
                                                >
                                                    <div class="legend-layer-item-icon" v-html="getCircle(item.color)" />
                                                    <div class="legend-layer-name">{{ $t(item.name) }}</div>
                                                </div>
                                            </div>

                                            <div v-if="getLayerType(layer).name === 'hexagon'">
                                                <div class="legend-layer-item">
                                                    <div class="legend-layer-item-icon" v-html="getHexagon(layer.style.texture.value, getLayerType(layer).color)" />
                                                    <div class="legend-layer-name">{{ `${getLabel(layer, $i18n.locale)} (${layer.layerGroup['imageOverlay'].length})` }}</div>
                                                </div>             
                                            </div>
                                        </div>

                                        <div v-if="layer.legend[key].length && key === 'marker'" class="legend-item marker">
                                            
                                                <div 
                                                    v-for="(item, k) in layer.legend['marker']" 
                                                    :key="k" 
                                                    class="legend-layer-item"
                                                >
                                                    <div class="legend-layer-item-marker" v-html="getIcon(item.icon, item.image)" />
                                                    <div class="legend-layer-name">{{ `${getLabel(layer, $i18n.locale)} (${layer.layerGroup['marker'].length})` }}</div>
                                                </div>
                                            
                                        </div>

                                        <div v-if="layer.legend[key].length && key === 'point'" class="legend-item point">
                                            
                                                <div class="legend-layer-name">{{ `${getLabel(layer, $i18n.locale)} (${layer.layerGroup['point'].length})` }}</div>
                                                <div 
                                                    v-for="(item, k) in layer.legend['point']" 
                                                    :key="k" 
                                                    class="legend-layer-item"
                                                >
                                                    <div class="legend-layer-item-icon" v-html="getCircle(item.color)" />
                                                    <div>{{ $t(item.name) }}</div>
                                                </div>
                                            
                                        </div>


                                        </div>
                                        
                                       
                                    </div>
                                </div>
                            </div>
              
                        </div>
                    </div>
                </v-card>
                
            </div>
            
        </v-card>
    </div>
</template>

<script>
import L from 'leaflet';
import { getLabel } from '../../utils';
import { isEmpty } from 'lodash';

export default {
    name: 'Legend',
    data: () => {
        return {
            legendOpened: true,
            loading: true,            
        }
    },
    mounted() {
        
        this.loading = true;
        // legend drag
        const legend = document.getElementById('legend');
        const draggable = new L.Draggable(legend);
        draggable.enable();

        // menu grabbing style
        const legendController = document.getElementsByClassName('legend-controller')[0];
        
        legendController.addEventListener('mousedown', () => {
            legendController.style.cursor = 'grabbing';
        });
        
        legendController.addEventListener('mouseup', () => {
            legendController.style.cursor = 'grab';
        });

        setTimeout(() => {
            this.loading = false;
        }, 600)
    },
    methods: {
        getLabel(item, language)     {
            return getLabel(item, language);
        },
        getActiveLayers() {
            const sections = this.$store.getters.layers;

            const selectedLayers = [];

            sections.map(section => {
                section.layers.map(layer => {
                    if (layer.selected) {
                        selectedLayers.push(layer);
                    }
                })
            });

            return selectedLayers;
        },
        getLayerType(layer) { 
            const layerType = layer.style.types.find(lt => lt.value);
            if (layerType) return layerType;    
            return { name: 'scale' };
        },       
        toggleLegend() {
            this.legendOpened = !this.legendOpened;
        },
        getIcon(icon, image) {
            let iconImage = null;

            try {
                iconImage = require(`../../assets/icons/${icon}`);
            } catch (e) {
                console.error(e);
                console.log("ICON NOT FOUND");
            }
            
            // GET THE LAYER IMAGE
            if (!isEmpty(image)) iconImage = image;

            return `
                <img src="${iconImage}" width="15px" height="15px"></img>
            `;
        },
        getCircle (color) {
            return `<svg height="20" width="20">
                        <circle cx="10" cy="10" r="5" stroke="white" stroke-width="1" fill="${color}" />
                    </svg>`
        },
        getHexagon (texture, color) {
            const border = this.$vuetify.theme.dark ? '#FFFFFF' : '#181818';
            const fillColor = this.$vuetify.theme.dark ? '#FFFFFF' : '#181818';
            switch (texture) {
                case 'HORIZONTAL':
                    return `<svg width="20" height="17.5" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path stroke="${border}" id="svg_1" d="m7.519513,-0.000008l7.352849,3.958512l0,7.917025l-7.352849,3.958512l-7.352849,-3.958512l0,-7.917025l7.352849,-3.958512z" fill="${color}" opacity="1"></path>
                                    <rect id="svg_17" height="1.5" width="11" y="2" x="2" fill="${fillColor}"></rect>
                                    <rect id="svg_14" height="1.5" width="15" y="5" x="0" fill="${fillColor}"></rect>
                                    <rect id="svg_15" height="1.5" width="15" y="8.3" x="0" fill="${fillColor}"></rect>
                                    <rect id="svg_16" height="1.5" width="11" y="11.5" x="2" fill="${fillColor}"></rect>
                                </g>
                            </svg>`
                case 'VERTICAL':
                    return `<svg width="20" height="17.5" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path stroke=${border}" id="svg_1" d="m7.519513,-0.000008l7.352849,3.958512l0,7.917025l-7.352849,3.958512l-7.352849,-3.958512l0,-7.917025l7.352849,-3.958512z" fill="${color}" opacity="1"></path>
                                    <rect id="svg_17" height="10.5" width="1.5" y="2.5" x="1.7" fill="${fillColor}"></rect>
                                    <rect id="svg_14" height="14.5" width="1.5" y="0.5" x="5.1" fill="${fillColor}"></rect>
                                    <rect id="svg_15" height="14.5" width="1.5" y="0.5" x="8.6" fill="${fillColor}"></rect>
                                    <rect id="svg_16" height="10.5" width="1.5" y="2.5" x="12" fill="${fillColor}"></rect>
                                </g>
                            </svg>`
                default:
                    return `<svg width="20" height="17.5" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path stroke="${border}" id="svg_1" d="m7.519513,-0.000008l7.352849,3.958512l0,7.917025l-7.352849,3.958512l-7.352849,-3.958512l0,-7.917025l7.352849,-3.958512z" fill="${color}" opacity="1"></path>
                                </g>
                            </svg>`
            }
        },
    },
    computed: {
        showLegend() {
            return this.$store.getters.legend;
        },
        sections() {
            return this.$store.getters.layers;
        },
        getMap() {
            return this.$store.getters.map;
        }
    }
}
</script>

<style lang="scss">
.legend {
    position: absolute !important;
    z-index: 999;
    right: 10px;
    top: 70px;
    width: 240px;    

    .legend-wrapper {
        z-index: inherit;
        opacity: 0.9;
        box-shadow: 0 1px 5px rgba(0,0,0,0.2);
        border: 2px solid rgba(0,0,0,0.2) !important;   
        background-clip: padding-box;
        border-radius: 5px !important;
        transition: all 0.7s ease-in-out 0s;

        .legend-controller {
            display: grid;
            grid-auto-flow: column;
            grid-template-columns: 9fr 1fr;
            align-items: center;
            height: 44px;
            padding: 5px;
            cursor: grab;

            .legend-controller-title {
                font-size: medium;
                margin-left: 10px;
            }
            // .legend-controller-actions {
            
            // }
        }

        .legend-content {
            padding: 10px;
            max-height: 800px;
            .legend-inner-content {
                padding: 10px;
                font-size: 14px;
                
                .legend-layer-name {
                    font-size: 14px;
                }

                .legend-item {
                    display: grid;
                    align-items: center;
                    padding: 5px;
                    gap: 5px;
                }

                .legend-layer-item {
                    display: grid;
                    grid-auto-flow: column;
                    grid-gap: 5px;
                    grid-template-columns: 1fr 4fr;
                    align-items: center;
                    font-size: 12px;
                    .legend-layer-item-icon {
                        display: flex;
                        align-items: center;
                        width: 20px;
                        height: 20px;
                        margin: auto;
                    }
                    .legend-layer-item-marker {
                        width: 20px; 
                        height: 20px; 
                        margin: auto; 
                        display: flex; 
                        align-items: center; 
                        font-size: 14px;
                    }
                }
            }
        }
    }
    

}
</style>