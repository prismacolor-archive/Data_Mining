import csv
import collections
import requests
from bs4 import BeautifulSoup


def find_school_data():
    master_list = []
    filename = 'school_contact_info.csv'
    school_item = collections.OrderedDict()
    max_count = 46

    for page in range(1, max_count):
        url = 'https://www.dallasisd.org//site/UserControls/Minibase/MinibaseListWrapper.aspx?ModuleInstanceID=26169&PageModuleInstanceID=66105&FilterFields=&DirectoryType=C&PageIndex=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")

        # Gather the school information
        school_data_list = soup.find_all('span')

        for link in school_data_list:
            data_point = link.text
            extra_info = ['School Name:', 'Address:', 'Phone:', 'Trustee District:', 'Grades:', 'Website']
            if data_point in extra_info or 'District' in data_point:
                continue
            else:
                if 'School' in data_point:
                    school_item['Name'] = data_point
                elif 'TX' in data_point:
                    school_item['Address'] = data_point
                elif '(' in data_point:
                    school_item['Phone Number'] = data_point
                elif '-' in data_point:
                    continue
                elif 'www' in data_point:
                    school_item['Website'] = data_point

                if len(school_item) == 4:
                    master_list.append(school_item)
                    school_item = collections.OrderedDict()

    # create the csv with the school data
    with open(filename, 'w+') as f:
        writer = csv.DictWriter(f, ['Name', 'Address', 'Phone Number', 'Website'])
        writer.writeheader()

        for item in master_list:
            writer.writerow(item)


find_school_data()
