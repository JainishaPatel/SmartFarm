import pickle
import numpy as np
import pandas as pd
import requests
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import re


from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, current_app, flash
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from . import mongo
from .middleware import login_required, roles_required
from flask_dance.contrib.google import google





main = Blueprint('main', __name__)


# ------------------- Load Environment Variables -------------------

# Load environment variables from .env
load_dotenv()

# Get CSV file path from .env
DATA_PATH = os.getenv("PRICES_DATASET_PATH")

# Now you can access keys safely
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")



# ------------------- Load Dataset -------------------
df = pd.read_csv(DATA_PATH)
print(df.columns.tolist()) 


# --- Safe model + encoder loading (from same dir as this file) ---
base_dir = os.path.dirname(__file__) # app/ folder
MODEL_PATH = os.path.join(base_dir, "crop_model.pkl")
ENCODER_PATH = os.path.join(base_dir, "crop_encoder.pkl")

model = None
crop_encoder = None

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(ENCODER_PATH, "rb") as f:
        crop_encoder = pickle.load(f)  # <--- assign to crop_encoder
    print("✅ Model and encoder loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load model/encoder: {e}")
    

# --- Helpers ---
def convert_to_ist(utc_timestamp):
    """Convert a unix timestamp (seconds) to IST formatted time string."""
    try:
        ts = int(utc_timestamp)
        return (datetime.utcfromtimestamp(ts) + timedelta(hours=5, minutes=30)).strftime("%I:%M %p")
    except Exception:
        return None

def get_farming_recommendation(weather):
    try:
        if weather.get("temp") is None:
            return None

        if weather.get("description") and "rain" in weather["description"].lower():
            return "🌧️ Avoid spraying – Rain is expected."
        elif weather["wind"] > 10:
            return "💨 Avoid spraying – High wind speed may cause pesticide drift."
        elif weather["temp"] > 35:
            return "🔥 Avoid spraying – High temperature may cause evaporation loss."
        elif "clear" in weather["description"].lower() and weather["wind"] < 5:
            return "✅ Good time to spray pesticide – Clear sky and low wind."
        elif weather["humidity"] > 85:
            return "⚠️ High humidity detected – Monitor for fungal diseases."
        else:
            return "ℹ️ Weather is moderate – Monitor conditions before spraying."
    except:
        return None
    
# ----------------- Local Marketplace routes -----------------

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
MAX_IMAGE_SIZE = 3 * 1024 * 1024  # 3 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------- Public pages -------------------
@main.route("/")
def index():
    return render_template("index.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        message = request.form.get("message", "").strip()

        # Basic validation
        if not all([name, email, message]):
            return render_template("contact.html", error="All fields are required.", name=name, email=email)

        # Save into MongoDB
        mongo.db.contacts.insert_one({
            "name": name,
            "email": email,
            "message": message,
            "created_at": datetime.utcnow()
        })

        return render_template("contact.html", success="✅ Your message has been sent!", name=name, email=email)

    return render_template("contact.html", 
                           name=session.get("user_name", ""), 
                           email=session.get("user_email", ""))


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

         # --- Basic validation ---
        if not email or not password:
            flash("⚠️ Both email and password are required.", "danger")
            return redirect(url_for("main.login"))

        # --- Fetch user from MongoDB ---
        user = mongo.db.users.find_one({"email": email})
        if not user:
            flash("⚠️ No account found with this email.", "danger")
            return redirect(url_for("main.login"))

        # --- Check password ---
        if not check_password_hash(user["password"], password):
            flash("⚠️ Incorrect password.", "danger")
            return redirect(url_for("main.login"))

        # --- Optional approval check ---
        # if user.get("approved") is False:
        #     flash("⚠️ Your account is not yet approved by admin.", "warning")
        #     return redirect(url_for("main.login"))
        
        # --- Create session ---
        session["user_email"] = user["email"]
        session["user_name"] = user["name"]
        session["user_role"] = user["role"]
        session["logged_in"] = True

        flash(f"✅ Welcome back, {user['name']}!", "success")
        return redirect(url_for("main.index"))

    # GET request
    return render_template("login.html")


@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # --- Get form data ---
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "").strip().lower()

        # --- Basic validation ---
        if not all([name, email, password, role]):
            flash("⚠️ All fields are required.", "danger")
            return redirect(url_for("main.signup"))

        # --- Role validation ---
        if role not in ["farmer", "buyer", "provider"]:
            flash("⚠️ Invalid role selected.", "danger")
            return redirect(url_for("main.signup"))

        # --- Email format validation ---
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            flash("⚠️ Invalid email format.", "danger")
            return redirect(url_for("main.signup"))

        # --- Password strength check ---
        if len(password) < 6:
            flash("⚠️ Password must be at least 6 characters.", "danger")
            return redirect(url_for("main.signup"))
        # Optional: you can add more checks (uppercase, digit, special char) here

        # --- Check if user already exists ---
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("⚠️ Email already registered.", "danger")
            return redirect(url_for("main.signup"))

        # --- Hash the password ---
        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
        

        # --- Default approval: only farmers auto-approved ---
        approved = True

        # --- Insert user into MongoDB ---
        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw,
            "role": role,
            "approved": approved,
            "created_at": datetime.utcnow()
        })

        # --- Automatically log in the user ---
        session["user_email"] = email
        session["user_role"] = role
        session["user_name"] = name
        session["logged_in"] = True

        flash(f"✅ Signup successful! Welcome, {name}", "success")
        return redirect(url_for("main.index"))

    return render_template("signup.html")


