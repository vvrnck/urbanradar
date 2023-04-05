<template>
    <div id="map-menu" class="map-menu" data-v-step="map-menu">
        <v-card class="map-menu-wrapper">
            <div class="map-menu-controller">
                <div class="map-menu-controller-title">
                    <span>{{ $t(`menu`)  }}</span>
                </div>
                <div class="map-menu-controller-actions">
                    <v-btn icon @click="clearMenu()">
                        <v-icon>mdi-broom</v-icon>
                    </v-btn>
                    
                    <div>
                        <v-btn icon v-if="getSelectedLayers().length <= 1">
                            <v-icon>mdi-layers-off</v-icon>
                        </v-btn>
                        <v-btn icon @click="toggleLayerOverlay()" v-else>
                            <v-icon>mdi-layers</v-icon>
                        </v-btn>

                    </div>
                    
                    
                    <v-btn icon @click="toggleMenu()">
                        <v-icon v-show="getMapMenuStatus">mdi-close</v-icon>
                        <v-icon v-show="!getMapMenuStatus">mdi-open-in-new</v-icon>
                    </v-btn>
                </div>
            </div>

            <div class="map-menu-content" v-show="getMapMenuStatus">
                <!-- SKELETON -->
                <div v-show="loading">
                    <v-skeleton-loader
                        class="mx-auto mb-5"
                        max-width="300"
                        type="image"
                        loading
                    ></v-skeleton-loader>

                     <v-skeleton-loader
                        class="mx-auto mb-3"
                        max-width="300"
                        v-for="i in 10"
                        :key="i"
                        type="text"
                        loading
                    ></v-skeleton-loader>
                    
                </div>

                <!-- CONTENT -->
                <div v-show="!loading">
                    <div class="map-menu-content-inner">
                        <DatePicker :loadFeatures="loadFeatures" />
                        <Layers 
                            :loadFeatures="loadFeatures" 
                            :clearMapData="clearMapData" 
                            :removeLayer="removeLayer"
                        />
                    </div>
                </div>
            </div>
        </v-card>
    </div>
</template>

<script src="./mapmenu.js"></script>

<style lang="scss">
    @import "./map-menu.scss";
</style>