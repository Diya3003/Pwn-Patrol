import csv
from risk_model import check_password_pwned

def check_passwords_in_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Reads as dict for each row
        results = []

        for row in reader:
            website = row.get("website")
            user = row.get("user_or_email")
            password = row.get("password")

            if not password:
                pwned_count = None
            else:
                try:
                    pwned_count = check_password_pwned(password)
                except Exception as e:
                    print(f"Error checking password for {website}: {e}")
                    pwned_count = None

            results.append({
                "website": website,
                "user": user,
                "password": password,
                "pwned_count": pwned_count,
            })

    return results

if __name__ == "__main__":
    csv_path = "passwords.csv"
    results = check_passwords_in_csv(csv_path)
    for r in results:
        print(f"Website: {r['website']}, User/Email: {r['user']}, Password Pwned Count: {r['pwned_count']}")
