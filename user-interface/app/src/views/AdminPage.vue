<template>
    <div class="admin-page">
        <Navbar 
            title="admin"
            :hasMenu="false"
        />
        <Admin />
    </div>
</template>

<script>


import Navbar from '../components/navbar/Navbar.vue';

export default {
    name: 'AdminPage',
    components: { 
        Admin: () => import('../components/admin/Admin.vue'), 
        Navbar 
    },
}

</script>

<style lang="scss">
.admin-page {
    display: flex;
    height: 100vh;

    @media (max-width: 768px) {
        flex-direction: column;
    }
}
</style>
