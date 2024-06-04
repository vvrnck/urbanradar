import axios from 'axios';
import { isEmpty } from 'lodash';
import store from '../store/store';
import router from '../routes/router';
import firebase from 'firebase/app';
import i18n from '../i18n/i18n';
import 'firebase/auth';

export const getApi = (endpoint, params = {}) => {
  const URL = process.env.VUE_APP_API_URL_PRD;
  const ENV = process.env.VUE_APP_NODE_ENV; 

  let url = `${URL}/${endpoint}`;

  if (!isEmpty(params)) {
    Object.keys(params).map((param, i) => {
      const value = params[param];
      if (i == 0) url += `?${param}=${value}`
      else url += `&${param}=${value}`;
    })
  }
  
  if (ENV !== 'production') console.info('%cRequesting: ' + url, "color: #000; font-style: italic; background-color: #643b9f; padding: 2px");

  return url;
}

export const getOrigin = () => process.env.VUE_APP_ORIGIN;

export const isMobile = () => {
  const agent = window.navigator.userAgent;
  const mobiles = /(Android|webOS|iPhone|iPad|iPod|BlackBerry|Windows Phone)/i;
  if (agent.match(mobiles)) return true;
  return false;
};

export const getSelectedLayers = () => {	
  const currentStoreLayers = store.getters.layers;
  
  const menu = Object.assign([], currentStoreLayers);

  const selectedLayers = [];

  menu.map(section => {
      section.layers.map(layer => {
          if (layer.selected) selectedLayers.push(layer);
      })
  });

  return selectedLayers;
};

export const getUser = () => {
  const user = JSON.parse(sessionStorage.getItem('user'));
  return user;
}

export const getUserEmail = () => {
  const  user = JSON.parse(sessionStorage.getItem('user'));
  return user.email || '';
}

export const getUserScopes = () => {
  	let user = JSON.parse(sessionStorage.getItem('user'));
  	let newScopes = [];
  	user.scope && user.scope.map(scope => newScopes.push(scope));
  	return newScopes;
}

export const getBucketURL = () => {
  return process.env.VUE_APP_AWS_BUCKET_URL;
}

export const getMapCoords = () => {
  return [-8, -38];
}

export const getGeojson = () => {
  return ['pernambuco'];
}

export const getMapZoom = () => {
  return 6.5;
}

export const getMapTileLayer = () => {
    return [
      {
          name: 'DARK',
          label: i18n.locale === 'en' ? 'Dark' : 'Escuro',
          visible: true,
          url: 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png?api_key=39637672-75ae-4744-80c2-5d63301f5b3f',
          options: { maxZoom: 18, attribution: 'Stadia' }
      },
      {
          name: 'ROADMAP',
          label: i18n.locale === 'en' ? 'Detailed' : 'Detalhado',
          visible: true,
          url: 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
          options: { maxZoom: 18, attribution: 'Google Maps',  subdomains: ['mt0','mt1','mt2','mt3'], }
      },
    ]  
}

export const setCookie = (name, value, days = 30) => {
  // create/set cookie
  const maxAge = (days*24*60*60);
  document.cookie = `${name}=${value || ""};Max-Age=${maxAge};path=/`;
}

export const getCookieByName = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

export const clearUserSession = () => {
  localStorage.clear();
  sessionStorage.clear();
}

export const getErrors = (errors) => {
  const { code, error_code, message } = errors[0];
  console.error(`
    code: ${code}
    error_code: ${error_code}
    message: ${message}
  `);
  const snackbar = { open: true, color: '', text: message, timeout: 2500, type: 'error' };
  store.dispatch('updateSnackbar', snackbar);

  if (code === 498) {
    refreshToken();
  }
}

export const refreshToken = async () => {
  try {
    let url = getApi(`auth/token`);

    if (!sessionStorage.getItem('user') || !JSON.parse(sessionStorage.getItem('user')).email) return router.push("/");

    const refreshToken = await firebase.auth().currentUser.getIdToken(true);

    const bodyData = {
      email: JSON.parse(sessionStorage.getItem('user')).email,
      access_token: refreshToken,
      tenant_id: process.env.VUE_APP_TENANT
    };

    axios.post(url, bodyData).then(response => {
        store.dispatch('updateSnackbar', { open: true, color: '', text: 'auth', timeout: 2500, type: 'warning' });
        const { data, errors } = response.data;

        if (!isEmpty(errors)) {
          return getErrors(errors);
        }

        const { active, tenants, email, token } = data;

        axios.defaults.headers.common['Authorization'] = token.access_token;

        const canLogin = tenants.find(tenant => tenant == process.env.VUE_APP_TENANT);
        if (!canLogin) {
            return store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_user_without_permission', timeout: 2500, type: 'error' });
        }

        if (active) {
          let loginURL = getApi(`auth/tenant/${process.env.VUE_APP_TENANT}/token`);
          
          axios.post(loginURL).then(response => {
              store.dispatch('updateSnackbar', { open: true, color: '', text: 'success_auth', timeout: 2500, type: 'success' });
              const { data : { email, name, roles, token: { scope, access_token, feature_collections, tenant_id } } } = response.data;
              localStorage.setItem('crimeradarToken', access_token);
              sessionStorage.setItem('featureCollections', JSON.stringify(feature_collections));
              sessionStorage.setItem('tenantId', tenant_id);
              sessionStorage.setItem('user', JSON.stringify({ name, roles, scope, tenants, email }));          
              router.go({ name: 'map' }).catch(err => console.log(err));
          }).catch(err => {
              console.log(err);
              return store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_api', timeout: 2500, type: 'error' });
          });
        }   
      });
  } catch (err) {
    console.error(err);
    router.push("/").catch(err => console.error(err));
  }
  
}

