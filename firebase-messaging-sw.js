importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-messaging-compat.js');

// Ваша конфигурация Firebase
const firebaseConfig = {
    apiKey: "AIzaSyD3wSSNQIbK5c-umYpELfgTys8OrtQSZIQ",
    authDomain: "manfaad-10112.firebaseapp.com",
    projectId: "manfaad-10112",
    storageBucket: "manfaad-10112.appspot.com",
    messagingSenderId: "535978628150",
    appId: "1:535978628150:web:3b6c4a513ca5fdd900f497",
    measurementId: "G-08R26LF4Z9"
  };

// Инициализация Firebase в Service Worker
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Обработка фоновых сообщений (background notifications)
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);

    // Настройки уведомления
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/firebase-logo.png'  // Иконка уведомления (можете указать свою)
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
