<template>
    <div class="feedback">
        
        <v-card outlined shaped class="feedback-card" elevation="5">
            <v-card-title class="headline">
                <div class="text-center card-title">
                    {{ $t('feedback') }}     
                </div>  
            </v-card-title>

            <v-card-text>
                <div class='feedback-header'>
                    <b>{{ $t('user') }}</b>: {{ getUserEmail }} <br />
                    <b>{{ $t('date') }}</b>: {{ getDate }} <br />
                </div>
                <div>
                    <v-text-field
                        v-model="title"
                        name="title"
                        type="text"
                        required
                        :label="`${$t('title')}*`"
                        autocomplete="off"
                    />

                   <v-textarea
                        required
                        name="description"
                        :label="`${$t('description')}*`"
                        no-resize
                        outlined
                        v-model="description"
                        autocomplete="off"
                    />

                    <v-file-input
                        small-chips
                        truncate-length="15"
                        :label="$t('images')"
                        accept="image/*"
                        ref="inputImage"
                        @change="(file) => handleFileUpload(file)"
                        @click:clear="clearFile()"
                    />
                    
                </div>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                 <v-btn
                    color="primary"
                    @click="sendFeedback()"
                    width="110"
                    :disabled="loading"
                >
                    <div v-if="!loading">{{ $t('btn_send_file') }}</div>
                    <v-progress-circular
                        v-if="loading"
                        indeterminate
                        :color="color"
                        size="25"
                        width="3"
                    ></v-progress-circular>
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>    
</template>

<script>
import moment from 'moment';
import { getUserEmail, getApi, getErrors } from '../../utils/index';
import axios from 'axios';
import { isEmpty } from 'lodash';
import Loading from '../loading/Loading.vue';

export default {
    name: 'Feedback',
    components: { Loading },
    data() {
        return {
            title: '',
            description: '',
            filename: '',
            file: null,
            loading: false,
            color: '#FFF',
        }
    },
    methods: {
        checkFields() {
            if (this.title !== '' && this.description !== '') return true;
            return false;
        },
        resetFields() {
            this.title = '';
            this.description = '';
            this.filename = null;
            this.file = null;
        },
        clearFile() {
            this.filename = '';
            this.file = null;
        },
        handleFileUpload(file) {
            if (!file) return;        
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                this.file = reader.result;
                this.filename = file.name;
            };
            reader.onerror = (error) => {
                console.log(error);
                const snackbar = { open: true, color: '', text: 'error_upload_image', timeout: 2500, type: 'error' };
                this.$store.dispatch('updateSnackbar', snackbar);
            };
        },
        sendFeedback() {
            if (this.checkFields()) {
                this.loading = true;

                const headers = { 'Content-Type': 'multipart/form-data' };
                const url = getApi('feedback');
                const payload = {
                    title: this.title,
                    description: this.description,
                    filename: this.filename,
                    file: this.file
                };

                axios.post(url, payload)
                    .then(response => {

                        const { data, errors } = response.data;

                        if (!isEmpty(errors)) {
                            this.loading = false;
                            return getErrors(errors);
                        }

                        this.resetFields();
                        this.loading = false;
                        const snackbar = { open: true, color: '', text: 'success_send_feedback', timeout: 2500, type: 'success' };
                        this.$store.dispatch('updateSnackbar', snackbar);
                    })
                    .catch(error => {
                        this.loading = false;
                        const snackbar = { open: true, color: '', text: 'error_send_feedback', timeout: 2500, type: 'error' };
                        this.$store.dispatch('updateSnackbar', snackbar);
                    });
            } else {
                const snackbar = { open: true, color: '', text: 'warning_fill_fields', timeout: 2500, type: 'warning' };
                this.$store.dispatch('updateSnackbar', snackbar);
            }
        },
    },    
    computed: {
        getUserEmail() {
            return getUserEmail();
        },
        getDate() {
            const format = this.$i18n.locale === 'en' ? 'MM/DD/YYYY' : 'DD/MM/YYYY'
            return moment().format(format);
        }
    }
}
</script>

<style lang="scss">
.feedback {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;

    .feedback-card {
        min-width: 500px;
        padding: 10px;

        .card-title {
            width: 100%;
        }
    }
}
</style>