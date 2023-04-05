<template>  
    <div id="feature-information" class="feature-information">
        <v-sheet class="feature-information-content">
            <v-card shaped outlined elevation="5">
                {{ featureInformation.data.imageOverlayType }}
            </v-card>
        </v-sheet>
        
    </div>
</template>

<script>
export default {
    name: 'FeatureInformation',
    props: ['featureInformation'],
}
</script>

<style lang="scss">
.feature-information {
    position: absolute;
    z-index: 9999;
    width: 215px;
    top: 10px;
    left: calc(50% - 56px);
    border: 2px solid rgba(0,0,0,0.2);   
    box-shadow: 0 1px 5px rgba(0,0,0,0.2);
    background-clip: padding-box;
    cursor: pointer;
    justify-content: center;
    align-items: center;
    max-width: 400px;
    max-height: 650px;
    overflow-y: hidden;    
    overflow-x: hidden;
    
  
    .feature-information-content {
        width: 100%;
        height: 100%;
        opacity: 0.9;
        border-radius: 3px;
        text-align: center;
        padding: 10px;
    }
}
</style>