import fix_yahoo_finance as yf
import os
import sys

stdout = None
stderr = None
devnull = None


def print_message(msg):
    global stdout, stderr, devnull
    sys.stderr = stderr
    sys.stdout = stdout
    print(msg)
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = devnull
    sys.stderr = devnull


def init_print():
    global stdout, stderr, devnull
    devnull = open(os.devnull, "w")
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = devnull
    sys.stderr = devnull


if __name__ == "__main__":
    init_print()
    periods = ["8mo", "2mo"]
    intervals = ["1wk", "1d"]
    average = ["20wk", "20d"]

    path = os.path.dirname(os.path.realpath(__file__))
    watch_path = path + '\my_portfolio.txt'
    history = -1

    print_message(watch_path)
    with open(watch_path) as f:
        share = f.readlines()
        share = [x.strip() for x in share]
        watch_list = share

    for i in range(0, len(periods)):
        period = periods[i]
        interval = intervals[i]
        action_list = []
        print_message("*****************************************************************************************")
        for share_name in watch_list:
            try:
                share = str(share_name) + ".NS"
                share_data = yf.download(tickers=share, periods=period, interval=interval, auto_adjust=True,
                                         prepost=True)
                share_data = share_data[share_data['Close'].notna()]
                share_ma = share_data['Close'].rolling(window=20, min_periods=1).mean()

                cp_share = share_data['Close'][history]
                ma_share = share_ma[history - 1]
                if ((ma_share + (0.05 * ma_share)) >= cp_share) or (ma_share >= cp_share):
                    down_percentage = ((ma_share - cp_share)/cp_share) * 100
                    action_list.append({"share": share_name, "percentage": down_percentage,
                                        "ma": ma_share, "cp": cp_share})
            except Exception:
                print_message("Share_name {} is not listed".format(share_name))
                continue

        print_message("****Shares Near {} moving average**********".format(average[i]))
        i = 1
        for share in action_list:
            print_message("{}.{} {:.2f}% below MA".format(i, share['share'], share['percentage']))
            i += 1

        print_message("*****************************************************************************************")
