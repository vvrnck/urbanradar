(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["node_vendors~app~1fb195ae"],{"7d28":function(t,e,n){"use strict";var r,i=n("cc84"),o=n("ffa6"),a=n("9ab4"),s=n("a8e9"),u=n("9dbb"),c="@firebase/installations",l="0.4.32",f=1e4,d="w:"+l,h="FIS_v2",p="https://firebaseinstallations.googleapis.com/v1",v=36e5,g="installations",b="Installations",m=(r={},r["missing-app-config-values"]='Missing App configuration value: "{$valueName}"',r["not-registered"]="Firebase Installation is not registered.",r["installation-not-found"]="Firebase Installation not found.",r["request-failed"]='{$requestName} request failed with error "{$serverCode} {$serverStatus}: {$serverMessage}"',r["app-offline"]="Could not process request. Application offline.",r["delete-pending-registration"]="Can't delete installation while there is a pending registration request.",r),y=new s["b"](g,b,m);function O(t){return t instanceof s["c"]&&t.code.includes("request-failed")}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function I(t){var e=t.projectId;return p+"/projects/"+e+"/installations"}function w(t){return{token:t.token,requestStatus:2,expiresIn:L(t.expiresIn),creationTime:Date.now()}}function j(t,e){return Object(a["b"])(this,void 0,void 0,(function(){var n,r;return Object(a["d"])(this,(function(i){switch(i.label){case 0:return[4,e.json()];case 1:return n=i.sent(),r=n.error,[2,y.create("request-failed",{requestName:t,serverCode:r.code,serverMessage:r.message,serverStatus:r.status})]}}))}))}function S(t){var e=t.apiKey;return new Headers({"Content-Type":"application/json",Accept:"application/json","x-goog-api-key":e})}function C(t,e){var n=e.refreshToken,r=S(t);return r.append("Authorization",T(n)),r}function E(t){return Object(a["b"])(this,void 0,void 0,(function(){var e;return Object(a["d"])(this,(function(n){switch(n.label){case 0:return[4,t()];case 1:return e=n.sent(),e.status>=500&&e.status<600?[2,t()]:[2,e]}}))}))}function L(t){return Number(t.replace("s","000"))}function T(t){return h+" "+t}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function k(t,e){var n=e.fid;return Object(a["b"])(this,void 0,void 0,(function(){var e,r,i,o,s,u,c;return Object(a["d"])(this,(function(a){switch(a.label){case 0:return e=I(t),r=S(t),i={fid:n,authVersion:h,appId:t.appId,sdkVersion:d},o={method:"POST",headers:r,body:JSON.stringify(i)},[4,E((function(){return fetch(e,o)}))];case 1:return s=a.sent(),s.ok?[4,s.json()]:[3,3];case 2:return u=a.sent(),c={fid:u.fid||n,registrationStatus:2,refreshToken:u.refreshToken,authToken:w(u.authToken)},[2,c];case 3:return[4,j("Create Installation",s)];case 4:throw a.sent()}}))}))}
/**
 * @license
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function R(t){return new Promise((function(e){setTimeout(e,t)}))}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function N(t){var e=btoa(String.fromCharCode.apply(String,Object(a["f"])([],Object(a["e"])(t))));return e.replace(/\+/g,"-").replace(/\//g,"_")}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var P=/^[cdef][\w-]{21}$/,_="";function A(){try{var t=new Uint8Array(17),e=self.crypto||self.msCrypto;e.getRandomValues(t),t[0]=112+t[0]%16;var n=D(t);return P.test(n)?n:_}catch(r){return _}}function D(t){var e=N(t);return e.substr(0,22)}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function z(t){return t.appName+"!"+t.appId}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var H=new Map;function q(t,e){var n=z(t);B(n,e),F(n,e)}function M(t,e){U();var n=z(t),r=H.get(n);r||(r=new Set,H.set(n,r)),r.add(e)}function x(t,e){var n=z(t),r=H.get(n);r&&(r.delete(e),0===r.size&&H.delete(n),G())}function B(t,e){var n,r,i=H.get(t);if(i)try{for(var o=Object(a["g"])(i),s=o.next();!s.done;s=o.next()){var u=s.value;u(e)}}catch(c){n={error:c}}finally{try{s&&!s.done&&(r=o.return)&&r.call(o)}finally{if(n)throw n.error}}}function F(t,e){var n=U();n&&n.postMessage({key:t,fid:e}),G()}var V=null;function U(){return!V&&"BroadcastChannel"in self&&(V=new BroadcastChannel("[Firebase] FID Change"),V.onmessage=function(t){B(t.data.key,t.data.fid)}),V}function G(){0===H.size&&V&&(V.close(),V=null)}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var W="firebase-installations-database",$=1,J="firebase-installations-store",K=null;function X(){return K||(K=Object(u["openDb"])(W,$,(function(t){switch(t.oldVersion){case 0:t.createObjectStore(J)}}))),K}function Y(t,e){return Object(a["b"])(this,void 0,void 0,(function(){var n,r,i,o,s;return Object(a["d"])(this,(function(a){switch(a.label){case 0:return n=z(t),[4,X()];case 1:return r=a.sent(),i=r.transaction(J,"readwrite"),o=i.objectStore(J),[4,o.get(n)];case 2:return s=a.sent(),[4,o.put(e,n)];case 3:return a.sent(),[4,i.complete];case 4:return a.sent(),s&&s.fid===e.fid||q(t,e.fid),[2,e]}}))}))}function Z(t){return Object(a["b"])(this,void 0,void 0,(function(){var e,n,r;return Object(a["d"])(this,(function(i){switch(i.label){case 0:return e=z(t),[4,X()];case 1:return n=i.sent(),r=n.transaction(J,"readwrite"),[4,r.objectStore(J).delete(e)];case 2:return i.sent(),[4,r.complete];case 3:return i.sent(),[2]}}))}))}function Q(t,e){return Object(a["b"])(this,void 0,void 0,(function(){var n,r,i,o,s,u;return Object(a["d"])(this,(function(a){switch(a.label){case 0:return n=z(t),[4,X()];case 1:return r=a.sent(),i=r.transaction(J,"readwrite"),o=i.objectStore(J),[4,o.get(n)];case 2:return s=a.sent(),u=e(s),void 0!==u?[3,4]:[4,o.delete(n)];case 3:return a.sent(),[3,6];case 4:return[4,o.put(u,n)];case 5:a.sent(),a.label=6;case 6:return[4,i.complete];case 7:return a.sent(),!u||s&&s.fid===u.fid||q(t,u.fid),[2,u]}}))}))}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function tt(t){return Object(a["b"])(this,void 0,void 0,(function(){var e,n,r;return Object(a["d"])(this,(function(i){switch(i.label){case 0:return[4,Q(t,(function(n){var r=et(n),i=nt(t,r);return e=i.registrationPromise,i.installationEntry}))];case 1:return n=i.sent(),n.fid!==_?[3,3]:(r={},[4,e]);case 2:return[2,(r.installationEntry=i.sent(),r)];case 3:return[2,{installationEntry:n,registrationPromise:e}]}}))}))}function et(t){var e=t||{fid:A(),registrationStatus:0};return at(e)}function nt(t,e){if(0===e.registrationStatus){if(!navigator.onLine){var n=Promise.reject(y.create("app-offline"));return{installationEntry:e,registrationPromise:n}}var r={fid:e.fid,registrationStatus:1,registrationTime:Date.now()},i=rt(t,r);return{installationEntry:r,registrationPromise:i}}return 1===e.registrationStatus?{installationEntry:e,registrationPromise:it(t)}:{installationEntry:e}}function rt(t,e){return Object(a["b"])(this,void 0,void 0,(function(){var n,r;return Object(a["d"])(this,(function(i){switch(i.label){case 0:return i.trys.push([0,2,,7]),[4,k(t,e)];case 1:return n=i.sent(),[2,Y(t,n)];case 2:return r=i.sent(),O(r)&&409===r.customData.serverCode?[4,Z(t)]:[3,4];case 3:return i.sent(),[3,6];case 4:return[4,Y(t,{fid:e.fid,registrationStatus:0})];case 5:i.sent(),i.label=6;case 6:throw r;case 7:return[2]}}))}))}function it(t){return Object(a["b"])(this,void 0,void 0,(function(){var e,n,r,i;return Object(a["d"])(this,(function(o){switch(o.label){case 0:return[4,ot(t)];case 1:e=o.sent(),o.label=2;case 2:return 1!==e.registrationStatus?[3,5]:[4,R(100)];case 3:return o.sent(),[4,ot(t)];case 4:return e=o.sent(),[3,2];case 5:return 0!==e.registrationStatus?[3,7]:[4,tt(t)];case 6:return n=o.sent(),r=n.installationEntry,i=n.registrationPromise,i?[2,i]:[2,r];case 7:return[2,e]}}))}))}function ot(t){return Q(t,(function(t){if(!t)throw y.create("installation-not-found");return at(t)}))}function at(t){return st(t)?{fid:t.fid,registrationStatus:0}:t}function st(t){return 1===t.registrationStatus&&t.registrationTime+f<Date.now()}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function ut(t,e){var n=t.appConfig,r=t.platformLoggerProvider;return Object(a["b"])(this,void 0,void 0,(function(){var t,i,o,s,u,c,l,f;return Object(a["d"])(this,(function(a){switch(a.label){case 0:return t=ct(n,e),i=C(n,e),o=r.getImmediate({optional:!0}),o&&i.append("x-firebase-client",o.getPlatformInfoString()),s={installation:{sdkVersion:d}},u={method:"POST",headers:i,body:JSON.stringify(s)},[4,E((function(){return fetch(t,u)}))];case 1:return c=a.sent(),c.ok?[4,c.json()]:[3,3];case 2:return l=a.sent(),f=w(l),[2,f];case 3:return[4,j("Generate Auth Token",c)];case 4:throw a.sent()}}))}))}function ct(t,e){var n=e.fid;return I(t)+"/"+n+"/authTokens:generate"}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function lt(t,e){return void 0===e&&(e=!1),Object(a["b"])(this,void 0,void 0,(function(){var n,r,i,o;return Object(a["d"])(this,(function(a){switch(a.label){case 0:return[4,Q(t.appConfig,(function(r){if(!pt(r))throw y.create("not-registered");var i=r.authToken;if(!e&&vt(i))return r;if(1===i.requestStatus)return n=ft(t,e),r;if(!navigator.onLine)throw y.create("app-offline");var o=bt(r);return n=ht(t,o),o}))];case 1:return r=a.sent(),n?[4,n]:[3,3];case 2:return o=a.sent(),[3,4];case 3:o=r.authToken,a.label=4;case 4:return i=o,[2,i]}}))}))}function ft(t,e){return Object(a["b"])(this,void 0,void 0,(function(){var n,r;return Object(a["d"])(this,(function(i){switch(i.label){case 0:return[4,dt(t.appConfig)];case 1:n=i.sent(),i.label=2;case 2:return 1!==n.authToken.requestStatus?[3,5]:[4,R(100)];case 3:return i.sent(),[4,dt(t.appConfig)];case 4:return n=i.sent(),[3,2];case 5:return r=n.authToken,0===r.requestStatus?[2,lt(t,e)]:[2,r]}}))}))}function dt(t){return Q(t,(function(t){if(!pt(t))throw y.create("not-registered");var e=t.authToken;return mt(e)?Object(a["a"])(Object(a["a"])({},t),{authToken:{requestStatus:0}}):t}))}function ht(t,e){return Object(a["b"])(this,void 0,void 0,(function(){var n,r,i;return Object(a["d"])(this,(function(o){switch(o.label){case 0:return o.trys.push([0,3,,8]),[4,ut(t,e)];case 1:return n=o.sent(),i=Object(a["a"])(Object(a["a"])({},e),{authToken:n}),[4,Y(t.appConfig,i)];case 2:return o.sent(),[2,n];case 3:return r=o.sent(),!O(r)||401!==r.customData.serverCode&&404!==r.customData.serverCode?[3,5]:[4,Z(t.appConfig)];case 4:return o.sent(),[3,7];case 5:return i=Object(a["a"])(Object(a["a"])({},e),{authToken:{requestStatus:0}}),[4,Y(t.appConfig,i)];case 6:o.sent(),o.label=7;case 7:throw r;case 8:return[2]}}))}))}function pt(t){return void 0!==t&&2===t.registrationStatus}function vt(t){return 2===t.requestStatus&&!gt(t)}function gt(t){var e=Date.now();return e<t.creationTime||t.creationTime+t.expiresIn<e+v}function bt(t){var e={requestStatus:1,requestTime:Date.now()};return Object(a["a"])(Object(a["a"])({},t),{authToken:e})}function mt(t){return 1===t.requestStatus&&t.requestTime+f<Date.now()}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function yt(t){return Object(a["b"])(this,void 0,void 0,(function(){var e,n,r;return Object(a["d"])(this,(function(i){switch(i.label){case 0:return[4,tt(t.appConfig)];case 1:return e=i.sent(),n=e.installationEntry,r=e.registrationPromise,r?r.catch(console.error):lt(t).catch(console.error),[2,n.fid]}}))}))}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Ot(t,e){return void 0===e&&(e=!1),Object(a["b"])(this,void 0,void 0,(function(){var n;return Object(a["d"])(this,(function(r){switch(r.label){case 0:return[4,It(t.appConfig)];case 1:return r.sent(),[4,lt(t,e)];case 2:return n=r.sent(),[2,n.token]}}))}))}function It(t){return Object(a["b"])(this,void 0,void 0,(function(){var e;return Object(a["d"])(this,(function(n){switch(n.label){case 0:return[4,tt(t)];case 1:return e=n.sent().registrationPromise,e?[4,e]:[3,3];case 2:n.sent(),n.label=3;case 3:return[2]}}))}))}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function wt(t,e){return Object(a["b"])(this,void 0,void 0,(function(){var n,r,i,o;return Object(a["d"])(this,(function(a){switch(a.label){case 0:return n=jt(t,e),r=C(t,e),i={method:"DELETE",headers:r},[4,E((function(){return fetch(n,i)}))];case 1:return o=a.sent(),o.ok?[3,3]:[4,j("Delete Installation",o)];case 2:throw a.sent();case 3:return[2]}}))}))}function jt(t,e){var n=e.fid;return I(t)+"/"+n}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function St(t){return Object(a["b"])(this,void 0,void 0,(function(){var e,n;return Object(a["d"])(this,(function(r){switch(r.label){case 0:return e=t.appConfig,[4,Q(e,(function(t){if(!t||0!==t.registrationStatus)return t}))];case 1:if(n=r.sent(),!n)return[3,6];if(1!==n.registrationStatus)return[3,2];throw y.create("delete-pending-registration");case 2:if(2!==n.registrationStatus)return[3,6];if(navigator.onLine)return[3,3];throw y.create("app-offline");case 3:return[4,wt(e,n)];case 4:return r.sent(),[4,Z(e)];case 5:r.sent(),r.label=6;case 6:return[2]}}))}))}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Ct(t,e){var n=t.appConfig;return M(n,e),function(){x(n,e)}}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Et(t){var e,n;if(!t||!t.options)throw Lt("App Configuration");if(!t.name)throw Lt("App Name");var r=["projectId","apiKey","appId"];try{for(var i=Object(a["g"])(r),o=i.next();!o.done;o=i.next()){var s=o.value;if(!t.options[s])throw Lt(s)}}catch(u){e={error:u}}finally{try{o&&!o.done&&(n=i.return)&&n.call(i)}finally{if(e)throw e.error}}return{appName:t.name,projectId:t.options.projectId,apiKey:t.options.apiKey,appId:t.options.appId}}function Lt(t){return y.create("missing-app-config-values",{valueName:t})}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function Tt(t){var e="installations";t.INTERNAL.registerComponent(new o["a"](e,(function(t){var e=t.getProvider("app").getImmediate(),n=Et(e),r=t.getProvider("platform-logger"),i={appConfig:n,platformLoggerProvider:r},o={app:e,getId:function(){return yt(i)},getToken:function(t){return Ot(i,t)},delete:function(){return St(i)},onIdChange:function(t){return Ct(i,t)}};return o}),"PUBLIC")),t.registerVersion(c,l)}Tt(i["a"])},abfd:function(t,e,n){"use strict";
/*! *****************************************************************************
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
MERCHANTABLITY OR NON-INFRINGEMENT.

See the Apache Version 2.0 License for specific language governing permissions
and limitations under the License.
***************************************************************************** */
function r(){for(var t=0,e=0,n=arguments.length;e<n;e++)t+=arguments[e].length;var r=Array(t),i=0;for(e=0;e<n;e++)for(var o=arguments[e],a=0,s=o.length;a<s;a++,i++)r[i]=o[a];return r}
/**
 * @license
 * Copyright 2017 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var i;n.d(e,"a",(function(){return f})),n.d(e,"b",(function(){return d})),n.d(e,"c",(function(){return h}));var o,a=[];(function(t){t[t["DEBUG"]=0]="DEBUG",t[t["VERBOSE"]=1]="VERBOSE",t[t["INFO"]=2]="INFO",t[t["WARN"]=3]="WARN",t[t["ERROR"]=4]="ERROR",t[t["SILENT"]=5]="SILENT"})(o||(o={}));var s={debug:o.DEBUG,verbose:o.VERBOSE,info:o.INFO,warn:o.WARN,error:o.ERROR,silent:o.SILENT},u=o.INFO,c=(i={},i[o.DEBUG]="log",i[o.VERBOSE]="log",i[o.INFO]="info",i[o.WARN]="warn",i[o.ERROR]="error",i),l=function(t,e){for(var n=[],i=2;i<arguments.length;i++)n[i-2]=arguments[i];if(!(e<t.logLevel)){var o=(new Date).toISOString(),a=c[e];if(!a)throw new Error("Attempted to log a message with an invalid logType (value: "+e+")");console[a].apply(console,r(["["+o+"]  "+t.name+":"],n))}},f=function(){function t(t){this.name=t,this._logLevel=u,this._logHandler=l,this._userLogHandler=null,a.push(this)}return Object.defineProperty(t.prototype,"logLevel",{get:function(){return this._logLevel},set:function(t){if(!(t in o))throw new TypeError('Invalid value "'+t+'" assigned to `logLevel`');this._logLevel=t},enumerable:!1,configurable:!0}),t.prototype.setLogLevel=function(t){this._logLevel="string"===typeof t?s[t]:t},Object.defineProperty(t.prototype,"logHandler",{get:function(){return this._logHandler},set:function(t){if("function"!==typeof t)throw new TypeError("Value assigned to `logHandler` must be a function");this._logHandler=t},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"userLogHandler",{get:function(){return this._userLogHandler},set:function(t){this._userLogHandler=t},enumerable:!1,configurable:!0}),t.prototype.debug=function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];this._userLogHandler&&this._userLogHandler.apply(this,r([this,o.DEBUG],t)),this._logHandler.apply(this,r([this,o.DEBUG],t))},t.prototype.log=function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];this._userLogHandler&&this._userLogHandler.apply(this,r([this,o.VERBOSE],t)),this._logHandler.apply(this,r([this,o.VERBOSE],t))},t.prototype.info=function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];this._userLogHandler&&this._userLogHandler.apply(this,r([this,o.INFO],t)),this._logHandler.apply(this,r([this,o.INFO],t))},t.prototype.warn=function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];this._userLogHandler&&this._userLogHandler.apply(this,r([this,o.WARN],t)),this._logHandler.apply(this,r([this,o.WARN],t))},t.prototype.error=function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];this._userLogHandler&&this._userLogHandler.apply(this,r([this,o.ERROR],t)),this._logHandler.apply(this,r([this,o.ERROR],t))},t}();function d(t){a.forEach((function(e){e.setLogLevel(t)}))}function h(t,e){for(var n=function(n){var r=null;e&&e.level&&(r=s[e.level]),n.userLogHandler=null===t?null:function(e,n){for(var i=[],a=2;a<arguments.length;a++)i[a-2]=arguments[a];var s=i.map((function(t){if(null==t)return null;if("string"===typeof t)return t;if("number"===typeof t||"boolean"===typeof t)return t.toString();if(t instanceof Error)return t.message;try{return JSON.stringify(t)}catch(e){return null}})).filter((function(t){return t})).join(" ");n>=(null!==r&&void 0!==r?r:e.logLevel)&&t({level:o[n].toLowerCase(),message:s,args:i,type:e.name})}},r=0,i=a;r<i.length;r++){var u=i[r];n(u)}}},ffa6:function(t,e,n){"use strict";n.d(e,"a",(function(){return o})),n.d(e,"b",(function(){return l}));var r=n("9ab4"),i=n("a8e9"),o=function(){function t(t,e,n){this.name=t,this.instanceFactory=e,this.type=n,this.multipleInstances=!1,this.serviceProps={},this.instantiationMode="LAZY",this.onInstanceCreated=null}return t.prototype.setInstantiationMode=function(t){return this.instantiationMode=t,this},t.prototype.setMultipleInstances=function(t){return this.multipleInstances=t,this},t.prototype.setServiceProps=function(t){return this.serviceProps=t,this},t.prototype.setInstanceCreatedCallback=function(t){return this.onInstanceCreated=t,this},t}(),a="[DEFAULT]",s=function(){function t(t,e){this.name=t,this.container=e,this.component=null,this.instances=new Map,this.instancesDeferred=new Map,this.instancesOptions=new Map,this.onInitCallbacks=new Map}return t.prototype.get=function(t){var e=this.normalizeInstanceIdentifier(t);if(!this.instancesDeferred.has(e)){var n=new i["a"];if(this.instancesDeferred.set(e,n),this.isInitialized(e)||this.shouldAutoInitialize())try{var r=this.getOrInitializeService({instanceIdentifier:e});r&&n.resolve(r)}catch(o){}}return this.instancesDeferred.get(e).promise},t.prototype.getImmediate=function(t){var e,n=this.normalizeInstanceIdentifier(null===t||void 0===t?void 0:t.identifier),r=null!==(e=null===t||void 0===t?void 0:t.optional)&&void 0!==e&&e;if(!this.isInitialized(n)&&!this.shouldAutoInitialize()){if(r)return null;throw Error("Service "+this.name+" is not available")}try{return this.getOrInitializeService({instanceIdentifier:n})}catch(i){if(r)return null;throw i}},t.prototype.getComponent=function(){return this.component},t.prototype.setComponent=function(t){var e,n;if(t.name!==this.name)throw Error("Mismatching Component "+t.name+" for Provider "+this.name+".");if(this.component)throw Error("Component for "+this.name+" has already been provided");if(this.component=t,this.shouldAutoInitialize()){if(c(t))try{this.getOrInitializeService({instanceIdentifier:a})}catch(h){}try{for(var i=Object(r["g"])(this.instancesDeferred.entries()),o=i.next();!o.done;o=i.next()){var s=Object(r["e"])(o.value,2),u=s[0],l=s[1],f=this.normalizeInstanceIdentifier(u);try{var d=this.getOrInitializeService({instanceIdentifier:f});l.resolve(d)}catch(h){}}}catch(p){e={error:p}}finally{try{o&&!o.done&&(n=i.return)&&n.call(i)}finally{if(e)throw e.error}}}},t.prototype.clearInstance=function(t){void 0===t&&(t=a),this.instancesDeferred.delete(t),this.instancesOptions.delete(t),this.instances.delete(t)},t.prototype.delete=function(){return Object(r["b"])(this,void 0,void 0,(function(){var t;return Object(r["d"])(this,(function(e){switch(e.label){case 0:return t=Array.from(this.instances.values()),[4,Promise.all(Object(r["f"])(Object(r["f"])([],Object(r["e"])(t.filter((function(t){return"INTERNAL"in t})).map((function(t){return t.INTERNAL.delete()})))),Object(r["e"])(t.filter((function(t){return"_delete"in t})).map((function(t){return t._delete()})))))];case 1:return e.sent(),[2]}}))}))},t.prototype.isComponentSet=function(){return null!=this.component},t.prototype.isInitialized=function(t){return void 0===t&&(t=a),this.instances.has(t)},t.prototype.getOptions=function(t){return void 0===t&&(t=a),this.instancesOptions.get(t)||{}},t.prototype.initialize=function(t){var e,n;void 0===t&&(t={});var i=t.options,o=void 0===i?{}:i,a=this.normalizeInstanceIdentifier(t.instanceIdentifier);if(this.isInitialized(a))throw Error(this.name+"("+a+") has already been initialized");if(!this.isComponentSet())throw Error("Component "+this.name+" has not been registered yet");var s=this.getOrInitializeService({instanceIdentifier:a,options:o});try{for(var u=Object(r["g"])(this.instancesDeferred.entries()),c=u.next();!c.done;c=u.next()){var l=Object(r["e"])(c.value,2),f=l[0],d=l[1],h=this.normalizeInstanceIdentifier(f);a===h&&d.resolve(s)}}catch(p){e={error:p}}finally{try{c&&!c.done&&(n=u.return)&&n.call(u)}finally{if(e)throw e.error}}return s},t.prototype.onInit=function(t,e){var n,r=this.normalizeInstanceIdentifier(e),i=null!==(n=this.onInitCallbacks.get(r))&&void 0!==n?n:new Set;i.add(t),this.onInitCallbacks.set(r,i);var o=this.instances.get(r);return o&&t(o,r),function(){i.delete(t)}},t.prototype.invokeOnInitCallbacks=function(t,e){var n,i,o=this.onInitCallbacks.get(e);if(o)try{for(var a=Object(r["g"])(o),s=a.next();!s.done;s=a.next()){var u=s.value;try{u(t,e)}catch(c){}}}catch(l){n={error:l}}finally{try{s&&!s.done&&(i=a.return)&&i.call(a)}finally{if(n)throw n.error}}},t.prototype.getOrInitializeService=function(t){var e=t.instanceIdentifier,n=t.options,r=void 0===n?{}:n,i=this.instances.get(e);if(!i&&this.component&&(i=this.component.instanceFactory(this.container,{instanceIdentifier:u(e),options:r}),this.instances.set(e,i),this.instancesOptions.set(e,r),this.invokeOnInitCallbacks(i,e),this.component.onInstanceCreated))try{this.component.onInstanceCreated(this.container,e,i)}catch(o){}return i||null},t.prototype.normalizeInstanceIdentifier=function(t){return void 0===t&&(t=a),this.component?this.component.multipleInstances?t:a:t},t.prototype.shouldAutoInitialize=function(){return!!this.component&&"EXPLICIT"!==this.component.instantiationMode},t}();function u(t){return t===a?void 0:t}function c(t){return"EAGER"===t.instantiationMode}
/**
 * @license
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var l=function(){function t(t){this.name=t,this.providers=new Map}return t.prototype.addComponent=function(t){var e=this.getProvider(t.name);if(e.isComponentSet())throw new Error("Component "+t.name+" has already been registered with "+this.name);e.setComponent(t)},t.prototype.addOrOverwriteComponent=function(t){var e=this.getProvider(t.name);e.isComponentSet()&&this.providers.delete(t.name),this.addComponent(t)},t.prototype.getProvider=function(t){if(this.providers.has(t))return this.providers.get(t);var e=new s(t,this);return this.providers.set(t,e),e},t.prototype.getProviders=function(){return Array.from(this.providers.values())},t}()}}]);