
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==========================================
# 1. KONFIGURASI DASHBOARD
# ==========================================

st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "main_data.csv"

st.title("🚲 Bike Sharing Analytics Dashboard")
st.caption(
    "Analisis pola penyewaan sepeda berdasarkan waktu, "
    "pengguna, cuaca, dan karakteristik aktivitas."
)


# ==========================================
# 2. LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["dteday"] = pd.to_datetime(
        df["dteday"],
        errors="coerce"
    )

    numeric_cols = [
        "cnt", "casual", "registered", "hr",
        "temp_c", "hum_pct", "windspeed_kmh"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.dropna(
        subset=["dteday", "cnt", "hr"]
    ).copy()

    df["bulan"] = df["dteday"].dt.to_period("M").astype(str)

    df["tanggal"] = df["dteday"].dt.date

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "File main_data.csv tidak ditemukan. "
        "Pastikan file berada di folder dashboard."
    )
    st.stop()
except Exception as e:
    st.error(f"Gagal membaca dataset: {e}")
    st.stop()


# ==========================================
# 3. SIDEBAR FILTER
# ==========================================

st.sidebar.header("🔎 Filter Analisis")

min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = end_date = date_range


def get_options(column):
    return sorted(df[column].dropna().unique().tolist())


selected_year = st.sidebar.multiselect(
    "Tahun",
    options=get_options("year"),
    default=get_options("year")
)

selected_season = st.sidebar.multiselect(
    "Musim",
    options=get_options("season_label"),
    default=get_options("season_label")
)

selected_weather = st.sidebar.multiselect(
    "Kondisi Cuaca",
    options=get_options("weather_label"),
    default=get_options("weather_label")
)

selected_day_type = st.sidebar.multiselect(
    "Jenis Hari",
    options=get_options("day_type"),
    default=get_options("day_type")
)

pages = [
    ("Overview", "🏠 Overview"),
    ("Customer Analysis", "👥 Customer Analysis"),
    ("Simulation Lab", "🧪 Simulation Lab"),
    ("Capacity Planning", "📦 Capacity Planning"),
    ("Data Explorer", "🔎 Data Explorer")
]

if "dashboard_page" not in st.session_state:
    st.session_state["dashboard_page"] = "Overview"

page = st.session_state["dashboard_page"]


# ==========================================
# 4. FILTER DATA
# ==========================================

filtered_df = df[
    (df["dteday"].dt.date >= start_date)
    & (df["dteday"].dt.date <= end_date)
    & (df["year"].isin(selected_year))
    & (df["season_label"].isin(selected_season))
    & (df["weather_label"].isin(selected_weather))
    & (df["day_type"].isin(selected_day_type))
].copy()

if filtered_df.empty:
    st.warning(
        "Tidak ada data untuk kombinasi filter tersebut. "
        "Silakan ubah filter."
    )
    st.stop()


