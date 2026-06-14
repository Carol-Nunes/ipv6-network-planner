'''
Funções auxiliares para conversão de hexadecimal <-> binário
'''

def ipv6_hextets_to_bit_string(ipv6_hextets):

    bit_string = ''

    for hextet in ipv6_hextets:

        for hex_digit in hextet:

            bit_string += f'{int(hex_digit, 16):04b}'

    return bit_string

def bit_string_to_ipv6_hextets(bit_string):

    ipv6_hextets = []

    # Corta o bloco de bits em 8 blocos de 16 bits. 
    for i in range(0, 128, 16):

        bit_group = bit_string[i: i + 16]

        # Para cada grupo de 16 bits obtidos, iremos 
        # convertê-los para hexadecimal. 
        hex_group = ''

        for j in range(0, 16, 4):

            hex_group += f"{int(bit_group[j:j+4], 2):X}"

        ipv6_hextets.append(hex_group)
    
    return ipv6_hextets    

'''
Converte bits + prefixo para string IPv6/CIDR (comprimida).
'''
def bits_to_prefix(bits_string, prefix):
    
    hextets = bit_string_to_ipv6_hextets(bits_string)
    ip = format_ipv6(hextets)
    return f'{ip}/{prefix}'

'''
Solicita ao usuário um bloco IPv6 válido.
Retorna o bloco IPv6 informado.
'''
def get_ipv6_block():

    while True:

        ipv6_block = input('\nEnter the IPv6 block (e.g. 2804:1f4a::/32): ')

        if validate_ipv6(ipv6_block):

            return ipv6_block

        print('\nInvalid IPv6 block. Try again.')

'''
Expande um endereço IPv6 abreviado para sua forma completa.
Exemplo:
2804:1f4a::/32
Então
2804:1f4a:0000:0000:0000:0000:0000:0000

A função retorna uma lista contendo os 8 blocos do IPv6,
cada um com 4 dígitos hexadecimais.
'''
def expand_ipv6(ipv6_block):

    # Separa o endereço IPv6 do tamanho do prefixo.
    ipv6_address = ipv6_block.split('/')[0]

    # Se o endereço estiver abreviado utilizando "::",
    # será necessário inserir os blocos de zeros faltantes.
    if "::" in ipv6_address:

        left_side, right_side = ipv6_address.split("::")

        left_blocks = []

        for block in left_side.split(":"):

            if block:

                left_blocks.append(block)

        right_blocks = []

        for block in right_side.split(":"):

            if block:

                right_blocks.append(block)

        # Calcula quantos blocos faltam para completar
        # os 8 blocos de um endereço IPv6.
        missing_blocks = 8 - (len(left_blocks) + len(right_blocks))

        # Cria os blocos de zeros que substituirão o "::".
        zero_blocks = ["0000"] * missing_blocks

        # Monta o IPv6 completo.
        ipv6_blocks = left_blocks + zero_blocks + right_blocks

    else:

        ipv6_blocks = ipv6_address.split(":")

    # Garante que todos os blocos possuam exatamente
    # 4 dígitos hexadecimais.
    expanded_blocks = []

    for block in ipv6_blocks:

        expanded_blocks.append(block.zfill(4))

    return expanded_blocks

def format_ipv6(ipv6_blocks):

    # Encontrar a maior sequência de blocos de '0000'
    longest_sequence_start = -1
    longest_sequence_length = 0
    current_sequence_start = -1
    current_sequence_length = 0

    # Percorremos os blocos a fim de encontrarmos a sequência mais longa
    # de '0000'
    for i, block in enumerate(ipv6_blocks):

        if block == '0000':

            if current_sequence_length == 0:

                current_sequence_start = i
        
            current_sequence_length += 1

        else:

            if current_sequence_length > longest_sequence_length:

                longest_sequence_length = current_sequence_length

                longest_sequence_start = current_sequence_start

            current_sequence_length = 0
            current_sequence_start = -1
    
    # Caso a maior sequência termine no último bloco.
    if current_sequence_length > longest_sequence_length:

        longest_sequence_length = current_sequence_length

        longest_sequence_start = current_sequence_start

    # Remove os zeros à esquerda de cada bloco. 
    formatted_blocks = []

    for block in ipv6_blocks:

        block = block.lstrip('0')

        if block == '':

            block = '0'
        
        formatted_blocks.append(block)
        
    # Se encontrarmos uma sequência de '0000' com mais de um bloco,
    # aplicamos o '::'. 
    if longest_sequence_length > 1:

        start = longest_sequence_start
        end = start + longest_sequence_length

        left_part = formatted_blocks[:start]
        right_part = formatted_blocks[end:]

        #Juntando as partes com o '::' no meio
        formatted_address = ':'.join(left_part) + '::' + ':'.join(right_part)

    else:

        # Se não tiver mais de um bloco, apenas juntamos com o ':'
        formatted_address = ':'.join(formatted_blocks)

    return formatted_address

