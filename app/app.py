import streamlit as st
import pandas as pd, numpy as np, joblib, json
from pathlib import Path

st.set_page_config(
    page_title="CropEthiopia",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)
BASE = Path(__file__).parent
ROOT = BASE.parent
model = joblib.load(BASE / "assets/final_model.joblib")
weather = pd.read_csv(BASE / "assets/clean_weather.csv")
prices = pd.read_csv(BASE / "assets/clean_prices.csv")
bench = pd.read_csv(BASE / "assets/benchmarks.csv")
meta = json.loads((BASE / "assets/model_metadata.json").read_text())
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
mnum = {m: i + 1 for i, m in enumerate(months)}

# ---------- UI theme ----------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

with st.sidebar:
    st.markdown(
        '<div class="brand-wrap"><div class="brand-mark">CY</div><div><div class="brand-name">CropEthiopia</div><div class="brand-sub">Ethiopian farm intelligence</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-label">WORKSPACE</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["Home", "Analysis", "Prediction", "Model & Project", "Alpha Team"],
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="side-label theme-label">APPEARANCE</div>', unsafe_allow_html=True
    )
    st.session_state.theme = st.selectbox(
        "Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1,
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="side-note"><div class="note-dot"></div><div><b>Leakage-safe design</b><br><span>Weather supports yield prediction. Price is used only after prediction for revenue.</span></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="side-footer">Qiyas / IADE · Crop-Yield Challenge<br><span>Analysis → Model → Decision</span></div>',
        unsafe_allow_html=True,
    )

DARK = st.session_state.theme == "Dark"
if DARK:
    bg = "#0B0F14"
    panel = "#111820"
    panel2 = "#151E27"
    text = "#F4F7F5"
    muted = "#8FA39A"
    border = "#24322C"
    accent = "#7ED957"
    accent2 = "#28C99A"
    soft = "#14251E"
    shadow = "rgba(0,0,0,.30)"
    side = "#0F151C"
else:
    bg = "#F5F8F5"
    panel = "#FFFFFF"
    panel2 = "#F0F5F1"
    text = "#142019"
    muted = "#66776E"
    border = "#DDE7E0"
    accent = "#247A4A"
    accent2 = "#0E9F78"
    soft = "#EAF5EE"
    shadow = "rgba(31,65,45,.10)"
    side = "#EEF4EF"

