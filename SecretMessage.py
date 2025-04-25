''' 
Title: Decoding a Secret Message 
Author: Matt Davies
Date: April 23, 2025

This program utilizes requests and BeautifulSoup libraries to extract rows, cells, 
and headers from a public document that has a table with symbols and associated x and y 
coordinates for the given symbol. This program parses each symbol with its xy-coordinates 
and then plots each symbol on a 2D-plane revealing a secret message.
'''

import requests # used to fetch data from websites
from bs4 import BeautifulSoup   # used to pull data from any HTML or XML files

def decode_secret_message(doc_url):
    def get_data_from_public_doc(url):
        try:
            response = requests.get(url)    # This sends an HTTP GET request to the URL stored in doc_url
            response.raise_for_status()     # checks for errors
            soup = BeautifulSoup(response.text, 'html.parser')  # response.text takes raw HTML doc a string while 'html.parser' uses beautiful soup's parser
            data = []

            rows = soup.find_all('tr')  # rows is equal to the data in the 'tr' which means table row in HTML.
            for row in rows:
                cells = row.find_all(['td', 'th'])  # cells is equal to the data in the 'td' table data and the 'th' table headers.
                row_data = [cell.get_text(strip=True) for cell in cells]    # row_data extracts and cleans up the text from each cell in a table row parsed from HTML.

                if len(row_data) == 3:
                    try:
                        if row_data[1] in ['█', '░', '▀']:
                            x = int(row_data[0])
                            char = row_data[1]
                            y = int(row_data[2])
                        elif row_data[2] in ['█', '░', '▀']:
                            x = int(row_data[0])
                            y = int(row_data[1])
                            char = row_data[2]
                        else:
                            raise ValueError("Invalid character format")
                        data.append((x, y, char))
                    except ValueError:
                        continue  # Skip bad rows
            return data
        except requests.RequestException:
            print("Failed to fetch or parse the document.")
            return []

    # Convert the data array of tuples into a grid and insert the whitespace where needed
    # symbols are plotted at valid xy-coordinates
    def convert_data_to_grid(data):
        if not data:
            return []
        max_x = max(x for x, y, _ in data) + 1   # These lines figure out how wide and tall the grid needs to be.
        max_y = max(y for x, y, _ in data) + 1
        grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]
        for x, y, char in data:
            grid[y][x] = char
        return grid

    # function to print the secret message
    def print_grid(grid):
        print(f"\nDecoded Secret Message:\n")
        for row in grid:
            print(''.join(cell if cell in ['█', '░', '▀'] else ' ' for cell in row))

    # Main logic
    data = get_data_from_public_doc(doc_url)
    if data:
        grid = convert_data_to_grid(data)
        print_grid(grid)
    else:
        print("No valid data found.")


def main():
    decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")

if __name__ == "__main__":
    main()
