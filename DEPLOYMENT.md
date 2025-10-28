# Deployment Guide - V1 Demo

🛂 **Visa Requirements Agent V1 Demo** - Deployment Instructions

## 🚀 Streamlit Cloud Deployment (Recommended)

### **Quick Deploy:**
1. **Visit**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click**: "New app"
4. **Repository**: `pbentle2006/visa-requirements-agent-v1-demo`
5. **Branch**: `master`
6. **Main file path**: `src/ui/streamlit_app.py`
7. **Click**: "Deploy!"

### **Configuration:**
- ✅ **No API keys required** (V1 uses fallbacks)
- ✅ **No environment variables needed**
- ✅ **Works immediately** after deployment
- ✅ **Free tier compatible**

### **Expected URL:**
`https://visa-requirements-agent-v1-demo-[hash].streamlit.app/`

## 🐳 Docker Deployment

### **Build and Run:**
```bash
# Build the image
docker build -t visa-agent-v1-demo .

# Run the container
docker run -p 8501:8501 visa-agent-v1-demo
```

### **Access:**
http://localhost:8501

## 🌐 Alternative Platforms

### **Heroku:**
```bash
# Install Heroku CLI and login
heroku create visa-agent-v1-demo
git push heroku master
```

### **Railway:**
1. Connect GitHub repository
2. Deploy automatically from `master` branch
3. Set build command: `pip install -r requirements_streamlit.txt`
4. Set start command: `streamlit run src/ui/streamlit_app.py --server.port=$PORT`

### **Render:**
1. Connect GitHub repository
2. Build command: `pip install -r requirements_streamlit.txt`
3. Start command: `streamlit run src/ui/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

## ⚡ Performance Optimization

### **For Public Deployment:**
- Uses `requirements_streamlit.txt` (lightweight)
- Instant execution (0.0s) - no API delays
- No external dependencies
- Optimized for high concurrent users

### **Resource Usage:**
- **Memory**: ~200MB
- **CPU**: Minimal (fallback processing)
- **Network**: No external API calls
- **Storage**: ~50MB

## 🎯 Demo Features

### **What Works Immediately:**
- ✅ Policy document upload
- ✅ Instant workflow execution
- ✅ Professional results display
- ✅ Agent Architecture page
- ✅ Policy Comparison functionality
- ✅ Consistent 75% validation scores
- ✅ 12+ generated questions

### **Perfect For:**
- 🎭 Sales presentations
- 👥 Customer demonstrations  
- 📚 Training and onboarding
- 🔄 Backup when APIs unavailable
- 🌐 Public showcases

## 🔧 Troubleshooting

### **Common Issues:**

**1. Import Errors:**
- Ensure `requirements_streamlit.txt` is used for deployment
- Check Python version compatibility (3.11+)

**2. File Path Issues:**
- Verify main file path: `src/ui/streamlit_app.py`
- Ensure all relative imports work from project root

**3. Memory Issues:**
- Use `requirements_streamlit.txt` instead of full `requirements.txt`
- Remove optional dependencies if needed

### **Debug Mode:**
Add to Streamlit secrets for debugging:
```toml
[debug]
enabled = true
```

## 📊 Monitoring

### **Streamlit Cloud:**
- Built-in analytics available
- Usage metrics in dashboard
- Error logging included

### **Custom Deployment:**
- Add health check endpoint: `/_stcore/health`
- Monitor memory usage
- Track response times

## 🎪 Demo Script for Deployed App

1. **Share URL** with customers/stakeholders
2. **Upload** Parent Boost Visitor Visa policy
3. **Click** "Run Complete Workflow"
4. **Show** instant results (0.0s execution)
5. **Navigate** to "Agent Architecture" for technical details
6. **Demonstrate** Policy Comparison with multiple documents

**Perfect for live demonstrations!** 🚀

## 📞 Support

For deployment issues:
- Check Streamlit Cloud logs
- Verify GitHub repository access
- Ensure all files are committed and pushed
- Test locally first with: `streamlit run src/ui/streamlit_app.py`