export const getDefaultColorScales = () => {
	return [
		["hsl(240, 100%, 50%)", "hsl(180, 100%, 50%)", "hsl(120, 100%, 50%)", "hsl(60, 100%, 50%)", "hsl(0, 100%, 50%)"],
		["hsl(9, 62%, 49%)", "hsl(91, 59%, 62%)", "hsl(283, 23%, 40%)", "hsl(42, 89%, 67%)", "hsl(193, 87%, 35%)"],
	]
}

export const getDefaultLayerStyles = () => {
  	return {
    	
       		colorScale: {
            point: { 
              key1: { color: "hsl(9, 62%, 49%)", fillColor: "hsl(255, 0%, 0%)", opacity: 0.6, fillOpacity: 0.6, radius: 3, stroke: false },
              key2: { color: "hsl(9, 62%, 49%)", fillColor: "hsl(255, 0%, 0%)", opacity: 0.6, fillOpacity: 0.6, radius: 3, stroke: false } 
            }, 
            polygon: ["hsl(240, 100%, 50%)", "hsl(180, 100%, 50%)", "hsl(120, 100%, 50%)", "hsl(60, 100%, 50%)", "hsl(0, 100%, 50%)"],
          },
       		color: "#FFFFFF",
       		types: [
          		{
                name: "scale",
                value: true,
                icon: "mdi-format-color-fill",
                label: "scale",
              },
              {
                name: "hexagon",
                value: false,
                icon: "mdi-hexagon",
                label: "hexagon"
              },
              {
                name: "icon",
                value: false,
                icon: "mdi-star-circle",
                label: "icon"
              },
              {
                name: "marker",
                value: false,
                icon: "mdi-map-marker",
                label: "marker"
              },
                    {
                name: "point",
                value: false,
                icon: "mdi-brightness-1",
                label: "point"
              }
       		],
       		texture:{
          		value:"NONE",
          		options:[
					"NONE",
					"HORIZONTAL",
					"VERTICAL"
				]
       		}
		
    }
}


export const getLabel = (item, language) => {
  if (item.label && item.label[language]) return item.label[language];
  return item.name || '--';
}

export const updateMobileItem = (item, value) => {
  const mobile = store.getters.mobile;

  Object.keys(mobile.toggle).map(key => {
    if (key === item) {
      mobile.toggle[key] = value;
    }
  });

  store.dispatch('updateMobile', mobile);
}

export const getGradientPattern = (layer, colorFillPallete, type) => {
  let fillPalette = [colorFillPallete, "#FFFFFF"];
  if (type === "HORIZONTAL") {
    return `
        <linearGradient id="layer-${layer.id}-stripes-${colorFillPallete}" x1="0" y1="0" x2="0" y2="1">
          <stop offset=0 stop-color=${fillPalette[0]} />
          <stop offset=20% stop-color=${fillPalette[1]} />
          <stop offset=20% stop-color=${fillPalette[0]} />
          <stop offset=40% stop-color=${fillPalette[1]} />
          <stop offset=40% stop-color=${fillPalette[0]} />
          <stop offset=60% stop-color=${fillPalette[1]} />
          <stop offset=60% stop-color=${fillPalette[0]} />
          <stop offset=80% stop-color=${fillPalette[1]} />
          <stop offset=80% stop-color=${fillPalette[0]} />                                                
          <stop offset=100% stop-color=${fillPalette[1]} />
          <stop offset=100% stop-color=${fillPalette[0]} />
        </linearGradient>
    `
  }

  if (type === "VERTICAL") {
    return `<linearGradient id="layer-${layer.id}-stripes-${colorFillPallete}" x1="0" y1="0" x2="1" y2="0">
              <stop offset=0 stop-color=${fillPalette[0]} />
              <stop offset=20% stop-color=${fillPalette[1]} />
              <stop offset=20% stop-color=${fillPalette[0]} />
              <stop offset=40% stop-color=${fillPalette[1]} />
              <stop offset=40% stop-color=${fillPalette[0]} />
              <stop offset=60% stop-color=${fillPalette[1]} />
              <stop offset=60% stop-color=${fillPalette[0]} />
              <stop offset=80% stop-color=${fillPalette[1]} />
              <stop offset=80% stop-color=${fillPalette[0]} />                                                
              <stop offset=100% stop-color=${fillPalette[1]} />
              <stop offset=100% stop-color=${fillPalette[0]} />
            </linearGradient>`
  }

  return "";
}


