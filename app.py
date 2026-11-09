import streamlit as st
import pandas as pd
import plotly.express as px
import os

EXCEL_FILE = "basketball_stats_pro.xlsx"

PLAYERS_LIST = ["ΜΕΛΕ", "ΧΟΧΛ", "ΣΤΑΜ", "ΚΟΥΚΟΥ", "ΔΡΑΜ", "ΚΟΝΤΟ", "ΠΙΤΑ", "ΚΡΗΤΙ", "ΜΗΛΙΩ", "ΦΟΥΝΤΟΥ", "ΜΑΝΟΥ", "ΣΤΡΙ", "ΓΚΟΤΣΟ", "ΚΥΡΙΑ", "ΠΑΠΑ", "ΓΙΑΝΝΑ", "ΔΕΛ"]

ALL_COLUMNS = [
    "Αγώνας", "Αποτέλεσμα", "Παίκτης", "Χρόνος", "Πόντοι", 
    "Βολές Εύστοχες", "Βολές Συνολικές", "Βολές %",
    "Δίποντα Εύστοχα", "Δίποντα Συνολικά", "Δίποντα %",
    "Τρίποντα Εύστοχα", "Τρίποντα Συνολικά", "Τρίποντα %",
    "Ριμπάουντ Αμυντικά", "Ριμπάουντ Επιθετικά", "Ριμπάουντ Σύνολο",
    "Ασίστ", "Κλεψίματα", "Λάθη", "Μπλοκ", "Φαουλ", "Κερδισμένα Φαουλ", "PIR", "Starting Five",
    "Επιθετικά Ριμπάουντ Αντιπάλου"
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
    "Ανάλυση & Γραφήματα",
    "Μέσοι Όροι Παικτών (Season)",
    "Μέσοι Όροι (Νίκες vs Ήττες)"
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
            opp_oreb = st.number_input("Επιθ. Ριμπάουντ Αντιπάλου (Σύνολο Αγώνα)", min_value=0, value=0, step=1)
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
                }
                new_row["Starting Five"] = "ΝΑΙ" if is_starter else "ΟΧΙ"
                new_row["Επιθετικά Ριμπάουντ Αντιπάλου"] = opp_oreb

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
            "Φαουλ": match_df["Φαουλ"].sum(), "Κερδισμένα Φαουλ": match_df["Κερδισμένα Φαουλ"].sum(), "PIR": match_df["PIR"].sum(),
            "Starting Five": "",            
            "Επιθετικά Ριμπάουντ Αντιπάλου": match_df["Επιθετικά Ριμπάουντ Αντιπάλου"].max() if "Επιθετικά Ριμπάουντ Αντιπάλου" in match_df.columns else 0
        }
        
        display_df = pd.concat([match_df, pd.DataFrame([team_sums])], ignore_index=True)
        display_df["Επιθετικά Ριμπάουντ Αντιπάλου"] = display_df["Επιθετικά Ριμπάουντ Αντιπάλου"].astype(object)
        display_df.iloc[:-1, display_df.columns.get_loc("Επιθετικά Ριμπάουντ Αντιπάλου")] = ""
        
        # ✨ ΝΕΟΣ ΤΡΟΠΟΣ: Προσθήκη emoji ⭐ στους starters για να ξεχωρίζουν σε Dark Mode
        if "Starting Five" in match_df.columns:
            match_df.loc[match_df["Starting Five"].str.strip().str.upper() == "ΝΑΙ", "Παίκτης"] = "⭐ " + match_df["Παίκτης"]

        def highlight_starters(row):
            if "⭐" in str(row["Παίκτης"]):
                return ['font-weight: bold; color: #ffaa00;'] * len(row) # Έντονα χρυσά γράμματα
            return [''] * len(row)

        # Λίστα στηλών για προβολή (βάλαμε και τη στήλη Starting Five για να φαίνεται)
        columns_view = [
            "Παίκτης", "Starting Five", "Χρόνος", "Πόντοι", "Βολές Εύστοχες", "Βολές Συνολικές", "Βολές %",
            "Δίποντα Εύστοχα", "Δίποντα Συνολικά", "Δίποντα %", "Τρίποντα Εύστοχα", "Τρίποντα Συνολικά", "Τρίποντα %",
            "Ριμπάουντ Σύνολο", "Ασίστ", "Κλεψίματα", "Λάθη", "Μπλοκ", "Φαουλ", "PIR", "Επιθετικά Ριμπάουντ Αντιπάλου"
        ]
        
        # Εφαρμογή του bold/χρώματος στους starters
        styled_df = display_df[columns_view].style.apply(highlight_starters, axis=1)
        
        # 🔥 ΔΙΟΡΘΩΘΗΚΕ: Μορφοποίηση με 1 δεκαδικό ΧΩΡΙΣ το σύμβολο % μέσα στον πίνακα
        styled_df = styled_df.format({
            "Βολές %": "{:.1f}",
            "Δίποντα %": "{:.1f}",
            "Τρίποντα %": "{:.1f}"
        })
        
        # Εμφάνιση του τελικού πίνακα
        # 🔥 ΔΙΟΡΘΩΘΗΚΕ: Σταθεροποίηση (Freeze) της πρώτης στήλης του Παίκτη κατά το Scroll δεξιά
        st.dataframe(
            styled_df, 
            height=400, 
            use_container_width=True, 
            hide_index=True,
            column_config={"Παίκτης": st.column_config.Column(pinned=True)}
        )

    
        st.markdown("---")
        st.subheader("👤 Σύγκριση Παικτών (Γράφημα)")
        numeric_cols = [c for c in ALL_COLUMNS if c not in ["Αγώνας", "Παίκτης", "Βολές %", "Δίποντα %", "Τρίποντα %", "Αποτέλεσμα"]]
        stat_to_plot = st.selectbox("Επιλέξτε Στατιστικό για το Γράφημα", numeric_cols)
        fig = px.bar(match_df, x="Παίκτης", y=stat_to_plot, text_auto=True, color="PIR", color_continuous_scale="Viridis", title=f"{stat_to_plot} ανά Παίκτη")
        st.plotly_chart(fig, use_container_width=True)