'''
Valida um endereço IPv6 no formato IPv6/CIDR.
A função verifica:
Se o endereço está no formato correto (IPv6/CIDR);
Se o prefixo está entre 0 e 128;
Se existe no máximo uma ocorrência de "::";
Se a quantidade de blocos IPv6 é válida;
cada bloco possui no máximo 4 dígitos hexadecimais;
Se todos os caracteres pertencem ao conjunto hexadecimal.
Retorna True caso o endereço seja válido e False caso contrário.
'''

def validate_ipv6(ipv6_block):

    try:

        ipv6_address, prefix_length = ipv6_block.split('/')

        prefix_length = int(prefix_length)

    except:

        return False

    # Verifica se o prefixo está entre 0 e 128.
    if prefix_length < 0 or prefix_length > 128:

        return False
    
    # Verifica se existe mais de um "::".
    if ipv6_address.count('::') > 1:

        return False 
    
    # Se existir "::", contamos os blocos dos dois lados.
    if '::' in ipv6_address:

        left_part, right_part = ipv6_address.split('::')

        left_blocks = []

        for block in left_part.split(':'):

            if block: 

                left_blocks.append(block)

        right_blocks = []

        for block in right_part.split(':'):

            if block:

                right_blocks.append(block)

        left_blocks_length = len(left_blocks)
        right_blocks_length = len(right_blocks)

        if(left_blocks_length + right_blocks_length) >= 8:

            return False
        
        blocks = left_blocks + right_blocks

    else:

        blocks = ipv6_address.split(':')

        blocks_length = len(blocks)

        if blocks_length != 8:

            return False
        
    # Verifica tamanho dos blocos e caracteres hexadecimais.
    valid_chars = "0123456789abcdefABCDEF"

    for block in blocks:

        if len(block) > 4:

            return False
        
        for char in block:

            if char not in valid_chars:

                return False
            
    return True


def get_number_of_clients():

    while True:

        try:

            num_clients = int(input('\nEnter the number of clients: '))

            if num_clients > 0:

                return num_clients

            print('\nThe number of clients must be greater than zero.')

        except:

            print('\nInvalid number. Try again.')

'''
Aloca a primeira rede disponível utilizando
o algoritmo Leftmost Allocation.
'''

def leftmost_allocation(clients_networks):
    
    clients_networks_length = len(clients_networks)

    if clients_networks_length == 0:

        return None
    
    return clients_networks.pop(0)

'''
Aloca a última rede disponível utilizando
o algoritmo Rightmost Allocation.
'''

def rightmost_allocation(clients_networks):

    clients_networks_length = len(clients_networks)

    if clients_networks_length == 0:

        return None
    
    return clients_networks.pop()

'''
Reserva um endereço Anycast dentro do bloco destinado
à categoria Anycast da localidade.

Por convenção neste trabalho, o endereço reservado
corresponde ao identificador ::1 do bloco.
'''

def reserve_anycast(subnet_ipv6):
    
    anycast_address_blocks = expand_ipv6(subnet_ipv6)

    # Utiliza o identificador ::1 como endereço Anycast.
    anycast_address_blocks[7] = '0001'

    formatted_anycast = format_ipv6(anycast_address_blocks)

    return formatted_anycast

'''
Gera uma sub-rede IPv6 a partir de um bloco pai utilizando manipulação de bits.

A função divide o espaço de endereçamento disponível entre o prefixo pai e o novo prefixo,
calculando quantas sub-redes são possíveis e utilizando um offset para selecionar a posição
da sub-rede dentro do espaço disponível.
'''

