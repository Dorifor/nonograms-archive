import requests
from bs4 import BeautifulSoup as bs4
from datetime import timedelta
import time

BASE_URL = "https://www.nonograms.org/nonograms/i/"
BASE_URL_COLOR = "https://www.nonograms.org/nonograms2/i/"
START_INDEX = 0
# START_INDEX = 5243  # it crashed lol
# START_INDEX = 11238  # it crashed lol
# START_INDEX = 14120  # it crashed lol
# START_INDEX = 15907  # it crashed lol
# START_INDEX = 20551  # it crashed lol
# MAX_INDEX = current_index + 100
MAX_INDEX = 100000


# returns tuple (non_empty_cells[] and colors_list[])
def get_consecutive_non_empty_cells(cells_list):
    _cells = []
    _colors = []

    cons = -1
    count = 0

    for cell in cells_list:
        # if 0 -> push count and color -> reset count and color -> continue
        if cell == 0:
            if cons == -1:
                continue
            _cells.append(count)
            _colors.append(cons - 1)
            count = 0
            cons = -1
            continue

        # if cons -> add count -> continue
        if cell == cons:
            count += 1
            continue

        # if diff -> push count and color -> reset count and set color to cell
        if cell != cons:
            if cons != -1:
                _cells.append(count)
                _colors.append(cons - 1)
            cons = cell
            count = 1
            continue

    if cons != -1:
        _cells.append(count)
        _colors.append(cons - 1)
    # nonograms.org actually uses a 0 as the end of an array to indicate last number, which is useless afaik
    # _cells.append(0)

    return _cells, _colors


def get_color_list(data, color_count):
    _colors = []

    for i in range(5, color_count + 5):
        color = hex((data[i][0] - data[4][1] + 256))[2:][1:] + hex(
            (data[i][1] - data[4][0] + 256 << 8) + (data[i][2] - data[4][3]))[2:][1:]

        _colors.append(color)

    return _colors


def get_result_grid(data, columns_count, rows_count, color_count):
    result_grid = []

    for i in range(columns_count):
        result_grid.append([])
        for _ in range(rows_count):
            result_grid[i].append(0)

    a = color_count + 5
    b = data[a][0] % data[a][3] * (data[a][0] % data[a][3]) + data[a][1] % data[a][3] * 2 + data[a][2] % data[a][3]
    c = a + 1
    for i in range(a + 2, a + b + 2):
        for j in range(data[i][0] - data[c][0] - 1, data[i][0] - data[c][0] + data[i][1] - data[c][1] - 1):
            result_grid[j][data[i][3] - data[c][3] - 1] = data[i][2] - data[c][2]

    return result_grid


def get_consecutive_cells_and_colors(result_grid, columns_count, rows_count):
    column_cells = []
    column_colors = []
    row_cells = []
    row_colors = []

    for i in range(columns_count):
        cells, colors = get_consecutive_non_empty_cells(result_grid[i])
        column_cells.append(cells)
        column_colors.append(colors)

    for i in range(rows_count):
        rows = [x[i] for x in result_grid]
        cells, colors = get_consecutive_non_empty_cells(rows)
        row_cells.append(cells)
        row_colors.append(colors)

    return column_cells, column_colors, row_cells, row_colors


def start_loop(start_index):
    with open('archive.nono', 'a', encoding="utf-8") as f:
        for _id in range(start_index, MAX_INDEX):
            res = requests.get(BASE_URL + str(_id))
            if res.status_code == 404:
                res = requests.get(BASE_URL_COLOR + str(_id))
                if res.status_code == 404:
                    continue

            soup = bs4(res.content, 'html.parser')

            is_deleted = soup.css.select_one('.content > div[style="color:red;font-size:16px;font-weight:bold;"]')

            if is_deleted:
                continue

            is_adult = 1 if soup.css.select_one('.nonogram_title_adult') else ''

            try:
                title = soup.css.select_one('#nonogram_title').text.replace(';', '-')
            except AttributeError:
                print('an error happened with the title line, probably a fetch mistake, restarting loop from this iteration')
                start_loop(_id)
                break

            author = soup.css.select_one('#nonogram_author_name')
            author_name = author.text.replace(';', '-') if author else ''
            author_id = author.attrs['href'].split('/')[-1] if author else ''

            raw_data_script = soup.select('.content')[0].find('script').string
            raw_data_string = raw_data_script.split("d=")[1].split(";")[0]
            raw_data = eval(raw_data_string)

            columns_count = raw_data[1][0] % raw_data[1][3] + raw_data[1][1] % raw_data[1][3] - raw_data[1][2] % raw_data[1][3]
            rows_count = raw_data[2][0] % raw_data[2][3] + raw_data[2][1] % raw_data[2][3] - raw_data[2][2] % raw_data[2][3]
            color_count = raw_data[3][0] % raw_data[3][3] + raw_data[3][1] % raw_data[3][3] - raw_data[3][2] % raw_data[3][3]

            colors = get_color_list(raw_data, color_count)

            result_grid = get_result_grid(raw_data, columns_count, rows_count, color_count)

            column_cells, column_colors, row_cells, row_colors = get_consecutive_cells_and_colors(result_grid, columns_count, rows_count)

            # print(f"id: {_id} ({BASE_URL}{_id})")
            # print(f"title: {title}")
            # print(f"author_name: {author_name}")
            # print(f"author_id: {author_id}")
            # print(f"column_count: {columns_count}")
            # print(f"rows_count: {rows_count}")
            # print(f"color_count: {color_count}")
            # print(f"colors: {colors}")
            # print(f"result_grid: {result_grid}")
            # print(f"column_cells: {column_cells}")
            # print(f"column_colors: {column_colors}")
            # print(f"row_cells: {row_cells}")
            # print(f"row_colors: {row_colors}")

            if color_count == 1:
                colors = []
                column_colors = ['']
                row_colors = ['']

            archive_line = [
                _id,
                author_id,
                title,
                author_name,
                is_adult,
                columns_count,
                rows_count,
                color_count,
                ','.join(colors),
                ';'.join([','.join(map(str, x)) for x in column_cells]),
                ';'.join([','.join(map(str, x)) for x in column_colors]),
                ';'.join([','.join(map(str, x)) for x in row_cells]),
                ';'.join([','.join(map(str, x)) for x in row_colors])
            ]

            f.write(f"{';'.join(map(str, archive_line))};\n")

            print(f"archived {_id} : {title}")

            # time.sleep(.1)  # trying not to make me banned


def main():
    start_time = time.time()
    start_loop(START_INDEX)
    end_time = time.time()

    print(f"time to archive {MAX_INDEX} nonograms: {str(timedelta(seconds=end_time - start_time))}")


if __name__ == '__main__':
    main()
