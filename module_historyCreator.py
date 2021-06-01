import time
import historyCreator as hc


def main():
    while True:
        hst = hc.HistoryCreator()
        hst.createHistory()
        time.sleep(300)  # Delay for 300 seconds


if __name__ == '__main__':
    main()
