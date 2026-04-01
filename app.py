import streamlit as st
import sqlite3
import pandas as pd
import requests
import re
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="AI Data Analytics Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #ec4899;
        --bg-dark: #1e1e2e;
        --bg-light: #2a2a3e;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom headers */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(20deg); }
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        color: white;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        color: white;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e1e2e 0%, #2a2a3e 100%);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: #1e1e2e !important;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    /* Animated loader */
    .loader {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(102, 126, 234, 0.3);
        border-top: 5px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #667eea;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI Client
AI_ENABLED = False
client = None
try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if api_key and api_key != "your-openai-api-key-here":
        client = OpenAI(api_key=api_key)
        AI_ENABLED = True
    else:
        st.sidebar.warning("AI features disabled. Add OPENAI_API_KEY to .streamlit/secrets.toml")
except Exception:
    st.sidebar.warning("AI features disabled. Add OPENAI_API_KEY to .streamlit/secrets.toml")

# Database Connection
@st.cache_resource
def get_database_connection():
    return sqlite3.connect("sales.db", check_same_thread=False)

conn = get_database_connection()

# Load data with caching
@st.cache_data(ttl=300)
def load_data():
    try:
        df_customers = pd.read_sql_query("SELECT * FROM customers", conn)
        df_orders = pd.read_sql_query("SELECT * FROM orders", conn)
        df_products = pd.read_sql_query("SELECT * FROM products", conn)
        df_order_items = pd.read_sql_query("SELECT * FROM order_items", conn)
        df_payments = pd.read_sql_query("SELECT * FROM payments", conn)
        df_employees = pd.read_sql_query("SELECT * FROM employees", conn)
        return df_customers, df_orders, df_products, df_order_items, df_payments, df_employees
    except Exception as e:
        st.error(f"Database error: {e}")
        return None, None, None, None, None, None

df_customers, df_orders, df_products, df_order_items, df_payments, df_employees = load_data()

# ===========================
# HELPER FUNCTIONS
# ===========================

def clean_sql(raw_sql):
    """Clean SQL query from markdown formatting"""
    if not raw_sql:
        return ""
    cleaned = raw_sql.replace("```sql", "").replace("```", "").strip()
    return cleaned

def generate_ai_response(prompt):
    """Generate AI response using OpenAI"""
    if not AI_ENABLED:
        return "AI is disabled. Please add your OpenAI API key to .streamlit/secrets.toml"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

def generate_sql(query):
    """Generate SQL from natural language"""
    if not AI_ENABLED:
        return ""
    try:
        schema_info = """
        Tables:
        - customers(id, name, city)
        - orders(id, customer_id, amount, date)
        - products(id, name, price)
        - order_items(id, order_id, product_id, quantity)
        - payments(id, order_id, payment_method, status)
        - employees(id, name, department)
        """
        
        prompt = f"""{schema_info}

Convert the following question to SQL. Return ONLY the SQL query without explanation or markdown.

Question: {query}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        return clean_sql(response.choices[0].message.content.strip())
    except Exception as e:
        st.error(f"SQL Generation Error: {e}")
        return ""

def fix_sql_with_ai(bad_sql, error_msg):
    """Fix SQL errors using AI"""
    if not AI_ENABLED:
        return None
    try:
        prompt = f"""Fix this SQL query that produced an error.

SQL Query:
{bad_sql}

Error Message:
{error_msg}

Return ONLY the corrected SQL query without explanation or markdown."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        return clean_sql(response.choices[0].message.content)
    except:
        return None

def create_chart(data, chart_type="bar", x_col=None, y_col=None):
    """Create interactive charts using Plotly"""
    if chart_type == "bar":
        fig = px.bar(data, x=x_col, y=y_col, 
                     color_discrete_sequence=['#667eea'],
                     template='plotly_dark')
    elif chart_type == "line":
        fig = px.line(data, x=x_col, y=y_col,
                      color_discrete_sequence=['#667eea'],
                      template='plotly_dark')
    elif chart_type == "pie":
        fig = px.pie(data, names=x_col, values=y_col,
                     color_discrete_sequence=px.colors.sequential.Purples,
                     template='plotly_dark')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

# ===========================
# MAIN HEADER
# ===========================

st.markdown('<h1 class="main-header">🤖 AI Data Analytics Copilot</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888; font-size: 1.2rem;">Autonomous Data Pipeline & Analytics Agent</p>', unsafe_allow_html=True)

# ===========================
# SIDEBAR
# ===========================

with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    
    # File Upload
    st.markdown("---")
    uploaded_file = st.file_uploader("📁 Upload CSV Data", type=["csv"])
    
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df_upload)} rows")
    else:
        df_upload = None
    
    # Quick Actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("📊 Refresh Dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat = []
        st.rerun()
    
    # Database Info
    st.markdown("---")
    st.markdown("### 📚 Database Schema")
    
    with st.expander("View Tables"):
        st.code("""
• customers (id, name, city)
• orders (id, customer_id, amount, date)
• products (id, name, price)
• order_items (id, order_id, product_id, quantity)
• payments (id, order_id, payment_method, status)
• employees (id, name, department)
        """)
    
    # Stats
    st.markdown("---")
    st.markdown("### 📈 Statistics")
    
    if df_customers is not None and df_orders is not None:
        st.metric("Total Customers", len(df_customers))
        st.metric("Total Orders", len(df_orders))
        st.metric("Total Revenue", f"₹{df_orders['amount'].sum():,.0f}")
    
    # Weather Widget
    st.markdown("---")
    st.markdown("### 🌤️ Weather")
    
    if st.button("Get Current Weather", use_container_width=True):
        try:
            data = requests.get(
                "https://api.open-meteo.com/v1/forecast?latitude=22.5&longitude=88.3&current_weather=true"
            ).json()
            w = data["current_weather"]
            st.info(f"🌡️ {w['temperature']}°C\n💨 Wind: {w['windspeed']} km/h")
        except:
            st.error("Weather data unavailable")

