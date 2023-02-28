def cria_gerador(b, s):
    '''
    cria_gerador: int x int -> gerador
    Recebe um inteiro b correspondente ao numero de bits do gerador e um inteiro positivo s correspondente à seed ou 
    estado inicial, e devolve o gerador correspondente. O construtor verifica a validade dos seus argumentos, gerando 
    um ValueError com a mensagem 'cria_gerador: argumentos invalidos' caso os seus argumentos nao sejam validos.
    '''
    if not isinstance(b, int) or not isinstance(s, int) or \
            s <= 0 or b != 32 and b != 64 or \
            (b == 32 and s > 2 ** 32) or (b == 64 and s > 2 ** 64):
        raise ValueError('cria_gerador: argumentos invalidos')
    return [b, s]


def cria_copia_gerador(g):
    '''
    cria_copia_gerador: gerador -> gerador
    Recebe um gerador e devolve uma cópia nova do gerador.
    '''
    return g.copy()


# ---------------------------------------------------- Seletores -----------------------------------------------------#


def obtem_estado(g):
    '''
    obtem_estado: gerador -> int
    Devolve o estado atual do gerador g sem o alterar.
    '''
    return g[1]


# -------------------------------------------------- Modificadores ---------------------------------------------------#


def define_estado(g, s):
    '''
    define_estado: gerador x int -> int
    Define o novo valor do estado do gerador g como sendo s, e devolve s.
    '''
    g[1] = s
    return s


def atualiza_estado(g):
    '''
    atualiza_estado: gerador -> int
    Atualiza o estado do gerador g de acordo com o algoritmo xorshift de geracao de numeros 
    pseudoaleatorios, e devolve-o.
    '''
    b, s = g[0], g[1]

    if b == 32:
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= (s >> 17) & 0xFFFFFFFF
        s ^= (s << 5) & 0xFFFFFFFF
        g[1] = s
        return s

    elif b == 64:
        s ^= (s << 13) & 0xFFFFFFFFFFFFFFFF
        s ^= (s >> 7) & 0xFFFFFFFFFFFFFFFF
        s ^= (s << 17) & 0xFFFFFFFFFFFFFFFF
        g[1] = s
        return s


# -------------------------------------------------- Reconhecedor ----------------------------------------------------#


def eh_gerador(arg):
    '''
    eh_gerador : universal -> booleano
    Devolve True caso o seu argumento seja um TAD gerador e False caso contrario.
    '''
    return isinstance(arg, list) and len(arg) == 2 and \
           isinstance(arg[0], int) and isinstance(arg[1], int) and arg[1] > 0 and \
           ((arg[0] == 32 and arg[1] < 2 ** 32) or (arg[0] == 64 and arg[1] < 2 ** 64))


# ------------------------------------------------------ Teste -------------------------------------------------------#


def geradores_iguais(g1, g2):
    '''
    geradores_iguais: gerador x gerador -> booleano
    Devolve True apenas se g1 e g2 sao geradores e sao iguais.
    '''
    return eh_gerador(g1) and eh_gerador(g2) and \
           g1[0] == g2[0] and g1[1] == g2[1]


# -------------------------------------------------- Transformador ---------------------------------------------------#


def gerador_para_str(g):
    '''
    gerador_para_str: gerador -> str
    Devolve a cadeia de carateres que representa o seu argumento.
    '''
    return 'xorshift' + str(g[0]) + '(s=' + str(g[1]) + ')'


# ---------------------------------------------- Funções de alto nível -----------------------------------------------#


def gera_numero_aleatorio(g, n):
    '''
    gera_numero_aleatorio: gerador x int -> int
    Atualiza o estado do gerador g e devolve um numero aleatorio no intervalo [1, n] obtido a partir do novo estado s 
    de g como 1 + mod(s, n).
    '''
    return (atualiza_estado(g) % n) + 1


def gera_carater_aleatorio(g, c):
    '''
    gera_carater_aleatorio: gerador x str -> str
    Atualiza o estado do gerador g e devolve um carater aleatorio no intervalo entre 'A' e o carater maiusculo c. 
    Este e obtido a partir do novo estado s de g como o carater na posicao mod(s, l) da cadeia de carateres
    de tamanho l formada por todos os carateres entre 'A' e c. 
    '''
    s = atualiza_estado(g)
    # Número de elementos da lista que começa em "A" e acaba em c
    l = ord(c) - ord("A") + 1
    return chr(s % l + ord("A"))