# --- 4. ΜΕΣΟΙ ΟΡΟΙ ΠΑΙΚΤΩΝ (SEASON) ---
elif menu == "Μέσοι Όροι Παικτών (Season)":
    st.header("📈 Μέσοι Όροι Παικτών για τη Σεζόν")
    if df.empty:
        st.warning("Δεν υπάρχουν ακόμα δεδομένα.")
    else:
        # Καθαρίζουμε τα ονόματα από τυχόν αστέρια για να γίνει σωστά το φιλτράρισμα
        unique_players = sorted(list(df["Παίκτης"].astype(str).str.replace("⭐ ", "").unique()))
        season_rows = []
        
        for p in unique_players:
            p_df = df[df["Παίκτης"].astype(str).str.contains(p)]
            if p_df.empty:
                continue
                
            ftm_s = pd.to_numeric(p_df["Βολές Εύστοχες"]).sum()
            fta_s = pd.to_numeric(p_df["Βολές Συνολικές"]).sum()
            fg2m_s = pd.to_numeric(p_df["Δίποντα Εύστοχα"]).sum()
            fg2a_s = pd.to_numeric(p_df["Δίποντα Συνολικά"]).sum()
            fg3m_s = pd.to_numeric(p_df["Τρίποντα Εύστοχα"]).sum()
            fg3a_s = pd.to_numeric(p_df["Τρίποντα Συνολικά"]).sum()
            
            season_rows.append({
                "Παίκτης": p,
                "Αγώνες": int(len(p_df)),
                "Χρόνος": round(pd.to_numeric(p_df["Χρόνος"]).mean(), 1),
                "Πόντοι": round(pd.to_numeric(p_df["Πόντοι"]).mean(), 1),
                "Βολές %": round((ftm_s / fta_s * 100), 1) if fta_s > 0 else 0.0,
                "Δίποντα %": round((fg2m_s / fg2a_s * 100), 1) if fg2a_s > 0 else 0.0,
                "Τρίποντα %": round((fg3m_s / fg3a_s * 100), 1) if fg3a_s > 0 else 0.0,
                "Ριμπάουντ Σύνολο": round(pd.to_numeric(p_df["Ριμπάουντ Σύνολο"]).mean(), 1),
                "Ασίστ": round(pd.to_numeric(p_df["Ασίστ"]).mean(), 1),
                "Κλεψίματα": round(pd.to_numeric(p_df["Κλεψίματα"]).mean(), 1),
                "Λάθη": round(pd.to_numeric(p_df["Λάθη"]).mean(), 1),
                "Μπλοκ": round(pd.to_numeric(p_df["Μπλοκ"]).mean(), 1),
                "Φαουλ": round(pd.to_numeric(p_df["Φαουλ"]).mean(), 1),
                "PIR": round(pd.to_numeric(p_df["PIR"]).mean(), 1)
            })
            
        player_stats_clean = pd.DataFrame(season_rows)
        
        # Εξαναγκασμός εμφάνισης 1 δεκαδικού σε όλες τις στήλες στατιστικών (εκτός από τους Αγώνες)
        styled_season = player_stats_clean.style.format({
            "Χρόνος": "{:.1f}",
            "Πόντοι": "{:.1f}",
            "Βολές %": "{:.1f}",
            "Δίποντα %": "{:.1f}",
            "Τρίποντα %": "{:.1f}",
            "Ριμπάουντ Σύνολο": "{:.1f}",
            "Ασίστ": "{:.1f}",
            "Κλεψίματα": "{:.1f}",
            "Λάθη": "{:.1f}",
            "Μπλοκ": "{:.1f}",
            "Φαουλ": "{:.1f}",
            "PIR": "{:.1f}"
        })
        
        # 🔥 ΔΙΟΡΘΩΘΗΚΕ: Σταθεροποίηση της στήλης του Παίκτη και στους Μέσους Όρους της Σεζόν
        st.dataframe(
            styled_season, 
            use_container_width=True, 
            hide_index=True,
            column_config={"Παίκτης": st.column_config.Column(pinned=True)}
        )
        
        st.markdown("---")
        st.subheader("📈 Διακύμανση Απόδοσης ανά Παίκτη")
        selected_player = st.selectbox("Επιλέξτε Παίκτη για να δείτε την πορεία του", unique_players)
        player_history = df[df["Παίκτης"].astype(str).str.contains(selected_player)].sort_values(by="Αγώνας")
        stat_history = st.selectbox("Επιλέξτε Στατιστικό για την πορεία", ["Πόντοι", "PIR", "Ασίστ", "Ριμπάουντ Σύνολο", "Λάθη"])
        
        player_history[stat_history] = pd.to_numeric(player_history[stat_history], errors='coerce').fillna(0).astype(float)
        fig_history = px.bar(player_history, x="Αγώνας", y=stat_history, text_auto=True, title=f"Πορεία στην κατηγορία '{stat_history}' για τον παίκτη: {selected_player}")
        st.plotly_chart(fig_history, use_container_width=True)

