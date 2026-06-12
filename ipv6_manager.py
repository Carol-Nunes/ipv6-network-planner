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


def validate_ipv6(ip):
    pass

def generate_locations():
    pass

def generate_subnets():
    pass

def leftmost_allocation():
    pass

def rightmost_allocation():
    pass

def reserve_anycast():
    pass

def show_concepts():
    pass

def menu():
    pass


if __name__ == "__main__":
    menu()