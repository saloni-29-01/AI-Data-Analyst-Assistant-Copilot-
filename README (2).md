# 🤖 AI Data Analytics Copilot

## Autonomous Data Pipeline & Analytics Agent

A modern, interactive AI-powered data analytics platform with natural language querying, automatic SQL generation, and intelligent data visualization.

---

## ✨ Features

### 🎯 Core Capabilities
- **Natural Language Queries**: Ask questions in plain English
- **Automatic SQL Generation**: AI converts your questions to SQL
- **Self-Healing Queries**: AI automatically fixes SQL errors
- **Interactive Dashboards**: Real-time data visualization with Plotly
- **Multi-Table Analysis**: Supports 6+ interconnected tables
- **CSV Upload & Analysis**: Upload and analyze custom datasets
- **Smart Chat Interface**: Conversational AI with context awareness

### 📊 Analytics Features
- Revenue analysis and trends
- Customer segmentation by geography
- Product performance tracking
- Payment method analytics
- Order pattern analysis
- Real-time weather integration

### 🎨 UI/UX Highlights
- Modern gradient-based design
- Responsive layout
- Interactive charts and graphs
- Real-time data updates
- Dark mode optimized
- Mobile-friendly interface

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- pip package manager

### Installation

1. **Clone or download the project**
```bash
cd ai-data-copilot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up OpenAI API Key**

Create the secrets file:
```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml` and add:
```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

4. **Initialize the database**
```bash
python database.py
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
ai-data-copilot/
├── app.py                      # Main Streamlit application
├── database.py                 # Database setup and initialization
├── requirements.txt            # Python dependencies
├── secrets_template.toml       # API key configuration template
├── README.md                   # This file
├── sales.db                    # SQLite database (created on first run)
└── .streamlit/
    └── secrets.toml           # Your API keys (DO NOT COMMIT)
```

---

## 📊 Database Schema

The application uses 6 interconnected tables:

### **customers**
- `id` (PRIMARY KEY)
- `name` (TEXT)
- `city` (TEXT)

### **orders**
- `id` (PRIMARY KEY)
- `customer_id` (FOREIGN KEY)
- `amount` (INTEGER)
- `date` (TEXT)

### **products**
- `id` (PRIMARY KEY)
- `name` (TEXT)
- `price` (INTEGER)

### **order_items**
- `id` (PRIMARY KEY)
- `order_id` (FOREIGN KEY)
- `product_id` (FOREIGN KEY)
- `quantity` (INTEGER)

### **payments**
- `id` (PRIMARY KEY)
- `order_id` (FOREIGN KEY)
- `payment_method` (TEXT)
- `status` (TEXT)

### **employees**
- `id` (PRIMARY KEY)
- `name` (TEXT)
- `department` (TEXT)

---

## 💡 Usage Examples

### Natural Language Queries

**Basic Queries:**
```
- "Show all customers"
- "List all orders"
- "Show products"
```

**Analytics Queries:**
```
- "Total sales this month"
- "Orders above 1000"
- "Customers from Delhi"
- "Average order value"
```

**Complex Queries:**
```
- "Which customers have spent more than 5000?"
- "Show me the top 5 products by revenue"
- "List all pending payments"
- "Find customers who ordered laptops"
```

**Visualization:**
```
- "Show me a chart of revenue by customer"
- "Visualize sales trends"
- "Create a graph of product prices"
```

### CSV Analysis

1. Upload a CSV file using the sidebar
2. Ask questions about your data:
   - "Summarize this data"
   - "What are the key insights?"
   - "Show me correlations"

---

## 🎨 UI Features

### Dashboard Metrics
- Total Customers
- Total Orders
- Total Revenue
- Average Order Value

### Interactive Charts
- Revenue by customer (Bar chart)
- Revenue trends (Line chart)
- Customer distribution (Pie chart)
- Payment methods (Pie chart)
- Product prices (Bar chart)

### Chat Interface
- Message history (last 10 messages)
- Code display for SQL queries
- Data table results
- Chart visualizations
- Error handling with AI-powered fixes

---

## 🔧 Configuration

### API Configuration
Edit `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-..."
```

### Database Configuration
The database is automatically created with sample data including:
- 10 customers across 5+ cities
- 50+ orders with realistic amounts
- 8 products in various price ranges
- 80+ order items
- Payment records with multiple methods
- 8 employees across departments

---

## 🛠️ Advanced Features

### AI-Powered SQL Generation
- Converts natural language to SQL
- Understands table relationships
- Handles complex joins and aggregations
- Auto-corrects syntax errors

### Error Recovery
- Detects SQL errors automatically
- Uses AI to fix broken queries
- Provides helpful error messages
- Logs issues for debugging

### Smart Caching
- Caches database queries (5 min TTL)
- Improves response times
- Reduces database load
- Automatic cache invalidation

---

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile devices
- Different screen sizes and orientations

---

## 🔒 Security Best Practices

1. **Never commit API keys**
   - Add `.streamlit/secrets.toml` to `.gitignore`
   - Use environment variables in production

2. **Database Security**
   - Use prepared statements (built-in with SQLite)
   - Sanitize user inputs
   - Regular backups

3. **API Rate Limiting**
   - Monitor OpenAI API usage
   - Implement user rate limits if needed

---

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets in Streamlit Cloud dashboard
4. Deploy!

### Docker (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API Key not found"**
- Ensure `.streamlit/secrets.toml` exists
- Check the key format
- Verify the file location

**"Database not found"**
- Run `python database.py` first
- Check file permissions
- Ensure `sales.db` is created

**"Module not found"**
- Run `pip install -r requirements.txt`
- Use a virtual environment
- Check Python version (3.8+)

**Charts not displaying**
- Clear browser cache
- Check Plotly installation
- Verify data format

---

## 📈 Performance Tips

1. **Database Optimization**
   - Add indexes on frequently queried columns
   - Use EXPLAIN for slow queries
   - Regular VACUUM for SQLite

2. **Caching**
   - Adjust cache TTL based on data update frequency
   - Use `st.cache_data` for expensive computations
   - Clear cache when needed

3. **API Usage**
   - Batch similar queries
   - Use lower-cost models for simple tasks
   - Implement request queuing

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional chart types
- More complex SQL patterns
- Export functionality
- User authentication
- Advanced analytics
- Multi-language support

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **OpenAI**: For GPT-4 API
- **Plotly**: For interactive visualizations
- **Pandas**: For data manipulation

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with sample data first
4. Check API quotas and limits

---

## 🎯 Roadmap

### Upcoming Features
- [ ] Multi-database support (PostgreSQL, MySQL)
- [ ] Advanced NLP for complex queries
- [ ] Data export (Excel, PDF reports)
- [ ] Scheduled reports
- [ ] User roles and permissions
- [ ] Real-time collaboration
- [ ] Custom dashboard builder
- [ ] Machine learning predictions
- [ ] API endpoints for integration
- [ ] Mobile app

---

## 📊 Version History

**v2.0** (Current)
- Complete UI redesign with modern gradients
- Enhanced chat interface
- Multiple visualization tabs
- Improved error handling
- Better SQL generation
- Performance optimizations

**v1.0**
- Initial release
- Basic chat functionality
- Simple SQL generation
- Static charts

---

**Built with ❤️ using Streamlit, OpenAI, and Python**

🤖 *Autonomous Data Pipeline & Analytics Agent*
