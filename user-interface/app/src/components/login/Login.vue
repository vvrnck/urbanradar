<template>
    <div class="login-page">
        <v-flex d-flex justify-center align-center class="login-form-wrapper">
            <div class="login-form">
                <v-form>
                    <div class="form-header">
                        <img src="../../assets/images/logo.svg" alt="CrimeRadar" />
                        <Loading color="#52FFEE" v-if="loading" type="linear" />
                    </div>
                    <div class="form-body">
                        <div class="form-fields">
                            <div v-for="input in inputs" :key="input.name">
                                <v-text-field
                                    v-model="input.value"
                                    :name="input.name"
                                    :type="input.type"
                                    :color="input.color"
                                    :counter="input.counter"
                                    :rules="input.rules"
                                    :required="input.required"
                                    :label="`${$t(input.label)}`"
                                    :append-icon="input.appendIcon.hasIcon ? input.appendIcon.iconOn : input.appendIcon.iconOff"
                                    @click:append="() => {
                                        input.appendIcon.hasIcon = !input.appendIcon.hasIcon;
                                        input.type = input.type === 'text' ? 'password' : 'text';
                                    }"
                                    @keydown.13="input.name === 'password' && login()"
                                    autocomplete="off"
                                >
                                </v-text-field>
                            </div>
                        </div>
                        <div class="form-actions">
                            <div class="form-actions-links">
                                <div @click="forgotPassword()">
                                    {{ $t('forgot_password') }}
                                </div>
                            </div>
                            <v-btn block @click="login()" :disabled="loading">
                                <div v-if="loading">
                                    <Loading color="#FFF" v-if="loading" type="circular" />
                                </div>
                                <div v-if="!loading">
                                    {{ $t('btn_login') }}
                                </div>
                            </v-btn>
                        </div>
                    </div>
                    <div class="form-footer">
                        <div class="system-version">
                            {{ getVersion }}
                        </div>
                    </div>
                </v-form>
            </div>
        </v-flex>
        <div class="change-language">
            <div v-for="(language, index) in languages" :key="language.type">
                <div class="language">
                    <div class="language-item" @click="changeLanguage(language.language)">{{ language.label }}</div>
                    <div v-if="index === 0" class="bullet">&#9679;</div>
                </div> 
                
            </div>
        </div>
    </div>
</template>
<script src="./index.js"></script>

<style lang="scss">
    @import "./login.scss";
</style>