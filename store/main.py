import pyrebase


firebaseConfig = {
    'apiKey' :"AIzaSyAgFw9yzFstVUQJPjVoaz9XoKSOytKPJRY",
    'authDomain': "webstoreproject-426ce.firebaseapp.com",
    'projectId': "webstoreproject-426ce",
    'storageBucket': "webstoreproject-426ce.appspot.com",
    'messagingSenderId': "61217059091",
    'appId': "1:61217059091:web:09d10060c569f9ed25eae6",
    'measurementId': "G-PWTXWHKR29"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

#firebase.analytics();
#Login
email= input("Enter your email")
password = input("Enter your email")
auth.sign_in_with_email_and_password(email, password)
