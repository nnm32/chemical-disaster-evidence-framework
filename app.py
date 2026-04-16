import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chemical Disaster Evidence Framework", layout="wide")

st.title("Chemical Disaster Evidence Framework")
st.caption("A structured academic tool for identifying evidence gaps after chemical incidents.")

st.header("1. Incident Intake")

incident_name = st.text_input("Incident name")
country = st.text_input("Country")
incident_date = st.date_input("Incident date")

combustion = st.selectbox(
    "Was there combustion or burn involved?",
    ["Unknown", "Yes", "No"]
)

known_chemicals = st.text_area(
    "Known chemicals on manifest or confirmed",
    placeholder="Example: vinyl chloride, benzene, butyl acrylate"
)

st.header("2. Sampling Coverage")

outdoor_air = st.checkbox("Outdoor air data available")
indoor_air = st.checkbox("Indoor air data available")
water = st.checkbox("Water data available")
soil = st.checkbox("Soil data available")
sediment = st.checkbox("Sediment data available")
biomonitoring = st.checkbox("Human biomonitoring available")

st.header("3. Evidence Gap Flags")

flags = []

if combustion == "Yes":
    flags.append("Combustion occurred → consider unexpected byproducts and need for non-targeted analysis")

if not outdoor_air:
    flags.append("Missing outdoor air data")

if not indoor_air:
    flags.append("Missing indoor air data")

if not biomonitoring:
    flags.append("No human biomonitoring → early exposure data gap")

if not soil:
    flags.append("No soil sampling")

if not sediment:
    flags.append("No sediment sampling")

if len(flags) == 0:
    st.success("No major gaps detected from inputs")
else:
    for f in flags:
        st.warning(f)

st.header("4. Export Summary")

summary = {
    "Incident": incident_name,
    "Country": country,
    "Combustion": combustion,
    "Chemicals": known_chemicals,
    "Flags": " | ".join(flags)
}

df = pd.DataFrame([summary])
st.dataframe(df)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "summary.csv", "text/csv")
