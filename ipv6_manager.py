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
Reserva um endereço IPv6 para utilização como Anycast.

O endereço reservado corresponde ao primeiro endereço utilizável
da sub-rede, sendo representado pelo identificador ::1.
'''

def reserve_anycast(subnet_ipv6):
    
    anycast_address_blocks = expand_ipv6(subnet_ipv6)

    # Utiliza o identificador ::1 como endereço Anycast.
    anycast_address_blocks[7] = '0001'

    formatted_anycast = format_ipv6(anycast_address_blocks)

    return formatted_anycast

def generate_ipv6_planning():

    ipv6_block = get_ipv6_block()

    locations_ipv6 = generate_locations(ipv6_block)

    subnets = get_subnets()

    num_clients = get_number_of_clients()

    planning = {}

    for location, location_prefix in locations_ipv6.items():

        planning[location] = {}

        subnets_ipv6 = generate_subnets(location_prefix, subnets)

        for subnet, subnet_prefix in subnets_ipv6.items():

            clients_networks = generate_clients_networks(subnet_prefix, num_clients)

            anycast_address = reserve_anycast(subnet_prefix)

            planning[location][subnet] = {

                'prefix': subnet_prefix,
                
                'anycast': anycast_address,

                'clients_networks': clients_networks
            }

    return planning, ipv6_block, locations_ipv6

'''
Exibe toda a estrutura de planejamento IPv6
gerada pelo sistema.
'''

def show_planning(planning, ipv6_block, locations_ipv6):

    print('\n=========================================')
    print('IPv6 Planning')
    print('=========================================')
    print(f'\nIPv6 block: {ipv6_block}')

    for location, subnets in planning.items():

        print(f'\nLocation: {location}')

        print(f'Location Prefix: {locations_ipv6[location]}')

        for subnet, subnet_data in subnets.items():

            print(f'\n    Subnet: {subnet}')

            print(f'    Prefix: '
                f'{subnet_data["prefix"]}')

            print(f'    Anycast: '
                f'{subnet_data["anycast"]}')

            print('\n    Client Networks:')

            for i, network in enumerate(subnet_data['clients_networks']):

                print(f'        Client Network {i + 1}'
                    f' -> {network}')
'''
Permite ao usuário selecionar uma localidade
do planejamento IPv6.

Retorna o nome da localidade selecionada.
'''
def select_location(planning):

    locations = list(planning.keys())

    while True:

        try:

            print('\nSelect a location:\n')

            for i, location in enumerate(locations):

                print(f'{i + 1} - {location}')

            option = int(input('\nOption: '))

            if 1 <= option <= len(locations):

                return locations[option - 1]

            print('\nInvalid option. Try again.')

        except:

            print('\nInvalid option. Try again.')

'''
Permite ao usuário selecionar uma sub-rede
de uma determinada localidade.

Retorna o nome da sub-rede selecionada.
'''
def select_subnet(planning, location):

    subnets = list(planning[location].keys())

    while True:

        try:

            print('\nSelect a subnet:\n')

            for i, subnet in enumerate(subnets):

                print(f'{i + 1} - {subnet}')

            option = int(input('\nOption: '))

            if 1<= option <= len(subnets):

                return subnets[option - 1]

            print('\nInvalid option. Try again.')

        except:

            print('\nInvalid option. Try again.')
'''
Simula a alocação de uma rede IPv6 utilizando
o algoritmo Leftmost Allocation.
'''
def simulate_leftmost(planning):

    location = select_location(planning)

    subnet = select_subnet(planning, location)

    allocated_network = leftmost_allocation(planning[location][subnet]['clients_networks'])

    print(f'\nLocation: {location}')

    print(f'Subnet: {subnet}')

    if allocated_network is None:

        print('\nNo client networks available.')

        return

    print(f'\nAllocated Network: {allocated_network}')

'''
Simula a alocação de uma rede IPv6 utilizando
o algoritmo Rightmost Allocation.
'''
def simulate_rightmost(planning):

    location = select_location(planning)

    subnet = select_subnet(planning,location)

    allocated_network = rightmost_allocation(planning[location][subnet]['clients_networks'])

    print(f'\nLocation: {location}')

    print(f'Subnet: {subnet}')

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

            planning, ipv6_block, locations_ipv6 = generate_ipv6_planning()

            show_planning(planning, ipv6_block, locations_ipv6)

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