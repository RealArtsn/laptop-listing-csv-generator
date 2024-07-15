import time
def main():
    item = get_item_info()
    generate_title(item)
    generate_filename(item)
    generate_fields(item)

def prompt_default(prompt):
    return True if (input(prompt).lower() in ['', 'y']) else False

def generate_title(item):
    title_list = [item['model'], item['cpu'], item['ram'] + 'GB RAM']
    missing_list = []
    if item['has_storage']:
        title_list.append(f'{item['storage_capacity']}GB SSD')
    else:
        missing_list.append('SSD')
    if item['os'] == 'Not Included':
        missing_list.append('OS')
    else:
        title_list.append('WIN11 PRO')
    if item['has_battery']:
        title_list.append(f'{item['battery_health']}% BATT')
    else:
        missing_list.append('BATTERY')
    if len(missing_list):
        title_list.append('NO ' + '/'.join(missing_list))
    return f'{' | '.join(title_list)}'

def get_item_info():
    item = dict()
    item['model'] = input('Model: ')
    item['cpu'] = input('CPU: ')
    item['ram'] = input('RAM capacity (GB): ')
    item['has_storage'] = prompt_default('Storage? (Y/n): ')
    if item['has_storage']:
        item['storage_capacity'] = input('Storage capacity? (GB): ')
    item['has_battery'] = prompt_default('Contains battery? (Y/n): ')
    if item['has_battery']:
        item['battery_health'] = input('Battery health (%): ')
    # get OS
    item['os'] = prompt_os()
    item['sku'] = input('SKU: ')
    item['price'] = input('Price ($): ')
    item['quantity'] = '1'
    return item

def prompt_os():
    print('1: Windows 11 Pro\n2: Not Included')
    invalid_input = True
    while True:
        match input('1 or 2? '):
            case '1':
                return 'Windows 11 Pro'
            case '2':
                return 'Not Included'

def generate_filename(item: dict):
    return item['model'].replace(' ','-') + '_' + str(int(time.time())) + '.csv'

def generate_fields(item: dict):
    listing = {
        'Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)': 'Draft',
        'Custom label (SKU)': item['sku'],
        'Category ID': '177',
        'Title': generate_title(item),
        'C:Brand': item['model'].split(' ')[0],
        'C:Screen Size': item['screen_size'],
        'C:Processor': item['cpu'],
        'UPC': '',
        'C:Model': item['model'],
        'C:Operating System': item['os'],
        'C:SSD Capacity': item['storage_capacity'] + ' GB',
        'C:Features': '',
        'C:Type': 'Notebook/Laptop',
        'C:Hard Drive Capacity': 'N/A',
        'C:Storage Type': 'SSD (Solid State Drive)',
        'C:Unit Quantity': '1',
        'C:Unit Type': 'Unit',
        'C:Series': item['model'].split(' ')[1],
        'C:RAM Size': item['ram'] + ' GB',
        'C:Most Suitable For': 'Casual Computing',
        'C:Graphics Processing Type': 'Integrated/On-Board Graphics',
        'Price': item['price'],
        'Quantity': item['quantity'],
        'Condition ID': '3000',
        'ConditionNote': 'Test Condition',
        'Description': '',
        'Format': 'FixedPrice'
    }
    with open(generate_filename(item), 'w') as f:
        HEADER = "#INFO,Version=0.0.2,Template= eBay-draft-listings-template_US,,,,,,,,\n#INFO,,,,,,,,,,"
        f.write(HEADER + '\n')
        f.write(','.join(list(listing.keys())) + '\n' + ','.join(list(listing.values())))
main()