st.markdown(
    f"""<style>
:root{{--bg:{bg};--panel:{panel};--panel2:{panel2};--text:{text};--muted:{muted};--border:{border};--accent:{accent};--accent2:{accent2};--soft:{soft};--shadow:{shadow};}}
.stApp{{background:var(--bg);color:var(--text)}}
.block-container{{padding-top:2rem;padding-bottom:4rem;max-width:1320px}}
[data-testid="stSidebar"]{{background:{side};border-right:1px solid var(--border)}}
[data-testid="stSidebar"] > div:first-child{{padding-top:1.25rem}}
.brand-wrap{{display:flex;align-items:center;gap:12px;padding:10px 7px 22px}}
.brand-mark{{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;font-weight:900;letter-spacing:-1px;background:linear-gradient(145deg,var(--accent),var(--accent2));color:#07120C;box-shadow:0 10px 28px var(--shadow)}}
.brand-name{{font-size:1.12rem;font-weight:800;color:var(--text);letter-spacing:-.02em}}
.brand-sub{{font-size:.72rem;color:var(--muted);margin-top:2px}}
.side-label{{font-size:.66rem;font-weight:800;letter-spacing:.14em;color:var(--muted);margin:4px 8px 8px}}
.theme-label{{margin-top:24px}}
[data-testid="stSidebar"] [role="radiogroup"]{{gap:7px}}
[data-testid="stSidebar"] [role="radiogroup"] label{{background:transparent;border:1px solid transparent;border-radius:13px;padding:8px 10px;transition:.18s ease}}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{{background:var(--panel2);border-color:var(--border);transform:translateX(2px)}}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){{background:var(--soft);border-color:var(--accent);box-shadow:0 8px 22px var(--shadow)}}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{{color:var(--accent);font-weight:800}}
.side-note{{display:flex;gap:10px;padding:14px;margin-top:24px;border-radius:15px;background:var(--panel);border:1px solid var(--border);color:var(--text);box-shadow:0 10px 28px var(--shadow)}}
.side-note span{{font-size:.75rem;color:var(--muted);line-height:1.45}}
.note-dot{{width:9px;height:9px;min-width:9px;margin-top:5px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 5px var(--soft)}}
.side-footer{{position:relative;margin:26px 8px 8px;color:var(--muted);font-size:.72rem;line-height:1.6}}
.side-footer span{{color:var(--accent)}}
.hero{{position:relative;overflow:hidden;padding:2.35rem 2.5rem;border-radius:28px;background:linear-gradient(120deg,#123D2A 0%,#176447 55%,#15966A 100%);color:white;margin-bottom:1.6rem;box-shadow:0 20px 55px var(--shadow)}}
.hero:after{{content:"";position:absolute;width:270px;height:270px;border-radius:50%;right:-70px;top:-120px;background:rgba(255,255,255,.10)}}
.hero:before{{content:"";position:absolute;width:160px;height:160px;border-radius:50%;right:130px;bottom:-110px;border:28px solid rgba(255,255,255,.07)}}
.hero h1{{position:relative;margin:0;font-size:2.5rem;letter-spacing:-.045em;z-index:1;color:white}}
.hero p{{position:relative;margin:.65rem 0 0;color:#DDF5E8;max-width:760px;font-size:1.02rem;z-index:1}}
.card{{padding:1.3rem 1.35rem;border-radius:20px;border:1px solid var(--border);background:var(--panel);height:100%;box-shadow:0 12px 35px var(--shadow);color:var(--text);transition:.2s ease}}
.card:hover{{transform:translateY(-3px);border-color:var(--accent)}}
.card b{{font-size:1.35rem;color:var(--text)}}
.small{{color:var(--muted);font-size:.88rem}}
.lookup{{padding:1.1rem 1.2rem;border-radius:17px;background:var(--soft);border:1px solid var(--border);color:var(--text)}}
[data-testid="stMetric"]{{background:var(--panel);border:1px solid var(--border);padding:15px 17px;border-radius:18px;box-shadow:0 10px 30px var(--shadow)}}
[data-testid="stMetricLabel"]{{color:var(--muted)}}
.stButton>button{{width:100%;border-radius:14px;height:3.15rem;font-weight:800;border:0;background:linear-gradient(90deg,var(--accent),var(--accent2));color:#07120C;box-shadow:0 10px 25px var(--shadow)}}
.stButton>button:hover{{transform:translateY(-1px);filter:brightness(1.04)}}
h1,h2,h3,p,label{{color:var(--text)}}
[data-testid="stTabs"] button p{{font-weight:700}}
[data-testid="stImage"] img{{border-radius:18px;border:1px solid var(--border);box-shadow:0 12px 35px var(--shadow)}}
div[data-baseweb="select"] > div, [data-testid="stNumberInput"] input{{border-radius:12px!important}}
.home-photo-hero{{position:relative;min-height:410px;border-radius:30px;overflow:hidden;margin-bottom:1.4rem;background-image:linear-gradient(90deg,rgba(5,25,16,.91) 0%,rgba(8,49,31,.73) 48%,rgba(8,35,25,.18) 100%),url("https://www.fao.org/images/newsroomlibraries/import-library/mg_6335.jpg");background-size:cover;background-position:center;box-shadow:0 24px 65px var(--shadow);border:1px solid var(--border)}}
.home-photo-content{{position:absolute;left:0;bottom:0;padding:2.4rem 2.5rem;max-width:760px;color:white}}
.home-kicker{{display:inline-flex;padding:.38rem .7rem;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);font-size:.72rem;font-weight:800;letter-spacing:.11em;margin-bottom:1rem}}
.home-photo-content h1{{font-size:3rem;line-height:1.03;letter-spacing:-.055em;color:white;margin:0 0 .8rem}}
.home-photo-content p{{font-size:1.05rem;line-height:1.65;color:#E7F7ED;max-width:650px;margin:0}}
.pill-row{{display:flex;gap:.55rem;flex-wrap:wrap;margin-top:1.25rem}}
.pill{{padding:.42rem .72rem;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);font-size:.78rem;color:white}}
.story-card{{padding:1.25rem;border-radius:22px;background:var(--panel);border:1px solid var(--border);box-shadow:0 12px 35px var(--shadow);height:100%}}
.story-num{{width:36px;height:36px;border-radius:12px;background:var(--soft);color:var(--accent);display:grid;place-items:center;font-weight:900;margin-bottom:.8rem}}
.story-title{{font-weight:850;font-size:1rem;margin-bottom:.3rem;color:var(--text)}}
.story-copy{{font-size:.84rem;color:var(--muted);line-height:1.55}}
.section-eyebrow{{font-size:.72rem;letter-spacing:.12em;font-weight:850;color:var(--accent);margin-top:1.2rem;margin-bottom:.25rem}}
.insight-strip{{display:flex;gap:1rem;align-items:center;padding:1.15rem 1.25rem;border-radius:18px;background:linear-gradient(110deg,var(--soft),var(--panel));border:1px solid var(--border);margin:1rem 0 1.3rem}}
.insight-icon{{font-size:1.6rem}}
@media(max-width:800px){{.home-photo-hero{{min-height:460px}}.home-photo-content{{padding:1.5rem}}.home-photo-content h1{{font-size:2.25rem}}}}
</style>""",
    unsafe_allow_html=True,
)


