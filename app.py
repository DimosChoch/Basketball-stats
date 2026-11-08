import streamlit as st
import pandas as pd
import plotly.express as px
import os

EXCEL_FILE = "basketball_stats_pro.xlsx"

PLAYERS_LIST = ["Μέλε", "Χοχλ", "Σταμ", "Κουκου", "Δραμ", "Κοντο", "Πιτα", "Κρητι", "Μηλιω", "Φουντου", "Μανου", "Στρι", "Γκοτσο", "Κυρια", "Παπα", "Γιαννα", "Δελ"]

ALL_COLUMNS = [
    "Αγώνας", "Αποτέλεσμα", "Παίκτης", "Χρόνος", "Πόντοι", 
    "Βολές Εύστοχες", "Βολές Συνολικές", "Βολές %",
    "Δίποντα Εύστοχα", "Δίποντα Συνολικά", "Δίποντα %",
    "Τρίποντα Εύστοχα", "Τρίποντα Συνολικά", "Τρίποντα %",
    "Ριμπάουντ Αμυντικά", "Ριμπάουντ Επιθετικά", "Ριμπάουντ Σύνολο",
    "Ασίστ", "Κλεψίματα", "Λάθη", "Μπλοκ", "Φαουλ", "Κερδισμένα Φαουλ", "PIR", "Starting Five"
]

if st.sidebar.button("🔄 Ανανέωση & Καθαρισμός Μνήμης"):
    st.cache_data.clear()
    st.rerun()

def load_data():
    if os.path.exists(EXCEL_FILE):
        try:
            loaded_df = pd.read_excel(EXCEL_FILE)
            loaded_df.columns = loaded_df.columns.astype(str).str.strip()
            numeric_cols = [
                "Χρόνος", "Πόντοι", "Βολές Εύστοχες", "Βολές Συνολικές", "Βολές %",
                "Δίποντα Εύστοχα", "Δίποντα Συνολικά", "Δίποντα %", "Τρίποντα Εύστοχα", 
                "Τρίποντα Συνολικά", "Τρίποντα %", "Ριμπάουντ Αμυντικά", "Ριμπάουντ Επιθετικά", 
                "Ριμπάουντ Σύνολο", "Ασίστ", "Κλεψίματα", "Λάθη", "Μπλοκ", "Φαουλ", "Κερδισμένα Φαουλ", "PIR"
            ]
            for col in numeric_cols:
                if col in loaded_df.columns:
                    loaded_df[col] = pd.to_numeric(loaded_df[col], errors='coerce').fillna(0)
            return loaded_df
        except:
            return pd.DataFrame(columns=ALL_COLUMNS)
    return pd.DataFrame(columns=ALL_COLUMNS)

def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

df = load_data()

st.set_page_config(layout="wide")
st.title("🏀 Advanced Basketball Analytics Platform")

if not df.empty:
    df["Αγώνας"] = df["Αγώνας"].astype(str).str.strip()
    df["Παίκτης"] = df["Παίκτης"].astype(str).str.strip()
    df["Αποτέλεσμα"] = df["Αποτέλεσμα"].astype(str).str.strip()

menu = st.sidebar.selectbox("Μενού Επιλογών", [
    "Προβολή Δεδομένων",
    "Εισαγωγή Στατιστικών", 
    "Ανάλυση & Γραφήματα"
])

# --- 1. ΠΡΟΒΟΛΗ ΔΕΔΟΜΕΝΩΝ ---
if menu == "Προβολή Δεδομένων":
    st.header("📋 Όλα τα Αποθηκευμένα Δεδομένα της Ομάδας")
    if df.empty:
        st.warning("⚠️ Η βάση δεδομένων είναι κενή.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Λήψη όλων των δεδομένων σε CSV", data=csv, file_name="basketball_stats_export.csv", mime="text/csv")

