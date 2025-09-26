# 🌾 SmartFarm – Farmer Assistance Web Platform

SmartFarm is a web-based platform designed to **empower farmers with modern digital tools**.  
It provides **crop guidance, real-time weather, market prices, online marketplace, government schemes, chatbot support, and more** — all in one place.

-----

## 🚀 Features
- 🌾 **Crop Guide** – Get crop recommendations based on **current weather**.    
- 🌦️ **Weather Updates** – Live weather and alerts for your region.  
- 🌍 **Multi-language** –  Supports Hindi, English, and more via Google Translate.  
- 💰 **Market Rates** – Get current mandi prices for crops.  
- 🛒 **Online Market (E-Commerce)** – Buy seeds, tools, fertilizers, and more online.  
- 🏪 **Farmer Marketplace** – Farmers can sell their crops and produce directly to buyers.    
- 🏛️ **Govt. Schemes** – Access latest subsidies, schemes, and Yojanas.  
- 🌳 **Crop Shelter** – Learn how to protect yield in extreme weather.  
- 🤖 **Smart Chatbot** – Get answers to farming queries 24/7 powered by **Ollama server**.

-----

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** MongoDB  
- **Cloud Storage:** Cloudinary (for images)  
- **APIs:** Weather API (for live updates & auto predictions) 

-----

## ⚙️ Set Up Environment Variables
Create a **.env** file in the root directory of the project and add the following:

- **WEATHER_API_KEY**=your_weather_api_key
- **SECRET_KEY**=your_flask_secret_key
- **DATASET_PATH**=path_to_your_crop_dataset_csv
- **PRICES_DATASET_PATH**=path_to_your_market_prices_csv
- **MONGO_URI**=your_mongodb_connection_uri
- **MONGO_DB**=your_mongodb_database_name
- **ADMIN_NAME**=your_admin_username
- **ADMIN_EMAIL**=your_admin_email
- **ADMIN_PASSWORD**=your_admin_password
- **GOOGLE_CLIENT_ID**=your_google_client_id
- **GOOGLE_CLIENT_SECRET**=your_google_client_secret
- **CLOUDINARY_CLOUD_NAME**=your_cloudinary_cloud_name
- **CLOUDINARY_API_KEY**=your_cloudinary_api_key
- **CLOUDINARY_API_SECRET**=your_cloudinary_api_secret