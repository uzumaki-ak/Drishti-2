// // TODO: Replace with actual Firebase implementation
// // This is a stub for future Firebase integration

// export interface FirebaseConfig {
//   apiKey: string
//   authDomain: string
//   databaseURL: string
//   projectId: string
//   storageBucket: string
//   messagingSenderId: string
//   appId: string
// }

// // TODO: Initialize Firebase with your actual configuration
// export const initializeFirebase = (config: FirebaseConfig) => {
//   console.log("Firebase would be initialized here with config:", config)
//   // import { initializeApp } from 'firebase/app'
//   // import { getAuth } from 'firebase/auth'
//   // import { getDatabase } from 'firebase/database'
//   //
//   // const app = initializeApp(config)
//   // export const auth = getAuth(app)
//   // export const database = getDatabase(app)
// }

// // TODO: Implement authentication functions
// export const signIn = async (email: string, password: string) => {
//   console.log("Sign in would be implemented here")
//   // Actual implementation would use Firebase Auth
// }

// export const signOut = async () => {
//   console.log("Sign out would be implemented here")
//   // Actual implementation would use Firebase Auth
// }

// // TODO: Implement real-time data functions
// export const subscribeToIncidents = (callback: (incidents: any[]) => void) => {
//   console.log("Real-time incident subscription would be implemented here")
//   // Actual implementation would use Firebase Realtime Database
// }

// export const subscribeToUnits = (callback: (units: any[]) => void) => {
//   console.log("Real-time unit subscription would be implemented here")
//   // Actual implementation would use Firebase Realtime Database
// }


// import { initializeApp } from "firebase/app"
// import { getFirestore } from "firebase/firestore"
// import { getStorage } from "firebase/storage"

// const firebaseConfig = {
//   apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
//   authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
//   projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
//   storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
//   messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
//   appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
// }

// // Initialize Firebase
// const app = initializeApp(firebaseConfig)

// // Initialize Firebase services
// export const db = getFirestore(app)
// export const storage = getStorage(app)

// export default app



// firebase


import { initializeApp } from "firebase/app"
import { getFirestore } from "firebase/firestore"
import { getStorage } from "firebase/storage"

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
}

const app = initializeApp(firebaseConfig)

export const db = getFirestore(app)
export const storage = getStorage(app)
export default app
