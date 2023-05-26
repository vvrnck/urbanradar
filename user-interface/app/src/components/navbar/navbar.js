import { isEmpty } from 'lodash';
import { clearUserSession, getUser, getBucketURL, getUserScopes, getLabel, isMobile } from '../../utils';
import LayerMenu from '../layer-menu/LayerMenu';

export default {
    name: 'Navbar',
    props: ['hasMenu', 'title'],
    components: { LayerMenu },
    data() {
        return {
            drawer: false,
            isMobile: true,
            items: [
                { icon: "mdi-map", name: "map", label: "Map", scopes: ["map.view"], route: "map" },
                { icon: "mdi-account-multiple", name: "management", label: "Management", scopes: ["management.view"], route: "management" },      
                { icon: "mdi-cog", name: "admin", label: "Admin", scopes: ["administration.view"], route: "admin" },    
            ],   
            options: [
                { icon: "mdi-home", label: "Users", scopes: [""] },
                { icon: "mdi-home", label: "Feedbacks List", scopes: [""] },
                { icon: "mdi-home", label: "Exit", scopes: [""] }
            ],
            languages: [
                { icon: '', name: 'English', label: '', language: 'en' },
                { icon: '', name: 'Português', label: '', language: 'pt' }
            ],
            layerOptions: {
                show: false,
                sectionName: null,
                options: []
            },
            availableDates: null,
            selectedItem: 0,
            mini: true
        }
    },
    created() {
        window.addEventListener("resize", this.resizeWindow);
    },
    destroyed() {
        window.removeEventListener("resize", this.resizeWindow);
    },
    mounted() {
        this.resizeWindow();    

        // if (!isMobile()) {
        //     document.querySelector('.map-wrapper').style.marginTop = '56px';
        // }
    },
    methods: {
        goToPage(item) {
            this.$router.push(item.route).catch(err => console.warn(err));
        },
        getLabel(item, language) {
            return getLabel(item, language);
        },
        hasScopes(scopes) {
            if (isEmpty(scopes)) return true;

            let hasScopes = false;
            this.getUserScopes().map(scope => {
                if (scopes.includes(scope)) hasScopes = true;
            })
            return hasScopes;
        },
        getUserScopes() {
            return getUserScopes();
        },
        startTour() {
            this.$tours['tour'].start();
        },
        resetMapConfigs() {
            this.reset().then(() => {
                const initialMenuData = JSON.parse(localStorage.getItem('initialMenuData'));
                this.$store.dispatch('updateMenu', initialMenuData);
                this.layerOptions = {
                    show: false,
                    sectionName: null,
                    options: []
                }
            });
        }, 
        getFeatures() {
            const { loadFeatures } = window._mapFunctions;
            loadFeatures().then(() => {
                this.drawer = false;
                this.$store.dispatch('updateLegend', true);
            });
        },
        closeDrawer() {
            this.drawer = false;
        },  
        openLayerOptions(menuItem) {
            this.layerOptions = {
                show: true,
                name: getLabel(menuItem, this.$i18n.locale),
                options: menuItem.layers
            };
        },
        closeLayerOptions() {
            this.layerOptions.show = false;
            this.selectedItem = 0;
        },
        getUser () {
            return getUser();
        },
        changeTheme() {
            this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
        
            // change search theme                
            document.documentElement.style.setProperty('--darkcolor', `${!this.$vuetify.theme.isDark ? '#FFF' : '#2e322f'}`);
            document.documentElement.style.setProperty('--whitecolor', `${this.$vuetify.theme.isDark ? '#FFF' : '#2e322f'}`);
        },
        changeLanguage(language) {
            this.$i18n.locale = language;
            const layerControl = document.getElementsByClassName('leaflet-control-layers-selector');
            for (let i = 0;i < layerControl.length; i++) {
                let mapTitle = layerControl[i].nextSibling;
                const newName = this.getLayerControlNames(mapTitle.innerHTML.trim());
                mapTitle.innerHTML = newName;
            }
        },
        getLayerControlNames(mapTitle) {
            if (['Detailed','Detalhado'].includes(mapTitle)) return this.$i18n.locale === 'en' ? ' Detailed' : ' Detalhado';
            else if (['Dark','Escuro'].includes(mapTitle)) return this.$i18n.locale === 'en' ? ' Dark' : ' Escuro';
        },
        logout() {
            clearUserSession();
            this.$router.push('/login').catch(err => console.warn(err));
        },
        resizeWindow() {
            if (window.innerWidth <= 768) this.isMobile = true;
            else this.isMobile = false;
        }
    },
    computed: {
        menuItems() {
            return this.$store.getters.menu;
        },
        sectionItems() {
            return this.$store.getters.layers;
        }
    },
    
};