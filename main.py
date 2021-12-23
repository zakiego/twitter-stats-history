import pandas as pd
import requests as req


def get_data(username):
    url = "https://app.zakiego.my.id/api/twitter/v1/public?username="
    resp = req.get(url + username)
    data = resp.json()['data']
    df = pd.DataFrame(data, index=[0])
    return df


def read_before():
    before = pd.read_csv('user.csv')
    return before


def get_and_combine(username):
    new = get_data(username)
    before = read_before()

    # combine dataframe
    final = pd.concat([new, before]).reset_index(drop=True)

    # change column format
    final['id'] = final['id'].astype('int')
    final['timestamp'] = pd.to_datetime(final['timestamp'])

    # sort dataframe
    final = final.sort_values(by=['id', 'timestamp'], ascending=[True, False])

    # save dataframe to csv
    final.to_csv("user.csv", index=False)


def main():
    with open("list_user.txt") as file:
        users = file.read()
        users = users.split(",")
        for user in users:
            get_and_combine(user)


if __name__ == "__main__":
    main()
