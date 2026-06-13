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
    ipv6_address, _ = ipv6_block.split('/')

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

'''
Recebe do usuário a quantidade de localidades e seus respectivos nomes.
Retorna uma lista contendo os nomes informados.
'''

def get_locations():

    locations = []

    while True:

        try:
        
            num_locations = int(input('\nEnter the number of locations: '))

            if num_locations > 0:

                break

            print('\nThe number of locations must be greater than zero.')

        except:

            print('\nInvalid number. Try again.')

    for i in range(num_locations):

        location = input(f'\nEnter the name of location {i + 1}: ')

        locations.append(location)
    
    return locations 

'''
Gera um prefixo IPv6 /48 para cada localidade informada pelo usuário.
Retorna um dicionário contendo o nome da localidade e seu
respectivo prefixo IPv6.
'''

def generate_locations(ipv6_block):
    
    ipv6_blocks = expand_ipv6(ipv6_block)

    locations = get_locations()

    # Dicionário que armazenará cada localidade e seu respectivo ipv6. 
    locations_ipv6 = {}

    # Para cada uma das localidades 
    for i, location in enumerate(locations):

        # Copiamos o endereço base. 
        location_blocks = ipv6_blocks.copy()

        # O bloco principal do trabalho é um /32.
        # Portanto, utilizamos o terceiro bloco IPv6 para identificar
        # cada localidade, gerando prefixos /48.
        location_blocks[2] = hex(i)[2:].zfill(4)

        # Comprimindo o bloco. 
        formatted_location_blocks = format_ipv6(location_blocks)

        #Adiciona o prefixo '/48'
        location_prefix = formatted_location_blocks + '/48'

        #Guarda no dicionário. 
        locations_ipv6[location] = location_prefix
    
    return locations_ipv6

'''
Recebe do usuário a quantidade de subredes e seus respectivos nomes.
Retorna uma lista contendo os nomes informados.
'''

def get_subnets():

    subnets = []

    while True:

        try:
        
            num_subnets = int(input('\nEnter the number of subnets: '))

            if num_subnets > 0:

                break

            print('\nThe number of subnets must be greater than zero.')

        except:

            print('\nInvalid number. Try again.')

    for i in range(num_subnets):

        subnet = input(f'\nEnter the name of subnet {i + 1}: ')

        subnets.append(subnet)
    
    return subnets 

'''
Divide o prefixo IPv6 de uma localidade (/48) em sub-redes /56.
Cada sub-rede recebe um identificador único no quarto bloco do
endereço IPv6, permitindo a organização hierárquica do
endereçamento e futuras subdivisões em redes menores.
'''


def generate_subnets(location_ipv6):
    
    ipv6_blocks = expand_ipv6(location_ipv6)

    subnets = get_subnets()

    # Dicionário que armazenará cada sub-rede e seu respectivo IPv6.
    subnets_ipv6 = {}

    # Para cada uma das sub-redes. 
    for i, subnet in enumerate(subnets):

        # Copiamos o endereço base. 
        subnet_blocks = ipv6_blocks.copy()

        # Como estamos dividindo um prefixo /48 em prefixos /56,
        # utilizamos os primeiros 8 bits do quarto bloco para
        # identificar cada sub-rede.
        subnet_blocks[3] = hex(i * 256)[2:].zfill(4)

        # Comprimindo o bloco. 
        formatted_subnet_blocks = format_ipv6(subnet_blocks)

        #Adiciona o prefixo '/56'
        subnet_prefix = formatted_subnet_blocks + '/56'

        #Guarda no dicionário. 
        subnets_ipv6[subnet] = subnet_prefix
    
    return subnets_ipv6

'''
Gera redes IPv6 /64 para clientes a partir de uma sub-rede /56.

Essa função é utilizada para simular a distribuição de redes
IPv6 para clientes e servir de base para os algoritmos de
alocação Leftmost e Rightmost.

Retorna uma lista contendo os prefixos IPv6 gerados.
'''

def generate_clients_allocation(subnet_ipv6):

    ipv6_blocks = expand_ipv6(subnet_ipv6)

    # Lista que armazenará os prefixos IPv6 gerados para os clientes.
    clients_networks = []

    while True:

        try:

            num_clients = int(input('\nEnter the number of clients: '))

            if num_clients > 0:

                break

            else:

                print('\nThe number of clients must be greater than zero.')

        except:

            print('\nInvalid number. Try again.')

    # Para cada uma das sub-redes. 
    for i in range(num_clients):

        # Copiamos o endereço base. 
        client_blocks = ipv6_blocks.copy()

        # Em uma divisão /56 -> /64 utilizamos os
        # últimos 8 bits do quarto bloco.
        client_blocks[3] = hex(i)[2:].zfill(4)

        # Comprimindo o bloco. 
        formatted_client_blocks = format_ipv6(client_blocks)

        # Adiciona o prefixo '/64'.
        client_prefix = formatted_client_blocks + '/64'

        clients_networks.append(client_prefix)
        
    
    return clients_networks


def leftmost_allocation():
    pass

def rightmost_allocation():
    pass

def reserve_anycast():
    pass



if __name__ == "__main__":
    menu()