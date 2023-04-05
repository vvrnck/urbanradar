<template>
    <div class="custom-control">
            <div class="settings-control">
                <div class="leaflet-control-layers control" @click="toggleSettings()">
                    <v-icon>
                        mdi-cog
                    </v-icon>
                </div>
            </div>
            <div class="menu-control" v-show="settings" @click="toggleSettings()">
                    <div class="menu-options">
                        <div class="location-control">
                            <div class="leaflet-control-layers control" @click="goToInitialLocation()" v-show="settings">
                                <v-icon>
                                    mdi-crosshairs-gps
                                </v-icon>
                            </div>
                        </div>
                        <div class="location-control">
                            <div class="leaflet-control-layers control" @click="toggleFeature()" v-show="settings">
                                <v-icon>
                                    mdi-map-marker
                                </v-icon>
                            </div>
                        </div>
                        <div class="caption-control" position="topleft" v-show="settings">
                            <div class="leaflet-control-layers control" @click="toggleCaption()">
                                <v-icon>
                                    mdi-closed-caption
                                </v-icon>
                            </div>
                        </div>
                        <div class="expand-control" position="topleft" v-show="settings">
                            <div class="leaflet-control-layers control" @click="toggleExpand()">
                                <v-icon>
                                    {{ isExpanded ? `mdi-fullscreen-exit` : 'mdi-fullscreen' }}
                                </v-icon>
                            </div>
                        </div>
                        <div class="logout-control" position="topleft" v-show="settings">
                            <div class="leaflet-control-layers control" @click="logout()">
                                <v-icon>
                                    mdi-logout
                                </v-icon>
                            </div>
                        </div> 
                    </div>
            </div>
            <Caption />
        </div>
</template>

<script>
import { updateMobileItem } from '../../../utils';
import Caption from '../caption/Caption';

export default {
    name: 'CustomControl',
    props: ['map', 'goToInitialLocation'],
    components: { Caption },
    methods: {
        toggleCaption() {
            const mobile = this.$store.getters.mobile;
            const currentCaptionState = mobile.toggle.caption;

            updateMobileItem('caption', !currentCaptionState);
        },
        toggleSettings() {
            const mobile = this.$store.getters.mobile;
            const currentSettingsState = mobile.toggle.settings;
            
            updateMobileItem('settings', !currentSettingsState);
        },
        toggleFeature() {
            const mobile = this.$store.getters.mobile;
            const currentFeatureState = mobile.toggle.feature;
            
            const sections = this.$store.getters.layers;

            sections.map(section => {
                section.layers.map(l => {
                    const { extra_props, style } = l;
                    if (style.extra_props && style.extra_props.mobile && style.extra_props.type === 'marker') {
                        const draw = {
                            type: 'CREATE',
                            layer: l,
                            feature: null
                        }
                        this.$store.dispatch('updateMobile', { ...mobile, draw: draw });
                    }
                })
            });
            
            updateMobileItem('feature', !currentFeatureState);
        },
        toggleExpand() {
            const mobile = this.$store.getters.mobile;
            const isExpanded = mobile.toggle.fullscreen;
           
            var element = document.getElementById('app');

            if (isExpanded) {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
                updateMobileItem('fullscreen', false);
            } else {
                if (element.requestFullscreen) {
                    element.requestFullscreen(); 
                }
                else if (element.mozRequestFullScreen) {
                    element.mozRequestFullScreen();
                }
                else if (element.webkitRequestFullscreen) {
                    element.webkitRequestFullscreen();
                }
                else if (element.webkitEnterFullscreen) {
                    element.webkitEnterFullscreen();
                }
                else if (element.msRequestFullscreen) {
                    element.msRequestFullscreen();
                }
                updateMobileItem('fullscreen', true);
            }
        },
        showCaption() {

        },
        logout() {
            sessionStorage.clear();
            localStorage.clear();
            this.$router.replace('/');
        },
    },
    computed: {
        settings() {
            const mobile = this.$store.getters.mobile;
            return mobile.toggle.settings;
        },
        isExpanded() {
            const mobile = this.$store.getters.mobile;
            return mobile.toggle.fullscreen;
        }
    }
}
</script>

<style lang="scss">

.logout-control {
    i {
        transform: rotate(180deg);
    }
}

.settings-control {
    z-index: 999999 !important;
    position: absolute;
    top: 10px;
    left: 10px;
}

.menu-control {
    position: absolute;
    width: 100%;
    height: 100%;
    bottom: 0;
    top: 0;
    left: 0;
    right: 0;
    z-index: 99999;
    background-color: rgba(0,0,0, 0.5);
    
    .control { max-width: 50px; }
    .menu-options {
        position: absolute;
        top: 50px;
        left: 10px;
    }
}

</style>