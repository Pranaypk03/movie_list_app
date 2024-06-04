from flask import Flask, render_template, request, redirect, url_for, \
    session  # Import session for storing search results (optional)
from firebase_admin import auth, db
import requests  # For OMDb API requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hgvdsfvsavfuy'  # Replace with a strong secret key

# Firebase Admin SDK initialization (replace with your credentials)
cred = credentials.Certificate('path/to/serviceAccountKey.json')  # Replace with your Firebase service account key path
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-name.firebaseio.com/'  # Replace with your Firebase project database URL
})
# Get auth and database references
auth_ref = auth.Client()
db_ref = db.reference()


# Helper functions for authentication
def is_logged_in():
    # Implement logic to check if a user is logged in using Firebase Authentication
    # You can access the current user with auth_ref.current_user
    # This function should return True if a user is logged in, False otherwise
    return auth_ref.current_user is not None


def get_current_user_id():
    # Implement logic to get the current user's ID
    # You can access the current user with auth_ref.current_user
    # This function should return the current user's ID as a string
    current_user = auth_ref.current_user
    return current_user.uid if current_user else None


# Routes for authentication, search, and list management
@app.route('/')
def home():
    # Check login status and redirect if needed
    if not is_logged_in():
        return redirect(url_for('login'))

    # Get user's watchlist/favorites from Firebase Realtime Database
    user_id = get_current_user_id()
    watchlist_movies = db_ref.child('users').child(user_id).child('watchlist').get().val() or []

    return render_template('index.html', watchlist_movies=watchlist_movies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Attempt user sign in with Firebase Authentication
            user = auth_ref.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))  # Redirect to home after successful login
        except ValueError as e:
            error_message = str(e)  # Handle potential value errors

        return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Attempt user creation with Firebase Authentication
            user = auth_ref.create_user_with_email_and_password(email, password)
            return redirect(url_for('login'))  # Redirect to login after successful signup

        except ValueError as e:
            error_message = str(e)  # Handle potential value errors

        return render_template('signup.html', error_message=error_message)
    else:
        return render_template('signup.html')


@app.route('/search', methods=['POST'])
def search_movies():
    if request.method == 'POST':
        search_term = request.form['search_term']

        # Use OMDb API to search for movies
        api_key = '1a49dc47'
        url = f'http://www.omdbapi.com/?s={search_term}&apikey={"AIzaSyDRIKRL_IWoaXHv12qmXr7-rXjVqu31724"}'
        response = requests.get(' http://www.omdbapi.com/?i=tt3896198&apikey=1a49dc47')
        search_results = response.json().get('Search', [])  # Handle potential API errors

        # Optional: Store search results in session for one request
        session['search_results'] = search_results

        return render_template('search_results.html', search_results=search_results)

