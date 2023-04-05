<template>
    <div>
        <div v-if="type === 'linear'">
            <v-progress-linear
                indeterminate
                :color="color"
            ></v-progress-linear>
        </div>

        <div :class="page !== 'login' && 'circular'" v-if="type === 'circular'">
            <v-progress-circular
                :size="page !== 'login' ? 30 : 25"
                :width="2"
                :color="color"
                indeterminate
            ></v-progress-circular>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Loading',
    props: ['color', 'type', 'page']
}
</script>

<style lang="scss">

.circular {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    top: 50%;
    background-color: #000;
    opacity: 0.5;
}

</style>