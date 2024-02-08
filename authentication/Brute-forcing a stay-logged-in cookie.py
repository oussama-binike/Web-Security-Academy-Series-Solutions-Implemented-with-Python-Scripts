import hashlib,base64

with open('passwords.txt', 'r') as f:
    passwords = f.readlines()
    for password in passwords:
        password = password.split('\n')[0]
        # Create a new MD5 object for each password
        md5 = hashlib.md5()
        # Update the object with the data you want to hash
        data = str(password).encode()  # Convert the string to bytes
        md5.update(data)
        # Get the MD5 hash as a hexadecimal string
        md5_hash = md5.hexdigest()
        cookie = 'carlos:'+md5_hash
        
        data2 = cookie.encode()  # Convert the string to bytes
        base64_encoded = base64.b64encode(data2)

        encoded_data = base64_encoded.decode()  # Convert the bytes to a string

        with open('hashes.txt',"a") as f:
            f.write(encoded_data+'\n')
        f.close()










