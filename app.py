import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Chemical Disaster Evidence Framework",
    layout="wide"
)

st.title("Chemical Disaster Evidence Framework")
st.caption("A structured academic tool for identifying environmental and health evidence gaps after chemical incidents.")
st.markdown("### This tool identifies evidence gaps. It does not determine safety or individual risk.")

demo_mode = st.checkbox("Load Example Case: East Palestine Train Derailment")

st.header("1. Incident Intake")

if demo_mode:
    incident_name = st.text_input("Incident name", value="East Palestine Train Derailment")
    country = st.text_input("Country", value="USA")
    incident_date = st.date_input("Incident date", value=date(2023, 2, 3))
    combustion = st.selectbox(
        "Was there combustion or burn involved?",
        ["Unknown", "Yes", "No"],
        index=1
    )
    known_chemicals = st.text_area(
        "Known chemicals on manifest or confirmed",
        value="Vinyl chloride, butyl acrylate, benzene, ethylhexyl acrylate, ethylene glycol monobutyl ether"
    )
else:
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
plant_tissue = st.checkbox("Plant tissue data available")
symptom_surveys = st.checkbox("Resident or responder symptom survey data available")

st.header("3. Evidence Gap Flags")

flags = []

if combustion == "Yes":
    flags.append("Combustion occurred. Consider unexpected byproducts and the need for non-targeted chemical analysis.")

if not outdoor_air:
    flags.append("Missing outdoor air data.")

if not indoor_air:
    flags.append("Missing indoor air data.")

if not water:
    flags.append("Missing water data.")

if not soil:
    flags.append("No soil sampling recorded.")

if not sediment:
    flags.append("No sediment sampling recorded.")

if not biomonitoring:
    flags.append("No human biomonitoring recorded. Early exposure assessment may be incomplete.")

if not plant_tissue:
    flags.append("No plant tissue sampling recorded.")

if not symptom_surveys:
    flags.append("No structured resident or responder symptom survey data recorded.")

if len(flags) == 0:
    st.success("No major structural evidence gaps were flagged from the selected inputs.")
else:
    for f in flags:
        st.warning(f)

st.header("4. Interpretation")

if len(flags) > 0:
    st.info(
        "Based on available inputs, current data is insufficient to conclude long-term safety. "
        "Key evidence gaps remain across environmental and or human exposure domains."
    )
else:
    st.success(
        "No major structural evidence gaps were identified from the selected inputs, "
        "but this still does not confirm safety."
    )

st.header("5. Clinical Considerations")

clinical_flags = []

if not biomonitoring:
    clinical_flags.append(
        "Consider whether early biomonitoring such as blood or urine testing may be appropriate if still within a meaningful exposure window."
    )

if combustion == "Yes":
    clinical_flags.append(
        "Consider assessment for inhalational exposure symptoms, including respiratory, ocular, throat, and neurologic complaints."
    )

if not symptom_surveys:
    clinical_flags.append(
        "Consider structured symptom collection among residents, workers, or first responders if not already performed."
    )

if len(clinical_flags) > 0:
    for c in clinical_flags:
        st.warning(c)
else:
    st.success("No immediate clinical follow-up flags were generated from the selected inputs.")

st.header("6. Export Summary")

summary = {
    "Incident": incident_name,
    "Country": country,
    "Incident Date": incident_date,
    "Combustion": combustion,
    "Chemicals": known_chemicals,
    "Outdoor Air Data": outdoor_air,
    "Indoor Air Data": indoor_air,
    "Water Data": water,
    "Soil Data": soil,
    "Sediment Data": sediment,
    "Biomonitoring": biomonitoring,
    "Plant Tissue Data": plant_tissue,
    "Symptom Survey Data": symptom_surveys,
    "Evidence Gap Count": len(flags),
    "Evidence Gap Flags": " | ".join(flags),
    "Clinical Considerations": " | ".join(clinical_flags)
}

df = pd.DataFrame([summary])
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download CSV",
    csv,
    "chemical_disaster_summary.csv",
    "text/csv"
)
