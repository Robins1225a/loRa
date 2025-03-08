def ascii_to_decimal(message):
    return [ord(char) for char in message]  # Convert each character to its ASCII decimal value.

message = "HELLOworld"
decimal_message = ascii_to_decimal(message)
print("original meassage:",message)
print("Decimal Message:", decimal_message)


def hamming_encode_8bit(data_list):
    
    encoded_list = []

    for data in data_list:
        # Extract the 8 data bits
        d1 = (data >> 7) & 1
        d2 = (data >> 6) & 1
        d3 = (data >> 5) & 1
        d4 = (data >> 4) & 1
        d5 = (data >> 3) & 1
        d6 = (data >> 2) & 1
        d7 = (data >> 1) & 1
        d8 = data & 1

        # Calculate parity bits
        p1 = d1 ^ d2 ^ d4 ^ d5 ^ d7
        p2 = d1 ^ d3 ^ d4 ^ d6 ^ d7
        p3 = d2 ^ d3 ^ d4 ^ d8
        p4 = d5 ^ d6 ^ d7 ^ d8

        # Combine parity bits and data bits into a 12-bit value
        encoded = (p1 << 11) | (p2 << 10) | (d1 << 9) | (p3 << 8) | (d2 << 7) | \
                  (d3 << 6) | (d4 << 5) | (p4 << 4) | (d5 << 3) | (d6 << 2) | (d7 << 1) | d8
        encoded_list.append(encoded)

    return encoded_list


encoded_payload = hamming_encode_8bit(decimal_message)

# Output the results
print("Hamming Encoded Payload:", encoded_payload)


def whiten(data, seed=0x55):
    return [byte ^ seed for byte in data]  # XOR each byte with a seed value.

whitened_payload = whiten(encoded_payload)
print("Whitened Payload:", whitened_payload)

def interleave(data, rows, cols):
    if len(data) != rows * cols:
        raise ValueError("Data size must match rows * cols.")
    matrix = [data[i * cols:(i + 1) * cols] for i in range(rows)]
    interleaved = []
    for col in range(cols):
        for row in range(rows):
            interleaved.append(matrix[row][col])
    return interleaved


rows, cols = 2, 5

interleaved_payload = interleave(whitened_payload, rows, cols)
print("Interleaved Data:", interleaved_payload)


def gray_encode(data):
    return [byte ^ (byte >> 1) for byte in data]

gray_coded_payload = gray_encode(interleaved_payload)
print("Gray Coded Payload:", gray_coded_payload)

def add_preamble_and_sync(payload):
    preamble_length = 12
    preamble = [0xAA] * preamble_length # Example preamble.
    sync_word = [0x12]  # Example sync word.
    return preamble + sync_word + payload

final_packet = add_preamble_and_sync(gray_coded_payload)
print("Final Packet:", final_packet)


#Receiving part

def extract_payload(packet, preamble_length=12, sync_word_length=1):
    payload_start = preamble_length + sync_word_length
    return packet[payload_start:]

received_packet = final_packet  # Simulate receiving the transmitted packet.
extracted_payload = extract_payload(received_packet)
print("Extracted Payload:", extracted_payload)


def gray_to_binary(gray_list):
    
    binary_list = []
    for gray in gray_list:
        binary = gray
        while gray > 0:
            gray = gray >> 1
            binary = binary ^ gray
        binary_list.append(binary)
    return binary_list

de_gray_payload = gray_to_binary(extracted_payload)
print("De-Gray Payload:",de_gray_payload)


def deinterleave(data, rows, cols):
    if len(data) != rows * cols:
        raise ValueError("Data size must match rows * cols.")
    matrix = [[0] * cols for _ in range(rows)]
    index = 0
    for col in range(cols):
        for row in range(rows):
            matrix[row][col] = data[index]
            index += 1
    deinterleaved = []
    for row in range(rows):
        deinterleaved.extend(matrix[row])
    return deinterleaved


deinterleaved_payload = deinterleave(de_gray_payload, rows, cols)
print("Deinterleaved Data:", deinterleaved_payload)


def dewhiten(data, seed=0x55):
    return [byte ^ seed for byte in data]

dewhitened_payload = dewhiten(deinterleaved_payload)
print("De-whitened Payload:", dewhitened_payload)


def hamming_decode_12bit(encoded_list):
    
    decoded_list = []
    a =0

    for encoded in encoded_list:
        
        p1 = (encoded >> 11) & 1
        p2 = (encoded >> 10) & 1
        d1 = (encoded >> 9) & 1
        p3 = (encoded >> 8) & 1
        d2 = (encoded >> 7) & 1
        d3 = (encoded >> 6) & 1
        d4 = (encoded >> 5) & 1
        p4 = (encoded >> 4) & 1
        d5 = (encoded >> 3) & 1
        d6 = (encoded >> 2) & 1
        d7 = (encoded >> 1) & 1
        d8 = encoded & 1

        
        s1 = p1 ^ d1 ^ d2 ^ d4 ^ d5 ^ d7
        s2 = p2 ^ d1 ^ d3 ^ d4 ^ d6 ^ d7
        s3 = p3 ^ d2 ^ d3 ^ d4 ^ d8
        s4 = p4 ^ d5 ^ d6 ^ d7 ^ d8

        p = (s4 << 3) | (s3 << 2) | (s2 << 1) | s1

       


       
        d1 = (encoded >> 9) & 1
        d2 = (encoded >> 7) & 1
        d3 = (encoded >> 6) & 1
        d4 = (encoded >> 5) & 1
        d5 = (encoded >> 3) & 1
        d6 = (encoded >> 2) & 1
        d7 = (encoded >> 1) & 1
        d8 = encoded & 1

       
        decoded = (d1 << 7) | (d2 << 6) | (d3 << 5) | (d4 << 4) | (d5 << 3) | (d6 << 2) | (d7 << 1) | d8
        decoded_list.append(decoded)
        a=a+p

    return decoded_list

decoded_data= hamming_decode_12bit(dewhitened_payload)
print("De_Hamming Data:", decoded_data)




def decimal_to_ascii(decimal_list):
    ascii_string = ''.join(chr(num) for num in decimal_list if 0 <= num <= 127)
    return ascii_string



ascii_result = decimal_to_ascii(decoded_data)


print("ASCII String:", ascii_result)