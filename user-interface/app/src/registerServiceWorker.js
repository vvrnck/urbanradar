import { Workbox } from "workbox-window";

let wb = null;
 
if (process.env.VUE_APP_NODE_ENV === "production") {
  if ("serviceWorker" in navigator) {
    wb = new Workbox(`${process.env.VUE_APP_BASE_URL}service-worker.js`);
  
    wb.addEventListener("controlling", () => {
      window.location.reload();
    });
  
    wb.register();
  }
}

export default wb;