// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDRIKRL_IWoaXHv12qmXr7-rXjVqu31724",
  authDomain: "movie-recommendation-5250b.firebaseapp.com",
  projectId: "movie-recommendation-5250b",
  storageBucket: "movie-recommendation-5250b.appspot.com",
  messagingSenderId: "592544454475",
  appId: "1:592544454475:web:aede05accb9e1ac6e1face",
  measurementId: "G-30VS8LVG8Z"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Login form handling
const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Login successful
      // Redirect user to home page or perform other actions
      console.log('Logged in successfully!');
    })
    .catch((error) => {
      const errorMessage = document.querySelector('.error-message');
      errorMessage.textContent = error.message;
    });
});

// Signup form handling (similar logic to login)
const signupForm = document.getElementById('signup-form');
signupForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signup successful
      // Redirect user to login page or perform other actions
      console.log('Signed up successfully!');
    })
    .catch((error) => {
      const errorMessage = document.querySelector('.error-message');
      errorMessage.textContent = error.message;
    });
});
