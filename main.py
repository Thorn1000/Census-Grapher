import requests
import time
import datetime
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np


def fetch_census_data(nation, target, scale):
    headers = {
        "User-Agent": f"Census Grapher/0.1 (github: https://github.com/Thorn1000 ; user:{nation}; Authenticating)"
    }
    # url = "https://www.nationstates.net/cgi-bin/api.cgi?nation={};q=census;scale={};mode=history;from=1641013201".format(target, scale)
    url = "https://www.nationstates.net/cgi-bin/api.cgi?nation={};q=census;scale={};mode=history;from=1714449600".format(
        target, scale)
    response = requests.get(url, headers=headers)
    time.sleep(0.6)  # Wait for 600ms before making the next request
    return response.text


def parse_census_data(xml_data):
    root = ET.fromstring(xml_data)
    points = root.findall('.//POINT')
    x_coords = []
    y_coords = []
    for point in points:
        timestamp = int(point.find('TIMESTAMP').text)
        score = float(point.find('SCORE').text)
        x_coords.append(timestamp)
        y_coords.append(score)
    return x_coords, y_coords


def normalize_data(y_coords):
    min_val = min(y_coords)
    max_val = max(y_coords)
    normalized_data = [(val - min_val) / (max_val - min_val) for val in y_coords]
    return normalized_data


def plot_census_graph(stats_data, target):
    fig, ax = plt.subplots()

    for stat_data in stats_data:
        x_dates = [datetime.datetime.fromtimestamp(timestamp) for timestamp in stat_data['x_coords']]
        normalized_y = normalize_data(stat_data['y_coords'])
        ax.plot(x_dates, normalized_y, label=stat_data['label'])

    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Score')
    ax.set_title("Census Scores over Time for {}".format(target))
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()  # Format x-axis date labels
    plt.show()


def main():
    nation = input("Enter your main nation: ")
    target = input("Enter the nation you are graphing: ")

    num_stats = int(input("Enter the number of stats you want to graph: "))
    arr_stats = []

    stats_data = []
    for i in range(num_stats):
        scale = input("Enter scale {}: ".format(i + 1))
        label = input("Enter label for scale {}: ".format(i + 1))
        xml_data = fetch_census_data(nation, target, scale)
        x_coords, y_coords = parse_census_data(xml_data)
        stats_data.append({'x_coords': x_coords, 'y_coords': y_coords, 'label': label})

        arr_stats += y_coords

    plot_census_graph(stats_data, target)

    if num_stats == 2:
        one = arr_stats[:len(arr_stats) // 2]
        two = arr_stats[len(arr_stats) // 2:]
        r = np.corrcoef(one, two)

    print(r)


if __name__ == "__main__":
    main()
