# ArthVeda QuantView

A professional-grade quantitative analytics platform for financial market data analysis. Built with Streamlit and Plotly.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **50+ Advanced Visualizations** - Comprehensive charts including Heikin-Ashi, Keltner Channels, Ichimoku Cloud, Stochastic Oscillator, MACD, RSI, Bollinger Bands, and many more
- **Multi-File Upload** - Upload multiple CSV/Excel files to compare and analyze
- **Professional Dark Theme** - Sleek dark color palette optimized for financial data visualization
- **Technical Indicators** - 20+ technical indicators including ATR, CCI, Williams %R, OBV, MFI, VWAP, Parabolic SAR, TRIX, KAMA, Aroon, KST, PPO
- **Pattern Recognition** - ZigZag, Line Break, Renko charts, support/resistance detection, breakout analysis
- **Risk Analysis** - Drawdown analysis, anomaly detection with Z-score, volatility heatmaps
- **Statistical Insights** - Returns distribution, autocorrelation, correlation heatmaps, seasonal patterns
- **Export Options** - Download analyzed data as CSV or Excel with summary statistics
- **Sample Template** - Built-in Excel template downloader for proper data formatting

## Installation

```bash
# Clone the repository
git clone https://github.com/sourishdey2005/ArthVeda-QuantView-.git
cd ArthVeda-QuantView

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Data Format

### Supported File Types
- CSV (.csv)
- Excel (.xlsx, .xls)

### Expected Columns
The application automatically detects the following column types:
- **Date**: date, datetime, time, timestamp, trade_date
- **Open**: open, open_price, opening, o
- **High**: high, high_price, h
- **Low**: low, low_price, l
- **Close**: close, close_price, closing, c, last, last_price
- **Volume**: volume, vol, shares, shares_traded
- **Symbol**: symbol, ticker, stock, code, scrip
- **Exchange**: listing exchange, exchange, market

### Sample Template
Download the built-in Excel template from the sidebar when no file is uploaded. It contains proper column structure with sample data.

## Dashboard Sections

1. **Overview** - Dataset summary, column types, missing values, data preview
2. **Price Analytics** - Candlestick, moving averages, Bollinger bands, distribution
3. **Volume Analytics** - Volume charts, MA, spikes, distribution
4. **Statistical Insights** - Returns analysis, volatility, autocorrelation
5. **Technical Indicators** - RSI, MACD, EMA, Stochastic, CCI, Williams %R, and more
6. **Trend & Pattern** - Trend direction, support/resistance, breakouts
7. **Risk & Outliers** - Drawdown, anomaly detection, outlier table
8. **Multi-Symbol** - Compare multiple symbols (when symbol column present)
9. **Export** - Download cleaned data and reports

## Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Statistics**: SciPy, Scikit-learn, Statsmodels
- **Excel Handling**: Openpyxl, XlsxWriter

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

**Sourish Dey** 
- GitHub: [@sourishdey2005](https://github.com/sourishdey2005)

## Acknowledgments

- Built with Streamlit and Plotly
- Inspired by professional trading platforms
- Designed for quantitative analysts and traders