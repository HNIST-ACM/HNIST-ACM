from json import dump
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from openpyxl import load_workbook
from requests import get

wb = load_workbook('info/id.xlsx')

info: dict[int, list[dict]] = {}
cf_ids: list[str] = []
for ws in wb:
    users = info[ws.title] = []
    for row in ws.iter_rows(2):
        row: tuple[str, str, str, str] = tuple(map(lambda s: str(s.value).strip()
                                                   if s.value else None, row))
        name = row[0]
        if not name:
            break

        users.append({
            'name': name,
            'cf': {'id': row[1]},
            'nc': {'id': row[2]},
            'atc': {'id': row[3]}
        })
        if row[1] is not None:
            cf_ids.append(row[1])

wb.close()

# 统一获取 cf rating
cf_url = f"https://codeforces.com/api/user.info?checkHistoricHandles=false&handles={';'.join(cf_ids)}"
cf_res: dict = get(cf_url).json()
if cf_res['status'] != 'OK':
    raise Exception(cf_res['comment'])

cf_rating_color = {
    'unrated': '#000000',
    'headquarters': '#000000',
    'newbie': '#808080',
    'pupil': '#008000',
    'specialist': '#03a89e',
    'expert': '#0000ff',
    'candidate master': '#aa00aa',
    'master': '#ff8c00',
    'grandmaster': '#ff0000',
    'international master': '#ff0000',
}

cf_res_map = {user['handle']: {'rating': user['rating'], 'color': cf_rating_color[user['rank']]}
              if 'rating' in user else {'rating': 'unrated', 'color': cf_rating_color['unrated']} for user in cf_res['result']}


nc_rating_color = {
    'rate-score5': '#ffd700',
    'rate-score4': '#25bb9b',
    'rate-score3': '#5ea1f4',
    'rate-score2': '#c177e7',
    'rate-score1': '#b4b4b4',
}

for users in info.values():
    for user in users:
        # codeforces
        cf_info: dict = user['cf']
        if cf_info['id'] is not None:
            cf_info.update(cf_res_map[cf_info['id']])

        # 牛客
        nc_info: dict = user['nc']
        if nc_info['id'] is not None:
            nc_url = f"https://ac.nowcoder.com/acm/contest/rating-index?searchUserName={nc_info['id']}"
            nc_res = get(nc_url).text

            bs = BeautifulSoup(nc_res, 'html.parser')
            tbody: Tag = bs.find('tbody')
            if tbody is not None:
                tr: Tag = bs.find('tbody').tr
                nc_info['uid'] = tr['data-uid']
                span: Tag = tr.find_all('td')[4].span
                nc_info['rating'] = int(span.get_text())
                nc_info['color'] = nc_rating_color[span['class'][0]]

Path('docs/public').mkdir(exist_ok=True)
with open('docs/public/info.json', 'w') as f:
    dump(info, f)
