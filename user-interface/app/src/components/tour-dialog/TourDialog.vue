<template>
    <v-col cols="auto">
        <v-dialog
            v-model="dialog"
            transition="dialog-top-transition"
            max-width="550"
        >
            <v-card>
                <v-toolbar
                    color="teal"
                >
                    <div class="tour-title">{{ $t('system_welcome') }}</div>
                </v-toolbar>
                <v-card-text>
                    <div class="subtitle-1 pa-8">
                        {{ $t('system_welcome_text_1') }} <b>Urban Map</b>, {{ $t('system_welcome_text_2') }} <br><br> 
                        {{ $t('system_welcome_text_3') }} <b>TOUR</b> {{ $t('system_welcome_text_4') }}
                    </div>
                </v-card-text>
                <v-card-actions class="justify-end">
                    <div class="dialog-actions-button">
                        <v-btn
                            color="red"
                            class="button-width"
                            @click="dialog = false"
                        >
                            {{ $t('system_welcome_btn_no') }}
                        </v-btn>
                        <v-btn
                            color="green"
                            class="button-width"
                            @click="startTour()"
                        >
                            {{ $t('system_welcome_btn_yes') }}
                        </v-btn>
                    </div>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-col>
</template>

<script>
import { getCookieByName, setCookie } from '../../utils';

export default {
    name: 'TourDialog',
    data() {
        return {
            dialog: false
        }
    },
    mounted() {
        const cookie = getCookieByName('SHOW_TOUR');
        if (!cookie) {
            this.dialog = true;
        } 
    },
    methods: {
        toggleDialog() {
            this.dialog = !this.dialog;
        },
        startTour() {
            this.toggleDialog();
            setCookie('SHOW_TOUR', true);
            setTimeout(() => {
                this.$tours['tour'].start();
            }, 900);
        },
    }
}
</script>

<style lang="scss">
    .tour-title {
        font-size: 28px !important;
    }

    .dialog-actions-button {
        display: flex;
        gap: 10px;

        .button-width {
            width: 160px;       
        }
    }

    @media (max-width: 768px) {
        .dialog-actions-button {
            display: grid;
            width: 100%;     

            .button-width {
                width: 100%;       
            }
        }

        .tour-title {
            font-size: 22px !important;
        }
    }
</style>