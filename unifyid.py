import requests
from PIL import Image
import os


def main():
    if not check_quota():
        print('Quota limit has already been reached! Please try again later...')
        return

    os.makedirs('out', exist_ok=True)

    with open('out/random.txt', 'w') as out_file:
        out_file.write(str(single_random_integer(1, 10000)))

    img = generate_img(128, 128)
    img.save('out/rbg.png')


def generate_img(width, height):
    img = Image.new('RGB', (width, height))
    y = multiple_random_integers(0, 256*256*256-1, width * height)
    print(img.size)
    print(len(y))
    img.putdata(y)
    return img


def multiple_random_integers(minimum, maximum, count):
    remaining = count
    result = []

    while remaining > 0:
        if remaining > 10000:
            count = 10000
        else:
            count = remaining

        remaining = remaining - count

        resp = send_random_request(minimum, maximum, count)

        if resp.status_code != 200:
            print('Could not generate multiple random integers! reason: {}'.format(resp.text))

            if check_quota():
                print('Retrying..')
                return multiple_random_integers(minimum, maximum, count)
            else:
                return None

        lines = resp.text.splitlines()
        result = result + [int(line) for line in lines]

    return result


def single_random_integer(minimum, maximum):
    resp = send_random_request(minimum, maximum, 1)

    if resp.status_code != 200:
        print('Could not generate a single random integer! reason: {}'.format(resp.text))
        if check_quota():
            print('Retrying..')
            return single_random_integer(minimum, maximum)
        else:
            return None

    return int(resp.text)


def check_quota():
    resp = requests.request('GET', 'https://www.random.org/quota/?format=plain')

    if resp.status_code != 200 or int(resp.text) <= 0:
        return False
    return True

def send_random_request(minimum, maximum, count):
    return requests.request('GET', 'https://www.random.org/integers/',
                            params={'num': count,
                                    'min': minimum,
                                    'max': maximum,
                                    'col': 1,
                                    'base': 10,
                                    'format': 'plain',
                                    'rnd': 'new'})


if __name__ == "__main__":
    main()