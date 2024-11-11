if __name__ == '__main__':
    with open('archive.nono', 'r') as file:
        for line in file:
            if line[0] == "#":
                continue

            elements = line.split(';')

            nonogram_id = elements.pop(0)
            author_id = elements.pop(0)
            nonogram_title = elements.pop(0)
            author_name = elements.pop(0)
            is_adult = elements.pop(0)
            column_count = int(elements.pop(0))
            row_count = int(elements.pop(0))
            color_count = int(elements.pop(0))
            colors = elements.pop(0).split(',')

            column_cells = []
            column_colors = []

            for _ in range(column_count):
                column_cells.append([int(x) for x in elements.pop(0).split(',') if x])

            if color_count == 1:
                elements.pop(0)
            else:
                for _ in range(column_count):
                    column_colors.append([int(x) for x in elements.pop(0).split(',') if x])

            row_cells = []
            row_colors = []

            for _ in range(row_count):
                row_cells.append([int(x) for x in elements.pop(0).split(',') if x])

            if color_count == 1:
                elements.pop(0)
            else:
                for _ in range(row_count):
                    row_colors.append([int(x) for x in elements.pop(0).split(',') if x])

            print(f"id: {nonogram_id}")
            print(f"title: {nonogram_title}")
            print(f"author_name: {author_name}")
            print(f"author_id: {author_id}")
            print(f"is_adult: {is_adult == '1'}")
            print(f"column_count: {column_count}")
            print(f"rows_count: {row_count}")
            print(f"color_count: {color_count}")
            print(f"colors: {colors}")
            print(f"column_cells: {column_cells}")
            print(f"column_colors: {column_colors}")
            print(f"row_cells: {row_cells}")
            print(f"row_colors: {row_colors}")