def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def show_image(name, caption=None):
    p = ROOT / "figures" / name
    if p.exists():
        st.image(str(p), caption=caption, use_container_width=True)


def lookup_weather(region, year, planting):
    rows = []
    start = mnum[planting]
    for off in range(4):
        n = start + off
        yy = year + (n - 1) // 12
        mm = months[(n - 1) % 12]
        q = weather[
            (weather.region == region) & (weather.year == yy) & (weather.month == mm)
        ]
        if len(q):
            rows.append(q.iloc[0])
    return pd.DataFrame(rows)


def context_values(region, crop, year, planting):
    w = lookup_weather(region, year, planting)
    if w.empty:
        return None
    p = prices[
        (prices.region == region) & (prices.crop_type == crop) & (prices.year == year)
    ]
    if p.empty:
        return None
    bm = bench[
        (bench.region == region)
        & (bench.crop_type == crop)
        & (bench.survey_year == year)
    ]
    if bm.empty:
        bm = bench[(bench.region == region) & (bench.crop_type == crop)]
    typical_rain = (
        float(bm.typical_plot_rainfall_mm.median())
        if len(bm)
        else float(bench.typical_plot_rainfall_mm.median())
    )
    avg_y = (
        float(bm.avg_yield_tons_per_ha.mean()) if len(bm) else float(meta["mean_yield"])
    )
    return w, float(p.price_birr_per_quintal.iloc[0]), typical_rain, avg_y


def make_row(
    region,
    crop,
    year,
    planting,
    alt,
    farm,
    fertilizer,
    soil,
    seed_i,
    pest_i,
    labor,
    dist,
):
    ctx = context_values(region, crop, year, planting)
    if ctx is None:
        return None, None
    w, price, plot_rain, avg_y = ctx
    temp = float(w.avg_temp_c.mean())
    wrain = float(w.monthly_rainfall_mm.sum())
    heat = float(w.extreme_heat_days.sum())
    region_temp = float(weather[weather.region == region].avg_temp_c.mean())
    row = pd.DataFrame(
        [
            {
                "region": region,
                "crop_type": crop,
                "survey_year": year,
                "planting_month": planting,
                "altitude_m": alt,
                "rainfall_mm_season": plot_rain,
                "farm_size_ha": farm,
                "fertilizer_kg_per_ha": fertilizer,
                "improved_seed_used": seed_i,
                "pest_disease_flag": pest_i,
                "soil_quality_index": soil,
                "labor_days_per_ha": labor,
                "distance_to_market_km": dist,
                "season_avg_temp_c": temp,
                "season_rainfall_mm": wrain,
                "season_extreme_heat_days": heat,
                "season_temp_deviation_c": temp - region_temp,
                "planting_month_num": mnum[planting],
                "fertilizer_seed_interaction": fertilizer * seed_i,
                "rainfall_gap_mm": plot_rain - wrain,
            }
        ]
    )[meta["features"]]
    return row, {
        "temp": temp,
        "rain": wrain,
        "heat": heat,
        "price": price,
        "plot_rain": plot_rain,
        "avg_y": avg_y,
        "months": len(w),
    }


