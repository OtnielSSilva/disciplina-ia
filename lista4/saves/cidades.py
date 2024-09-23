edges = [
    ('Arad', 'Sibiu', 140), ('Arad', 'Timisoara', 118), ('Arad', 'Zerind', 75),
    ('Bucareste', 'Fagaras', 211), ('Bucareste', 'Giurgiu', 90),
    ('Bucareste', 'Pitesti', 101), ('Bucareste', 'Urziceni', 85),
    ('Craiova', 'Drobeta', 120), ('Craiova', 'Pitesti',
                                  138), ('Craiova', 'Rimnicu Vilcea', 146),
    ('Drobeta', 'Craiova', 120), ('Drobeta', 'Mehadia', 75),
    ('Eforie', 'Hirsova', 86), ('Fagaras',
                                'Bucareste', 211), ('Fagaras', 'Sibiu', 99),
    ('Giurgiu', 'Bucareste', 90), ('Hirsova',
                                   'Eforie', 86), ('Hirsova', 'Urziceni', 98),
    ('Iasi', 'Neamt', 87), ('Iasi', 'Vaslui', 92),
    ('Lugoj', 'Mehadia', 70), ('Lugoj', 'Timisoara', 111),
    ('Mehadia', 'Drobeta', 75), ('Mehadia', 'Lugoj', 70),
    ('Neamt', 'Iasi', 87), ('Oradea', 'Sibiu', 151), ('Oradea', 'Zerind', 71),
    ('Pitesti', 'Bucareste', 101), ('Pitesti',
                                    'Craiova', 138), ('Pitesti', 'Rimnicu Vilcea', 97),
    ('Rimnicu Vilcea', 'Craiova', 146), ('Rimnicu Vilcea',
                                         'Pitesti', 97), ('Rimnicu Vilcea', 'Sibiu', 80),
    ('Sibiu', 'Arad', 140), ('Sibiu', 'Fagaras', 99), ('Sibiu',
                                                       'Oradea', 151), ('Sibiu', 'Rimnicu Vilcea', 80),
    ('Timisoara', 'Arad', 118), ('Timisoara', 'Lugoj', 111),
    ('Urziceni', 'Bucareste', 85), ('Urziceni',
                                    'Hirsova', 98), ('Urziceni', 'Vaslui', 142),
    ('Vaslui', 'Iasi', 92), ('Vaslui', 'Urziceni', 142),
    ('Zerind', 'Arad', 75), ('Zerind', 'Oradea', 71)
]

actions = {
    'Arad': ['Sibiu', 'Timisoara', 'Zerind'],
    'Bucareste': ['Fagaras', 'Giurgiu', 'Pitesti', 'Urziceni'],
    'Craiova': ['Drobeta', 'Pitesti', 'Rimnicu Vilcea'],
    'Drobeta': ['Craiova', 'Mehadia'],
    'Eforie': ['Hirsova'],
    'Fagaras': ['Bucareste', 'Sibiu'],
    'Giurgiu': ['Bucareste'],
    'Hirsova': ['Eforie', 'Urziceni'],
    'Iasi': ['Neamt', 'Vaslui'],
    'Lugoj': ['Mehadia', 'Timisoara'],
    'Mehadia': ['Drobeta', 'Lugoj'],
    'Neamt': ['Iasi'],
    'Oradea': ['Sibiu', 'Zerind'],
    'Pitesti': ['Bucareste', 'Craiova', 'Rimnicu Vilcea'],
    'Rimnicu Vilcea': ['Craiova', 'Pitesti', 'Sibiu'],
    'Sibiu': ['Arad', 'Fagaras', 'Oradea', 'Rimnicu Vilcea'],
    'Timisoara': ['Arad', 'Lugoj'],
    'Urziceni': ['Bucareste', 'Hirsova', 'Vaslui'],
    'Vaslui': ['Iasi', 'Urziceni'],
    'Zerind': ['Arad', 'Oradea']
}