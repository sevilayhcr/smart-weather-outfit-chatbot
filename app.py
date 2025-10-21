"""
Smart Weather Outfit Chatbot — Streamlit app
- API anahtarını .env veya Streamlit secrets aracılığıyla okur (gizli tutulur).
- OpenWeather ile gerçek hava verisi çeker (anahtar varsa).
- outfits.csv veri setini kullanarak en uygun kıyafet önerilerini sıralar.
- Demo modu: API anahtarı yoksa kullanıcı girdisine göre öneri verir.
"""

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# -----------------------------
# 1) Load environment / secrets
# -----------------------------
# load .env if present (local dev)
load_dotenv()

# Prefer environment variable, fallback to Streamlit secrets
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or st.secrets.get("OPENWEATHER_API_KEY") if "secrets" in dir(st) else None

# -----------------------------
# 2) Utilities / Data loading
# -----------------------------
@st.cache_data
def load_outfits(path="data/outfits.csv"):
    df = pd.read_csv(path)
    # normalize string columns for easier matching
    for col in ["weather", "gender", "activity", "season", "formality"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df

outfits_df = load_outfits()

def current_season():
    m = datetime.now().month
    if m in (12, 1, 2):
        return "winter"
    if m in (3, 4, 5):
        return "spring"
    if m in (6, 7, 8):
        return "summer"
    return "autumn"

# -----------------------------
# 3) Weather fetch (safe)
# -----------------------------
@st.cache_data(ttl=300)
def fetch_weather_for_city(city: str):
    """Returns dict like {'temp': float, 'condition': 'Clear', 'full': raw json} or None on failure.
    If no API key available, returns None (caller handles demo)."""
    if not OPENWEATHER_API_KEY:
        return None

    base = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric", "lang": "en"}
    try:
        r = requests.get(base, params=params, timeout=8)
        if r.status_code != 200:
            return None
        j = r.json()
        cond_short = j["weather"][0]["main"]  # matches our dataset values: Clear, Rain, Clouds, Snow, Mist...
        temp = j["main"]["temp"]
        return {"temp": float(temp), "condition": cond_short, "raw": j}
    except Exception:
        return None

# -----------------------------
# 4) Recommendation logic
# -----------------------------
def recommend_outfits(temp: float, condition: str, season_override=None, gender=None, activity=None, formality=None, top_k=3):
    """Return top_k suggestions from outfits_df based on scoring."""
    season = season_override or current_season()
    df = outfits_df.copy()

    # Filter by season first (reasonable default)
    if "season" in df.columns:
        df = df[df["season"].str.lower() == season.lower()]

    # Keep only rows where temp within min/max
    df = df[(df["min_temp"] <= temp) & (df["max_temp"] >= temp)]

    # If none left after strict temp+season, relax season filter
    if df.empty:
        df = outfits_df[(outfits_df["min_temp"] <= temp) & (outfits_df["max_temp"] >= temp)]

    # Scoring: start from 0, add points for matches
    def score_row(row):
        score = 0
        # weather match (strong)
        try:
            if str(row["weather"]).lower() == str(condition).lower():
                score += 3
            # partial matches (e.g., Clouds vs Clear) - if contains
            elif str(condition).lower() in str(row["weather"]).lower() or str(row["weather"]).lower() in str(condition).lower():
                score += 1
        except Exception:
            pass

        # gender match (+1) or if row is unisex (+1)
        try:
            if pd.isna(gender) or gender.lower() == "any":
                score += 0
            else:
                if str(row["gender"]).lower() == str(gender).lower():
                    score += 1
                elif str(row["gender"]).lower() == "unisex":
                    score += 1
        except Exception:
            pass

        # activity match
        try:
            if pd.notna(activity) and activity.lower() != "any":
                if str(row["activity"]).lower() == activity.lower():
                    score += 1
        except Exception:
            pass

        # formality match
        try:
            if pd.notna(formality) and formality.lower() != "any":
                if str(row["formality"]).lower() == formality.lower():
                    score += 1
        except Exception:
            pass

        # prefer rows whose min_temp is close to actual temp (smaller distance => +1)
        try:
            temp_center = (row["min_temp"] + row["max_temp"]) / 2.0
            if abs(temp_center - temp) <= 3:
                score += 0.5
        except Exception:
            pass

        return score

    # compute scores
    if df.empty:
        return []

    df = df.copy()
    df["score"] = df.apply(score_row, axis=1)

    # sort by score desc then by formality (prefer smart/formal when user asked), then by temp closeness
    df["temp_center"] = (df["min_temp"] + df["max_temp"]) / 2.0
    df["temp_diff"] = (df["temp_center"] - temp).abs()
    df = df.sort_values(by=["score", "temp_diff"], ascending=[False, True])

    # pick top_k unique suggestions
    suggestions = []
    used = set()
    for _, r in df.iterrows():
        s = r["suggestion"]
        key = (s, r["formality"], r["activity"])
        if key in used:
            continue
        used.add(key)
        suggestions.append({
            "weather": r["weather"],
            "temp_range": f"{r['min_temp']}–{r['max_temp']}°C",
            "gender": r["gender"],
            "activity": r["activity"],
            "season": r["season"],
            "formality": r["formality"],
            "suggestion": s,
            "score": float(r["score"])
        })
        if len(suggestions) >= top_k:
            break

    return suggestions

# -----------------------------
# 5) Streamlit UI
# -----------------------------
st.set_page_config(page_title="Smart Weather Outfit Chatbot", page_icon="👗", layout="centered")
st.title("👗 Smart Weather Outfit Chatbot")
st.write("Şehrine göre hava alır ve en uygun kıyafet önerilerini verir. (API anahtarını .env / Streamlit secrets ile gizli tut.)")

# Input: city
col1, col2 = st.columns([3,1])
with col1:
    city = st.text_input("Hangi şehirdesin? (örn. Istanbul, Ankara)", value="Istanbul")
with col2:
    if OPENWEATHER_API_KEY:
        st.success("API: ayarlı 🔒")
    else:
        st.warning("Demo modu — API yok")

# Optional filters
st.markdown("**Tercihleri (isteğe bağlı)**")
gender = st.selectbox("Cinsiyet (isteğe bağlı)", options=["Any", "female", "male", "unisex"], index=0)
activity_vals = ["Any"] + sorted(outfits_df["activity"].unique().tolist())
activity = st.selectbox("Etkinlik (isteğe bağlı)", options=activity_vals, index=0)
formality_vals = ["Any"] + sorted(outfits_df["formality"].unique().tolist())
formality = st.selectbox("Resmiyet (isteğe bağlı)", options=formality_vals, index=0)

# Button
if st.button("Öneri Al"):
    if not city.strip():
        st.warning("Lütfen geçerli bir şehir adı gir.")
    else:
        with st.spinner("Hava durumu alınıyor..."):
            weather = fetch_weather_for_city(city)
        # If weather is None due to no API key or fetch fail -> ask user for temp/condition or demo
        if weather is None:
            st.info("Gerçek API anahtarı yok veya hava alınamadı — demo modu aktif.")
            # ask manual inputs
            temp_manual = st.number_input("Şu an sıcaklık (°C) gir:", value=20.0, step=0.5)
            condition_manual = st.selectbox("Hava tipi seç (demo):", options=sorted(outfits_df["weather"].unique().tolist()))
            chosen_temp = float(temp_manual)
            chosen_condition = condition_manual
            st.write(f"Demo hava: {chosen_temp}°C, {chosen_condition}")
            suggestions = recommend_outfits(chosen_temp, chosen_condition,
                                           season_override=current_season(),
                                           gender=(None if gender=="Any" else gender),
                                           activity=(None if activity=="Any" else activity),
                                           formality=(None if formality=="Any" else formality),
                                           top_k=3)
        else:
            st.success(f"Hava: {weather['temp']:.1f}°C — {weather['condition']}")
            suggestions = recommend_outfits(weather["temp"], weather["condition"],
                                           season_override=current_season(),
                                           gender=(None if gender=="Any" else gender),
                                           activity=(None if activity=="Any" else activity),
                                           formality=(None if formality=="Any" else formality),
                                           top_k=3)

        if not suggestions:
            st.warning("Bu kriterlerle uygun öneri bulunamadı. Filtreleri gevşetmeyi deneyin.")
        else:
            st.markdown("### ✅ Öneriler")
            for i, s in enumerate(suggestions, start=1):
                st.markdown(f"**{i}. {s['suggestion']}**")
                st.caption(f"({s['weather']} • {s['temp_range']} • {s['gender']} • {s['activity']} • {s['season']} • {s['formality']})")

# Footer: small helper
st.markdown("---")
st.caption("API anahtarını .env dosyasına ekleyin veya Streamlit Secrets'a koyun. `.env` kesinlikle repoya eklenmemelidir.")