# ===========================
# DASHBOARD METRICS
# ===========================

if df_customers is not None and df_orders is not None:
    st.markdown('<div class="section-header">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df_customers)}</div>
            <div class="metric-label">Total Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df_orders)}</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{df_orders['amount'].sum():,.0f}</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_order = df_orders['amount'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{avg_order:,.0f}</div>
            <div class="metric-label">Avg Order Value</div>
        </div>
        """, unsafe_allow_html=True)

# ===========================
# DATA VISUALIZATION
# ===========================

st.markdown('<div class="section-header">📈 Visual Analytics</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Revenue Analysis", "👥 Customer Insights", "📦 Product Analytics", "💳 Payment Stats"])

with tab1:
    if df_orders is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by Customer
            revenue_by_customer = df_orders.groupby('customer_id')['amount'].sum().reset_index()
            revenue_by_customer = revenue_by_customer.merge(
                df_customers[['id', 'name']], 
                left_on='customer_id', 
                right_on='id'
            )
            fig = create_chart(revenue_by_customer, "bar", "name", "amount")
            fig.update_layout(title="Revenue by Customer")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Orders over time
            if 'date' in df_orders.columns:
                orders_by_date = df_orders.groupby('date')['amount'].sum().reset_index()
                fig = create_chart(orders_by_date, "line", "date", "amount")
                fig.update_layout(title="Revenue Trend")
                st.plotly_chart(fig, use_container_width=True)

with tab2:
    if df_customers is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            # Customers by city
            city_dist = df_customers['city'].value_counts().reset_index()
            city_dist.columns = ['city', 'count']
            fig = create_chart(city_dist, "pie", "city", "count")
            fig.update_layout(title="Customer Distribution by City")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df_customers, use_container_width=True, height=400)

with tab3:
    if df_products is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_chart(df_products, "bar", "name", "price")
            fig.update_layout(title="Product Prices")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df_products, use_container_width=True, height=400)

with tab4:
    if df_payments is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            payment_dist = df_payments['payment_method'].value_counts().reset_index()
            payment_dist.columns = ['method', 'count']
            fig = create_chart(payment_dist, "pie", "method", "count")
            fig.update_layout(title="Payment Methods Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            status_dist = df_payments['status'].value_counts().reset_index()
            status_dist.columns = ['status', 'count']
            fig = create_chart(status_dist, "bar", "status", "count")
            fig.update_layout(title="Payment Status")
            st.plotly_chart(fig, use_container_width=True)

# ===========================
# AI CHAT INTERFACE
# ===========================

st.markdown('<div class="section-header">💬 AI Copilot Chat</div>', unsafe_allow_html=True)

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat input
query = st.chat_input("Ask me anything about your data... 💭")

if query:
    q = query.lower()
    response = ""
    show_data = None
    show_chart = None
    
    try:
        # Add user message
        st.session_state.chat.append(("You", query))
        
        # ===========================
        # RULE-BASED RESPONSES
        # ===========================
        
        if "show all customers" in q or "list customers" in q:
            show_data = df_customers
            response = "✅ Displaying all customers from the database"
        
        elif "show all orders" in q or "list orders" in q:
            show_data = df_orders
            response = "✅ Displaying all orders from the database"
        
        elif "show all products" in q or "list products" in q:
            show_data = df_products
            response = "✅ Displaying all products from the database"
        
        elif re.search(r"(orders?|amount|revenue)\s+(above|greater|more|over|>\s*)\s*(\d+)", q):
            match = re.search(r"(\d+)", q)
            if match:
                num = int(match.group(1))
                show_data = df_orders[df_orders["amount"] > num]
                response = f"✅ Found {len(show_data)} orders above ₹{num}"
        
        elif "total sales" in q or "total revenue" in q:
            total = df_orders['amount'].sum()
            response = f"💰 **Total Sales/Revenue:** ₹{total:,.0f}"
        
        elif "average order" in q or "avg order" in q:
            avg = df_orders['amount'].mean()
            response = f"📊 **Average Order Value:** ₹{avg:,.2f}"
        
        elif "customers from" in q:
            city_match = re.search(r"from\s+(\w+)", q)
            if city_match:
                city = city_match.group(1).capitalize()
                show_data = df_customers[df_customers["city"].str.lower() == city.lower()]
                response = f"✅ Found {len(show_data)} customers from {city}"
        
        elif "chart" in q or "graph" in q or "visualize" in q:
            # Auto-generate appropriate chart
            if "revenue" in q or "sales" in q:
                show_chart = create_chart(
                    df_orders.groupby('customer_id')['amount'].sum().reset_index(),
                    "bar", "customer_id", "amount"
                )
                show_chart.update_layout(title="Revenue by Customer")
                response = "📊 Generated revenue chart"
            else:
                show_chart = create_chart(df_orders, "bar", "id", "amount")
                show_chart.update_layout(title="Order Amounts")
                response = "📊 Generated chart from order data"
        
        # ===========================
        # SQL GENERATION & EXECUTION
        # ===========================
        
        elif any(keyword in q for keyword in ["show", "list", "find", "get", "select", "which", "who"]):
            with st.spinner("🤖 Generating SQL query..."):
                sql = generate_sql(query)
                
                if not sql:
                    response = "❌ Could not generate SQL query. Please rephrase your question."
                else:
                    try:
                        st.code(sql, language="sql")
                        result = pd.read_sql_query(sql, conn)
                        show_data = result
                        response = f"✅ Query executed successfully! Found {len(result)} results."
                        
                    except Exception as e:
                        st.warning(f"⚠️ SQL Error: {str(e)}\n\n🔧 AI is fixing the query...")
                        
                        fixed_sql = fix_sql_with_ai(sql, str(e))
                        
                        if fixed_sql:
                            try:
                                st.code(fixed_sql, language="sql")
                                result = pd.read_sql_query(fixed_sql, conn)
                                show_data = result
                                response = f"✅ Error fixed! Query executed successfully. Found {len(result)} results."
                            except Exception as e2:
                                response = f"❌ Could not fix the error: {str(e2)}"
                        else:
                            response = "❌ AI could not fix the SQL error"
        
        # ===========================
        # CSV ANALYSIS
        # ===========================
        
        elif df_upload is not None:
            sample_data = df_upload.head(10).to_string()
            
            prompt = f"""You are an expert data analyst. Analyze this dataset and provide insights.

Dataset Preview:
{sample_data}

Dataset Info:
- Rows: {len(df_upload)}
- Columns: {list(df_upload.columns)}

Question: {query}

Provide a clear, insightful answer with specific data points."""
            
            with st.spinner("🤖 Analyzing your data..."):
                response = generate_ai_response(prompt)
        
        # ===========================
        # GENERAL AI RESPONSE
        # ===========================
        
        else:
            context = f"""You are an AI assistant for a data analytics platform.

Available data:
- {len(df_customers)} customers
- {len(df_orders)} orders
- Total revenue: ₹{df_orders['amount'].sum():,.0f}

Question: {query}

Provide a helpful response."""
            
            with st.spinner("🤖 Thinking..."):
                response = generate_ai_response(context)
    
    except Exception as main_error:
        response = f"❌ Error: {str(main_error)}"
    
    # Add bot response
    st.session_state.chat.append(("Copilot", response))
    
    # Display data if any
    if show_data is not None:
        st.dataframe(show_data, use_container_width=True)
    
    # Display chart if any
    if show_chart is not None:
        st.plotly_chart(show_chart, use_container_width=True)

# ===========================
# CHAT HISTORY DISPLAY
# ===========================

st.markdown("---")

for role, msg in st.session_state.chat[-10:]:  # Show last 10 messages
    if role == "You":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg)

# ===========================
# FOOTER
# ===========================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem;">
    <p>🤖 Powered by AI • Built with Streamlit • Data Analytics Copilot v2.0</p>
    <p style="font-size: 0.9rem;">Autonomous Data Pipeline & Analytics Agent</p>
</div>
""", unsafe_allow_html=True)