export const getDefaultSvg = () => {
  // number of requests = feature times
  // fetch(require("../assets/icons/boilerplate.svg"))
  //   .then(response => response.text())
  //   .then(data => {
  //     return data
  //   });
  
  // THIS WAY THE BROWSER DOES NOT REQUEST THE IMAGE BY FEATURE
  return `<svg 
	version="1.0" xmlns="http://www.w3.org/2000/svg"
    width="[width]" height="[height]" viewBox="0 0 301 350"
    preserveAspectRatio="xMidYMid meet"
>
    <metadata>
        written by Rodrigo Werneck 2020-2021
    </metadata>

    <g 
        transform="translate(0.000000,350.000000) scale(0.100000,-0.100000)"
        fill="[color]" stroke="none" 
        opacity="[opacity]"
    >
        <path 
            d="M733 3058 l-732 -423 0 -885 0 -885 734 -424 c404 -233 735 -428 735
                -432 0 -14 42 -10 54 5 10 12 1435 839 1470 852 15 6 16 78 16 883 l0 877 -32
		        16 c-18 9 -352 201 -743 427 -505 293 -719 411 -740 411 -21 0 -241 -122 -762
                -422z m1387 -578 c0 -7 -212 -10 -615 -10 -403 0 -615 3 -615 10 0 7 212 10
               615 10 403 0 615 -3 615 -10z m12 -59 c14 -7 34 -28 44 -46 17 -31 17 -64 5
              -600 -13 -613 -12 -605 -68 -642 -25 -17 -70 -18 -608 -18 -538 0 -583 1 -608
              18 -56 37 -55 29 -68 642 -12 539 -12 569 5 600 19 34 48 51 101 58 17 3 287
              4 600 3 461 -1 575 -4 597 -15z m-1352 -656 c0 -390 -3 -595 -10 -595 -7 0
              -10 205 -10 595 0 390 3 595 10 595 7 0 10 -205 10 -595z m1480 0 c0 -522 -2
              -595 -15 -595 -13 0 -15 73 -15 595 0 522 2 595 15 595 13 0 15 -73 15 -595z"
        />
        <path d="M940 2341 c-15 -4 -32 -21 -42 -41 -16 -30 -18 -66 -18 -276 0 -132
              -5 -301 -12 -375 -7 -73 -12 -200 -12 -281 -1 -136 1 -149 20 -168 20 -21 26
              -21 625 -21 332 0 612 3 621 6 32 13 41 70 34 225 -3 80 -10 192 -16 250 -5
              58 -9 218 -10 355 0 218 -2 255 -18 285 -10 20 -27 37 -42 41 -33 9 -1097 9
              -1130 0z m671 -109 c22 -18 22 -23 20 -188 -3 -212 -14 -302 -45 -364 -29 -58
              -27 -120 4 -120 10 0 20 5 22 12 3 7 9 8 18 3 19 -12 6 -243 -15 -265 -12 -11
              -39 -15 -110 -15 -71 0 -98 4 -110 15 -21 22 -34 253 -15 265 9 5 15 4 18 -3
              2 -7 12 -12 22 -12 31 0 33 62 4 120 -31 62 -42 152 -45 364 -3 208 -4 206
              126 206 66 0 88 -4 106 -18z"
        />
        <path d="M1443 2224 c-34 -8 -44 -28 -37 -72 8 -54 17 -66 40 -55 21 10 100 9
              126 -2 17 -7 22 2 33 66 5 25 2 39 -9 48 -16 13 -115 23 -153 15z"
        />
        <path d="M1399 1534 c-9 -12 -1 -133 10 -135 27 -4 185 -3 191 1 14 9 22 128
                9 136 -20 12 -200 10 -210 -2z"
        />
    </g>
</svg>`
}

export const getImageToDisplay = (imageString, color, opacity = 0.7, width = 350, height = 350) => { 
    return new Promise((resolve, reject) => {
      imageString.then(res => {
        let processedImage = !res ? null : res.slice(0);

        if (!processedImage) processedImage = getDefaultSvg();
        
        processedImage = processedImage.replace("[width]", width);
        processedImage = processedImage.replace("[height]", height);
        processedImage = processedImage.replace("[color]", color);
        processedImage = processedImage.replace("[opacity]", opacity);
        
        resolve(processedImage);
      })
    });
}