@main.route("/signout")
def signout():
    # Clear session or any logout logic here
    session.clear()
    return redirect(url_for("main.index"))

from flask_dance.contrib.google import google


# ------------ Google ----------------
@main.route("/auth/google/callback")
def google_login_callback():
    # Check if the user is authorized
    if not google.authorized:
        return redirect(url_for("google.login"))  # Redirects to Google login

    # Get user info
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        email = user_info.get("email")
        name = user_info.get("name")

        user = mongo.db.users.find_one({"email": email})
        if not user:
            # Temporarily store in session until role is chosen
            session["temp_name"] = name
            session["temp_email"] = email
            return redirect(url_for("main.choose_role")) 

        # If user already exists, proceed normally
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        session["user_role"] = user["role"]
        session["logged_in"] = True 


        flash(f"✅ Welcome back, {name}! Logged in as {user['role']}.", "success")
        return redirect(url_for("main.index"))

    flash("⚠️ Google login failed.", "danger")
    return redirect(url_for("main.login"))


@main.route("/choose-role", methods=["GET", "POST"])
def choose_role():
    if request.method == "POST":
        role = request.form.get("role")
        name = session.get("temp_name")
        email = session.get("temp_email")

        # Insert user into DB with chosen role
        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "role": role,
            "approved": True,
            "created_at": datetime.utcnow()
        })

        # Save session
        session["user_name"] = name
        session["user_email"] = email
        session["user_role"] = role
        session["logged_in"] = True

        # Remove temp
        session.pop("temp_name", None)
        session.pop("temp_email", None)

        flash(f"🎉 Account created successfully! Signed in as {name} ({role}).", "success")
        return redirect(url_for("main.index"))

    return render_template("choose_role.html")


# ------------------- Protected pages (login required) -------------------

# ================== ROUTES ================== #

@main.route("/crop_guide", methods=["GET", "POST"])
@login_required
def crop_guide():
    if request.method == "POST":
        if model is None or crop_encoder is None:
            # inside route, current_app is safe
            current_app.logger.error("Model or encoder not loaded for /predict")
            return render_template(
                "crop_guide.html",
                prediction=None,
                error="Model not available on server."
            )

        try:
            temp_raw = request.form.get("temperature")
            hum_raw = request.form.get("humidity")

            if temp_raw is None or hum_raw is None:
                return render_template(
                    "crop_guide.html",
                    prediction=None,
                    error="Temperature & humidity required."
                )

            temperature = float(temp_raw)
            humidity = float(hum_raw)

            current_app.logger.info(f"Input Data - Temp: {temperature}, Humidity: {humidity}")

            input_data = pd.DataFrame([[temperature, humidity]], columns=["temperature", "humidity"])
            crop_index = model.predict(input_data)[0]
            crop_name = crop_encoder.inverse_transform([crop_index])[0]

            return render_template("crop_guide.html", prediction=crop_name)

        except Exception as e:
            current_app.logger.error(f"Error in prediction: {e}")
            return render_template("crop_guide.html", prediction=None, error=str(e))

    return render_template("crop_guide.html", prediction=None)

#--------------------------------------------------------------------------------------------------------------

@main.route("/get_api_key", methods=["GET"])
@login_required
def get_api_key():
    # exposing API key is risky - confirm this is necessary
    if WEATHER_API_KEY:
        return jsonify({"api_key": WEATHER_API_KEY})
    return jsonify({"error": "API key not found"}), 500


