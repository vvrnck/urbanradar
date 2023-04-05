<template>
    <div class="map-page">
        <Navbar 
            title="map"
            :hasMenu="true"
        />
        <Map />
    </div>
</template>

<script>

import Map from '../components/map/Map.vue';
import Navbar from '../components/navbar/Navbar.vue';

export default {
    name: 'MapPage',
    components: { Map, Navbar },
}

</script>

<style lang="scss">
.map-page {
    display: flex;
    height: 100vh;

    @media (max-width: 768px) {
        flex-direction: column;
    }
}
</style>
