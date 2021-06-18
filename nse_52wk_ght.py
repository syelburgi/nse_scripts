import fix_yahoo_finance as yf
import sys
import os


def fetch_share_data(periods, interval):
    devnull = open(os.devnull, "w")
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = devnull
    sys.stderr = devnull
    data = yf.download(tickers=share, periods=periods, interval=interval, auto_adjust=True, prepost=True)
    sys.stderr = stderr
    sys.stdout = stdout
    return data


if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))
    watch_path = path + "\\nifty_500.txt"
    watch_list = []

    with open(watch_path) as f:
        share = f.readlines()
        share = [x.strip() for x in share]
        watch_list = share

    for share_name in watch_list:
        try:
            share = str(share_name) + ".NS"
            periods = "12mo"
            interval = "1wk"
            share_data = fetch_share_data(periods, interval)
            share_high_data = share_data[share_data['High'].notna()]
            share_close_data = share_data[share_data['Close'].notna()]

            max_52wk = share_high_data ['High'][-1]
            for i in range(0, 53):
                if max_52wk < share_high_data['High'][-i]:
                    max_52wk = share_high_data['High'][-i]

            share_cp = share_close_data['Close'][-1]
            if (share_cp + 0.02 * share_cp) > max_52wk:
                #print("{} near 52wk high".format(share_name))
                periods = "1mo"
                interval = "1d"
                share_data = fetch_share_data(periods, interval)
                share_vol_data = share_data[share_data['Volume'].notna()]
                share_vol_ma = share_data['Volume'].rolling(window=20, min_periods=1).mean()
                if share_vol_data['Volume'][-1] > share_vol_ma[-1]:
                    print("{} high : {}, cp : {} vol : {} vol_20d : {}".format(share_name, max_52wk, share_cp,
                                                                               share_vol_data['Volume'][-1],
                                                                               share_vol_ma[-1]))
        except Exception:
            continue
