import re

def decode_matrix():
    with open('matrix.txt', 'r') as file:
        n, m = map(int, file.readline().split())
        matrix = [list(file.readline().strip().ljust(m, ' ')) for _ in range(n)]
    
    decoded = ''.join(''.join(chars) for chars in zip(*matrix))
    decoded_cleaned = re.sub(r'\b[^a-zA-Z0-9]+\b', ' ', decoded)
    
    print(decoded_cleaned)

decode_matrix()
