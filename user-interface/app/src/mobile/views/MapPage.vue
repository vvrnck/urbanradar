<template>
    <main>
        <div class="mappage">
            <Map />
        </div>
    </main>
</template>

<script>
import { Map } from '../components'

export default {
    name: 'MapPage',
    components: { Map },
   
    data() {
        return {
            menu: "Map"
        }
    }
}
</script>

<style scss="lang">
    main {
        min-height: -webkit-fill-available;
    }
    .mappage {
        overflow-y: hidden !important;
        min-height: -webkit-fill-available;
        height: 100vh;
    }
</style>