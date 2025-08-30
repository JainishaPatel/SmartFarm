from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import pickle
import numpy as np
import requests
from datetime import datetime, timedelta
from flask import session
import os
from dotenv import load_dotenv

main = Blueprint('main', __name__)


# Load environment variables from .env
load_dotenv()

# Now you can access keys safely
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Load model and encoders
model = pickle.load(open('./app/crop_model.pkl', 'rb'))
season_encoder = pickle.load(open('./app/season_encoder.pkl', 'rb'))
state_encoder = pickle.load(open('./app/state_encoder.pkl', 'rb'))
crop_encoder = pickle.load(open('./app/crop_encoder.pkl', 'rb'))

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/signup")
def signup():
    return render_template("signup.html")

@main.route("/signout")
def signout():
    # Clear session or any logout logic here
    session.clear()
    return render_template("signout.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/contact")
def contact():  
    return render_template("contact.html")

@main.route("/crop_shelter")
def crop_shelter():
    return render_template("crop_shelter.html")

@main.route("/machine_rentals")
def machine_rentals():
    machines = [
        {
            "name": "Tractor",
            "description": "Available hourly/daily. Delivery to field possible.",
            "image": "assets/tractor.jpg"
        },
        {
            "name": "Harvester",
            "description": "Ideal for wheat & paddy. Operator included.",
            "image": "assets/harvester.jpg"
        },
        {
            "name": "Pesticide Sprayer",
            "description": "Battery-operated. Book with trained operator.",
            "image": "assets/sprayer.jpg"
        },
        {
            "name": "Power Tiller",
            "description": "Compact tilling tool for small/mid farms.",
            "image": "assets/tiller.jpg"
        },
        {
            "name": "Seed Drill",
            "description": "Plant seeds efficiently with minimal labor.",
            "image": "assets/seeder.jpg"
        },
        {
            "name": "Water Pump",
            "description": "Diesel/electric pump sets for irrigation.",
            "image": "assets/water_pump.jpg"
        }
    ]
    return render_template("machine_rentals.html", machines=machines)

@main.route("/market_rates")
def market_rates():
    return render_template("market_rates.html")

@main.route("/soli_analysis")
def soil_analysis():
    return render_template("soil_analysis.html")


# Dummy in-memory product store
market_items = [
    {
        "name": "Organic Wheat",
        "description": "High-quality organic wheat, 1kg pack.",
        "price": 55,
        "image_url": "/static/images/wheat.jpg",
        "seller": {
            "name": "Ravi Patel",
            "email": "ravi.patel@example.com",
            "phone": "+91-9876543210",
            "location": "Gujarat, India"
        }
    },
    {
        "name": "Hybrid Tomato Seeds",
        "description": "Premium quality seeds for high yield.",
        "price": 120,
        "image_url": "/static/images/tomato_seeds.jpg",
        "seller": {
            "name": "Sunita Sharma",
            "email": "sunita.sharma@example.com",
            "phone": "+91-9123456780",
            "location": "Maharashtra, India"
        }
    }
]

@main.route('/market-place', methods=['GET'])
def market_place():
    return render_template("market_place.html", items=market_items)

@main.route('/sell-product', methods=['POST'])
def sell_product():
    # Grab form data
    product = {
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "price": float(request.form.get('price')),
        "image_url": request.form.get('image_url') or "/static/images/default.jpg",
        "seller": {
            "name": request.form.get('seller_name'),
            "email": request.form.get('seller_email'),
            "phone": request.form.get('seller_phone'),
            "location": request.form.get('seller_location')
        }
    }

    # Add to global list
    market_items.append(product)
    return redirect(url_for('main.market_place'))

@main.route('/store')
def store():
    store_items = [
        {
            "name": "Urea Fertilizer",
            "description": "Effective nitrogen fertilizer for crops.",
            "price": 300,
            "image_url": "/static/images/urea.jpg"
        },
        {
            "name": "Pesticide Kit",
            "description": "Protect your crops from pests with this combo.",
            "price": 850,
            "image_url": "/static/images/pesticide.jpg"
        },
        {
            "name": "Hybrid Corn Seeds",
            "description": "High-yield hybrid corn seeds, 1kg pack.",
            "price": 150,
            "image_url": "/static/images/corn_seeds.jpg"
        }
    ]
    return render_template("store.html", store_items=store_items)

@main.route("/post_product", methods=["POST"])
def post_product():
    # Logic to handle product posting
    return render_template("market_place.html")

@main.route("/login_option")
def login_option():
    return render_template("login_feature.html")

@main.route("/google_login")
def google_login():
    # Logic for Google login
    return render_template("google_login.html")

