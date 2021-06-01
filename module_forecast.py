import time
import forecastCreator as fr

def main():
    while True:
        frc = fr.ForecastCreator()
        hst.createForecast()
        time.sleep(300) # Delay for 300 seconds

if __name__ == '__main__':
    main()