# --- 2. ΕΙΣΑΓΩΓΗ ΣΤΑΤΙΣΤΙΚΩΝ ---
elif menu == "Εισαγωγή Στατιστικών":
    st.header("📝 Καταγραφή Pro Στατιστικών ανά Παίκτη")
    with st.form("pro_stats_form", clear_on_submit=True):
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            match_name = st.text_input("Όνομα/Ημερομηνία Αγώνα", "Αγώνας 6")
        with col_m2:
            match_result = st.selectbox("Αποτέλεσμα Αγώνα", ["Νίκη", "Ήττα"])
        with col_m3:
            player_name = st.selectbox("Επιλέξτε Παίκτη", PLAYERS_LIST)
        with col_m4:
            minutes = st.number_input("Χρόνος (Λεπτά)", min_value=0, value=15, step=1)
            is_starter = st.checkbox("Βασική Πεντάδα (Starter);")

        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("🎯 Βολές")
            ftm = st.number_input("Εύστοχες Βολές", min_value=0, value=0, step=1)
            fta = st.number_input("Συνολικές Βολές", min_value=0, value=0, step=1)
            st.subheader("🛡️ Άμυνα")
            dreb = st.number_input("Αμυντικά Ριμπάουντ", min_value=0, value=0, step=1)
            blocks = st.number_input("Μπλοκ (Τάπες)", min_value=0, value=0, step=1)
        with col2:
            st.subheader("🎯 Δίποντα")
            fg2m = st.number_input("Εύστοχα Δίποντα", min_value=0, value=0, step=1)
            fg2a = st.number_input("Συνολικά Δίποντα", min_value=0, value=0, step=1)
            st.subheader("⚔️ Επίθεση")
            oreb = st.number_input("Επιθετικά Ριμπάουντ", min_value=0, value=0, step=1)
            turnovers = st.number_input("Λάθη", min_value=0, value=0, step=1)
        with col3:
            st.subheader("🎯 Τρίποντα")
            fg3m = st.number_input("Εύστοχα Τρίποντα", min_value=0, value=0, step=1)
            fg3a = st.number_input("Συνολικά Τρίποντα", min_value=0, value=0, step=1)
            st.subheader("🤝 Οργάνωση")
            assists = st.number_input("Ασίστ", min_value=0, value=0, step=1)
            steals = st.number_input("Κλεψίματα", min_value=0, value=0, step=1)
        with col4:
            st.subheader("⚠️ Φάουλ")
            fouls = st.number_input("Φάουλ Παίκτη", min_value=0, value=0, step=1)
            fouls_drawn = st.number_input("Κερδισμένα Φαουλ", min_value=0, value=0, step=1)
            
        submit = st.form_submit_button("💾 Υπολογισμός & Αποθήκευση")
        if submit:
            if ftm > fta or fg2m > fg2a or fg3m > fg3a:
                st.error("❌ Σφάλμα: Τα εύστοχα σουτ δεν μπορεί να είναι περισσότερα από τα συνολικά!")
            else:
                points = (ftm * 1) + (fg2m * 2) + (fg3m * 3)
                tot_reb = dreb + oreb
                ft_pct = round((ftm / fta) * 100, 1) if fta > 0 else 0.0
                fg2_pct = round((fg2m / fg2a) * 100, 1) if fg2a > 0 else 0.0
                fg3_pct = round((fg3m / fg3a) * 100, 1) if fg3a > 0 else 0.0
                missed_ft = fta - ftm
                missed_fg2 = fg2a - fg2m
                missed_fg3 = fg3a - fg3m
                pir = (points + tot_reb + assists + steals + blocks + fouls_drawn) - (missed_ft + missed_fg2 + missed_fg3 + turnovers + fouls)
                
                new_row = {
                    "Αγώνας": match_name.strip(), "Αποτέλεσμα": match_result, "Παίκτης": player_name.strip(), "Χρόνος": minutes, "Πόντοι": points,
                    "Βολές Εύστοχες": ftm, "Βολές Συνολικές": fta, "Βολές %": ft_pct,
                    "Δίποντα Εύστοχα": fg2m, "Δίποντα Συνολικά": fg2a, "Δίποντα %": fg2_pct,
                    "Τρίποντα Εύστοχα": fg3m, "Τρίποντα Συνολικά": fg3a, "Τρίποντα %": fg3_pct,
                    "Ριμπάουντ Αμυντικά": dreb, "Ριμπάουντ Επιθετικά": oreb, "Ριμπάουντ Σύνολο": tot_reb,
                    "Ασίστ": assists, "Κλεψίματα": steals, "Λάθη": turnovers, "Μπλοκ": blocks,
                    "Φαουλ": fouls, "Κερδισμένα Φαουλ": fouls_drawn, "PIR": pir
		    "Starting Five": "ΝΑΙ" if is_starter else "ΟΧΙ"
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success(f"✅ Ο παίκτης {player_name} καταχωρήθηκε!")

# --- 3. ΑΝΑΛΥΣΗ & ΓΡΑΦΗΜΑΤΑ ---
elif menu == "Ανάλυση & Γραφήματα":
    st.header("📊 Στατιστική Ανάλυση Αγώνα")
    if df.empty:
        st.warning("Δεν υπάρχουν δεδομένα.")
    else:
        selected_match = st.selectbox("Επιλέξτε Αγώνας", df["Αγώνας"].unique())
        match_df = df[df["Αγώνας"] == selected_match].copy()
        
        match_res = match_df["Αποτέλεσμα"].iloc[0] if not match_df.empty else "Νίκη"
        st.subheader(f"Αποτέλεσμα Αγώνα: {match_res}")
        
        team_sums = {
            "Αγώνας": selected_match, "Αποτέλεσμα": match_res, "Παίκτης": "🏀 ΣΥΝΟΛΟ ΟΜΑΔΑΣ",
            "Χρόνος": match_df["Χρόνος"].sum(), "Πόντοι": match_df["Πόντοι"].sum(),
            "Βολές Εύστοχες": match_df["Βολές Εύστοχες"].sum(), "Βολές Συνολικές": match_df["Βολές Συνολικές"].sum(),
            "Βολές %": round((match_df["Βολές Εύστοχες"].sum() / match_df["Βολές Συνολικές"].sum() * 100), 1) if match_df["Βολές Συνολικές"].sum() > 0 else 0.0,
            "Δίποντα Εύστοχα": match_df["Δίποντα Εύστοχα"].sum(), "Δίποντα Συνολικά": match_df["Δίποντα Συνολικά"].sum(),
            "Δίποντα %": round((match_df["Δίποντα Εύστοχα"].sum() / match_df["Δίποντα Συνολικά"].sum() * 100), 1) if match_df["Δίποντα Συνολικά"].sum() > 0 else 0.0,
            "Τρίποντα Εύστοχα": match_df["Τρίποντα Εύστοχα"].sum(), "Τρίποντα Συνολικά": match_df["Τρίποντα Συνολικά"].sum(),
            "Τρίποντα %": round((match_df["Τρίποντα Εύστοχα"].sum() / match_df["Τρίποντα Συνολικά"].sum() * 100), 1) if match_df["Τρίποντα Συνολικά"].sum() > 0 else 0.0,
            "Ριμπάουντ Αμυντικά": match_df["Ριμπάουντ Αμυντικά"].sum(), "Ριμπάουντ Επιθετικά": match_df["Ριμπάουντ Επιθετικά"].sum(),
            "Ριμπάουντ Σύνολο": match_df["Ριμπάουντ Σύνολο"].sum(), "Ασίστ": match_df["Ασίστ"].sum(),
            "Κλεψίματα": match_df["Κλεψίματα"].sum(), "Λάθη": match_df["Λάθη"].sum(), "Μπλοκ": match_df["Μπλοκ"].sum(),
            "Φαουλ": match_df["Φαουλ"].sum(), "Κερδισμένα Φαουλ": match_df["Κερδισμένα Φαουλ"].sum(), "PIR": match_df["PIR"].sum()
        }
        
        display_df = pd.concat([match_df, pd.DataFrame([team_sums])], ignore_index=True)
        st.dataframe(display_df[[
            "Παίκτης", "Χρόνος", "Πόντοι", "Βολές Εύστοχες", "Βολές Συνολικές", "Βολές %",
            "Δίποντα Εύστοχα", "Δίποντα Συνολικά", "Δίποντα %", "Τρίποντα Εύστοχα", "Τρίποντα Συνολικά", "Τρίποντα %",
            "Ριμπάουντ Σύνολο", "Ασίστ", "Κλεψίματα", "Λάθη", "Μπλοκ", "Φαουλ", "PIR"
        ]], height=400, hide_index=True)
        
        st.markdown("---")
        st.subheader("👤 Σύγκριση Παικτών (Γράφημα)")
        numeric_cols = [c for c in ALL_COLUMNS if c not in ["Αγώνας", "Παίκτης", "Βολές %", "Δίποντα %", "Τρίποντα %", "Αποτέλεσμα"]]
        stat_to_plot = st.selectbox("Επιλέξτε Στατιστικό για το Γράφημα", numeric_cols)
        fig = px.bar(match_df, x="Παίκτης", y=stat_to_plot, text_auto=True, color="PIR", color_continuous_scale="Viridis", title=f"{stat_to_plot} ανά Παίκτη")
        st.plotly_chart(fig, use_container_width=True)
