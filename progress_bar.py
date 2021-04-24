def progress_bar():
    import time
    formatter = '[{container:<51}] {percent}%'

    for i in range(1,51):
        print(formatter.format(container='='*i + '>',percent=round(i * 100 // 50)), end="\r")
        time.sleep(0.1)

    print(formatter.format(container='='*(i+1),percent=round(i  * 100 / 50)), end="\r")


if __name__ == '__main__':
    progress_bar()