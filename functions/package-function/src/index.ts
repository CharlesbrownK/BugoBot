import { https } from "firebase-functions";
import { initializeApp } from "firebase-admin";
import { schoolMenuApp } from "@school-api/menu";
import { schoolInfoApp } from "@school-api/info";

const firebaseApp = initializeApp();

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
exports.api = https.onRequest(schoolMenuApp(firebaseApp));
exports.code = https.onRequest(schoolInfoApp(firebaseApp));