# -##################################################################################################################-#
#                                                    TAD COORDENADA                                                   #
# -##################################################################################################################-#

# --------------------------------------------------- Construtor -----------------------------------------------------#


def cria_coordenada(col, lin):
    '''
    cria_coordenada: str x int -> coordenada
    Recebe os valores correspondentes à coluna e linha e devolve a coordenada correspondente. 
    O construtor verifica a validade dos seus argumentos, gerando um ValueError com a mensagem
    'cria_coordenada: argumentos invalidos' caso os seus argumentos nao sejam validos.
    '''
    if not isinstance(col, str) or not isinstance(lin, int) or \
            not 'A' <= col <= 'Z' or not 1 <= lin <= 99 or len(col) != 1:
        raise ValueError('cria_coordenada: argumentos invalidos')

    return (col, lin)


# ---------------------------------------------------- Seletores -----------------------------------------------------#


def obtem_coluna(c):
    '''
    obtem_coluna: coordenada -> st
    Devolve a coluna da coordenada c.
    '''
    return c[0]


def obtem_linha(c):
    '''
    obtem_linha: coordenada -> int
    Devolve a linha da coordenada c.
    '''
    return c[1]


# -------------------------------------------------- Reconhecedor ----------------------------------------------------#


def eh_coordenada(arg):
    '''
    eh_coordenada: universal -> booleano
    Devolve True caso o seu argumento seja um TAD coordenada e False caso contrario.
    '''
    return isinstance(arg, tuple) and len(arg) == 2 and \
           isinstance(arg[0], str) and isinstance(arg[1], int) and \
           'A' <= arg[0] <= 'Z' and 1 <= arg[1] <= 99 and len(arg[0]) == 1


# ------------------------------------------------------ Teste -------------------------------------------------------#


def coordenadas_iguais(c1, c2):
    '''
    coordenadas_iguais: coordenada x coordenada -> booleano
    Devolve True apenas se c1 e c2 sao coordenadas e sao iguais.
    '''
    if not eh_coordenada(c1) or not eh_coordenada(c2):
        return False
    return obtem_linha(c1) == obtem_linha(c2) and obtem_coluna(c1) == obtem_coluna(c2)


# -------------------------------------------------- Transformador ---------------------------------------------------#


def coordenada_para_str(c):
    '''
    coordenada_para_str: coordenada -> str
    Devolve a cadeia de carateres que representa o seu argumento, como mostrado nos exemplos.
    '''
    col = obtem_coluna(c)
    lin = obtem_linha(c)
    s = col
    if lin < 10:
        s += '0'
    s += str(lin)
    return s


def str_para_coordenada(s):
    '''
    str_para_coordenada: str -> coordenada
    Devolve a coordenada reapresentada pelo seu argumento.
    '''
    col = s[0]
    lin = int(s[1:])
    return (col, lin)


# ---------------------------------------------- Funções de alto nível -----------------------------------------------#


def obtem_coordenadas_vizinhas(c):
    '''
    obtem_coordenadas_vizinhas: coordenada -> tuplo
    Devolve um tuplo com as coordenadas vizinhas à coordenada c, comecando pela coordenada na diagonal 
    acima-esquerda de c e seguindo no sentido horario.
    '''
    col = obtem_coluna(c)
    lin = obtem_linha(c)
    add = [(-1, -1), (0, -1), (1, -1), (1, 0),
           (1, 1), (0, 1), (-1, 1), (-1, 0)]
    res = []
    for x, y in add:
        if col == 'A' and x == -1:
            continue
        if col == 'Z' and x == 1:
            continue
        if lin == 1 and y == -1:
            continue
        if lin == 99 and y == 1:
            continue
        new_col = chr(ord(col) + x)
        new_lin = lin + y
        res.append(cria_coordenada(new_col, new_lin))
    return tuple(res)


def obtem_coordenada_aleatoria(c, g):
    '''
    obtem_coordenada_aleatoria: coordenada x gerador -> coordenada
    Recebe uma coordenada c e um TAD gerador g, e devolve uma coordenada gerada aleatoriamente como descrito 
    anteriormente em que c define a maior coluna e maior linha possíveis. 
    Deve ser gerada, em sequencia, primeiro a coluna e depois a linha da coordenada resultado.
    '''
    max_col = obtem_coluna(c)
    max_lin = obtem_linha(c)
    col = gera_carater_aleatorio(g, max_col)
    lin = gera_numero_aleatorio(g, max_lin)
    return (col, lin)


