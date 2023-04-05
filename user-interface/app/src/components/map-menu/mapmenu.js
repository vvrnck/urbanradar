import L from 'leaflet';
import { getApi, getErrors, getSelectedLayers } from '../../utils';
import moment from 'moment';
import axios from 'axios';
import DatePicker from '../date-picker/DatePicker.vue';
import Layers from '../layers/Layers.vue';
import { isEmpty, sortBy } from 'lodash';

export default {
    name: 'MapMenu',
    props: ['loadFeatures', 'clearMapData', 'removeLayer'],
    components: { DatePicker, Layers },
    data() {
        return {
            loading: true,
            initialMenuData: {}
        }
    },
    mounted() {        
        this.loading = true;

        // menu grab activation
        const mapMenu = document.getElementById('map-menu');
        const draggable = new L.Draggable(mapMenu);
        draggable.enable();

        // menu grabbing style
        const mapMenuController = document.getElementsByClassName('map-menu-controller')[0];
        
        mapMenuController.addEventListener('mousedown', () => {
            mapMenuController.style.cursor = 'grabbing';
        });
        
        mapMenuController.addEventListener('mouseup', () => {
            mapMenuController.style.cursor = 'grab';
        });


        let url_layers = getApi('layer');
        this.updateLoading(true);
        axios.get(url_layers).then(response => {
            
            const { data, errors } = response.data;
            
            if (!isEmpty(errors)) {
                this.updateLoading(false);
                return getErrors(errors);
            }
            
            const newData = Object.assign([], data);
            
            const initialData = Object.assign([], newData);
            this.$store.dispatch('updateInitialLayers', initialData);            

            localStorage.setItem('menu', JSON.stringify(newData));
            this.$store.dispatch('updateLayers', newData);

            this.loading = false;
            this.updateLoading(false);
        }).catch(error => {
            console.error(error);
            const snackbar = { open: true, color: '', text: 'error_get_layers', timeout: 2500, type: 'error' };
            this.$store.dispatch('updateSnackbar', snackbar);
            this.loading = false;
            this.updateLoading(false);
        });
    },
    methods: {
        updateLoading(value) {
            const map = this.$store.getters.map;
            this.$store.dispatch('updateMap', { ...map, loading: value });
        },
        clearMenu() {
            this.clearMapData().then(() => {
                const newData = JSON.parse(localStorage.getItem('menu'));
                this.$store.dispatch('updateLayers', newData);
                let currentDate = moment().format('yyyy-MM-DD');
                this.$store.dispatch('updateDates', [currentDate, currentDate]);this.$store.dispatch('updateDates', [currentDate, currentDate]);
            });
            const snackbar = { open: true, color: '', text: 'reset_menu', timeout: 2500, type: 'success' };
            this.$store.dispatch('updateSnackbar', snackbar);
        },
        toggleMenu() {
            let menuStatus = this.getMapMenuStatus;
            this.$store.dispatch('updateMenu', !menuStatus);
        },
        toggleLayerOverlay() {
            let layerOverlay = this.$store.getters.layerOverlay;
            this.$store.dispatch('updateLayerOverlay', !layerOverlay);
        },
        getSelectedLayers() {
            return getSelectedLayers();
        }
    },
    computed: {
        getMapMenuStatus() {
            return this.$store.getters.menu;
        }
    }
}