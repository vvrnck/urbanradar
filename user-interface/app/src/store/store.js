import Vue from 'vue';
import Vuex from 'vuex';
import moment from 'moment';

Vue.use(Vuex);

let currentDate = moment().format('yyyy-MM-DD');

const store = new Vuex.Store({
  state: {
    menu: true, 
    filter: true,
    layerOverlay: false,
    map: { layerGroups: [], loading: true }, // features information
    dates: [currentDate, currentDate], 
    sections: [],
    layers: {}, // map layers configuration
    selectedLayers: [],
    initialLayers: {}, // map layers configuration
    availableDates: {},
    snackbar: { open: false, color: '', text: '', timeout: 2500, type: '' },
    legend: false,
    drawDialog: { 
      open: false, 
      layer: null,
      feature: null,
      type: ''
    },
    featureData: {
      layer_id: null,
      tenant_id:  null,
      feature_collection_id: null,
      language: process.env.VUE_APP_DEFAULT_LOCALE,
      fields: [],
      properties: {},
      geometry: null,
      type: null,
      popup: null
    },
    tabs: [],

    mobile: {
      toggle: {
        layers: false,
        dates: false,
        settings: false,
        fullscreen: false,
        caption: false,
        feature: false
      },
      sections: [],
      draw: { type: '', layer: null, feature: null }
    },
    
  },
  mutations: {
    setMap(state, map) {
      state.map = map;
    },
    setMenu(state, menu) {
      state.menu = menu;
    },
    setFilter(state, filter) {
      state.filter = filter;
    },
    setDates(state, dates) {
      state.dates = dates;
    },
    setInitialLayers(state, initialLayers) {
      state.initialLayers = initialLayers;
    },
    setLayers(state, layers) {
      state.layers = layers;
    },
    setSelectedLayers(state, selectedLayers) {
      state.selectedLayers = selectedLayers;
    },
    setAvailableDates(state, availableDates) {
      state.availableDates = availableDates;
    },
    setSnackbar(state, snackbar) {
      state.snackbar = snackbar;
    },
    setLegend(state, legend) {
      state.legend = legend;
    },
    setDrawDialog(state, drawDialog) {
      state.drawDialog = drawDialog;
    },
    setLayerOverlay(state, layerOverlay) {
      state.layerOverlay = layerOverlay;
    },
    setFeatureData(state, featureData) {
      state.featureData = featureData;
    },
    setTabs(state, tabs) {
      state.tabs = tabs;
    },
    setMobile(state, mobile) {
      state.mobile = mobile;
    }
  },
  getters: {
    map: state => state.map,
    menu: state => state.menu,
    filter: state => state.filter,
    dates: state => state.dates,
    layers: state => state.layers,
    selectedLayers: state => state.selectedLayers,
    initialLayers: state => state.initialLayers,
    availableDates: state => state.availableDates,
    snackbar: state => state.snackbar,
    legend: state => state.legend,
    drawDialog: state => state.drawDialog,
    layerOverlay: state => state.layerOverlay,
    featureData: state => state.featureData,
    tabs: state => state.tabs,
    mobile: state => state.mobile,
  },
  actions: {
    updateMap(context, map) {
      context.commit('setMap', map);
    },
    updateMenu(context, menu) {
      context.commit('setMenu', menu);
    },
    updateFilter(context, filter) {
      context.commit('setFilter', filter);
    },
    updateDates(context, dates) {
      context.commit('setDates', dates);
    },
    updateInitialLayers(context, initialLayers) {
      context.commit('setInitialLayers', initialLayers);
    },  
    updateLayers(context, layers) {
      context.commit('setLayers', layers);
    },    
    updateSelectedLayers(context, selectedLayers) {
      context.commit('setSelectedLayers', selectedLayers);
    },    
    updateAvailableDates(context, availableDates) {
      context.commit('setAvailableDates', availableDates);
    },    
    updateSnackbar(context, snackbar) {
      context.commit('setSnackbar', snackbar);
    },
    updateLegend(context, legend) {
      context.commit('setLegend', legend);
    },
    updateDrawDialog(context, drawDialog) {
      context.commit('setDrawDialog', drawDialog);
    },
    updateLayerOverlay(context, layerOverlay) {
      context.commit('setLayerOverlay', layerOverlay);
    },
    updateFeatureData(context, featureData) {
      context.commit('setFeatureData', featureData);
    },
    updateTabs(context, tabs) {
      context.commit('setTabs', tabs);
    },
    updateMobile(context, mobile) {
      context.commit('setMobile', mobile);
    }
  }
});

export default store;