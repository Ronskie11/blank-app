import streamlit as st

st.title("🎈 Project Zeus")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd


st.title("📊 Weekly Case Completion Tracker")

st.markdown("Use the inputs below to dynamically generate the weekly case glidepath based on workforce variables.")

# Input fields
headcount = st.number_input("👥 Headcount (HC)", min_value=1, step=1, value=20)
aht = st.number_input("⏱️ Average Handling Time (AHT) in minutes", min_value=1.0, step=1.0, value=15.0)
out_of_office = st.slider("🌴 Out-of-office Shrinkage (%)", 0, 100, 10)
in_office = st.slider("🏢 In-office Shrinkage (%)", 0, 100, 5)
attrition = st.slider("🔻 Attrition Rate (%)", 0, 100, 2)
network_days = st.number_input("📅 Working Days in the Week (Networkdays)", min_value=1, max_value=7, value=5)

# Calculations
effective_hc = headcount * (1 - out_of_office / 100) * (1 - in_office / 100) * (1 - attrition / 100)
minutes_available = effective_hc * network_days * 8 * 60  # 8 working hours/day
total_cases_possible = minutes_available / aht

# Weekly glidepath
glidepath = []
for day in range(1, network_days + 1):
    daily_target = total_cases_possible / network_days
    glidepath.append({
        "Day": f"Day {day}",
        "Target Cases": round(daily_target)
    })

df = pd.DataFrame(glidepath)

# Display metrics
st.subheader("📈 Glidepath Projection")
st.metric("Estimated Total Cases Possible", round(total_cases_possible))
st.metric("Effective Headcount", round(effective_hc, 2))

# Display chart
st.line_chart(df.set_index("Day"))

# Display table
st.dataframe(df, use_container_width=True)

# File download
file_format = st.selectbox("Choose download format:", ["CSV", "Excel"])

if file_format == "CSV":
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="weekly_glidepath.csv", mime="text/csv")
else:
    import io
    from openpyxl import Workbook

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Glidepath')
    writer.close()
    st.download_button("📥 Download Excel", data=output.getvalue(), file_name="weekly_glidepath.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("⚙️ Adjust the sliders and inputs above to recalculate your weekly targets in real time.")