# -##################################################################################################################-#
#                                                    TAD PARCELA                                                      #
# -##################################################################################################################-#

# -------------------------------------------------- Construtores ----------------------------------------------------#


def cria_parcela():
    '''
    cria_parcela: {} -> parcela
    Devolve uma parcela tapada sem mina escondida
    '''
    return ["#", False]


def cria_copia_parcela(p):
    '''
    cria_copia_parcela: parcela -> parcela
    Recebe uma parcela p e devolve uma nova copia da parcela.

    '''
    return p.copy()


# -------------------------------------------------- Modificadores ---------------------------------------------------#


def limpa_parcela(p):
    '''
    limpa_parcela: parcela -> parcela
    Modifica destrutivamente a parcela p modificando o seu estado para limpa, e devolve a propria parcela.
    '''
    p.pop(0)
    p.insert(0, '?')
    return p


def marca_parcela(p):
    '''
    marca_parcela: parcela -> parcela
    Modifica destrutivamente a parcela p modificando o seu estado para marcada com uma bandeira, 
    e devolve a propria parcela.
    '''
    p.pop(0)
    p.insert(0, '@')
    return p


def desmarca_parcela(p):
    '''
    desmarca_parcela: parcela -> parcela
    Modifica destrutivamente a parcela p modificando o seu estado para tapada, e devolve a propria parcela.
    '''
    p.pop(0)
    p.insert(0, '#')
    return p


def esconde_mina(p):
    '''
    esconde_mina: parcela -> parcela
    Modifica destrutivamente a parcela p escondendo uma mina na parcela, e devolve a propria parcela.
    '''
    p.pop(1)
    p.insert(1, True)
    return p


# -------------------------------------------------- Reconhecedor ----------------------------------------------------#


def eh_parcela(arg):
    '''
    eh_parcela: universal -> booleano
    Devolve True caso o seu argumento seja um TAD parcela e False caso contrario.
    '''
    return isinstance(arg, list) and len(arg) == 2 and \
           isinstance(arg[0], str) and isinstance(arg[1], bool) and \
           len(arg[0]) == 1 and arg[0] in '#?@'


def eh_parcela_tapada(p):
    '''
    eh_parcela_tapada: parcela -> booleano
    Devolve True caso a parcela p se encontre tapada e False caso contrario.
    '''
    return p[0] == '#'


def eh_parcela_marcada(p):
    '''
    eh_parcela_marcada: parcela -> booleano
    Devolve True caso a parcela p se encontre marcada com uma bandeira e False caso contrario.
    '''
    return p[0] == '@'


def eh_parcela_limpa(p):
    '''
    eh_parcela_limpa: parcela -> booleano
    Devolve True caso a parcela p se encontre limpa e False caso contrario.
    '''
    return p[0] == '?'


def eh_parcela_minada(p):
    '''
    eh_parcela_minada: parcela -> booleano
    Devolve True caso a parcela p esconda uma mina e False caso contrario.
    '''
    return p[1] == True


# ------------------------------------------------------ Teste -------------------------------------------------------#


def parcelas_iguais(p1, p2):
    '''
    parcelas_iguais: parcela x parcela -> booleano
    Devolve True apenas se p1 e p2 sao parcelas e sao iguais.
    '''
    return eh_parcela(p1) and eh_parcela(p2) and \
           p1[0] == p2[0] and p1[1] == p2[1]


# -------------------------------------------------- Transformador ---------------------------------------------------#


def parcela_para_str(p):
    '''
    parcela_para_str : parcela -> str
    Devolve a cadeia de caracteres que representa a parcela em funcao do seu estado.
    '''
    if p[0] == '?' and p[1] == False:
        return '?'
    if p[0] == '?' and p[1] == True:
        return 'X'
    return p[0]


# ---------------------------------------------- Funções de alto nível -----------------------------------------------#


def alterna_bandeira(p):
    '''
    alterna_bandeira: parcela -> booleano
    Recebe uma parcela p e modifica-a destrutivamente da seguinte forma: desmarca se estiver marcada e marca se 
    estiver tapada, devolvendo True. Em qualquer outro caso, nao modifica a parcela e devolve False.
    '''
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    else:
        return False


# -##################################################################################################################-#
#                                                     TAD CAMPO                                                       #
# -##################################################################################################################-#

# -------------------------------------------------- Construtores ----------------------------------------------------#