# --- 5. ΜΕΣΟΙ ΟΡΟΙ (ΝΙΚΕΣ VS ΗΤΤΕΣ) ---
elif menu == "Μέσοι Όροι (Νίκες vs Ήττες)":
    st.header("📈 Σύγκριση Μέσων Όρων Ομάδας")
    if df.empty:
        st.warning("Δεν υπάρχουν δεδομένα.")
    else:
        unique_matches = df["Αγώνας"].dropna().unique()
        match_sums_list = []
        
        for m in unique_matches:
            m_df = df[df["Αγώνας"] == m]
            if m_df.empty:
                continue
            res_val = str(m_df["Αποτέλεσμα"].dropna().iloc[0]).strip().upper() if not m_df.empty else "ΝΙΚΗ"
            
            match_sums_list.append({
                "Αγώνας": m,
                "Αποτέλεσμα": res_val,
                "Πόντοι": pd.to_numeric(m_df["Πόντοι"]).sum(),
                "Βολές Εύστοχες": pd.to_numeric(m_df["Βολές Εύστοχες"]).sum(),
                "Βολές Συνολικές": pd.to_numeric(m_df["Βολές Συνολικές"]).sum(),
                "Δίποντα Εύστοχα": pd.to_numeric(m_df["Δίποντα Εύστοχα"]).sum(),
                "Δίποντα Συνολικά": pd.to_numeric(m_df["Δίποντα Συνολικά"]).sum(),
                "Τρίποντα Εύστοχα": pd.to_numeric(m_df["Τρίποντα Εύστοχα"]).sum(),
                "Τρίποντα Συνολικά": pd.to_numeric(m_df["Τρίποντα Συνολικά"]).sum(),
                "Ριμπάουντ Σύνολο": pd.to_numeric(m_df["Ριμπάουντ Σύνολο"]).sum(),
                "Ασίστ": pd.to_numeric(m_df["Ασίστ"]).sum(),
                "Κλεψίματα": pd.to_numeric(m_df["Κλεψίματα"]).sum(),
                "Λάθη": pd.to_numeric(m_df["Λάθη"]).sum(),
                "Μπλοκ": pd.to_numeric(m_df["Μπλοκ"]).sum(),
                "Φαουλ": pd.to_numeric(m_df["Φαουλ"]).sum(),
                "PIR": pd.to_numeric(m_df["PIR"]).sum()
            })
            
        match_totals_df = pd.DataFrame(match_sums_list)
        results_list = []
        
        for r in ["ΝΙΚΗ", "ΗΤΤΑ"]:
            r_df = match_totals_df[match_totals_df["Αποτέλεσμα"] == r]
            if r_df.empty:
                continue
                
            ftm_sum = r_df["Βολές Εύστοχες"].sum()
            fta_sum = r_df["Βολές Συνολικές"].sum()
            fg2m_sum = r_df["Δίποντα Εύστοχα"].sum()
            fg2a_sum = r_df["Δίποντα Συνολικά"].sum()
            fg3m_sum = r_df["Τρίποντα Εύστοχα"].sum()
            fg3a_sum = r_df["Τρίποντα Συνολικά"].sum()
            
            results_list.append({
                "Αποτέλεσμα": r,
                "Πόντοι": round(r_df["Πόντοι"].mean(), 1),
                "Βολές %": round((ftm_sum / fta_sum * 100), 1) if fta_sum > 0 else 0.0,
                "Δίποντα %": round((fg2m_sum / fg2a_sum * 100), 1) if fg2a_sum > 0 else 0.0,
                "Τρίποντα %": round((fg3m_sum / fg3a_sum * 100), 1) if fg3a_sum > 0 else 0.0,
                "Ριμπάουντ Σύνολο": round(r_df["Ριμπάουντ Σύνολο"].mean(), 1),
                "Ασίστ": round(r_df["Ασίστ"].mean(), 1),
                "Κλεψίματα": round(r_df["Κλεψίματα"].mean(), 1),
                "Λάθη": round(r_df["Λάθη"].mean(), 1),
                "Μπλοκ": round(r_df["Μπλοκ"].mean(), 1),
                "Φαουλ": round(r_df["Φαουλ"].mean(), 1),
                "PIR": round(r_df["PIR"].mean(), 1)
            })
            
        if not results_list:
            st.warning("Δεν βρέθηκαν επαρκή δεδομένα για τον διαχωρισμό Νικών/Ηττών.")
        else:
            avg_by_result = pd.DataFrame(results_list)
            columns_to_show = ["Αποτέλεσμα", "Πόντοι", "Βολές %", "Δίποντα %", "Τρίποντα %", "Ριμπάουντ Σύνολο", "Ασίστ", "Κλεψίματα", "Λάθη", "Μπλοκ", "Φαουλ", "PIR"]
            
            # 🔥 ΔΙΟΡΘΩΘΗΚΕ: Εξαναγκασμός εμφάνισης 1 δεκαδικού σε ΟΛΕΣ τις στήλες στατιστικών του πίνακα Νικών/Ηττών
            styled_result = avg_by_result[columns_to_show].style.format({
                "Πόντοι": "{:.1f}",
                "Βολές %": "{:.1f}",
                "Δίποντα %": "{:.1f}",
                "Τρίποντα %": "{:.1f}",
                "Ριμπάουντ Σύνολο": "{:.1f}",
                "Ασίστ": "{:.1f}",
                "Κλεψίματα": "{:.1f}",
                "Λάθη": "{:.1f}",
                "Μπλοκ": "{:.1f}",
                "Φαουλ": "{:.1f}",
                "PIR": "{:.1f}"
            })
            st.dataframe(styled_result, use_container_width=True, hide_index=True)

            st.subheader("📊 Οπτική Σύγκριση Στατιστικών (Νίκες vs Ήττες)")
            
            # 🔥 ΠΡΟΣΘΗΚΗ: Δυναμική επιλογή στατιστικού για το γράφημα σύγκρισης
            chart_cols = ["Πόντοι", "Βολές %", "Δίποντα %", "Τρίποντα %", "Ριμπάουντ Σύνολο", "Ασίστ", "Κλεψίματα", "Λάθη", "Μπλοκ", "Φαουλ", "PIR"]
            selected_stat_group = st.selectbox("Επιλέξτε Στατιστικό για Οπτική Σύγκριση", chart_cols)
            
            # Σχεδίαση του γραφήματος με βάση την επιλογή
            fig = px.bar(
                avg_by_result, 
                x="Αποτέλεσμα", 
                y=selected_stat_group, 
                text_auto=True, 
                color="Αποτέλεσμα",
                color_discrete_map={"ΝΙΚΗ": "#2ca02c", "ΗΤΤΑ": "#d62728"}, # Πράσινο για νίκη, Κόκκινο για ήττα
                title=f"Σύγκριση: Μέσος Όρος στην κατηγορία '{selected_stat_group}'"
            )
            st.plotly_chart(fig, use_container_width=True)
