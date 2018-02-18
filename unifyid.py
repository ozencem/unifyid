import requests
from PIL import Image


def main():
    print(single_random_integer(1, 10000))


def generate_png():
    img = Image.new('RGB', (128, 128))
    img.putdata()


def multiple_random_integers(minimum, maximum, count):
    resp = send_random_request(minimum, maximum, count)

    if resp.status_code != 200:
        return None

    lines = resp.text.splitlines()
    return [int(line) for line in lines]


def single_random_integer(minimum, maximum):
    resp = send_random_request(minimum, maximum, 1)

    if resp.status_code != 200:
        return None

    return int(resp.text)


def send_random_request(minimum, maximum, count):
    return requests.request('GET', "https://www.random.org/integers/",
                            params={'num': count,
                                    'min': minimum,
                                    'max': maximum,
                                    'col': 1,
                                    'base': 10,
                                    'format': 'plain',
                                    'rnd': 'new'})


if __name__ == "__main__":
    main()