def render_customer_analysis(data):
    """Render customer behavior analysis using the active filtered data."""
    st.header("👥 Customer Analysis")
    st.caption(
        "Analisis ini menggambarkan perilaku historis pengguna pada filter aktif."
    )

    total_casual = data["casual"].sum()
    total_registered = data["registered"].sum()
    total_users = total_casual + total_registered
    casual_share = total_casual / total_users * 100 if total_users else 0
    registered_share = (
        total_registered / total_users * 100 if total_users else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Casual", f"{total_casual:,.0f}")
    col2.metric("Total Registered", f"{total_registered:,.0f}")
    col3.metric("Proporsi Casual", f"{casual_share:.1f}%")
    col4.metric("Proporsi Registered", f"{registered_share:.1f}%")

    user_data = pd.DataFrame({
        "Kategori": ["Casual", "Registered"],
        "Total": [total_casual, total_registered]
    })

    col1, col2 = st.columns(2)
    with col1:
        fig_share = px.pie(
            user_data,
            names="Kategori",
            values="Total",
            hole=0.55,
            title="Proporsi Pengguna"
        )
        fig_share.update_traces(textinfo="percent+label")
        fig_share.update_layout(template="plotly_white")
        st.plotly_chart(fig_share, use_container_width=True)

    hourly_users = (
        data.groupby("hr", as_index=False)
        .agg(casual=("casual", "mean"), registered=("registered", "mean"))
    )
    with col2:
        fig_hourly = go.Figure()
        fig_hourly.add_trace(go.Scatter(
            x=hourly_users["hr"],
            y=hourly_users["casual"],
            mode="lines+markers",
            name="Casual"
        ))
        fig_hourly.add_trace(go.Scatter(
            x=hourly_users["hr"],
            y=hourly_users["registered"],
            mode="lines+markers",
            name="Registered"
        ))
        fig_hourly.update_layout(
            title="Pola Pengguna Berdasarkan Jam",
            xaxis_title="Jam",
            yaxis_title="Rata-rata Penyewaan",
            template="plotly_white",
            xaxis=dict(dtick=1)
        )
        st.plotly_chart(fig_hourly, use_container_width=True)

    st.subheader("Perbandingan Hari Kerja dan Akhir Pekan")
    day_type_users = (
        data.groupby("day_type", as_index=False)
        .agg(
            casual_avg=("casual", "mean"),
            registered_avg=("registered", "mean")
        )
    )
    fig_day_type = go.Figure()
    fig_day_type.add_trace(go.Bar(
        x=day_type_users["day_type"],
        y=day_type_users["casual_avg"],
        name="Casual"
    ))
    fig_day_type.add_trace(go.Bar(
        x=day_type_users["day_type"],
        y=day_type_users["registered_avg"],
        name="Registered"
    ))
    fig_day_type.update_layout(
        barmode="group",
        title="Rata-rata Penyewaan Menurut Jenis Hari",
        xaxis_title="Jenis Hari",
        yaxis_title="Rata-rata Penyewaan",
        template="plotly_white"
    )
    st.plotly_chart(fig_day_type, use_container_width=True)

    st.subheader("Simulasi Hipotetis Perpindahan Casual ke Registered")
    conversion_rate = st.slider(
        "Persentase Casual yang diasumsikan berpindah menjadi Registered",
        min_value=0,
        max_value=100,
        value=10,
        step=5,
        format="%d%%",
        key="customer_conversion_rate"
    )
    converted_users = total_casual * conversion_rate / 100
    simulated_casual = total_casual - converted_users
    simulated_registered = total_registered + converted_users

    simulation_data = pd.DataFrame({
        "Kategori": ["Casual", "Registered"],
        "Baseline": [total_casual, total_registered],
        "Simulasi": [simulated_casual, simulated_registered]
    })
    fig_conversion = px.bar(
        simulation_data,
        x="Kategori",
        y=["Baseline", "Simulasi"],
        barmode="group",
        title="Baseline vs Simulasi Komposisi Pengguna",
        labels={"value": "Total Pengguna", "variable": "Kondisi"}
    )
    fig_conversion.update_layout(template="plotly_white")
    st.plotly_chart(fig_conversion, use_container_width=True)
    st.info(
        f"Simulasi hipotetis: {converted_users:,.0f} penyewaan pengguna "
        "diasumsikan berpindah kategori. Dataset asli tidak diubah."
    )


def render_simulation_lab(data):
    """Render a non-predictive what-if demand simulation."""
    st.markdown(
        """
        <div style="background-color:#f7f9fc;padding:1.2rem 1.4rem;
        border-radius:0.6rem;border:1px solid #dfe5ec;margin-bottom:1rem;">
        <h1 style="margin:0;color:#1f3a5f;">🧪 Simulation Lab</h1>
        <p style="margin:0.4rem 0 0;color:#52606d;">
        Uji skenario perubahan permintaan secara interaktif.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption(
        "What-if analysis berbasis data historis terfilter; hasilnya bukan "
        "prediksi aktual dan tidak mengubah dataset asli."
    )
    demand_change = st.slider(
        "Perubahan permintaan penyewaan",
        min_value=-50,
        max_value=50,
        value=0,
        step=5,
        format="%d%%",
        key="demand_change"
    )
    baseline_total = data["cnt"].sum()
    simulated_total = baseline_total * (1 + demand_change / 100)
    difference = simulated_total - baseline_total

    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline", f"{baseline_total:,.0f}")
    col2.metric("Hasil Simulasi", f"{simulated_total:,.0f}")
    col3.metric("Selisih", f"{difference:+,.0f}")

    comparison = pd.DataFrame({
        "Kondisi": ["Baseline", "Simulasi"],
        "Total Penyewaan": [baseline_total, simulated_total]
    })
    fig_comparison = px.bar(
        comparison,
        x="Kondisi",
        y="Total Penyewaan",
        text_auto=".0f",
        title="Perbandingan Total Penyewaan"
    )
    fig_comparison.update_layout(template="plotly_white")
    st.plotly_chart(fig_comparison, use_container_width=True)

    if demand_change > 0:
        interpretation = (
            f"Permintaan simulasi meningkat {demand_change}%, sehingga total "
            f"bertambah sekitar {difference:,.0f} penyewaan dibanding baseline."
        )
    elif demand_change < 0:
        interpretation = (
            f"Permintaan simulasi menurun {abs(demand_change)}%, sehingga total "
            f"berkurang sekitar {abs(difference):,.0f} penyewaan dibanding baseline."
        )
    else:
        interpretation = "Tidak ada perubahan permintaan pada skenario simulasi."
    st.info(interpretation)


def render_capacity_planning(data):
    """Render capacity threshold analysis as an explicit simulation parameter."""
    st.header("📦 Capacity Planning")
    st.caption(
        "Ambang kapasitas adalah parameter simulasi manual, bukan jumlah "
        "armada aktual yang tersedia."
    )
    hourly_demand = (
        data.groupby("hr", as_index=False)
        .agg(avg_rentals=("cnt", "mean"))
        .sort_values("hr")
    )
    max_demand = max(1, int(np.ceil(hourly_demand["avg_rentals"].max())))
    capacity_threshold = st.slider(
        "Ambang kapasitas penyewaan per jam",
        min_value=1,
        max_value=max_demand * 2,
        value=max(1, int(round(hourly_demand["avg_rentals"].median()))),
        step=1,
        key="capacity_threshold"
    )
    hourly_demand["capacity"] = capacity_threshold
    exceeds = hourly_demand[hourly_demand["avg_rentals"] > capacity_threshold]

    fig_capacity = go.Figure()
    fig_capacity.add_trace(go.Bar(
        x=hourly_demand["hr"],
        y=hourly_demand["avg_rentals"],
        name="Rata-rata Permintaan"
    ))
    fig_capacity.add_trace(go.Scatter(
        x=hourly_demand["hr"],
        y=hourly_demand["capacity"],
        mode="lines",
        name="Ambang Kapasitas",
        line=dict(color="#d62728", dash="dash")
    ))
    fig_capacity.update_layout(
        title="Permintaan Rata-rata per Jam dan Ambang Kapasitas",
        xaxis_title="Jam",
        yaxis_title="Rata-rata Penyewaan",
        template="plotly_white",
        xaxis=dict(dtick=1)
    )
    st.plotly_chart(fig_capacity, use_container_width=True)
    st.metric("Jumlah Jam Melampaui Ambang", len(exceeds))
    if exceeds.empty:
        st.success("Tidak ada jam yang melampaui ambang kapasitas pada filter aktif.")
    else:
        st.warning("Jam berikut berpotensi membutuhkan perhatian operasional.")
        st.dataframe(
            exceeds.rename(columns={
                "hr": "Jam",
                "avg_rentals": "Rata-rata Permintaan",
                "capacity": "Ambang Kapasitas"
            }),
            use_container_width=True,
            hide_index=True
        )


def render_data_explorer(data):
    """Render filtered data exploration and export controls."""
    st.header("🔎 Data Explorer")
    st.caption("Eksplorasi hanya menggunakan data yang sesuai filter global aktif.")
    available_columns = data.columns.tolist()
    selected_columns = st.multiselect(
        "Kolom yang ditampilkan",
        options=available_columns,
        default=available_columns,
        key="explorer_columns"
    )
    if not selected_columns:
        st.warning("Pilih setidaknya satu kolom untuk menampilkan tabel.")
        return

    display_data = data[selected_columns].copy()
    st.dataframe(display_data, use_container_width=True, hide_index=True)
    st.download_button(
        "Download hasil filter (CSV)",
        data=display_data.to_csv(index=False).encode("utf-8"),
        file_name="bike_sharing_filtered.csv",
        mime="text/csv"
    )

    numeric_data = display_data.select_dtypes(include=np.number)
    st.subheader("Statistik Deskriptif Numerik")
    if numeric_data.empty:
        st.info("Tidak ada kolom numerik pada pilihan saat ini.")
    else:
        st.dataframe(
            numeric_data.describe().transpose(),
            use_container_width=True
        )


# ==========================================
# 5. KPI UTAMA
# ==========================================

total_rentals = filtered_df["cnt"].sum()
average_rentals = filtered_df["cnt"].mean()
total_casual = filtered_df["casual"].sum()
total_registered = filtered_df["registered"].sum()

peak_hour = (
    filtered_df.groupby("hr")["cnt"]
    .mean()
    .idxmax()
)

peak_value = (
    filtered_df.groupby("hr")["cnt"]
    .mean()
    .max()
)

casual_percentage = (
    total_casual / total_rentals * 100
    if total_rentals > 0 else 0
)

registered_percentage = (
    total_registered / total_rentals * 100
    if total_rentals > 0 else 0
)

st.subheader("📊 Ringkasan Performa Penyewaan")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Penyewaan",
    f"{total_rentals:,.0f}"
)

col2.metric(
    "Rata-rata Penyewaan/Jam",
    f"{average_rentals:,.1f}"
)

col3.metric(
    "Jam Puncak",
    f"{int(peak_hour):02d}:00"
)

col4.metric(
    "Rata-rata pada Jam Puncak",
    f"{peak_value:,.1f}"
)

st.subheader("🧭 Navigasi Fitur")
st.caption("Pilih tombol untuk membuka halaman analisis interaktif.")
navigation_columns = st.columns(len(pages))
for navigation_column, (page_key, page_label) in zip(
    navigation_columns,
    pages
):
    with navigation_column:
        if st.button(
            page_label,
            key=f"navigation_{page_key}",
            use_container_width=True
        ):
            st.session_state["dashboard_page"] = page_key
            st.rerun()

page = st.session_state["dashboard_page"]
if page != "Overview":
    page_renderers = {
        "Customer Analysis": render_customer_analysis,
        "Simulation Lab": render_simulation_lab,
        "Capacity Planning": render_capacity_planning,
        "Data Explorer": render_data_explorer
    }
    page_renderers[page](filtered_df)
    st.stop()

st.divider()


# ==========================================
# 6. OVERVIEW TREN PENYEWAAN
# ==========================================

st.subheader("📈 Tren Penyewaan Sepeda")

daily_trend = (
    filtered_df.groupby("dteday", as_index=False)
    .agg(total_rentals=("cnt", "sum"))
)

fig_trend = px.line(
    daily_trend,
    x="dteday",
    y="total_rentals",
    markers=True,
    title="Tren Total Penyewaan Harian",
    labels={
        "dteday": "Tanggal",
        "total_rentals": "Total Penyewaan"
    }
)

fig_trend.update_layout(
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig_trend, use_container_width=True)


monthly_trend = (
    filtered_df.groupby("bulan", as_index=False)
    .agg(total_rentals=("cnt", "sum"))
)

fig_month = px.bar(
    monthly_trend,
    x="bulan",
    y="total_rentals",
    title="Total Penyewaan Berdasarkan Bulan",
    labels={
        "bulan": "Bulan",
        "total_rentals": "Total Penyewaan"
    },
    text_auto=".2s"
)

fig_month.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig_month, use_container_width=True)

st.divider()


# ==========================================
# 7. ANALISIS POLA WAKTU
# ==========================================

st.subheader("🕒 Analisis Pola Waktu Penyewaan")

col1, col2 = st.columns(2)

hourly_avg = (
    filtered_df.groupby("hr", as_index=False)
    .agg(avg_rentals=("cnt", "mean"))
)

with col1:
    fig_hour = px.bar(
        hourly_avg,
        x="hr",
        y="avg_rentals",
        title="Rata-rata Penyewaan Berdasarkan Jam",
        labels={
            "hr": "Jam",
            "avg_rentals": "Rata-rata Penyewaan"
        }
    )

    fig_hour.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )


day_order = [
    "Senin", "Selasa", "Rabu", "Kamis",
    "Jumat", "Sabtu", "Minggu"
]

weekday_avg = (
    filtered_df.groupby("nama_hari", as_index=False)
    .agg(avg_rentals=("cnt", "mean"))
)

weekday_avg["nama_hari"] = pd.Categorical(
    weekday_avg["nama_hari"],
    categories=day_order,
    ordered=True
)

weekday_avg = weekday_avg.sort_values("nama_hari")

with col2:
    fig_weekday = px.bar(
        weekday_avg,
        x="nama_hari",
        y="avg_rentals",
        title="Rata-rata Penyewaan Berdasarkan Hari",
        labels={
            "nama_hari": "Hari",
            "avg_rentals": "Rata-rata Penyewaan"
        }
    )

    fig_weekday.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_weekday,
        use_container_width=True
    )


# ==========================================
# 8. HEATMAP HARI DAN JAM
# ==========================================

st.subheader("🔥 Distribusi Penyewaan Berdasarkan Hari dan Jam")

heatmap_data = filtered_df.pivot_table(
    index="nama_hari",
    columns="hr",
    values="cnt",
    aggfunc="mean"
)

heatmap_data = heatmap_data.reindex(
    day_order
)

fig_heatmap = px.imshow(
    heatmap_data,
    aspect="auto",
    color_continuous_scale="YlOrRd",
    labels={
        "x": "Jam",
        "y": "Hari",
        "color": "Rata-rata Penyewaan"
    },
    title="Heatmap Rata-rata Penyewaan Sepeda"
)

fig_heatmap.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

st.divider()


# ==========================================
# 9. ANALISIS PENGGUNA
# ==========================================

st.subheader("👥 Analisis Karakteristik Pengguna")

col1, col2 = st.columns(2)

user_data = pd.DataFrame({
    "Kategori": ["Casual", "Registered"],
    "Total": [total_casual, total_registered]
})

with col1:
    fig_user = px.pie(
        user_data,
        names="Kategori",
        values="Total",
        hole=0.55,
        title="Proporsi Jenis Pengguna"
    )

    fig_user.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_user,
        use_container_width=True
    )

with col2:
    user_hour = (
        filtered_df.groupby("hr", as_index=False)
        .agg(
            casual=("casual", "mean"),
            registered=("registered", "mean")
        )
    )

    fig_user_hour = go.Figure()

    fig_user_hour.add_trace(
        go.Scatter(
            x=user_hour["hr"],
            y=user_hour["casual"],
            mode="lines+markers",
            name="Casual"
        )
    )

    fig_user_hour.add_trace(
        go.Scatter(
            x=user_hour["hr"],
            y=user_hour["registered"],
            mode="lines+markers",
            name="Registered"
        )
    )

    fig_user_hour.update_layout(
        title="Pola Pengguna Berdasarkan Jam",
        xaxis_title="Jam",
        yaxis_title="Rata-rata Penyewaan",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_user_hour,
        use_container_width=True
    )

st.divider()


# ==========================================
# 10. ANALISIS MUSIM DAN CUACA
# ==========================================

st.subheader("🌦️ Analisis Musim dan Cuaca")

col1, col2 = st.columns(2)

season_avg = (
    filtered_df.groupby("season_label", as_index=False)
    .agg(avg_rentals=("cnt", "mean"))
)

with col1:
    fig_season = px.bar(
        season_avg,
        x="season_label",
        y="avg_rentals",
        title="Rata-rata Penyewaan Berdasarkan Musim",
        labels={
            "season_label": "Musim",
            "avg_rentals": "Rata-rata Penyewaan"
        }
    )

    fig_season.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_season,
        use_container_width=True
    )


weather_avg = (
    filtered_df.groupby("weather_label", as_index=False)
    .agg(avg_rentals=("cnt", "mean"))
    .sort_values("avg_rentals", ascending=False)
)

with col2:
    fig_weather = px.bar(
        weather_avg,
        x="weather_label",
        y="avg_rentals",
        title="Rata-rata Penyewaan Berdasarkan Cuaca",
        labels={
            "weather_label": "Kondisi Cuaca",
            "avg_rentals": "Rata-rata Penyewaan"
        }
    )

    fig_weather.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_weather,
        use_container_width=True
    )


# ==========================================
# 11. ANALISIS LINGKUNGAN
# ==========================================

st.subheader("🌡️ Hubungan Kondisi Lingkungan dan Penyewaan")

environment_cols = [
    "temp_c",
    "hum_pct",
    "windspeed_kmh"
]

environment_cols = [
    c for c in environment_cols
    if c in filtered_df.columns
]

if environment_cols:
    correlation_data = filtered_df[
        environment_cols + ["cnt"]
    ].corr(numeric_only=True)

    fig_corr = px.imshow(
        correlation_data,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Korelasi Variabel Lingkungan dan Penyewaan"
    )

    fig_corr.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

    st.caption(
        "Korelasi menunjukkan hubungan statistik, "
        "bukan bukti hubungan sebab-akibat."
    )


# ==========================================
# 12. ADVANCED ANALYTICS
# ==========================================

st.divider()

st.header("🔬 Advanced Analytics")

st.caption(
    "Analisis lanjutan untuk mengidentifikasi "
    "karakteristik intensitas dan pola permintaan."
)


# A. Segmentasi Intensitas Penyewaan

st.subheader("A. Segmentasi Intensitas Penyewaan")

segment_avg = (
    filtered_df.groupby("segmen", as_index=False)
    .agg(
        avg_rentals=("cnt", "mean"),
        total_rentals=("cnt", "sum"),
        observations=("cnt", "count")
    )
    .sort_values("avg_rentals", ascending=False)
)

fig_segment = px.bar(
    segment_avg,
    x="segmen",
    y="avg_rentals",
    color="avg_rentals",
    color_continuous_scale="YlOrRd",
    text_auto=".2f",
    title="Rata-rata Penyewaan Berdasarkan Segmen Waktu",
    labels={
        "segmen": "Segmen Waktu",
        "avg_rentals": "Rata-rata Penyewaan"
    }
)

fig_segment.update_layout(
    template="plotly_white",
    showlegend=False
)

st.plotly_chart(
    fig_segment,
    use_container_width=True
)

st.dataframe(
    segment_avg,
    use_container_width=True,
    hide_index=True
)


# B. Perbandingan Hari Kerja dan Akhir Pekan

st.subheader("B. Perbandingan Intensitas Jam Puncak")

peak_comparison = (
    filtered_df.groupby(
        ["day_type", "hr"],
        as_index=False
    )
    .agg(avg_rentals=("cnt", "mean"))
)

peak_hours = (
    peak_comparison.loc[
        peak_comparison.groupby("day_type")[
            "avg_rentals"
        ].idxmax()
    ]
    .sort_values("day_type")
)

fig_peak = px.line(
    peak_comparison,
    x="hr",
    y="avg_rentals",
    color="day_type",
    markers=True,
    title="Perbandingan Pola Penyewaan per Jam",
    labels={
        "hr": "Jam",
        "avg_rentals": "Rata-rata Penyewaan",
        "day_type": "Jenis Hari"
    }
)

fig_peak.update_layout(
    template="plotly_white",
    xaxis=dict(dtick=1)
)

st.plotly_chart(
    fig_peak,
    use_container_width=True
)

st.markdown("**Jam puncak masing-masing jenis hari:**")

st.dataframe(
    peak_hours.rename(columns={
        "day_type": "Jenis Hari",
        "hr": "Jam Puncak",
        "avg_rentals": "Rata-rata Penyewaan"
    }),
    use_container_width=True,
    hide_index=True
)


# C. Analisis Perilaku Pengguna

st.subheader("C. Perbandingan Perilaku Pengguna")

user_behavior = (
    filtered_df.groupby("day_type", as_index=False)
    .agg(
        casual_avg=("casual", "mean"),
        registered_avg=("registered", "mean")
    )
)

fig_behavior = go.Figure()

fig_behavior.add_trace(
    go.Bar(
        x=user_behavior["day_type"],
        y=user_behavior["casual_avg"],
        name="Casual"
    )
)

fig_behavior.add_trace(
    go.Bar(
        x=user_behavior["day_type"],
        y=user_behavior["registered_avg"],
        name="Registered"
    )
)

fig_behavior.update_layout(
    barmode="group",
    title="Rata-rata Penyewaan Menurut Jenis Pengguna dan Hari",
    xaxis_title="Jenis Hari",
    yaxis_title="Rata-rata Penyewaan",
    template="plotly_white"
)

st.plotly_chart(
    fig_behavior,
    use_container_width=True
)


# ==========================================
# 13. INSIGHT OTOMATIS
# ==========================================

st.divider()

st.header("💡 Ringkasan Temuan Data")

best_day = (
    filtered_df.groupby("nama_hari")["cnt"]
    .mean()
    .idxmax()
)

best_weather = (
    filtered_df.groupby("weather_label")["cnt"]
    .mean()
    .idxmax()
)

best_season = (
    filtered_df.groupby("season_label")["cnt"]
    .mean()
    .idxmax()
)

st.markdown(
    f"""
    - **Hari dengan rata-rata penyewaan tertinggi:** {best_day}.
    - **Kondisi cuaca dengan rata-rata penyewaan tertinggi:** {best_weather}.
    - **Musim dengan rata-rata penyewaan tertinggi:** {best_season}.
    - **Jam puncak pada filter aktif:** {int(peak_hour):02d}:00.
    - **Kontribusi pengguna terdaftar:** {registered_percentage:.1f}%.
    - **Kontribusi pengguna kasual:** {casual_percentage:.1f}%.
    """
)

st.caption(
    "Seluruh ringkasan mengikuti data dan filter yang sedang aktif."
)


# ==========================================
# 14. FOOTER
# ==========================================

st.divider()

st.caption(
    "Bike Sharing Data Analysis | Final Project "
    "| Python, Pandas, Plotly & Streamlit"
)

st.caption(
    f"Menampilkan {len(filtered_df):,} dari {len(df):,} "
    "observasi dataset."
)
