<template>
    <div class="caption-control-content" v-show="caption" > 
        <div class="leaflet-control-layers control" >
            <div class="caption-menu-action" @click="toggleCaption()">
                <v-icon>mdi-close</v-icon>
            </div>
            <div class="caption">
                
                <div v-for="layer in layers" :key="layer.id">
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
                                    <div class="legend-layer-item-marker" v-html="getIcon(item.icon)" />
                                    <div class="legend-layer-name">{{ `${getLabel(layer, $i18n.locale)} (${layer.layerGroup['marker'].length})` }}</div>
                                </div>
                            
                        </div>


                     </div>
                    
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { updateMobileItem, getLabel } from '../../../utils';

export default {
    name: 'Caption',
    data() {
        return {
           
        }
    },
    methods: {
        toggleCaption() {
            const mobile = this.$store.getters.mobile;
            updateMobileItem('caption', !mobile.toggle.caption);
        },
        getLabel(item, language)     {
            return getLabel(item, language);
        },
        getLayerType(layer) { 
            const layerType = layer.style.types.find(lt => lt.value);
            if (layerType) return layerType;    
            return { name: 'scale' };
        },     
        getIcon(icon) {
            // @TODO - CHANGE SRC PATH TO URL
            return `
                <img src="${require(`../../../assets/icons/${icon}`)}" width="15px" height="15px"></img>
            `;
        },  
        getCircle (color) {
            return `<svg height="18" width="18">
                        <circle cx="10" cy="10" r="5" stroke="white" stroke-width="1" fill="${color}" />
                    </svg>`
        },
        getHexagon (texture, color) {
            switch (texture) {
                case 'horizontal':
                    return `<svg width="15" height="17" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path stroke="#333" id="svg_1" d="m7.519513,-0.000008l7.352849,3.958512l0,7.917025l-7.352849,3.958512l-7.352849,-3.958512l0,-7.917025l7.352849,-3.958512z" fill="${color}" opacity="1"></path>
                                    <rect id="svg_17" height="1.5" width="11" y="2" x="2" fill="#000"></rect>
                                    <rect id="svg_14" height="1.5" width="15" y="5" x="0" fill="#000"></rect>
                                    <rect id="svg_15" height="1.5" width="15" y="8.3" x="0" fill="#000"></rect>
                                    <rect id="svg_16" height="1.5" width="11" y="11.5" x="2" fill="#000"></rect>
                                </g>
                            </svg>`
                case 'vertical':
                    return `<svg width="15" height="17" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path stroke="#333" id="svg_1" d="m7.519513,-0.000008l7.352849,3.958512l0,7.917025l-7.352849,3.958512l-7.352849,-3.958512l0,-7.917025l7.352849,-3.958512z" fill="${color}" opacity="1"></path>
                                    <rect id="svg_17" height="15" width="1.5" y="1" x="1.7" fill="#000"></rect>
                                    <rect id="svg_14" height="15" width="1.5" y="0" x="5.1" fill="#000"></rect>
                                    <rect id="svg_15" height="15" width="1.5" y="0" x="8.6" fill="#000"></rect>
                                    <rect id="svg_16" height="15" width="1.5" y="1" x="12" fill="#000"></rect>
                                </g>
                            </svg>`
                default:
                    return `<svg width="15" height="17" xmlns="http://www.w3.org/2000/svg">
                                <g>
                                    <path stroke="#333" id="svg_1" d="m7.519513,-0.000008l7.352849,3.958512l0,7.917025l-7.352849,3.958512l-7.352849,-3.958512l0,-7.917025l7.352849,-3.958512z" fill="${color}" opacity="1"></path>
                                </g>
                            </svg>`
            }
        },
    },
    computed: {
        caption() {
            const mobile = this.$store.getters.mobile;
            return mobile.toggle.caption;
        },
        layers() {
            const sections = this.$store.getters.layers;

            const newSections = Object.assign([], sections);

            const selectedLayers = [];

            newSections.map(section => {
                section.layers.map(layer => {
                    const { extra_props } = layer.style;
                    if (extra_props && extra_props.mobile && layer.selected) selectedLayers.push(layer);
                })
            })

            return selectedLayers;    
        }

    }
}
</script>

<style lang="scss">

.caption-menu-action {
    cursor: pointer;
    position: absolute;
    right: 5px;
}

.caption-control-content {
    position: absolute;
    top: 50px;
    left: 10px;
    width: 160px;
    height: 100px;
    z-index: 9999;

    .caption {
       min-height: 30px;
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
</style>