# Ethereal Glow SEO Research Toolkit Setup & Execution Script
# Run this in PowerShell as Administrator

Write-Host "🚀 ETHEREAL GLOW SEO RESEARCH TOOLKIT SETUP" -ForegroundColor Green
Write-Host "=" * 50

# Check if Node.js is installed
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check if npm is available
try {
    $npmVersion = npm --version
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found. Please install npm." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow
try {
    npm install
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install dependencies. Check your internet connection." -ForegroundColor Red
    exit 1
}

# Create output directory for reports
Write-Host "`n📁 Creating reports directory..." -ForegroundColor Yellow
$reportsDir = "reports"
if (!(Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Path $reportsDir
    Write-Host "✅ Reports directory created" -ForegroundColor Green
} else {
    Write-Host "✅ Reports directory already exists" -ForegroundColor Green
}

Write-Host "`n🔍 STARTING COMPREHENSIVE SEO ANALYSIS..." -ForegroundColor Cyan
Write-Host "This will take a few minutes. Please wait..." -ForegroundColor Yellow

# Run SEO Research Toolkit
Write-Host "`n1️⃣ Running Basic SEO Analysis..." -ForegroundColor Magenta
try {
    node seo-research-toolkit.js
    Write-Host "✅ Basic SEO analysis completed!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Basic SEO analysis had issues, continuing..." -ForegroundColor Yellow
}

# Run Advanced Keyword Research
Write-Host "`n2️⃣ Running Advanced Keyword Research..." -ForegroundColor Magenta
try {
    node keyword-research.js
    Write-Host "✅ Keyword research completed!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Keyword research had issues, continuing..." -ForegroundColor Yellow
}

# Run Web Intelligence Scraper (might fail due to network restrictions)
Write-Host "`n3️⃣ Running Web Intelligence Analysis..." -ForegroundColor Magenta
Write-Host "⚠️ Note: This may take longer and might be blocked by some websites" -ForegroundColor Yellow
try {
    node web-intelligence-scraper.js
    Write-Host "✅ Web intelligence analysis completed!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Web scraping partially completed or blocked by websites" -ForegroundColor Yellow
}

# Display results summary
Write-Host "`n📊 ANALYSIS COMPLETE!" -ForegroundColor Green
Write-Host "=" * 50

Write-Host "`n📄 Generated Reports:" -ForegroundColor Cyan
Get-ChildItem -Path . -Name "*report*.json" | ForEach-Object {
    Write-Host "  📋 $_" -ForegroundColor White
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review the generated JSON reports for detailed insights"
Write-Host "2. Open MASTER_SEO_STRATEGY.md for complete strategy guide"
Write-Host "3. Implement the recommended technical SEO improvements"
Write-Host "4. Start creating content based on keyword opportunities"
Write-Host "5. Set up tracking and monitoring tools"

Write-Host "`n🎯 Key Actions for Immediate Impact:" -ForegroundColor Green
Write-Host "• Focus on high-priority, low-competition keywords identified"
Write-Host "• Create comprehensive guides for 'Multani Mitti' and 'Neem Ubtan'"
Write-Host "• Optimize existing product pages with psychological triggers"
Write-Host "• Set up Google Search Console and track rankings"
Write-Host "• Begin local SEO optimization for major Indian cities"

Write-Host "`n🔄 To Re-run Analysis:" -ForegroundColor Cyan
Write-Host "npm run full-analysis"

Write-Host "`n🆘 Need Help?" -ForegroundColor Yellow
Write-Host "• Check the generated reports for specific recommendations"
Write-Host "• Review MASTER_SEO_STRATEGY.md for detailed guidance"
Write-Host "• Run individual tools: npm run seo-analysis, npm run keyword-research"

Write-Host "`n🎉 SUCCESS! Your Ethereal Glow SEO research is complete!" -ForegroundColor Green
Write-Host "Start implementing the strategy to flood your website with targeted traffic!" -ForegroundColor White

# Pause to let user read results
Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