@main.route("/predict_auto", methods=["POST"])
@login_required
def predict_auto():
    if model is None or crop_encoder is None:
        current_app.logger.error("Model or encoder not loaded for /predict_auto")
        return jsonify({"error": "Model not available on server."}), 500

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "JSON body expected"}), 400

        # Try to get latitude & longitude from client
        lat = data.get("lat")
        lon = data.get("lon")
        fertilizer = data.get("fertilizer", 0)  # optional

        if lat is None or lon is None:
            return jsonify({"error": "lat and lon required"}), 400

        # Fetch weather from OpenWeatherMap using server-side API key
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(weather_url, timeout=10)
        res.raise_for_status()
        w = res.json()

        temperature = w["main"]["temp"]
        humidity = w["main"]["humidity"]

        current_app.logger.info(f"Auto Prediction - Temp: {temperature}, Humidity: {humidity}, Fertilizer: {fertilizer}")

        # Prepare input for model (adjust column names to your model)
        input_data = pd.DataFrame([[temperature, humidity]], columns=["temperature", "humidity"])
        crop_index = model.predict(input_data)[0]
        crop_name = crop_encoder.inverse_transform([crop_index])[0]

        return jsonify({
            "prediction": crop_name,
            "temperature": temperature,
            "humidity": humidity
        })

    except Exception as e:
        current_app.logger.error(f"Error in auto prediction: {e}")
        return jsonify({"error": str(e)}), 500
    


@main.route("/weather_input")
@login_required
def weather_input():
    try:
        ip_info = requests.get("https://ipapi.co/json/").json()
        city = ip_info.get("city", "Delhi")
        return redirect(url_for("main.weather", city=city))
    except Exception:
        return redirect(url_for("main.weather", city="Delhi"))

@main.route("/weather_redirect", methods=["GET"])
@login_required
def weather_redirect():
    city = request.args.get("city")
    if city:
        return redirect(url_for("main.weather", city=city))
    return redirect(url_for("main.weather", city="Delhi"))  # fallback




@main.route('/weather/<city>')
@login_required
def weather(city):
    api_key = os.getenv("WEATHER_API_KEY")  # Replace with your OpenWeatherMap API key
    weather_data = {}
    

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            raise Exception("API error")

        weather_data = {
            "city": city,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "wind": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"], # <-- THIS is what powers the icon image!
            "country": data["sys"]["country"],  # Add country
            # Convert sunrise and sunset times to IST
            "sunrise_time": convert_to_ist(data["sys"]["sunrise"]),
            "sunset_time": convert_to_ist(data["sys"]["sunset"]),
            "date": datetime.fromtimestamp(data["dt"]).strftime('%d-%m-%Y'),
            "time": datetime.fromtimestamp(data["dt"]).strftime('%I:%M %p'),
            

        }

        # 💡 Generate smart farming advice
        recommendation = get_farming_recommendation(weather_data)

    except Exception:
        weather_data = {"error": "Unable to fetch weather data"}

    return render_template("weather.html", weather=weather_data, recommendation=recommendation)


@main.route("/api/weather")
@login_required
def get_weather():
    try:
        API_KEY = os.getenv("WEATHER_API_KEY")  # Replace with your actual key

        if not API_KEY:
            return jsonify({"error": "API key not found."}), 500
        
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q=auto:ip"
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": f"Weather API returned status {response.status_code}"}), response.status_code

        return jsonify(response.json())
    except Exception as e:
        print("Weather API error:", e)
        return jsonify({"error": str(e)}), 500

#--------------------------------------------------------------------------------------


@main.route("/schemes")
@login_required
def schemes():  
    # Logic to display government schemes and subsidies
    return render_template("schemes.html")

#--------------------------------------------------------------------------------------

@main.route("/crop_shelter")
def crop_shelter():
    return render_template("crop_shelter.html")

#--------------------------------------------------------------------------------------

@main.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html", response=None)

