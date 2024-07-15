import time, re

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
        title_list.append(f'{item['storage_capacity']}GB {item['storage_type'].split(' ')[0]}')
    else:
        missing_list.append(item['storage_type'].split(' ')[0])
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
    item['gpu'] = prompt_gpu()
    print(item['gpu'])
    item['screen_size'] = input('Screen size (in): ')
    item['has_storage'] = prompt_default('Storage? (Y/n): ')
    if item['has_storage']:
        (item['storage_type'], item['storage_capacity']) = prompt_storage()
        item['Hard Drive Capacity'] = 'N/A'
        item['SSD Capacity'] = 'N/A'
        match item['storage_type']:
            case 'SSD (Solid State Drive)':
                item['SSD Capacity'] = item['storage_capacity'] + ' GB'
            case 'HDD (Hard Disk Drive)':
                item['Hard Drive Capacity'] = item['storage_capacity'] + ' GB'

    item['has_battery'] = prompt_default('Contains battery? (Y/n): ')
    if item['has_battery']:
        item['battery_health'] = input('Battery health (%): ')
    item['os'] = prompt_os()
    item['sku'] = input('SKU: ')
    item['price'] = input('Price ($): ')
    item['quantity'] = '1'
    return item

def prompt_os():
    return select_number_or_custom(['Windows 11 Pro', 'Not Included'])

def prompt_gpu():
    gpus = [
        'Intel HD Graphics',
        'Intel UHD Graphics',
        'Intel UHD Graphics 620',
        'Intel Iris XE Graphics',
    ]
    selected_gpu = select_number_or_custom(gpus)
    if selected_gpu in gpus:
        gpu_type = 'Integrated/On-Board Graphics'
        return [selected_gpu, gpu_type]
    gpu_types = [
        'Integrated/On-Board Graphics',
        'Hybrid Graphics',
        'Dedicated Graphics'
    ]
    gpu_type = select_number_or_custom(gpu_types)
    return [selected_gpu, gpu_type]

def prompt_storage():
    storage_types = [
        'SSD (Solid State Drive)',
        'HDD (Hard Disk Drive)'
    ]
    storage_type = select_number_or_custom(storage_types)
    while True:
        storage_capacity = input('Storage Capacity (GB): ')
        print(re.match('[0-9]*',storage_capacity))
        storage_capacity = re.match('[0-9]*',storage_capacity)[0]
        if storage_capacity == '':
            continue
        break    
    return (storage_type, storage_capacity)
    

def select_number_or_custom(choices):
    print('Select:')
    for choice in enumerate(choices):
        print(f'{choice[0] + 1}: {choice[1]}')
    while True:
        response = input('Select number or type custom: ')
        try:
            return choices[int(response) - 1]
        except(ValueError):
            return response
        except(IndexError):
            continue

def generate_filename(item: dict):
    return item['model'].replace(' ','-') + '_' + str(int(time.time())) + '.csv'

def generate_condition(item: dict):
    return 'Condition field test'

def get_description(file):
    with open(file) as f:
        return f'"{f.read()}"'

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
        'C:GPU': item['gpu'][0],
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
        'C:Graphics Processing Type': item['gpu'][1],
        'Price': item['price'],
        'Quantity': item['quantity'],
        'Condition ID': 'USED',
        'ConditionDescription': generate_condition(item), # TODO: FIX CONDITION
        'Description': get_description('template.html'),
        'Format': 'FixedPrice'
    }
    with open(generate_filename(item), 'w') as f:
        HEADER = "#INFO,Version=0.0.2,Template= eBay-draft-listings-template_US,,,,,,,,\n#INFO,,,,,,,,,,"
        f.write(HEADER + '\n')
        f.write(','.join(list(listing.keys())) + '\n' + ','.join(list(listing.values())))
main()