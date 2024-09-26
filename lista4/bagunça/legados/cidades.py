def cidades_romenia():
    return {
        'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
        'Zerind': {'Arad': 75, 'Oradea': 71},
        'Oradea': {'Zerind': 71, 'Sibiu': 151},
        'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
        'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
        'Rimnicu Vilcea': {'Sibiu': 80, 'Pitesti': 97, 'Craiova': 146},
        'Pitesti': {'Rimnicu Vilcea': 97, 'Bucharest': 101},
        'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
        'Drobeta': {'Mehadia': 75, 'Craiova': 120},
        'Mehadia': {'Drobeta': 75, 'Lugoj': 70},
        'Lugoj': {'Mehadia': 70, 'Timisoara': 111},
        'Timisoara': {'Arad': 118, 'Lugoj': 111},
        'Bucharest': {'Fagaras': 211, 'Pitesti': 101}
    }
