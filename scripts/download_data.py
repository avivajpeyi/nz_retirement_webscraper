import requests
import pandas as pd
from bs4 import BeautifulSoup


# Send a GET request to the website


def main(csv_fname: str):
    url = "https://www.retirementvillages.org.nz/tools/clients/directory.aspx?SECT=Auckland#Auckland"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    all_data = []

    villages = soup.find_all('table')
    for village in villages:
        rows = village.find_all('tr')
        data = {}
        for row in rows:
            columns = row.find_all('td')
            for column in columns:
                if column.get('class') is None:
                    continue
                class_name = column.get('class')
                if not isinstance(class_name, str):
                    class_name = " ".join(class_name)
                txt = column.get_text()
                data[class_name] = txt
        all_data.append(data)

    df = pd.DataFrame(all_data)
    # drop 'report' 'keyterms' 'villageWeb' columns
    df = df.drop(columns=['report', 'keyterms', 'villagesCol VillageWeb'])
    df.rename(columns={
        'villagesCol VillageAddress': 'Address',
        'villagesCol VillageOrganisation': 'Name',
        'villagesCol VillagePhone': 'Phone+Fax',
        'villagesCol VillageAge': 'Minimum Age',
        'villagesCol': 'Electorate',

    }, inplace=True)
    df = df.applymap(lambda x: x.replace('\r', '').replace('\n', '') if isinstance(x, str) else x)

    # Clean address
    df['Address'] = df['Address'].str.replace('Street Address: ', '')
    df['Address'] = df['Address'].str.strip()

    # Clean phone+fax to separate phone and fax columns
    df['Phone+Fax'] = df['Phone+Fax'].str.replace(' ', '')
    df['Phone+Fax'] = df['Phone+Fax'].str.replace('-', '')
    df['Phone'] = df['Phone+Fax'].str.extract(r'Phone:(\d+)')
    df['Fax'] = df['Phone+Fax'].str.extract(r'Fax:(\d+)')
    df['Phone'] = df['Phone'].fillna(df['Phone+Fax'])
    df = df.drop(columns=['Phone+Fax'])

    # remove "Electorate: " from Electorate column
    df['Electorate'] = df['Electorate'].str.replace('Electorate: ', '')

    # remove "Minimum Age Entry for New Residents: " from Minimum Age column
    df['Minimum Age'] = df['Minimum Age'].str.replace('Minimum Age Entry for New Residents: ', '')

    df.to_csv(csv_fname, index=False)
    print(f"Data saved to {csv_fname}")


if __name__ == "__main__":
    main("retirement_villages.csv")
