import pandas as pd
import os

# "data" klasörünü oluştur (yoksa)
os.makedirs("data", exist_ok=True)

# Örnek kıyafet önerileri verisi
data = [
    ["Clear", 30, 45, "unisex", "casual", "summer", "casual", "Tişört, şort ve güneş gözlüğü giyebilirsin."],
    ["Clear", 10, 20, "unisex", "travel", "spring", "smart casual", "Kot pantolon ve ince mont uygun olur."],
    ["Rain", 5, 15, "unisex", "casual", "autumn", "smart casual", "Yağmurluk, bot ve şemsiye almayı unutma."],
    ["Snow", -10, 0, "unisex", "casual", "winter", "casual", "Kalın mont, bere, atkı ve eldiven tak."],
    ["Clouds", 15, 25, "male", "casual", "summer", "casual", "Keten gömlek ve açık renk pantolon uygundur."],
    ["Thunderstorm", 20, 30, "unisex", "travel", "summer", "smart casual", "Yağmurluk giy, şemsiye taşı."]
]

# Veriyi tabloya dönüştür
df = pd.DataFrame(data, columns=[
    "weather", "min_temp", "max_temp", "gender",
    "activity", "season", "formality", "suggestion"
])

# CSV olarak kaydet
os.makedirs("data", exist_ok=True)
df.to_csv("data/outfits.csv", index=False, encoding="utf-8")

print("✅ outfits.csv dosyası başarıyla oluşturuldu!")