def generate_subnets(parent_bits, parent_prefix, new_prefix, offset):

    # Você NÃO pode criar uma rede “maior” que a anterior.
    if new_prefix < parent_prefix:

        raise ValueError("new_prefix cannot be less than parent_prefix")
    
    # Verificando quantos bits estão disponíveis para a criação da subrede. 
    bits_needed = new_prefix - parent_prefix

    max_offset = (2 ** bits_needed) - 1

    if offset > max_offset:

        raise ValueError(f"Offset {offset} exceeds limit for {bits_needed} bits")
    
    # Mantém a parte fixa da rede pai. 
    new_bits = parent_bits[:parent_prefix]

    # Transforma o offset em binário. 
    # Pega o offset, transforma em binário (por isso o b), 
    # adiciona zeros à esquerda (por isso o 0) e deixa no tamanho 
    # da quantidade de bits que estarão disponsíveis para a subrede. 
    offset_bits = format(offset, f'0{bits_needed}b')

    new_bits += offset_bits

    # Zerando a parte de host 
    new_bits += '0' * (128 - new_prefix)

    return new_bits

'''
Gera uma lista de sub-redes IPv6 exclusivas de uma rede para um número específico de clientes.
'''

def generate_clients_networks(parent_prefix, num_clients, new_prefix):

    parent_address = parent_prefix.split('/')[0]

    parent_address_hextets = expand_ipv6(parent_address)

    parent_address_bits = ipv6_hextets_to_bit_string(parent_address_hextets)

    parent_prefix_len = int(parent_prefix.split('/')[1])

    client_networks = []

    # Percorre o número de clientes para gerar uma sub-rede para cada um
    for i in range(num_clients):

        client_bits = generate_subnets(parent_address_bits, parent_prefix_len, new_prefix, i)

        client_prefix = bits_to_prefix(client_bits, new_prefix)

        client_networks.append(client_prefix)

    
    return client_networks


def generate_ipv6_planning():

    # Entrada do endereço base, expansão dele, 
    # conversão para binário e captura do prefixo. 
    main_block = get_ipv6_block()
    expanded_main_block = expand_ipv6(main_block)
    main_block_bits = ipv6_hextets_to_bit_string(expanded_main_block)
    main_block_prefix = int(main_block.split('/')[1])

    if main_block_prefix != 32:

        raise ValueError("The main block must be /32 for this planning.")
    
    # Zerando a parte de host só por garantia. 
    main_block_bits = main_block_bits[:main_block_prefix] + '0' * (128 - main_block_prefix)

    # Aqui, eu optei por criar listas fixas a fim de facilitar o programa. 
    # Aí caso, queira colocar novas cidades é só adicionar na lista. 
    cities = ["São Paulo", "Rio de Janeiro", "Curitiba", "Recife", "Porto Alegre"]
    categories = ["residencial", "corporativo", "infraestrutura", "servicos_internos", "anycast"]

    # Segundo a Aula 05, os prefixos devem ser distribuídos da seguinte maneira: 
    # residencial: /40 
    # corporativo: /40 
    # infraestrutura: /48
    # servicos_internos: /48
    # anycast: /64
    categories_prefixes = {
        'residencial': 40,
        'corporativo': 40,
        'infraestrutura': 48,
        'servicos_internos': 48,
        'anycast': 64
    } 

    num_clients = get_number_of_clients()

    planning = {}

    for i, city in enumerate(cities):

        # Segundo a Aula 5, as cidades devem receber prefixo /36. 
        city_bits = generate_subnets(main_block_bits, 32, 36, i)
        city_prefix = bits_to_prefix(city_bits, 36)

        city_data = {

            'prefix': city_prefix,
            'categories': {}
        }

        # Gerando os blocos de ipv6 para cada categoria. 
        for i, category in enumerate(categories):

            categorie_bits = generate_subnets(city_bits, 36, categories_prefixes[category], i)
            categorie_prefix = bits_to_prefix(categorie_bits, categories_prefixes[category])

            city_data['categories'][category] = {

                'prefix': categorie_prefix,
                'clients': []
            }

        # Gerando clientes residenciais. 
        # Segundo a aula 5, a partir do bloco /40, geramos /56
        residential_prefix = city_data['categories']['residencial']['prefix']

        residential_clients = generate_clients_networks(residential_prefix, num_clients, 56)

        city_data['categories']['residencial']['clients'] = residential_clients

        # Gerando clientes corporativos. 
        # Segundo a aula 5, a partir do bloco /40, geramos /48
        corporative_prefix = city_data['categories']['corporativo']['prefix']

        corporative_clients = generate_clients_networks(corporative_prefix, num_clients, 48)

        city_data['categories']['corporativo']['clients'] = corporative_clients

        # Reservando endereços anycast 
        anycast_prefix = city_data['categories']['anycast']['prefix']

        anycast_address = reserve_anycast(anycast_prefix)

        city_data['categories']['anycast']['address'] = anycast_address

        planning[city] = city_data


    return planning, main_block

