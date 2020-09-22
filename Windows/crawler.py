import sys, re
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

def get_digimon_base_stats(driver, digimon_code):
   digimon_info_base_url = r'https://www.grindosaur.com/en/games/digimon/digimon-story-cyber-sleuth/digimon'
   digimon_url = digimon_info_base_url + '/' + digimon_code

   driver.get(digimon_url)
   html = driver.page_source

   stats_table_html = find_expr_in_html(
      r'<h2 id="base-stats"[^>]+>[^<]+<\/h2></div><div[^>]+>\s*<div[^>]+>\s*(<table[^>]+>.*?</table>)',
      # r'<h2 id="base-stats"[^>]+>',
      html
   )

   print(stats_table_html)

def find_expr_in_html(expr, html):
    return re.findall(expr, html, re.S)

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(options=options)

# get_digimon_evolutions(driver, '1-kuramon')
get_digimon_base_stats(driver, '1-kuramon')

# digimon_codes = get_digimon_codes(driver)

# for digimon_code in digimon_codes:
#    print(digimon_code)
#    get_digimon_evolutions(driver, digimon_code)
#    sys.exit()









driver.quit()