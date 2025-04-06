import streamlit as st
import os
import sqlite3
import pandas as pd
import traceback
from pathlib import Path
from agents.disaster_monitor import DisasterMonitor
from agents.business_analyst import BusinessAnalyst
from agents.data_architecture import DataArchitect
from agents.data_governance import DataGovernanceAgent
from agents.data_mapper import DataMapper
from agents.loan_manager import LoanManager
from agents.certifier import Certifier
from agents.documentation import DocumentationAgent
from agents.whatsapp_alert import WhatsAppAlert
from agents.gemma_agent import GemmaAgent
import base64

# Configuration
DATA_DIR = Path(__file__).parent / "data"
FARMERS_CSV = DATA_DIR / "farmers.csv"

def initialize_database():
    with sqlite3.connect('loans.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS farmers")
        cursor.execute("DROP TABLE IF EXISTS loans")
        cursor.execute("""
            CREATE TABLE farmers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                region TEXT NOT NULL,
                practices TEXT,
                language TEXT,
                crop TEXT
            )""")
        try:
            if os.path.exists('data/farmers.csv'):
                df = pd.read_csv('data/farmers.csv')
                df.to_sql('farmers', conn, if_exists='append', index=False)
            else:
                cursor.executemany("INSERT INTO farmers VALUES (?,?,?,?,?,?)", [
                    (1, 'Raju', 'Andhra Pradesh', 'organic, drip irrigation', 'Telugu', 'Rice'),
                    (2, 'Meena', 'Maharashtra', 'chemical fertilizers', 'Marathi', 'Cotton'),
                    (3, 'Singh', 'Punjab', 'wheat farming', 'Punjabi', 'Wheat')
                ])
        except Exception as e:
            st.sidebar.error(f"Data load failed: {str(e)}")
            raise
        cursor.execute("""
            CREATE TABLE loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER,
                amount REAL,
                interest_rate REAL,       
                status TEXT DEFAULT 'pending',
                FOREIGN KEY(farmer_id) REFERENCES farmers(id)
            )""")
        conn.commit()

def local_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

def main():
    st.set_page_config(page_title="🌾 भारतKredit (BharatKredit) - AI-Powered Agricultural Loan System", layout="wide")

    # Style
    st.markdown("""
        <style>
            body {
                background-color: #F3F8F0;
            }
            .st-emotion-cache-6qob1r {
                background-color: #FEEBDA !important;
            }
            h1, h2, h3 {
                font-family: 'Segoe UI', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

    # Banner
    banner_path = "D:/d/farming_loans/BharatKredit.jpg"
    if os.path.exists(banner_path):
        banner_base64 = local_image_to_base64(banner_path)
        st.markdown(f"""
            <div style="width: 100%; margin-bottom: 25px; border-radius: 8px; border: 1px solid #ccc;">
                <img src="{banner_base64}" style="width: 100%; object-fit: contain;">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Banner image not found at specified path.")

    if st.sidebar.button("🔄 Initialize System"):
        initialize_database()
        st.sidebar.success("System ready!")

    with sqlite3.connect('loans.db') as conn:
        st.title("भारतKredit (BharatKredit) - AI-Powered Agricultural Loan System")
        farmers_df = pd.read_sql("SELECT * FROM farmers", conn)
        selected_farmer = st.selectbox("Select Farmer", farmers_df['name'])
        farmer = farmers_df[farmers_df['name'] == selected_farmer].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.header("👨🌾 Farmer Profile")
            st.markdown(f"""
            - **Region**: {farmer['region']}
            - **Practices**: {farmer['practices']}
            - **Language**: {farmer['language']}
            - **Crop**: {farmer.get('crop','Not specified')}
            """)

        with col2:
            st.header("🌪️ Risk Management")
            if st.button("Check Disaster Risk"):
                try:
                    monitor = DisasterMonitor()
                    risk_level = monitor.get_risk(farmer['region'])
                    alert = monitor.send_alert(farmer['id'])
                    if risk_level == "High":
                        st.error(f"🚨 {alert}")
                    elif risk_level == "Medium":
                        st.warning(f"⚠️ {alert}")
                    else:
                        st.success(f"✅ {alert}")
                except Exception as e:
                    st.error(f"Risk check failed: {str(e)}")

        st.header("💰 Loan Processing")
        loan_amount = st.number_input("Loan Amount (₹)", 1000, 10000000, 50000)

        if st.button("Process Loan Application"):
            try:
                with conn:
                    st.write("🔄 Starting loan processing...")

                    analyst = BusinessAnalyst()
                    requirements = analyst.analyze_use_case(f"{farmer['crop']} farming in {farmer['region']}")
                    st.write("✅ Business analysis complete")

                    architect = DataArchitect()
                    schema = architect.design_schema(requirements)
                    st.write("✅ Data schema created")

                    governance = DataGovernanceAgent()
                    source_attrs = governance.get_attribute_info("FARMER_DB")
                    st.write("✅ Data governance verified")

                    mapper = DataMapper()
                    mappings = mapper.generate_mappings(source_attrs, schema)
                    st.write("✅ Data mappings generated")

                    manager = LoanManager(conn)
                    interest_rate = manager.approve_loan(int(farmer['id']), float(loan_amount))
                    st.write(f"✅ Approved interest rate: {interest_rate}%")

                    conn.execute(
                        "INSERT INTO loans (farmer_id, amount, interest_rate, status) VALUES (?, ?, ?, ?)",
                        (int(farmer['id']), float(loan_amount), float(interest_rate), 'approved'))

                    certifier = Certifier()
                    certification = certifier.validate(schema, mappings)
                    st.write(f"✅ Certification: {certification}")

                    doc_agent = DocumentationAgent()
                    report = doc_agent.generate_report(schema, mappings, certification)

                    original_message = f"Loan of ₹{loan_amount} approved at {interest_rate}% interest"
                    try:
                        gemma = GemmaAgent()
                        translated_message = gemma.translate(original_message, farmer['language'])
                        message_to_send = translated_message
                    except Exception as e:
                        st.warning(f"⚠️ Translation failed. Sending message in English. Reason: {str(e)}")
                        message_to_send = original_message

                    whatsapp_alert = WhatsAppAlert()
                    whatsapp_result = whatsapp_alert.send(
                        message_to_send,
                        "9876543210"
                    )

                    if whatsapp_result['status'] == 'success':
                        st.success(f"📲 WhatsApp message sent to {whatsapp_result['to']}")
                    else:
                        st.error(f"❌ Failed to send WhatsApp: {whatsapp_result.get('error', 'Unknown error')}")

                    st.success("### Loan Approved! ✅")
                    st.metric("Interest Rate", f"{interest_rate}%")
                    st.download_button("Download Documentation", report, file_name="loan_docs.txt")

            except Exception as e:
                st.error(f"🚨 Processing failed: {str(e)}")
                st.text(traceback.format_exc())

        st.header("📜 Loan History")
        loans_df = pd.read_sql("SELECT * FROM loans", conn)
        st.dataframe(loans_df)

if __name__ == "__main__":
    main()