@main.route('/prompt', methods=['POST'])
@login_required
def prompt():
    prompt = request.form.get("prompt", "")

    template = {
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post('http://127.0.0.1:11434/api/generate', json=template) 
    llm_response = response.json()

    # Ollama puts the text in 'response' key at top level
    bot_answer = llm_response.get("response", "No response from model")

    return render_template("chatbot.html", response=bot_answer)






@main.route("/market_rates", methods=["GET", "POST"])
def market_rates():
    state = district = commodity = None

    # Dropdown lists
    states = sorted(df["STATE"].dropna().unique())
    districts = sorted(df["District Name"].dropna().unique())
    commodities = sorted(df["Commodity"].dropna().unique())

    rates = df.copy()

    if request.method == "POST":
        state = request.form.get("state")
        district = request.form.get("district")
        commodity = request.form.get("commodity")

        # Filtering
        if state:
            rates = rates[rates["STATE"] == state]
        if district:
            rates = rates[rates["District Name"] == district]
        if commodity:
            rates = rates[rates["Commodity"] == commodity]

    return render_template(
        "market_rates.html",
        states=states,
        districts=districts,
        commodities=commodities,
        state=state,
        district=district,
        commodity=commodity,
        rates=rates.to_dict(orient="records")
    )




# ----------------- E-Commerce -----------------

# Main e-commerce page
@main.route('/e_commerce')
@login_required
def e_commerce():
    products = [
        {"name":"Seeds","icon":"fa-seedling","color":"text-success","types":["Wheat","Rice","Maize"]},
        {"name":"Fertilizers","icon":"fa-bottle-water","color":"text-warning","types":["Urea","DAP","NPK"]},
        {"name":"Pesticides","icon":"fa-skull-crossbones","color":"text-dark","types":["Insecticide","Fungicide"]}
    ]
    return render_template('e_commerce.html', products=products)

# Product type page (shows images)
@main.route('/product/<product_name>', methods=['GET'])
@login_required
def product_types(product_name):
    
    # Seed categories
    seed_categories = {
        "Cereals": ["Wheat", "Rice", "Maize", "Barley", "Millet"],
        "Pulses": ["Lentil", "Chickpea", "Green Gram", "Black Gram"],
        "Oilseeds": ["Groundnut", "Mustard", "Soybean", "Sesame"],
        "Vegetables": ["Tomato", "Onion", "Potato", "Brinjal"],
        "Fruits": ["Mango", "Banana", "Papaya", "Guava"]
    }

    if product_name.lower() == "seeds":
        types = seed_categories
    else:
        product_data = {
            "Fertilizers": ["Urea", "DAP", "NPK", "Compost"],
            "Pesticides": ["Herbicide", "Insecticide", "Fungicide"]
        }
        types = {"Other": product_data.get(product_name, [])}

    return render_template(
        "product_types.html",
        product_name=product_name,
        types=types
    )



# Order form submission

@main.route('/order', methods=['POST'])
@login_required
def order_form():
    # Get form data
    product = request.form.get('product')
    subtype = request.form.get('subtype')
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')  # NEW: fetch from form
    address = request.form.get('address')
    quantity = request.form.get('quantity')
    unit = request.form.get('unit')  # make sure unit is sent from form

    # Basic validation
    if not all([product, subtype, name, phone, email, address, quantity, unit]):
        flash("⚠️ Please fill all the fields to place an order.", "danger")
        return redirect(request.referrer or url_for('main.e_commerce'))

    # Convert quantity safely
    try:
        quantity_value = float(quantity)
        if quantity_value <= 0:
            flash("⚠️ Quantity must be greater than 0.", "danger")
            return redirect(request.referrer or url_for('main.e_commerce'))
    except ValueError:
        flash("⚠️ Quantity must be a number.", "danger")
        return redirect(request.referrer or url_for('main.e_commerce'))

    # Prepare order data
    order_data = {
        "user_email": email,  # now taken from form
        "product": product,
        "subtype": subtype,
        "name": name,
        "phone": phone,
        "address": address,
        "quantity": quantity_value,
        "unit": unit,
        "status": "Booked",
        "created_at": datetime.utcnow()
    }

    # Save order to MongoDB with error handling
    try:
        mongo.db.orders.insert_one(order_data)
        flash(f"✅ Your order for {quantity} {unit} of {subtype} ({product}) has been booked successfully!", "success")
    except Exception as e:
        flash("❌ Something went wrong while placing your order. Please try again.", "danger")
        print("Order insert error:", e)

    # Redirect back to the product page
    return redirect(request.referrer or url_for('main.e_commerce'))


# ------------------- Marketplace Page -------------------
@main.route("/farmer_marketplace")
@login_required
def farmer_marketplace():
    """
    Renders the Local Marketplace page.
    Listings will be loaded asynchronously via JS from /api/listings
    """
    return render_template("farmer_marketplace.html")


# ------------------- API for Listings -------------------
@main.route("/api/listings", methods=["GET"])
@login_required
def api_listings():
    """
    Returns JSON list of marketplace listings.
    Optional query parameters:
    - q: search query (crop_name, seller_name, location)
    - location: filter by location
    - seller_email: filter by seller
    - limit: maximum results (default 100)
    """
    try:
        q = request.args.get("q", "").strip().lower()
        location = request.args.get("location", "").strip().lower()
        seller_email = request.args.get("seller_email")
        limit = int(request.args.get("limit", 100))

        query = {}

        # Text search across crop_name, seller_name, location
        if q:
            query["$or"] = [
                {"crop_name": {"$regex": q, "$options": "i"}},
                {"seller_name": {"$regex": q, "$options": "i"}},
                {"location": {"$regex": q, "$options": "i"}}
            ]
        if location:
            query["location"] = {"$regex": location, "$options": "i"}
        if seller_email:
            query["seller_email"] = seller_email

        # Fetch listings from MongoDB
        docs = list(mongo.db.marketplace.find(query).sort("created_at", -1).limit(limit))

        # Convert ObjectId & datetime to JSON-friendly
        for d in docs:
            d["_id"] = str(d["_id"])
            if d.get("created_at"):
                d["created_at"] = d["created_at"].isoformat()

        return jsonify(docs)

    except Exception as e:
        print("API listings error:", e)
        return jsonify({"error": "Server error"}), 500


# ------------------- Add Listing Page -------------------
@main.route("/add_listing", methods=["GET", "POST"])
@login_required
@roles_required("farmer")
def add_listing():
    """
    Farmers can post a listing.
    Handles image upload and inserts document into MongoDB.
    """
    # user_role = session.get("user_role", "")
    # if user_role != "farmer":
    #     flash("Only farmers can post listings.", "danger")
    #     return redirect(url_for("main.farmer_marketplace"))

    if request.method == "POST":
        crop_name = request.form.get("crop_name", "").strip()
        quantity = request.form.get("quantity", "").strip()
        unit = request.form.get("unit", "kg")  # default kg
        price = request.form.get("price", "").strip()
        contact = request.form.get("contact", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()

        # Image upload handling (optional)
        file = request.files.get("image")
        image_url = url_for("static", filename="images/default_crop.jpg")
        if file and file.filename != "":
            from werkzeug.utils import secure_filename
            import os
            filename = secure_filename(file.filename)
            timestamp = int(datetime.utcnow().timestamp())
            saved_name = f"{timestamp}_{filename}"
            upload_dir = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, saved_name))
            image_url = url_for("static", filename=f"uploads/{saved_name}")

        doc = {
            "crop_name": crop_name,
            "quantity": quantity,
            "unit": unit,
            "price": price,
            "contact": contact,
            "location": location,
            "description": description,
            "image_url": image_url,
            "seller_name": session.get("user_name", "Anonymous"),
            "seller_email": session.get("user_email"),
            "created_at": datetime.utcnow()
        }

        mongo.db.marketplace.insert_one(doc)
        flash("Listing added successfully.", "success")
        return redirect(url_for("main.farmer_marketplace"))

    return render_template(
        "add_listing.html",
        seller_name=session.get("user_name", ""),
        seller_contact=session.get("user_email", "")  # prefill contact if stored
    )



