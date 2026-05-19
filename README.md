# Parser LL(1)

Este proyecto contiene un analizador de gramáticas que calcula los conjuntos `FIRST` y `FOLLOW`, verifica si una gramática es LL(1) y construye la tabla de análisis LL(1).

## Qué hace el código

- Lee una gramática escrita en texto con la forma `NT -> producción1 | producción2`.
- Convierte `epsilon` en la producción vacía.
- Calcula los conjuntos `FIRST` para cada no terminal.
- Calcula los conjuntos `FOLLOW` para cada no terminal.
- Verifica si la gramática cumple la condición LL(1).
- Construye e imprime la tabla de análisis LL(1) cuando la gramática es LL(1).

## Formato de la gramática

Cada regla debe escribirse en una línea con:

```text
NoTerminal -> símbolo1 símbolo2 | otraProducción | epsilon
```

Ejemplo:

```text
E  -> T Ep
Ep -> + T Ep | epsilon
T  -> F Tp
Tp -> * F Tp | epsilon
F  -> ( E ) | id
```

- `epsilon` representa la producción vacía.
- Los símbolos separados por espacios se consideran tokens individuales.

## Manual de usuario

### Ejecutar el script

1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar el archivo `Parser.py` con Python:

```powershell
python Parser.py
```

### Qué esperar

El programa imprimirá:

- Los conjuntos `FIRST` de cada no terminal.
- Los conjuntos `FOLLOW` de cada no terminal.
- Si la gramática es LL(1) o no.
- Si es LL(1), la tabla de análisis predictiva.

### Modificar la gramática

Para usar otra gramática, abre `Parser.py` y cambia la variable `gramatica_texto` al final del archivo con tu nueva definición.

### Importar como módulo

Si deseas reutilizar las funciones desde otro script, importa `main` o cualquier otra función desde `Parser.py`.

```python
from Parser import main

main(mi_gramatica)
```
