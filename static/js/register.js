// استيراد Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

// إعداد Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDgwzqb8KWYCjMXlkTRJbhIZnWLIz_BVF0",
    authDomain: "lastnewapp.firebaseapp.com",
    projectId: "lastnewapp",
    storageBucket: "lastnewapp.firebasestorage.app",
    messagingSenderId: "793438014459",
    appId: "1:793438014459:web:5969fe74a895f9f2dd195e",
    measurementId: "G-X1WCJV12KZ"
};

// تهيئة Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Telegram WebApp API
const tg = window.Telegram.WebApp;
tg.ready();

const user = tg.initDataUnsafe?.user;

if (user) {
    const userId = user.id;
    const username = user.username || user.first_name || 'Unknown';

    async function saveUserToFirebase() {
        const userRef = doc(db, "users", userId.toString());
        const userSnap = await getDoc(userRef);

        if (!userSnap.exists()) {
            // إضافة المستخدم إذا لم يكن موجودًا
            await setDoc(userRef, {
                user_id: userId,
                username: username,
                points: 0  // نقاط افتراضية
            });
        }

        // جلب البيانات المحدثة من Firestore
        const updatedUserSnap = await getDoc(userRef);
        const userData = updatedUserSnap.data();

        // تحديث الصفحة
        document.getElementById('user-id').innerText = userData.user_id;
        document.getElementById('username').innerText = userData.username;
        document.getElementById('points').innerText = userData.points;
    }

    saveUserToFirebase().catch(error => console.error('Error:', error));
}
