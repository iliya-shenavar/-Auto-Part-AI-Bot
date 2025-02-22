import os
import cv2
import numpy as np
import pandas as pd
import re
import time
import telebot
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Bot Settings
TOKEN = "It's private :)))"
bot = telebot.TeleBot(TOKEN)

# Class for Analysis DataBase
class DataProcessor:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path, engine="openpyxl")
        self.preprocess_data()
    
    @staticmethod
    def normalize_persian_text(text):
        if not isinstance(text, str):
            return ""
        text = text.strip()
        text = re.sub(r"ي", "ی", text)
        text = re.sub(r"ك", "ک", text)
        text = re.sub(r"\s+", " ", text)
        return text
    
    def preprocess_column(self, column):
        return column.fillna("").astype(str).apply(self.normalize_persian_text)
    
    def preprocess_data(self):
        columns_to_clean = ["نام کالا", "قیمت مصرف کننده(ریال)", "آدرس عکس", "لینک خرید"]
        for col in columns_to_clean:
            self.df[col] = self.preprocess_column(self.df[col])
    
    def search(self, query):
        query_words = self.normalize_persian_text(query).split()
        results = self.df[
            self.df.apply(lambda row: any(all(word in cell for word in query_words if word) for cell in row), axis=1)
        ]
        return results

# CNN Class
class CNNModel:
    def __init__(self, model_path="car_parts_cnn.h5"):
        self.categories = ['روغن LHM بیگرز ','گردگیر جک فرمان بیگرز', 'گوی زانتیا 50 بار', 'ماهک تنظیم ارتفاع بیگرز']
        self.model_path = model_path
        if os.path.exists(self.model_path):
            self.model = load_model(self.model_path)
        else:
            self.train_model()
    
    def train_model(self):
        base_path = '/content/database'
        data, labels = [], []
        for label, category in enumerate(self.categories):
            folder_path = os.path.join(base_path, category)
            for file in os.listdir(folder_path):
                img_path = os.path.join(folder_path, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (50, 50))
                data.append(img)
                labels.append(label)
        
        data = np.array(data).reshape(-1, 50, 50, 1) / 255.0
        labels = to_categorical(labels, num_classes=len(self.categories))
        x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
        
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(50, 50, 1)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.3),
            Dense(len(self.categories), activation='softmax')
        ])
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=15, validation_data=(x_test, y_test), verbose=2)
        model.save(self.model_path)
        self.model = model
    
    def predict_image(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (50, 50))
        img = img.reshape(1, 50, 50, 1) / 255.0
        prediction = self.model.predict(img)
        predicted_label = np.argmax(prediction)
        confidence = np.max(prediction)
        return self.categories[predicted_label] if confidence > 0.6 else "تصویر در دسته‌بندی‌های مدل یافت نشد."

# Prototyping classes
data_processor = DataProcessor("DataBase.xlsx")
cnn_model = CNNModel()

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "سلام! لطفاً نام کالا یا تصویر موردنظر را ارسال کنید.")

@bot.message_handler(func=lambda message: True)
def search_product(message):
    results = data_processor.search(message.text)
    if results.empty:
        bot.reply_to(message, "نتیجه‌ای پیدا نشد.")
    else:
        for _, row in results.head(10).iterrows():
            response = f"نام کالا: {row['نام کالا']}\nقیمت مصرف کننده(ریال): {row['قیمت مصرف کننده(ریال)']}\nلینک خرید: {row['لینک خرید']}"
            if row["آدرس عکس"].startswith("http"):
                bot.send_photo(message.chat.id, row["آدرس عکس"], caption=response)
            else:
                bot.send_message(message.chat.id, response + "\n(عکس موجود نیست)")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_path = "received_image.jpg"
    with open(image_path, 'wb') as f:
        f.write(downloaded_file)
    
    result = cnn_model.predict_image(image_path)
    output = bot.reply_to(message, result)
    search_product(output)
    os.remove(image_path)

# Run Bot
while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Error: {e}. Reconnecting in 5 seconds...")
        time.sleep(5)