def cria_campo(c, l):
    '''
    cria_campo: str x int -> campo
    Recebe uma cadeia de carateres e um inteiro correspondentes à ultima coluna e à ultima linha de um campo de minas, 
    e devolve o campo do tamanho pretendido formado por parcelas tapadas sem minas. 
    O construtor verifica a validade dos seus argumentos, gerando um ValueError com a mensagem 
    'cria_campo: argumentos invalidos' caso os seus argumentos nao sejam validos.
    '''
    if not isinstance(c, str) or not isinstance(l, int) or \
            not 'A' <= c <= 'Z' or not 1 <= l <= 99 or len(c) != 1:
        raise ValueError('cria_campo: argumentos invalidos')

    campo = {}
    cols = []
    lines = []
    current_col = 'A'
    current_lin = 1
    while current_col <= c:
        cols.append(current_col)
        current_col = chr(ord(current_col) + 1)
    while current_lin <= l:
        lines.append(current_lin)
        current_lin += 1
    for lin in lines:
        for col in cols:
            campo[(col, lin)] = cria_parcela()
    return campo


def cria_copia_campo(m):
    '''
    cria_copia_campo: campo -> campo
    Recebe um campo e devolve uma nova copia do campo.
    '''
    copia_campo = {}
    for coordenada in m:
        copia_campo[coordenada] = cria_copia_parcela(m[coordenada])
    return copia_campo


# ---------------------------------------------------- Seletores -----------------------------------------------------#


def obtem_ultima_coluna(m):
    '''
    obtem_ultima_coluna: campo -> str
    Devolve a cadeia de caracteres que corresponde à ultima coluna do campo de minas.
    '''
    return list(m.keys())[-1][0]


def obtem_ultima_linha(m):
    '''
    obtem_ultima_linha: campo -> int
    Devolve o valor inteiro que corresponde à ultima linha do campo de minas.
    '''
    return list(m.keys())[-1][1]


def obtem_parcela(m, c):
    '''
    obtem_parcela: campo x coordenada -> parcela
    Devolve a parcela do campo m que se encontra na coordenada c.
    '''
    return m[c]


def obtem_coordenadas(m, s):
    '''
    obtem_coordenadas: campo x str -> tuplo
    Devolve o tuplo formado pelas coordenadas ordenadas em ordem ascendente de esquerda à direita 
    e de cima a baixo das parcelas dependendo do valor de s.
    '''
    lst = []
    if s == 'limpas':
        for coordenada in m:
            if eh_parcela_limpa(obtem_parcela(m, coordenada)):
                lst.append(coordenada)
        return tuple(lst)

    if s == 'tapadas':
        for coordenada in m:
            if eh_parcela_tapada(obtem_parcela(m, coordenada)):
                lst.append(coordenada)
        return tuple(lst)

    if s == 'marcadas':
        for coordenada in m:
            if eh_parcela_marcada(obtem_parcela(m, coordenada)):
                lst.append(coordenada)
        return tuple(lst)

    if s == 'minadas':
        for coordenada in m:
            if eh_parcela_minada(obtem_parcela(m, coordenada)):
                lst.append(coordenada)
        return tuple(lst)

    else:
        for coordenada in m:
            lst.append(coordenada)
        return tuple(lst)


def obtem_numero_minas_vizinhas(m, c):
    '''
    obtem_numero_minas_vizinhas: campo x coordenada -> int
    Devolve o numero de parcelas vizinhas da parcela na coordenada c que escondem uma mina.
    '''
    i = 0
    for coordenada in obtem_coordenadas_vizinhas(c):
        if eh_coordenada_do_campo(m, coordenada):
            if eh_parcela_minada(obtem_parcela(m, coordenada)):
                i += 1
    return i


# ------------------------------------------------- Reconhecedores ---------------------------------------------------#


def eh_campo(arg):
    '''
    eh_campo: universal -> booleano
    Devolve True caso o seu argumento seja um TAD campo e False caso contrario.
    '''
    if not isinstance(arg, dict) or len(arg) == 0:
        return False
    for coordenada, parcela in arg.items():
        if not eh_coordenada(coordenada) or not eh_parcela(parcela):
            return False
    return True


def eh_coordenada_do_campo(m, c):
    '''
    eh_coordenada_do_campo: campo x coordenada -> booleano
    Devolve True se c e uma coordenada valida
    dentro do campo m.
    '''
    return eh_coordenada(c) and c in m


# ------------------------------------------------------ Teste -------------------------------------------------------#


def campos_iguais(m1, m2):
    '''
    campos_iguais: campo x campo -> booleano
    Devolve True apenas se m1 e m2 forem campos e forem iguais.
    '''
    return eh_campo(m1) and eh_campo(m2) and m1 == m2




