import sys, re, datetime, json, csv, os
from selenium import webdriver

def get_digimon_codes(driver):
   digimon_list_url = r'https://www.grindosaur.com/en/games/digimon/digimon-story-cyber-sleuth/digimon'

   driver.get(digimon_list_url)   

   table = driver.find_element_by_id('searchable-table')

   rows = table.find_elements_by_tag_name('tr')

   digimon_codes = []

   for row in rows:
      tds = row.find_elements_by_tag_name('td')
      a_element = tds[2].find_element_by_tag_name('a')
      url = a_element.get_attribute('href')

      digimon_code = url.split('/')[-1]
      digimon_codes.append(digimon_code)

   return digimon_codes

'''

gets an object representing the digimmon's evolutions, for example:

{
   'evolves from' : [
      'digimon_code3',
      'digimon_code4'
   ],
   'evolves to' : [
      'digimon_code1',
      'digimon_code2'
   ]
}

'''
def get_digimon_evolutions(driver, digimon_code):
   digimon_info_base_url = r'https://www.grindosaur.com/en/games/digimon/digimon-story-cyber-sleuth/digimon'
   digimon_url = digimon_info_base_url + '/' + digimon_code

   # print(digimon_url)

   driver.get(digimon_url)
   # print(driver.page_source)

   html = driver.page_source

   evolves_to_table_html = find_expr_in_html(
      r'<h2[\s]+id="evolves-to"[\s]+class="[^"]+">[^<]+</h2>[\s]*</div>[\s]*<div[\s]+class="box">[\s]*<div[\s]*class="element-overflow">[\s]*(<table[\s]+class="table">.*</table>)',
      html
   )[0]

   tbody_html = find_expr_in_html(
      r'<tbody>(.*?)</tbody>',
      evolves_to_table_html
   )[0]

   rows_html = find_expr_in_html(
      r'<tr>(.*)</tr>',
      tbody_html
   )

   print(rows_html)
   print(len(rows_html))

def get_level_99_base_stats(driver, digimon_code):
   digimon_info_base_url = r'https://www.grindosaur.com/en/games/digimon/digimon-story-cyber-sleuth/digimon'
   digimon_url = digimon_info_base_url + '/' + digimon_code

   driver.get(digimon_url)
   html = driver.page_source

   stats_table_html = find_expr_in_html(
      r'<h2 id="base-stats"[^>]+>[^<]+<\/h2></div><div[^>]+>\s*<div[^>]+>\s*(<table[^>]+>.*?</table>)',
      html
   )[0]

   stats_list_html = find_expr_in_html(
      r'<tr>.*?</tr>',
      stats_table_html
   )

   stats = {}

   for html in stats_list_html:

      stat_name = find_expr_in_html(
         r'<th[^>]+>(.*?)</th>',
         html
      )[0]

      if stat_name == 'Stats':
         continue
   
      # the level 99 value of the stat
      level_99_val = find_expr_in_html(
         r'<td>(.*?)</td>',
         html
      )[-1]

      stats[stat_name] = level_99_val

   return stats


def find_expr_in_html(expr, html):
    return re.findall(expr, html, re.S)

start_date = datetime.datetime.now()
print("start: {}\n".format(start_date))

workspace = os.path.dirname(os.path.abspath(__file__))
csv_path = workspace + r'\digimon_stats.csv'
json_path = workspace + r'\digimon_data.json'

stat_data = None

if os.path.exists(json_path):
   with open(json_path) as json_data_file:
      stat_data = json.load(json_data_file)

if os.path.exists(csv_path):
   os.remove(csv_path)

fields = ['Name', 'HP', 'SP', 'ATK', 'INT', 'DEF', 'SPD', 'Total']
with open(csv_path, 'a') as stat_csv:
   writer = csv.writer(stat_csv, lineterminator="\n")
   writer.writerow(fields)

if stat_data is None:
   options = webdriver.ChromeOptions()
   options.add_argument('headless')

   driver = webdriver.Chrome('./chromedriver', options=options)

   digimon_codes = get_digimon_codes(driver)

   stat_data = {}

   for digimon_code in digimon_codes:
      print(digimon_code)
      level_99_base_stats = get_level_99_base_stats(driver, digimon_code)

      stat_data[digimon_code] = level_99_base_stats

      row = [
         digimon_code,
         level_99_base_stats['HP'],
         level_99_base_stats['SP'],
         level_99_base_stats['ATK'],
         level_99_base_stats['INT'],
         level_99_base_stats['DEF'],
         level_99_base_stats['SPD'],
         level_99_base_stats['Total']
      ]

      with open(csv_path, 'a') as stat_csv:
         writer = csv.writer(stat_csv, lineterminator="\n")
         writer.writerow(row)

   with open('./digimon_data.json', 'w') as outfile:
      json.dump(stat_data, outfile)

   driver.quit()
else:
   for key in stat_data:
      print(key)

end_date = datetime.datetime.now()
print("\nend: {}\n".format(end_date))
print("time elapsed: {}".format(end_date - start_date))