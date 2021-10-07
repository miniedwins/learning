# Python 進制轉換



## 2進制轉換

~~~python
# bin to int
bin_number = '0b1010'
int(bin_number, base=2) # 10

# bin to hex
bin_number = 0b1010
hex(bin_number) # '0xa'
~~~



## 10進制轉換

~~~python
# int to bin
number = 10
bin(number) # '0b1010'

# int to hex
number = 10
hex(number) # '0x0a'

# int to chr
number = 97
chr(number) # 'a'

# int to string
number = 97
str(number) # '97'


~~~



## 16進制轉換

~~~python
# hex to int
hex_number = '0x61'
int(hex_number, 16) # 97

# hex to string
hex_number = '0x61'
str(hex_number) # '97'

# hex to bin
hex_number = 0xa
bin(hex_number) # '0b1010'

# hex to char
hex_number = '0x61'
chr(int(hex_number, 16)) # 'a'
chr(0x61) # 'a'

# hex to string
hex_string = "0x616263"[2:] # 616263
bytes_object = bytes.fromhex(hex_string) # b'abc'
ascii_string = bytes_object.decode("ASCII") # 'abc'

string = '61626364'
''.join(chr(int(string[i:i+2], 16)) for i in range(0, len(string), 2))  # 'abcd'

~~~



## string 轉換其它進制

~~~python
# char to int
ord('a') # 97

# char to hex
hex(ord('a')) # '0x61'

# string to int
int('97')  # 97

# string to hex
# 1. ord 會將字元轉10進位, ord('a') = 97
# 2. hex(97) 轉換成 '0x61'  
# 3. '0x61'[2:] 擷取字串 '61'
string = 'abcd'
''.join([hex(ord(x))[2:] for x in string])  # '61626364'
~~~

