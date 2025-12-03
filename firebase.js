import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyBMS6k351FEmsu7Lu3kF4tcRXLbgPecDLM",
  authDomain: "travel-agent-85a83.firebaseapp.com",
  projectId: "travel-agent-85a83",
  storageBucket: "travel-agent-85a83.firebasestorage.app",
  messagingSenderId: "35843876350",
  appId: "1:35843876350:web:cd19fca52fe7460a2a0caf",
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
export default firebaseApp;