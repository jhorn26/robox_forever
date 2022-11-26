import poligon
def main():
    with open("levels.txt", "a") as f:
        item = ["robot_position", "boxes_positions", "goal_positions", "corners_positions", "walls_positions", "walk_positions"]
        line = {k:[] for k in item}
        k = 0
        print(f"Categoria {item[0]} (digite s para passar para a próxima categoria)\n") 
        while True:
            res = anexa(item, line, k)
            if res[0] == 1:
                break
            if res[0] == 2:
                k = k + 1
                print("===========================================================")
                print(f"Categoria {item[k]} (digite s para passar para a próxima categoria)\n")
            else:
                line = res[1]

        line = poligon.create_level(line)
        f.write(str(line) + "\n") 

def anexa(item, line, k):
    foobar = entrada()
    if foobar[0] == 1:
        if k == 5:
            return 1, line
        else:
            return 2, line
    else:            
        try:
            line[item[k]].append((int(foobar[0]), int(foobar[1])))
        except:
            print("ERRO: entrada inválida! Insira novamente:")
            anexa(item, line, k)
    return False, line

def entrada():
    foo = input("Primeira coordenada: ")
    if foo == "s":
        return True, True
    else:
        bar = input("Segunda coordenada: ")
    return foo, bar

main()