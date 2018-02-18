import requests

def main():
    print(generateRandom(1, 10000))

def generateRandom(min, max):
    resp = requests.request('GET', "https://www.random.org/integers/",
                            params = {'num': 1,
                                      'min': min,
                                      'max': max,
                                      'col': 1,
                                      'base': 10,
                                      'format': 'plain',
                                      'rnd': 'new'})

    if resp.status_code != 200:
        return None

    return int(resp.text)


if __name__ == "__main__":
    main()