@main.route("/pest-management")
def pest_management():
    pests = [
        {
            "name": "Stem Borer",
            "short_desc": "Damages rice crops by boring into the stem.",
            "long_desc": "Stem borers are caterpillars that damage rice and maize. Look for dead hearts in plants.",
            "natural_tip": "Use neem oil spray weekly.",
            "govt_help": "Contact nearest Krishi Vigyan Kendra (KVK).",
            "image": "assets/stem_borer.jpg"
        },
        {
            "name": "Aphids",
            "short_desc": "Tiny insects sucking sap from vegetables and fruits.",
            "long_desc": "Aphids cluster on the underside of leaves, causing yellowing and curling.",
            "natural_tip": "Mix garlic + chili spray and apply early morning.",
            "govt_help": "Pest Management Unit helpline: 1800-180-1551.",
            "image": "assets/aphids.jpg"
        },
        {
            "name": "White Grubs",
            "short_desc": "Grubs eat roots of sugarcane, potatoes, etc.",
            "long_desc": "Visible in soil. They cause wilting and poor crop growth.",
            "natural_tip": "Apply light irrigation and release neem cake.",
            "govt_help": "Get soil treatment advice from Agri Dept.",
            "image": "assets/white_grub.jpg"
        }
    ]
    return render_template("pest_management.html", pests=pests)


@main.route("/iot_dashboard")
def iot_dashboard():
    # Logic to fetch and display IoT sensor data
    return render_template("iot_dashboard.html")    

@main.route("/knowledge_base")
def knowledge_base():   
    # Logic to fetch and display knowledge base articles
    return render_template("knowledge_base.html")

@main.route("/expert_help")
def expert_help():  
    # Logic to provide expert help options
    return render_template("expert_help.html")

@main.route("/community")
def community():    
    # Logic to display community discussions
    return render_template("community.html")

@main.route("/insurance")
def insurance():
    # Logic to display crop insurance information
    return render_template("insurance.html")

@main.route("/schemes")
def schemes():  
    # Logic to display government schemes and subsidies
    return render_template("schemes.html")

@main.route("/weather_input")
def weather_input():
    try:
        ip_info = requests.get("https://ipapi.co/json/").json()
        city = ip_info.get("city", "Delhi")
        return redirect(url_for("main.weather", city=city))
    except Exception:
        return redirect(url_for("main.weather", city="Delhi"))

@main.route("/weather_redirect", methods=["GET"])
def weather_redirect():
    city = request.args.get("city")
    if city:
        return redirect(url_for("main.weather", city=city))
    return redirect(url_for("main.weather", city="Delhi"))  # fallback

# Function to convert UTC to IST (UTC +5:30)
def convert_to_ist(utc_timestamp):
    return (datetime.utcfromtimestamp(utc_timestamp) + timedelta(hours=5, minutes=30)).strftime('%I:%M %p')

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


@main.route('/weather/<city>')

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

@main.route('/crop_guide', methods=['GET', 'POST'])
def crop_guide():
    predicted_crop = None

    if request.method == 'POST':
        try:
            season = request.form['season']
            state = request.form.get('state', 'Jammu and Kashmir')  # default
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            rainfall = float(request.form['rainfall'])

            encoded_season = season_encoder.transform([season])[0]
            encoded_state = state_encoder.transform([state])[0]

            input_data = np.array([[encoded_season, encoded_state, temperature, humidity, rainfall]])
            prediction = model.predict(input_data)[0]
            predicted_crop = crop_encoder.inverse_transform([prediction])[0]

        except Exception as e:
            print("Crop prediction error:", e)
            predicted_crop = "Invalid input or internal error"

    return render_template('crop_guide.html', predicted_crop=predicted_crop)

@main.route("/api/weather")
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

@main.route("/auto-crop", methods=['GET'])
def auto_crop_prediction():
    try:
        # Get location by IP
        ip_info = requests.get("https://ipapi.co/json/").json()
        city = ip_info.get("city", "Delhi")
        state = ip_info.get("region", "Jammu and Kashmir")

        # Load API key from .env
        weather_key = os.getenv("WEATHER_API_KEY")  # Replace with actual

        if not weather_key:
            return render_template("crop_guide.html", predicted_crop="⚠️ API key missing")
        
        # Fetch weather data
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric"
        weather_data = requests.get(weather_url).json()

        # Basic error handling for API response
        if weather_data.get("cod") != 200:
            return render_template("crop_guide.html", predicted_crop="⚠️ Failed to fetch weather")
        
        # Extract weather values
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        rainfall = 120  # assumed default value

        # Determine season based on month
        month = datetime.now().month
        if month in [6, 7, 8, 9]:
            season = "Kharif"
        elif month in [10, 11]:
            season = "Autumn"
        elif month in [12, 1, 2]:
            season = "Rabi"
        elif month in [3, 4, 5]:
            season = "Summer"
        else:
            season = "Whole Year"

        # Encode input data
        encoded_season = season_encoder.transform([season])[0]
        encoded_state = state_encoder.transform([state])[0]

        input_data = np.array([[encoded_season, encoded_state, temperature, humidity, rainfall]])
        prediction = model.predict(input_data)[0]
        predicted_crop = crop_encoder.inverse_transform([prediction])[0]

        return render_template("crop_guide.html", predicted_crop=predicted_crop)

    except Exception as e:
        print("Auto prediction error:", e)
        return render_template("crop_guide.html", predicted_crop="Error in auto prediction")


