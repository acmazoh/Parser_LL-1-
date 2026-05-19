def parsear_gramatica(texto):
    gramatica = {}
    no_terminales = set()
    terminales = set()
    for linea in texto.strip().split('\n'):
        linea = linea.strip()
        if not linea:
            continue
        izquierda, derecha = linea.split('->')
        nt = izquierda.strip()
        no_terminales.add(nt)
        alternativas = derecha.split('|')
        producciones = []
        for alt in alternativas:
            simbolos = alt.strip().split()
            if simbolos == ['epsilon']:
                producciones.append([])
            else:
                producciones.append(simbolos)
        gramatica[nt] = producciones
    for nt, prods in gramatica.items():
        for prod in prods:
            for s in prod:
                if s not in no_terminales:
                    terminales.add(s)

    return gramatica, no_terminales, terminales
def calcular_first(gramatica, no_terminales):
    first = {nt: set() for nt in no_terminales}
    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                if prod == []:
                    if 'ε' not in first[nt]:
                        first[nt].add('ε')
                        cambio = True
                else:
                    for simbolo in prod:
                        if simbolo not in no_terminales:
                            if simbolo not in first[nt]:
                                first[nt].add(simbolo)
                                cambio = True
                            break  
                        else:
                            nuevos = first[simbolo] - {'ε'}
                            if not nuevos.issubset(first[nt]):
                                first[nt] |= nuevos
                                cambio = True
                            if 'ε' not in first[simbolo]:
                                break  
                    else:
                        if 'ε' not in first[nt]:
                            first[nt].add('ε')
                            cambio = True

    return first
def first_forma(alpha, first, no_terminales):
    resultado = set()
    for simbolo in alpha:
        if simbolo not in no_terminales:
            resultado.add(simbolo)
            return resultado          
        resultado |= first[simbolo] - {'ε'}
        if 'ε' not in first[simbolo]:
            return resultado         
    resultado.add('ε')           
    return resultado

def calcular_follow(gramatica, no_terminales, first, simbolo_inicial):
    follow = {nt: set() for nt in no_terminales}
    follow[simbolo_inicial].add('$')   
    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                for i, simbolo in enumerate(prod):
                    if simbolo not in no_terminales:
                        continue  
                    beta = prod[i+1:]
                    fb = first_forma(beta, first, no_terminales)
                    nuevos = fb - {'ε'}
                    if not nuevos.issubset(follow[simbolo]):
                        follow[simbolo] |= nuevos
                        cambio = True
                    if 'ε' in fb:
                        if not follow[nt].issubset(follow[simbolo]):
                            follow[simbolo] |= follow[nt]
                            cambio = True

    return follow
def verificar_ll1(gramatica, no_terminales, first, follow):
    es_ll1 = True
    conflictos = []
    for nt, producciones in gramatica.items():
        n = len(producciones)
        for i in range(n):
            for j in range(i+1, n):
                alpha = producciones[i]
                beta  = producciones[j]
                fa = first_forma(alpha, first, no_terminales)
                fb = first_forma(beta,  first, no_terminales)
                interseccion = fa & fb - {'ε'}
                if interseccion:
                    es_ll1 = False
                    conflictos.append(
                        f"[{nt}] FIRST({alpha}) ∩ FIRST({beta}) = {interseccion}"
                    )

                if 'ε' in fa:
                    conf = (fb - {'ε'}) & follow[nt]
                    if conf:
                        es_ll1 = False
                        conflictos.append(
                            f"[{nt}] ε∈FIRST({alpha}), "
                            f"pero FIRST({beta})∩FOLLOW({nt}) = {conf}"
                        )
                if 'ε' in fb:
                    conf = (fa - {'ε'}) & follow[nt]
                    if conf:
                        es_ll1 = False
                        conflictos.append(
                            f"[{nt}] ε∈FIRST({beta}), "
                            f"pero FIRST({alpha})∩FOLLOW({nt}) = {conf}"
                        )

    return es_ll1, conflictos

def construir_tabla(gramatica, no_terminales, terminales, first, follow):
    tabla = {nt: {} for nt in no_terminales}
    conflictos_tabla = []
    for nt, producciones in gramatica.items():
        for prod in producciones:
            fa = first_forma(prod, first, no_terminales)
            for terminal in fa - {'ε'}:
                if terminal in tabla[nt]:
                    conflictos_tabla.append(
                        f"Conflicto en M[{nt},{terminal}]"
                    )
                tabla[nt][terminal] = prod
            if 'ε' in fa:
                for terminal in follow[nt]:
                    if terminal in tabla[nt]:
                        conflictos_tabla.append(
                            f"Conflicto en M[{nt},{terminal}]"
                        )
                    tabla[nt][terminal] = []   # producción epsilon

    return tabla, conflictos_tabla

def main(texto_gramatica):
    gramatica, no_terminales, terminales = parsear_gramatica(texto_gramatica)
    simbolo_inicial = list(gramatica.keys())[0]  # primer NT = inicio
    first  = calcular_first(gramatica, no_terminales)
    follow = calcular_follow(gramatica, no_terminales, first, simbolo_inicial)
    print("=== FIRST ===")
    for nt in gramatica:
        print(f"  FIRST({nt}) = {first[nt]}")
    print("\n=== FOLLOW ===")
    for nt in gramatica:
        print(f"  FOLLOW({nt}) = {follow[nt]}")
    es_ll1, conflictos = verificar_ll1(gramatica, no_terminales, first, follow)
    print("\n=== Verificación LL(1) ===")
    if es_ll1:
        print(" La gramática ES LL(1)")
    else:
        print(" La gramática NO es LL(1). Conflictos encontrados:")
        for c in conflictos:
            print(f"    → {c}")
        return  
    tabla, _ = construir_tabla(
        gramatica, no_terminales, terminales | {'$'}, first, follow
    )
    print("\n=== Tabla de análisis LL(1) ===")
    todos_terminales = sorted(terminales | {'$'})
    encabezado = f"{'NT':<8}" + "".join(f"{t:<16}" for t in todos_terminales)
    print(encabezado)
    print("-" * len(encabezado))
    for nt in gramatica:
        fila = f"{nt:<8}"
        for t in todos_terminales:
            if t in tabla[nt]:
                prod = tabla[nt][t]
                celda = f"{nt} → {' '.join(prod) if prod else 'ε'}"
            else:
                celda = ""
            fila += f"{celda:<16}"
        print(fila)

gramatica_texto = """
E  -> T Ep
Ep -> + T Ep | epsilon
T  -> F Tp
Tp -> * F Tp | epsilon
F  -> ( E ) | id
"""
main(gramatica_texto)