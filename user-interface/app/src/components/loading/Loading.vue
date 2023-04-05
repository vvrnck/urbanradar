<template>
    <div>
        <div v-if="type === 'linear'">
            <v-progress-linear
                indeterminate
                :color="color"
            ></v-progress-linear>
        </div>

        <div v-if="type === 'circular'">
            <v-progress-circular
                :size="20"
                :width="3"
                :color="color"
                indeterminate
            ></v-progress-circular>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Loading',
    props: ['color', 'type']
}
</script>