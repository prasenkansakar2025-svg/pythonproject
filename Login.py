UsernameInput = input("Enter Username: ")
PasswordInput = input("Enter Password: ")

user_found = False

try:
    with open('Login.txt', 'r') as file:
        for line in file:
            clean_line = line.strip()

            if not clean_line:
                continue

            try:
                file_username, file_password = clean_line.split(' ')

                if file_username == UsernameInput and file_password == PasswordInput:
                    print("✅ Login Successful! The user exists.")
                    user_found = True
                    break

            except ValueError:
                print()

    if not user_found:
        print("❌ Login Failed. The user is not exists or credentials are wrong.")


except FileNotFoundError:
    print("Customised Error: The 'Login.txt' file was not found.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")