def expand_ipv6(ipv6_block):

    ipv6_address = ipv6_block.split('/')
    
    # Se "::" estiver no endereço informado, quer dizer que ele
    # está na forma abreviada e precisa ser expandido. 
    if '::' in ipv6_address:

        left_side, right_side = ipv6_address.split('::')

        left_blocks = [block for block in left_side.split(':') if block]

        right_blocks = [block for block in right_side.split(':') if block]

        # Calcula quantos blocos de zeros precisarão ser inseridos. 
        # Lembrando que o IPv6 é formado por 8 blocos. 
        zeros_blocks_qtd = 8 - (len(left_blocks) + len(right_blocks))

        # Criando esses blocos de zeros. 
        zeros_blocks = ['0000'] * zeros_blocks_qtd

        # Adicionado os blocos de zeros no endereço do IPv6.
        ipv6_address = left_blocks + zeros_blocks + right_blocks

    else:

        ipv6_address = ipv6_address.split(':')

    return ipv6_address

def compress_ipv6(ip):
    pass

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