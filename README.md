# 🚀 AutoPartAI Bot

AutoPartAI Bot is an **AI-powered** Telegram bot designed for **(TKPC)** that allows users to identify car parts by uploading an image. Using **deep learning** and **computer vision**, the bot accurately classifies car parts and provides a purchase link from the company's website.

---

## ✨ Features
✅ AI-based **image recognition** for car parts.  
✅ Accepts **product name** or **image** for identification.  
✅ Uses **text normalization** for Persian queries.  
✅ Implements a **CNN model** for accurate classification.  
✅ Searches a **product database** and provides purchase links.  
✅ Automatically handles **Telegram bot interactions**.  

---

## 🛠 Installation & Setup
### 1️⃣ Clone the repository:
```sh
git clone https://github.com/yourusername/AutoPartAIBot.git
cd AutoPartAIBot
```
### 2️⃣ Install dependencies:
```sh
pip install -r requirements.txt
```
### 3️⃣ Prepare the dataset and model:
- Ensure `DataBase.xlsx` contains product details.
- Train or provide `car_parts_cnn.h5` for AI-based image classification.
### 4️⃣ Set up the Telegram bot:
- Replace `TOKEN` in `main.py` with your **Telegram Bot API Token**.
### 5️⃣ Run the bot:
```sh
python main.py
```

---

## 🎯 Usage
📌 **Search by text:** Send a product name to search.  
📌 **Search by image:** Upload a car part image for automatic AI recognition.  
📌 The bot will return the **product name, price, and purchase link**.  

---

## 👥 Contributors
🔹 **Iliya Shenavar** (CTO, TKPC)  
🔹 **Mojtaba Khaleghi** ([GitHub](https://github.com/mojtabaKhaleghi12))  

---

## 📜 License
This project is licensed under the Strict Proprietary License.Unauthorized use, modification, or distribution of this software is strictly prohibited without prior written permission from Iliya Shenavar and Mojtaba Khaleghi. For inquiries, please contact iliya.shenavar@gmail.com.

