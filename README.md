🧠 README.md — Smart Weather Outfit Chatbot
🌦️ “Bugün ne giymeliyim?” sorusuna cevap alabileceğiniz bir programdır.
Bu proje, yaşadığın şehre göre hava durumunu analiz ederek ve bize en uygun kıyafet önerilerini yapar.



📌 Proje Hakkında
Smart Weather Outfit Chatbot, OpenWeather API’sinden aldığı anlık hava durumu verisini kullanarak sıcaklık, hava tipi, mevsim, etkinlik ve kullanıcı tercihlerine göre kıyafet önerileri verir.
Eğer API anahtarın yoksa, uygulama otomatik olarak demo moduna geçer ve kullanıcıdan sıcaklık & hava durumu bilgisini manuel ister. 



UYARI
Bu yüzden kendi openweather Apı ve open Apı anahtarınızı sisteme yüklemeyi unutmayın!



🎯 Amaç
Python, Pandas ve Streamlit kullanarak veri temelli akıllı öneri sistemi geliştirmek
API yönetimi, veri seti hazırlama, çevresel değişken yönetimi (.env) ve GitHub projesi oluşturmayı öğrenmek
Bootcamp projesi kapsamında uygulanabilir ve kullanıcı dostu bir çözüm üretmek



⚙️ Kullanılan Teknolojiler
Teknoloji	           Açıklama
🐍 Python 3.9+	      Temel dil
🧠 Pandas	          Veri işleme
☁️ OpenWeather API	  Hava durumu verisi
💬 Streamlit	      Web arayüzü
🔐 python-dotenv	  API anahtarını gizleme
📦 Requests	API       isteği gönderme



📁 Proje Dosya Yapısı
📦 weather-outfit-chatbot
├── app.py                 # Streamlit ana uygulama
├── requirements.txt       # Gerekli Python paketleri
├── .env                   # (gizli) OpenWeather API anahtarı
    .env.example           # örnek env dosyası
├── .gitignore             # .env ve gereksiz dosyaları gizler
├── data/
│   └── outfits.csv        # Hava durumuna göre kıyafet öneri 
    create_dataset.py      # Hava durumuna göre kıyafet öneri veri seti
└── README.md              # Bu dosya 



🧩 Veri Seti Hakkında

Veri seti (data/outfits.csv) tamamen Python ile oluşturulmuştur.
Aşağıdaki sütunları içerir:

Sütun	                 Açıklama
weather	                 Hava tipi (Clear, Rain, Snow, Clouds, Mist, vb.)
min_temp, max_temp	     Geçerli sıcaklık aralığı
gender	                 “male”, “female”, “unisex”
activity	             Kullanıcının etkinliği (work, casual, sport, travel)
season	                 Mevsim (winter, spring, summer, autumn)
formality	             Tarz (casual, sporty, formal, smart casual)
suggestion	             kıyafet önerisi

Veri seti, mevsim + sıcaklık + cinsiyet + etkinlik kombinasyonlarına göre öneriler içerir.   

Arayüz sistem çalıştırma
 python -m streamlit run app.py
 You can now view your Streamlit app in your browser.
 
 Chatbot 
  Local URL: http://localhost:8510
  Network URL: http://10.27.30.187:8510

Live Demo(kendi openweather Apı ve open Apı anahtarınızı sisteme yüklemeyi unutmayın!)
https://smart-weather-outfit-chatbot-whxtn8uofgsfqvahp3phn9.streamlit.app/