# ------------------- My Listings -------------------
@main.route("/my_listings")
@login_required
@roles_required("farmer")
def my_listings():
    """Shows listings posted by current user"""
    user_email = session.get("user_email")
    docs = list(mongo.db.marketplace.find({"seller_email": user_email}).sort("created_at", -1))
    for d in docs:
        d["_id"] = str(d["_id"])
        if d.get("created_at"):
            d["created_at"] = d["created_at"].isoformat()
    return render_template("my_listings.html", listings=docs)


# ------------------- Delete Listing -------------------
@main.route("/delete_listing/<listing_id>", methods=["POST"])
@login_required
@roles_required("farmer")
def delete_listing(listing_id):
    """Delete a listing (only by seller or admin)"""
    try:
        doc = mongo.db.marketplace.find_one({"_id": ObjectId(listing_id)})
        if not doc:
            flash("Listing not found.", "danger")
            return redirect(url_for("main.my_listings"))

        user_email = session.get("user_email")
        user_role = session.get("user_role", "")

        if doc.get("seller_email") != user_email and user_role != "admin":
            flash("Not authorized to delete this listing.", "danger")
            return redirect(url_for("main.my_listings"))

        # Optionally remove image file
        img_url = doc.get("image_url", "")
        try:
            if img_url and img_url.startswith("/static/uploads/"):
                import os
                filename = img_url.split("/static/uploads/")[-1]
                path = os.path.join(current_app.static_folder, "uploads", filename)
                if os.path.exists(path):
                    os.remove(path)
        except Exception as e:
            print("Could not remove image file:", e)

        mongo.db.marketplace.delete_one({"_id": ObjectId(listing_id)})
        flash("Listing deleted successfully.", "success")
        return redirect(url_for("main.my_listings"))

    except Exception as e:
        print("Error deleting listing:", e)
        flash("Error deleting listing.", "danger")
        return redirect(url_for("main.my_listings"))
    