'''
Exibe toda a estrutura de planejamento IPv6
gerada pelo sistema.
'''

def show_planning(planning, ipv6_block):

    print('\n=========================================')
    print('IPv6 Planning')
    print('=========================================')
    print(f'\nIPv6 block: {ipv6_block}')

    for city, data in planning.items():

        print(f'\nCity: {city}')

        print(f'City Prefix: {data['prefix']}')

        for cat_name, cat_data in data['categories'].items():

            print(f'\n    Category: {cat_name}')

            print(f'    Block: {cat_data["prefix"]}')

            if cat_name == 'anycast':

                print(f'    Reserved Address: {cat_data["address"]}')

            if cat_data['clients']:

                print('    Client Networks:')

                for i, net in enumerate(cat_data['clients']):

                    print(f'        Client {i + 1} -> {net}')

            else:

                print('    (No clients generated for this category)')

'''
Permite ao usuário selecionar uma localidade
do planejamento IPv6.

Retorna o nome da localidade selecionada.
'''
def select_city(planning):

    cities = list(planning.keys())

    while True:

        try:

            print('\nSelect a city:\n')

            for i, city in enumerate(cities):

                print(f'{i + 1} - {city}')

            option = int(input('\nOption: '))

            if 1 <= option <= len(cities):

                return cities[option - 1]

            print('\nInvalid option. Try again.')

        except:

            print('\nInvalid option. Try again.')

'''
Permite ao usuário selecionar uma sub-rede
de uma determinada localidade.

Retorna o nome da sub-rede selecionada.
'''
def select_client_category(planning, location):

    categories = ['residencial', 'corporativo']

    while True:

        try:

            print('\nSelect a category:\n')

            for i, category in enumerate(categories):

                print(f'{i + 1} - {category}')

            option = int(input('\nOption: '))

            if 1<= option <= len(categories):

                return categories[option - 1]

            print('\nInvalid option. Try again.')

        except:

            print('\nInvalid option. Try again.')
'''
Simula a alocação de uma rede IPv6 utilizando
o algoritmo Leftmost Allocation.
'''
def simulate_leftmost(planning):

    city = select_city(planning)

    category = select_client_category(planning, city)

    clients_list = planning[city]['categories'][category]['clients']

    allocated_network = leftmost_allocation(clients_list)

    print(f'\nCity: {city}')

    print(f'Category: {category}')

    if allocated_network is None:

        print('\nNo client networks available.')

        return

    print(f'\nAllocated Network: {allocated_network}')

'''
Simula a alocação de uma rede IPv6 utilizando
o algoritmo Rightmost Allocation.
'''
def simulate_rightmost(planning):

    city = select_city(planning)

    category = select_client_category(planning,city)

    clients_list = planning[city]['categories'][category]['clients']

    allocated_network = rightmost_allocation(clients_list)

    print(f'\nCity: {city}')

    print(f'Category: {category}')

    if allocated_network is None:

        print('\nNo client networks available.')

        return

    print(f'\nAllocated Network: {allocated_network}')

def show_menu():

    
    print('\n=========================================')
    print(' IPv6 Network Planner ')
    print('=========================================')
    print('1 - Generate IPv6 Planning')
    print('2 - Simulate Leftmost Allocation')
    print('3 - Simulate Rightmost Allocation')
    print('0 - Exit')
    print('=========================================')

def menu():

    planning = None

    while True:

        show_menu()

        option = input('Enter the option: ')

        if option == '1':

            try:

                planning, main_block = generate_ipv6_planning()

                show_planning(planning, main_block)

            except ValueError as error:

                print(f'\nError: {error}')

        elif option == '2':

            if planning is None:

                print('\nGenerate an IPv6 planning first.')

            else:

                simulate_leftmost(planning)

        elif option == '3':

            if planning is None:

                print('\nGenerate an IPv6 planning first.')

            else:

                simulate_rightmost(planning)


        elif option == '0':

                print('\nExiting program...')
                break

        else:

                print('\nInvalid option.')



if __name__ == "__main__":
    menu()