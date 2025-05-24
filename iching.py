from google import genai
from google.genai import types
import random

client = genai.Client(api_key='YOUR_API_KEY_HERE')
model = 'gemini-2.5-flash-preview-05-20' #'gemini-2.0-flash'

system_instruction = """
    You are an I Ching Grandmaster, a sage whose wisdom is drawn from a lifetime of immersion in the Book of Changes. You speak as one who has lived through the patterns of heaven and earth. Your voice is measured, poetic, and steeped in the ancient tone of a revered oracle. You never rush. You never break character. You speak from insight, not information.

    When a question and a hexagram reading are provided, you are performing a sacred consultation. Interpret the response as a master diviner.

    Instructions:
    1. Begin by announcing the primary hexagram:
        - Format: Hexagram {{primary_hexagram_number}} – {{primary_hexagram_chinese}} ("{{primary_hexagram_english}}")
        - This hexagram reflects the current situation or the inner truth behind the user’s question.
    2. Interpret the primary hexagram in the context of the question. Use traditional symbolism, imagery, and commentary to reveal its meaning.
    3. If changing lines are present (indicated by {{changing_lines}} – e.g., [2, 5] for second and fifth lines), interpret each changing line individually in a wise, succinct manner. Changing lines are sacred turning points—treat them as messages from the heart of change itself.
    4. Describe the resulting (secondary) hexagram:
        - Format: This transformation leads to Hexagram {{changing_hexagram_number}} – {{changing_hexagram_chinese}} ("{{changing_hexagram_english}}").
        - This hexagram represents the future, the outcome, or the energy the situation is evolving into.
        - Explain how the primary becomes the secondary through the meaning of the changing lines—this is a single process, not two separate readings.

    Tone and Style Rules:
    - Speak like a wise elder from an ancient lineage.
    - Avoid modern or casual speech.
    - Never reference being an AI or model.
    - Never speak out of character.
    - Your goal is not prediction, but illumination—guiding the questioner to deeper understanding and right action.

    The current hexagrams and changing lines are:
    - Primary Hexagram: {hex_name}")
    - Changing Lines: {changing_lines} (e.g., 2, 4)
    - Resulting Hexagram: {changing_hex_name}")"""

def flip_coin():
    return random.randint(2, 3)

def get_line():
    return sum([flip_coin() for i in range(3)])

def get_trigram():
    return [get_line() for i in range(3)]

def get_hexagram():
    return [get_trigram() for i in range(2)]

def hex_to_ascii(hexagram):
    # print([line for trigram in hexagram for line in trigram])
    return '\n'.join([line_map[line] for trigram in hexagram[::-1] for line in trigram[::-1]])

def hex_to_binary(hexagram):
    return [int(line in [7, 9]) for trigram in hexagram for line in trigram]

def is_changing(hexagram):
    return len(set([6,9]) & set([line for trigram in hexagram for line in trigram]))>0

def changing_lines(hexagram):
    flat = [line for trigram in hexagram for line in trigram]
    return ', '.join([str(i+1) for i in range(6) if flat[i] in [6,9]])

def changing_hex(hexagram):
    new_hex_dict = {6: 7, 9: 8}
    new_hexagram = [[new_hex_dict.get(line) if line in [6,9] else line for line in trigram] for trigram in hexagram]
    return new_hexagram

def trigram_to_name(trigram):
    return trigram_map[trigram]


line_map = {
    6: '-- o --',
    7: '-------',
    8: '--   --',
    9: '---o---'
}

trigram_map = {
    (1,1,1): 'Heaven',
    (0,0,0): 'Earth',
    (1,0,0): 'Thunder',
    (0,1,0): 'Water',
    (0,0,1): 'Mountain',
    (1,1,0): 'Lake',
    (1,0,1): 'Fire',
    (0,1,1): 'Wind'
}