# -------------------------------------------------- Transformador ---------------------------------------------------#


def campo_para_str(m):
    '''
    campo_para_str : campo -> str
    Devolve uma cadeia de caracteres que representa o campo
    de minas como mostrado nos exemplos.
    '''
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    grelha = '+---------------------------'
    n_colunas = ord(obtem_ultima_coluna(m)) - ord("A") + 1
    s = '   ' + alfabeto[:n_colunas] + '\n  '
    limite = grelha[:n_colunas + 1] + '+'
    meio_campo = ''
    todas_parcelas = ''

    for coordenada in m:
        parcela = obtem_parcela(m, coordenada)
        if eh_parcela_limpa(parcela) and not eh_parcela_minada(parcela):
            if obtem_numero_minas_vizinhas(m, coordenada) == 0:
                todas_parcelas += ' '
            else:
                todas_parcelas += str(obtem_numero_minas_vizinhas(m, coordenada))
        elif eh_parcela_limpa(parcela) and eh_parcela_minada(parcela):
            todas_parcelas += 'X'
        else:
            todas_parcelas += parcela_para_str(obtem_parcela(m, coordenada))
    for i in range(obtem_ultima_linha(m)):
        if i < 9:
            meio_campo += '0' + str(i + 1) + '|' + todas_parcelas[:n_colunas] + '|\n'
            todas_parcelas = todas_parcelas[n_colunas:]
        else:
            meio_campo += str(i + 1) + '|' + todas_parcelas[:n_colunas] + '|\n'
            todas_parcelas = todas_parcelas[n_colunas:]

    res = s + limite + '\n' + meio_campo + '  ' + limite

    return res


# ---------------------------------------------- Funções de alto nível -----------------------------------------------#


def coloca_minas(m, c, g, n):
    '''
    coloca_minas: campo x coordenada x gerador x int -> campo
    Modifica destrutivamente o campo m escondendo n minas em parcelas dentro do campo. 
    As n coordenadas sao geradas em sequencia utilizando o gerador g, de modo a que nao coincidam com a coordenada c 
    nem com nenhuma parcela vizinha desta, nem se sobreponham com minas colocadas anteriormente.
    '''
    coordenadas_minas = [c]
    while len(coordenadas_minas) < n + 1:
        nova_c = obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
        parcela = obtem_parcela(m, nova_c)
        if nova_c not in coordenadas_minas and not eh_parcela_minada(parcela) and \
                nova_c not in obtem_coordenadas_vizinhas(c):  # VER IDENTACAO DISSO
            esconde_mina(parcela)
            coordenadas_minas.append(nova_c)
    return m


# n = {('A', 1): ['?', True], ('B', 1): ['@', True], ('C', 1): ['#', True], ('A', 2): ['?', False], ('B', 2): ['#', False], ('C', 2): ['#', False], ('A', 3): ['#', False], ('B', 3): ['#', False], ('C', 3): ['#', True]}
# print(n)
# print(campo_para_str(n))

# MUITO IMPORTANTE, CRIA CAMPO FAZER PARA FICAR A1 B1 C1, A2, B2, C2
# VER SE É BENEFICO ISSO
# SE SIM, FAZER sorted(m.items(), key=lambda x:x[0][1]

def limpa_campo(m, c):
    '''
    limpa_campo: campo x coordenada -> campo
    Modifica destrutivamente o campo limpando a parcela na coordenada c, devolvendo-o. 
    Se nao houver nenhuma mina vizinha escondida, limpa iterativamente todas as parcelas vizinhas tapadas.
    Caso a parcela se encontre ja limpa, a operacao nao tem efeito.
    '''
    parcela = obtem_parcela(m, c)
    if obtem_numero_minas_vizinhas(m, c) != 0:
        if eh_parcela_tapada(parcela) or eh_parcela_marcada(parcela):
            limpa_parcela(parcela)
    if obtem_numero_minas_vizinhas(m, c) == 0:
        limpa_parcela(parcela)
        if not eh_parcela_minada(parcela):
            for coordenada in obtem_coordenadas_vizinhas(c):
                if eh_coordenada_do_campo(m, coordenada) and eh_parcela_tapada(obtem_parcela(m, coordenada)):
                    limpa_campo(m, coordenada)
    return m




# -##################################################################################################################-#
#                                                  FUNCOES ADICIONAIS                                                 #
# -##################################################################################################################-#