if page == "Home":
    st.markdown(
        """<div class="home-photo-hero"><div class="home-photo-content"><div class="home-kicker">ETHIOPIAN SMALLHOLDER INTELLIGENCE</div><h1>From field data to smarter yield decisions.</h1><p>CropYield AI connects farm conditions, growing-season weather and machine learning to estimate crop yield and turn predictions into practical farm revenue insights.</p><div class="pill-row"><span class="pill">5 regions</span><span class="pill">5 crops</span><span class="pill">15,090 training plots</span><span class="pill">LightGBM</span></div></div></div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-eyebrow">PROJECT AT A GLANCE</div>', unsafe_allow_html=True
    )
    st.subheader("Built around the full crop-yield workflow")
    a, b, c = st.columns(3)
    a.markdown(
        '<div class="card"><b>15,090</b><br>training farm plots<br><span class="small">Five Ethiopian regions and five crop types</span></div>',
        unsafe_allow_html=True,
    )
    b.markdown(
        '<div class="card"><b>3,750</b><br>competition test plots<br><span class="small">Final unseen plots receive yield predictions</span></div>',
        unsafe_allow_html=True,
    )
    c.markdown(
        '<div class="card"><b>3 sources</b><br>farm + weather + prices<br><span class="small">Price is used for revenue, never as a yield feature</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-eyebrow">HOW IT WORKS</div>', unsafe_allow_html=True
    )
    st.subheader("One pipeline, from raw data to a farm decision")
    s1, s2, s3, s4 = st.columns(4)
    s1.markdown(
        '<div class="story-card"><div class="story-num">01</div><div class="story-title">Clean</div><div class="story-copy">Fix missing, invalid and inconsistent farm, weather and price records.</div></div>',
        unsafe_allow_html=True,
    )
    s2.markdown(
        '<div class="story-card"><div class="story-num">02</div><div class="story-title">Connect</div><div class="story-copy">Join each plot to its planting month plus the following three weather months.</div></div>',
        unsafe_allow_html=True,
    )
    s3.markdown(
        '<div class="story-card"><div class="story-num">03</div><div class="story-title">Learn</div><div class="story-copy">Analyze agronomic patterns and train leakage-safe regression models.</div></div>',
        unsafe_allow_html=True,
    )
    s4.markdown(
        '<div class="story-card"><div class="story-num">04</div><div class="story-title">Predict</div><div class="story-copy">Estimate yield, automatically look up price and calculate expected revenue.</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-eyebrow">DATA STORY</div>', unsafe_allow_html=True)
    st.subheader("What the farms told us")
    x, y = st.columns(2)
    with x:
        show_image(
            "fig04_region_crop_heatmap.png",
            "Yield varies strongly across region × crop combinations.",
        )
    with y:
        show_image(
            "fig07_yield_vs_season_temp.png",
            "Growing-season temperature is associated with different yield patterns by crop.",
        )
    st.markdown(
        '<div class="insight-strip"><div class="insight-icon">🌱</div><div><b>Agronomic insight</b><br><span class="small">We examined fertilizer, altitude, planting month and distance to market. Distance showed almost no linear relationship with yield (correlation ≈ 0.005), while fertilizer bands showed clearer yield differences.</span></div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-eyebrow">MODEL TO DECISION</div>', unsafe_allow_html=True
    )
    st.subheader("A prediction is useful only when it becomes understandable")
    m1, m2, m3 = st.columns(3)
    m1.markdown(
        '<div class="story-card"><div class="story-title">Weather-aware</div><div class="story-copy">The model uses growing-season temperature, rainfall and extreme-heat information automatically.</div></div>',
        unsafe_allow_html=True,
    )
    m2.markdown(
        '<div class="story-card"><div class="story-title">Leakage-safe</div><div class="story-copy">Market price is excluded from yield prediction and is used only after prediction to estimate revenue.</div></div>',
        unsafe_allow_html=True,
    )
    m3.markdown(
        '<div class="story-card"><div class="story-title">Actionable output</div><div class="story-copy">The Prediction page returns tons/ha, estimated farm revenue, a benchmark and a fertilizer what-if view.</div></div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Homepage farm photograph: FAO imagery of Ethiopian agriculture. Analysis figures are generated from this project data."
    )

elif page == "Analysis":
    hero(
        "Data Analysis",
        "Explore the main patterns we found before building the prediction model.",
    )
    tab1, tab2, tab3 = st.tabs(
        ["Yield patterns", "Agronomic drivers", "Climate & value"]
    )
    with tab1:
        a, b = st.columns(2)
        with a:
            show_image(
                "fig03_yield_distribution.png",
                "Yield distribution overall and by crop.",
            )
        with b:
            show_image(
                "fig04_region_crop_heatmap.png", "Mean yield by region and crop."
            )
        st.write(
            "These views show that crop type and region are important sources of yield variation."
        )
    with tab2:
        st.markdown("### Agronomic drivers")
        st.write(
            "We tested how fertilizer, altitude, planting month and distance to market relate to yield. Fertilizer bands showed higher average yield at higher fertilizer levels, while distance to market had almost zero linear correlation with yield (≈ 0.005). These are associations, not proof of causation."
        )
        show_image(
            "fig05_correlation_heatmap.png",
            "Numeric plot and weather relationships with yield.",
        )
    with tab3:
        a, b = st.columns(2)
        with a:
            show_image(
                "fig06_climate_by_region.png",
                "Regional climate patterns used to build growing-season weather features.",
            )
        with b:
            show_image(
                "fig09_revenue_by_crop_region.png",
                "Estimated revenue per hectare by crop and region.",
            )
        show_image(
            "fig08_price_trends.png",
            "Cleaned crop-price trends used for analysis and revenue estimation only.",
        )

elif page == "Prediction":
    hero(
        "Yield & Revenue Prediction",
        "Enter farm information. Weather and market price are looked up automatically.",
    )
    st.subheader("1. Plot identity")
    a, b, c, d = st.columns(4)
    region = a.selectbox("Region", ["Oromia", "Amhara", "SNNPR", "Tigray", "Somali"])
    crop = b.selectbox("Crop type", ["teff", "wheat", "maize", "sorghum", "barley"])
    year = c.selectbox("Survey year", [2021, 2022, 2023, 2024], index=3)
    planting = d.selectbox("Planting month", months, index=5)
    st.subheader("2. Farm details")
    c1, c2, c3, c4 = st.columns(4)
    alt = c1.number_input("Altitude (m)", 0.0, 5000.0, 1800.0, step=50.0)
    farm = c2.number_input("Farm size (ha)", 0.01, 100.0, 1.0, step=0.1)
    fert = c3.number_input("Fertilizer (kg/ha)", 0.0, 1000.0, 50.0, step=5.0)
    soil = c4.slider("Soil quality index", 0.0, 1.0, 0.5, 0.01)
    c5, c6, c7, c8 = st.columns(4)
    seed = c5.selectbox("Improved seed used?", ["No", "Yes"])
    pest = c6.selectbox("Pest/disease observed?", ["No", "Yes"])
    labor = c7.number_input("Labor days/ha", 0.0, 300.0, 40.0, step=1.0)
    dist = c8.number_input("Distance to market (km)", 0.0, 300.0, 10.0, step=1.0)
    seed_i = int(seed == "Yes")
    pest_i = int(pest == "Yes")
    if st.button("Predict yield & revenue", type="primary"):
        if farm <= 0 or alt < 0 or fert < 0 or labor < 0 or dist < 0:
            st.error(
                "Please enter sensible non-negative plot values and a farm size above zero."
            )
        else:
            row, ctx = make_row(
                region,
                crop,
                year,
                planting,
                alt,
                farm,
                fert,
                soil,
                seed_i,
                pest_i,
                labor,
                dist,
            )
            if row is None:
                st.error(
                    "Weather or price lookup is unavailable for this selection. Please choose another region/year/month combination."
                )
            else:
                pred = max(0.0, float(model.predict(row)[0]))
                revenue = pred * farm * 10 * ctx["price"]
                st.subheader("3. Prediction result")
                x, y, z = st.columns(3)
                x.metric("Predicted yield", f"{pred:.2f} t/ha")
                y.metric("Estimated revenue", f"{revenue:,.0f} birr")
                z.metric("Region/crop benchmark", f"{ctx['avg_y']:.2f} t/ha")
                st.markdown(
                    f"""<div class="lookup"><b>Automatic lookup used</b><br>Season average temperature: <b>{ctx["temp"]:.1f} °C</b> • Station rainfall: <b>{ctx["rain"]:.0f} mm</b> • Extreme-heat days: <b>{ctx["heat"]:.0f}</b> • Price: <b>{ctx["price"]:,.0f} birr/quintal</b><br><span class="small">Weather months found: {ctx["months"]}/4. The app uses a training-derived typical plot rainfall value ({ctx["plot_rain"]:.0f} mm) because plot-reported rainfall is not an app input.</span></div>""",
                    unsafe_allow_html=True,
                )
                st.subheader("Prediction vs benchmark")
                st.bar_chart(
                    pd.DataFrame(
                        {"Yield (tons/ha)": [pred, ctx["avg_y"]]},
                        index=["Your prediction", "Region/crop average"],
                    )
                )
                st.subheader("What-if: fertilizer response")
                levels = np.linspace(max(0, fert - 50), fert + 50, 9)
                vals = []
                for f in levels:
                    rr, _ = make_row(
                        region,
                        crop,
                        year,
                        planting,
                        alt,
                        farm,
                        float(f),
                        soil,
                        seed_i,
                        pest_i,
                        labor,
                        dist,
                    )
                    vals.append(max(0, float(model.predict(rr)[0])))
                st.line_chart(
                    pd.DataFrame(
                        {
                            "Fertilizer (kg/ha)": levels,
                            "Predicted yield (tons/ha)": vals,
                        }
                    ).set_index("Fertilizer (kg/ha)")
                )
                st.caption(
                    "The what-if chart changes fertilizer only. It shows model behavior, not a causal fertilizer recommendation."
                )

elif page == "Model & Project":
    hero(
        "Model & Project",
        "A compact view of model performance, methodology and project deliverables.",
    )
    a, b, c = st.columns(3)
    a.metric("Validation RMSE", "0.459 t/ha")
    b.metric("Validation MAE", "0.336 t/ha")
    c.metric("5-fold CV RMSE", "0.469 ± 0.011")
    st.write(
        "LightGBM was selected after comparing baseline and stronger regression models. Weather-derived features improved validation RMSE from about 0.490 to 0.459 t/ha."
    )
    x, y = st.columns(2)
    with x:
        show_image(
            "fig10_model_comparison.png",
            "Validation performance across model families.",
        )
    with y:
        show_image(
            "fig12_feature_importance.png",
            "Permutation importance, including weather-derived features.",
        )
    st.subheader("Project sections")
    st.write(
        "A — Cleaning & integration • B — Analysis • C — 12 visualization figures • D — Modeling & evaluation • E — This demo • F — 5-slide presentation • G — Reproducible project structure"
    )
    st.info(
        "Final competition test data is used only to create predictions. Model evaluation is performed on held-out training data because the competition test file has no true yield target."
    )


elif page == "Alpha Team":
    hero(
        "Alpha Team",
        "The six-member team behind CropYield AI for the Qiyas / IADE Crop-Yield Challenge.",
    )
    members = [
        ("01", "Saron Hailemichael"),
        ("02", "Abdi Mudesir"),
        ("03", "Meftuha Kedir"),
        ("04", "Wissam Jemal"),
        ("05", "Yedidya Solomon"),
        ("06", "Kidist Dagnachaew"),
    ]
    c1, c2, c3 = st.columns(3)
    for i, (n, name) in enumerate(members):
        col = [c1, c2, c3][i % 3]
        with col:
            st.markdown(
                f"""<div class='story-card'><div class='story-num'>{n}</div><h3>{name}</h3><p>Alpha Team · Data Science / AI Hackathon</p></div>""",
                unsafe_allow_html=True,
            )
    st.info(
        "Project focus: reproducible data cleaning, weather-aware yield modeling, clear analysis, leakage-safe evaluation and an interactive farm decision demo."
    )
