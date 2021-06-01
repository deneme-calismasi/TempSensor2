import time
import modelCreator as mc


def main():
    while True:
        mdc = mc.ModelCreator()
        mdc.createForecastModels()
        time.sleep(2419200)  # Delay for 1 month


if __name__ == '__main__':
    main()
