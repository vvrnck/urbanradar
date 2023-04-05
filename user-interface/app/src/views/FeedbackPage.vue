<template>
    <div class="feedback-page">
        <Navbar 
            title="Feedback"
            :hasMenu="false"
        />
        <Feedback />
    </div>
</template>

<script>

import Feedback from '../components/feedback/Feedback.vue';
import Navbar from '../components/navbar/Navbar.vue';

export default {
    name: 'FeedbackPage',
    components: { Feedback, Navbar }
}

</script>

<style lang="scss">
.feedback-page {
    display: flex;
    height: 100vh;

    @media (max-width: 768px) {
        flex-direction: column;
    }
}
</style>
