import requests
def get_excel(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('local_file.xlsx', 'wb') as f:
            f.write(response.content)
        return response.content
    else:
        return 'local_file.xlsx'
        print(f"Failed to download file. Status code: {response.status_code}")

