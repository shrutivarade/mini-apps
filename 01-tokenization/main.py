import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I love to play football/soccer! ❤️ ⚽️"
tokens = enc.encode(text)

print("Tokens:", tokens)

tokens = [13225, 11, 357, 3047, 316, 2107, 13332, 5031, 432, 3308, 0, 122205, 181418, 121, 15148]
decoded = enc.decode(tokens)

print("Decoded Text:", decoded)