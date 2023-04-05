<template>
    <v-dialog
        v-model="popup.open"
        fullscreen
        persistent
        transition="dialog-bottom-transition"
        scrollable
        class="popup"
        eager
        no-click-animation
        retain-focus
    >
        <v-sheet :class="`opacity-95`">
             <div class="popup-content">
                <div :class="`popup-header`">
                    <span>
                        {{ popup.data && popup.data.name }}
                    </span>
                    <div class="popup-header-actions">
                        <v-btn
                            icon
                            @click="toggleTray()"
                        >
                            <v-icon>{{ popup.tray ? 'mdi-arrow-up' : 'mdi-arrow-down' }}</v-icon>
                        </v-btn>
                        <v-btn
                            icon
                            @click="closePopup()"
                        >
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </div>
                    
                </div>
                <div class="popup-body">
                    <div class="popup-wrapper-content">
                        <div class="popup-tabs" v-show="popup.tabs">
                            <v-tabs 
                                grow 
                                :color="getColor()" 
                                v-model="selectedTab"
                            >
                                <v-tabs-slider color="teal"></v-tabs-slider>
                                <v-tab 
                                    v-for="(tab, tabIndex) in popup.tabs" 
                                    :key="tabIndex" 
                                    
                                >
                                    {{ getLabel(tab, $i18n.locale) }}
                                </v-tab>
                            </v-tabs>

                            <v-tabs-items v-model="selectedTab" class="popup-tab-items">
                                <v-tab-item
                                    v-for="(tab, tabIndex) in popup.tabs" 
                                    :key="tabIndex" 
                                    class="popup-tab-item"
                                >
                                    <v-card elevation="2" outlined shaped>
                                        <div class="popup-tab-content">
                                            <div class="popup-tab" :style="tab.style">
                                                <div
                                                    v-for="(chart, chartIndex) in tab.charts"
                                                    :key="chartIndex"
                                                    
                                                    class="chart"
                                                >
                                                    <Chart 
                                                        :options="chart.options"
                                                        :styles="chart.style"
                                                        :gridName="`${chart.name}`"
                                                        :interactive="chart.interactive"
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    </v-card>
                                </v-tab-item>
                            </v-tabs-items>
                        </div>                        
                    </div>
                </div>
            </div>
        </v-sheet>
       
    </v-dialog>
</template>

<script>



import Chart from '../charts/Chart.vue';
import { getLabel } from '../../utils';
import { lang } from 'moment';

export default {
    name: 'Popup',
    props: ['popup', 'closePopup'],
    components: {
    
        Chart
    },
    data() {
        return {
            selectedTab: null
        }
    },
    mounted() {
        
    },
    methods: {    
        getLabel(item, language)     {
            return getLabel(item, language);
        },
        isPredictionLayer() {
            const sections = Object.assign([], this.$store.getters.layers);
                        
            let isPredictionLayer = false;

            sections.map(section => {
                section.layers.map(layer => {
                    if (layer.id === 49 && layer.selected) isPredictionLayer = true;
                });
            })

            return isPredictionLayer;
            
        },
        toggleTray() {
            this.popup.tray = !this.popup.tray;
            const dialog = document.querySelector('.opacity-95').parentNode;
            const popupHeader = document.querySelector('.popup-header');
            if (this.popup.tray) {
                dialog.style.top = '99999px';
                popupHeader.style.bottom = '0px';
                popupHeader.style.top = 'unset';
                
            } else {
                dialog.style.top = 'unset';
                popupHeader.style.bottom = 'unset';
                popupHeader.style.top = '0px';
            }
        },
        getColor() {
            if (this.$vuetify.theme.dark) return '#FFF';
            else return '#000'
        },
       
    },
    computed: {
        getSelectedTab() {
            const selectedTab = this.popup.tabs.find(t => t.selected);
            return selectedTab;
        }
    }
}
</script>

<style lang="scss">

.popup {
    position: absolute;
    top:0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 99999999;        
    transition: all 0.7s ease-in-out 0s;
}

.opacity-95 {
    opacity: 0.95;
    transition: all 0.7s ease-in-out 0s;
}

.popup-content  {
    overflow-y: auto;
    height: 100%;
    transition: all 0.7s ease-in-out 0s;
    .popup-header {
        position: fixed;
        top: 0;
        bottom: unset;
        width: 100%;
        font-size: 18px;
        display: flex;
        justify-content: space-between;
        padding: 15px 10px;
        height: 64px;
        background: teal;
        z-index: 9999999;
        transition: all 0.7s ease-in-out 0s;
    }
    .popup-body {
        margin-top: 64px;
        overflow: hidden;

        .popup-wrapper-content {
            display: flex;
            flex-direction: column;
            gap: 50px;
            margin: 10px 80px;
            .popup-tab-item {
                margin-top: 20px;
            }
            .popup-tab-content {
                padding: 10px;
                overflow: hidden;
                display: grid;
                gap: 20px;
                //align-items: center;
                justify-content: center;
               
                .popup-tab {
                    display: grid;
                    gap: 10px;
                }
                
            }
        }
        
        .chart {
            display: contents;
            width: 100%;
            height: 100%;
            margin: 20px 0px; 
            
        }
    }
}
</style>
