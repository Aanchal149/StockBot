from local_llm import get_local_llm
import yfinance as yf
import gradio as gr

def get_stock_price(ticker):
    try:
        price = yf.Ticker(ticker).fast_info.get("last_price")
        if price:
            return f"The current price of {ticker} is ₹{price:.2f}"
        return f"Could not retrieve price for {ticker}."
    except Exception as e:
        return f"Error fetching price: {e}"

def summarize_intraday(ticker):
    try:
        df = yf.Ticker(ticker).history(interval="5m", period="1d")
        if df.empty:
            return f"No intraday data available for {ticker}."

        open_price = df["Open"].iloc[0]
        high = df["High"].max()
        low = df["Low"].min()
        close_price = df["Close"].iloc[-1]
        pct_change = ((close_price - open_price) / open_price) * 100

        return (
            f"📊 {ticker} Intraday Summary:\n"
            f"- Open: ₹{open_price:.2f}\n"
            f"- High: ₹{high:.2f}\n"
            f"- Low: ₹{low:.2f}\n"
            f"- Close: ₹{close_price:.2f}\n"
            f"- Change: {pct_change:+.2f}%"
        )
    except Exception as e:
        return f"Error summarizing {ticker}: {e}"

def extract_ticker(message):
    words = message.upper().split()
    for word in words:
        if "." in word or word.isalpha():
            try:
                if yf.Ticker(word).info.get("regularMarketPrice") is not None:
                    return word
            except:
                continue
    return None

def get_response(message):
    msg = message.lower()
    ticker = extract_ticker(message)

    if ticker:
        if "summary" in msg or "high" in msg or "low" in msg or "intraday" in msg:
            return summarize_intraday(ticker)
        elif "price" in msg or "value" in msg or "current" in msg:
            return get_stock_price(ticker)

    return get_local_llm()(f"Q: {message}\nA:")

with gr.Blocks() as app:
    gr.Markdown("# 📈 StockBot — Real-Time Stock Data + Finance Chat")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask about stocks or finance (e.g. 'Price of RELIANCE.NS')")

    def respond(message, history):
        reply = get_response(message)
        history.append((message, reply))
        return history

    msg.submit(respond, [msg, chatbot], chatbot)

if __name__ == "__main__":
    app.launch()