# --------------------------------------------------- Jogo_ganho -----------------------------------------------------#


def jogo_ganho(m):

    for coordenada in obtem_coordenadas(m, ''):
        parcela = obtem_parcela(m, coordenada)
        if not eh_parcela_minada(parcela) and not eh_parcela_limpa(parcela):
            return False
    return True




# -------------------------------------------------- Turno_jogador ---------------------------------------------------#



# 2.2.2
# Função Auxiliar
def valida_coordenada(arg):
    '''
    valida_coordenada: string → booleano
    A função devolve True caso a string corresponder a uma
    coordenada em forma de string.
    '''
    return len(arg) == 3 and isinstance(arg[0], str) and arg[1:].isnumeric()


def turno_jogador(m):
    '''
    turno jogador: campo → booleano:
    Recebe um campo de minas e oferece ao jogador a opção de escolher
    uma ação e uma coordenada.
    Devolve False caso o jogador tenha limpo uma parcela que continha
    um mina, ou True caso contrário.
    '''

    while True:
        acao = input('Escolha uma ação, [L]impar ou [M]arcar:')
        if acao == 'M':
            while True:
                coord_str = input('Escolha uma coordenada:')
                if valida_coordenada(coord_str):
                    coordenada = str_para_coordenada(coord_str)
                    if eh_coordenada_do_campo(m, coordenada) and \
                            coordenada not in obtem_coordenadas(m, 'limpas'):
                        alterna_bandeira(obtem_parcela(m, coordenada))
                        break
            break
        if acao == 'L':
            while True:
                coord_str = input('Escolha uma coordenada:')
                if valida_coordenada(coord_str):
                    coordenada = str_para_coordenada(coord_str)
                    if eh_coordenada_do_campo(m, coordenada) and \
                            not coordenada in obtem_coordenadas(m, 'limpas'):
                        if eh_parcela_minada(obtem_parcela(m, coordenada)):
                            limpa_campo(m, coordenada)
                            return False
                        else:
                            limpa_campo(m, coordenada)
                            return True





# ------------------------------------------------------ Minas -------------------------------------------------------#


def minas(c, l, n, d, s):
    '''
    minas: str × int × int × int × int → booleano
    Recebe a última coluna c, última linha l, dimensão do gerador
    de números d, e o estado inicial ou seed s.
    A função

    '''
    if not isinstance(c, str) or not isinstance(l, int) or \
            not 'A' <= c <= 'Z' or not 1 <= l <= 99 or len(c) != 1:
        raise ValueError('minas: argumentos invalidos')
    if not isinstance(d, int) or not isinstance(s, int) or \
            s <= 0 or (d != 32 and d != 64) or \
            (d == 32 and s > 2 ** 32) or (d == 64 and s > 2 ** 64):
        raise ValueError('minas: argumentos invalidos')
    if not isinstance(n, int) or n <= 0:
        raise ValueError('minas: argumentos invalidos')
    if not isinstance(n, int) or n <= 0:
        raise ValueError('minas: argumentos invalidos')
    max_col = (ord(c) - ord("A") + 1)
    if max(max_col, l) > 3:
        if min(max_col, l) == 1 or min(max_col, l) == 2:
            if n > l * max_col - (3 * min(max_col, l)):
                raise ValueError('minas: argumentos invalidos')
        elif n > l * max_col - 9:
            raise ValueError('minas: argumentos invalidos')
    else:
        raise ValueError('minas: argumentos invalidos')

    g = cria_gerador(d, s)
    m = cria_campo(c, l)
    n_bandeiras = len(obtem_coordenadas(m, 'marcadas'))
    bandeiras = '   [Bandeiras ' + str(n_bandeiras) + '/' + str(n) + ']'
    print(bandeiras)
    print(campo_para_str(m))
    c_inicial = str_para_coordenada(input('Escolha uma coordenada:'))
    coloca_minas(m, c_inicial, g, n)
    limpa_campo(m, c_inicial)
    while True:
        n_bandeiras = len(obtem_coordenadas(m, 'marcadas'))
        bandeiras = '   [Bandeiras ' + str(n_bandeiras) + '/' + str(n) + ']'
        print(bandeiras)
        print(campo_para_str(m))
        if turno_jogador(m) == False:
            print(bandeiras)
            print(campo_para_str(m))
            print("BOOOOOOOM!!!")
            return False
        if jogo_ganho(m):
            print(bandeiras)
            print(campo_para_str(m))
            print("VITORIA!!!")
            return True
