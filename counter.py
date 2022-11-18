from time import sleep
def main():
    time = 1
    counter = 1
    while time < 5:
        print("cur time is ", time)
        for _ in range (1000):
            counter += 1
        sleep(1)
        time += 1
    return

if __name__ == "__main__":
    main()