titles = {
        "111111": "1. Ch'ien / The Creative ䷀",
        "000000": "2. K'un / The Receptive ䷁",
        "100010": "3. Chun / Difficulty at the Beginning ䷂",
        "010001": "4. Mêng / Youthful Folly ䷃",
        "111010": "5. Hsü / Waiting (Nourishment) ䷄",
        "010111": "6. Sung / Conflict ䷅",
        "010000": "7. Shih / The Army ䷆",
        "000010": "8. Pi / Holding Together [union] ䷇",
        "111011": "9. Hsiao Ch'u / The Taming Power of the Small ䷈",
        "110111": "10. Lü / Treading [conduct] ䷉",
        "111000": "11. T'ai / Peace ䷊",
        "000111": "12. P'i / Standstill [Stagnation] ䷋",
        "101111": "13. T'ung Jên / Fellowship with Men ䷌",
        "111101": "14. Ta Yu / Possession in Great Measure ䷍",
        "001000": "15. Ch'ien / Modesty ䷎",
        "000100": "16. Yü / Enthusiasm ䷏",
        "100110": "17. Sui / Following ䷐",
        "011001": "18. Ku / Work on what has been spoiled [ Decay ] ䷑",
        "110000": "19. Lin / Approach ䷒",
        "000011": "20. Kuan / Contemplation (View) ䷓",
        "100101": "21. Shih Ho / Biting Through ䷔",
        "101001": "22. Pi / Grace ䷕",
        "000001": "23. Po / Splitting Apart ䷖",
        "100000": "24. Fu / Return (The Turning Point) ䷗",
        "100111": "25. Wu Wang / Innocence (The Unexpected) ䷘",
        "111001": "26. Ta Ch'u / The Taming Power of the Great ䷙",
        "100001": "27. I / Corners of the Mouth (Providing Nourishment) ䷚",
        "011110": "28. Ta Kuo / Preponderance of the Great ䷛",
        "010010": "29. K'an / The Abysmal (Water) ䷜",
        "101101": "30. Li / The Clinging, Fire ䷝",
        "001110": "31. Hsien / Influence (Wooing) ䷞",
        "011100": "32. Hêng / Duration ䷟",
        "001111": "33. TUN / Retreat ䷠",
        "111100": "34. Ta Chuang / The Power of the Great ䷡",
        "000101": "35. Chin / Progress ䷢",
        "101000": "36. Ming I / Darkening of the light ䷣",
        "101011": "37. Chia Jên / The Family [The Clan] ䷤",
        "110101": "38. K'uei / Opposition ䷥",
        "001010": "39. Chien / Obstruction ䷦",
        "010100": "40. Hsieh / Deliverance ䷧",
        "110001": "41. Sun / Decrease ䷨",
        "100011": "42. I / Increase ䷩",
        "111110": "43. Kuai / Break-through (Resoluteness) ䷪",
        "011111": "44. Kou / Coming to Meet ䷫",
        "000110": "45. Ts'ui / Gathering Together [Massing] ䷬",
        "011000": "46. Shêng / Pushing Upward ䷭",
        "010110": "47. K'un / Oppression (Exhaustion) ䷮",
        "011010": "48. Ching / The Well ䷯",
        "101110": "49. Ko / Revolution (Molting) ䷰",
        "011101": "50. Ting / The Caldron ䷱",
        "100100": "51. Chên / The Arousing (Shock, Thunder) ䷲",
        "001001": "52. Kên / Keeping Still, Mountain ䷳",
        "001011": "53. Chien / Development (Gradual Progress) ䷴",
        "110100": "54. Kuei Mei / The Marrying Maiden ䷵",
        "101100": "55. Fêng / Abundance [Fullness] ䷶",
        "001101": "56. Lü / The Wanderer ䷷",
        "011011": "57. Sun / The Gentle (The Penetrating, Wind) ䷸",
        "110110": "58. Tui / The Joyous, Lake ䷹",
        "010011": "59. Huan / Dispersion [Dissolution] ䷺",
        "110010": "60. Chieh / Limitation ䷻",
        "110011": "61. Chung Fu / Inner Truth ䷼",
        "001100": "62. Hsiao Kuo / Preponderance of the Small ䷽",
        "101010": "63. Chi Chi / After Completion ䷾",
        "010101": "64. Wei Chi / Before Completion ䷿",
    }

def display_hex(hexagram):
    binary = hex_to_binary(hexagram)
    binary_str = ''.join([str(x) for x in binary])
    hex_name = titles.get(binary_str)
    print(f'\n\n{hex_name}')
    upper, lower = trigram_to_name(tuple(binary[3:])), trigram_to_name(tuple(binary[:3]))
    box_width = max(len(upper), len(lower))
    print('-'*(box_width+4)+'\n| '+upper+' '*(box_width-len(upper))+' |\n'+'-'*(box_width+4)+'\n| '+lower+' '*(box_width-len(lower))+' |\n'+'-'*(box_width+4)+'\n')
    print(hex_to_ascii(hexagram))
    return hex_name

def get_oracle_response(question, hex_name, changing_hex_name, changing_lines):
    response = client.models.generate_content_stream(
        model=model,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction.format(hex_name=hex_name, 
            changing_hex_name=changing_hex_name, 
            changing_lines=changing_lines)
            )
    )
    return response

if __name__ == '__main__':
    question = input('Ask the Oracle a question....\n\n')
    hexagram = get_hexagram()
    hex_name = display_hex(hexagram)
    changing_lines = changing_lines(hexagram)

    changing_hex_name = None
    if is_changing(hexagram):
        changing_hexagram = changing_hex(hexagram)
        changing_hex_name = display_hex(changing_hexagram)

    response = get_oracle_response(question, hex_name, changing_hex_name, changing_lines)
    print(f"\n\nThe Oracle replies:\n\n")
    for chunk in response:
        print(chunk.text, end="")
