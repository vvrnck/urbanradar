<template>
    <div class="management-page">
        <Navbar 
            title="management"
            :hasMenu="false"
        />
        <Management />
    </div>
</template>

<script>

import Navbar from '../components/navbar/Navbar.vue';
import Management from '../components/management/Management.vue';

export default {
    name: 'ManagementPage',
    components: { Navbar, Management }
}

</script>

<style lang="scss">
.management-page {
    display: flex;
    height: 100vh;

    @media (max-width: 768px) {
        flex-direction: column;
    }
}
</style>
