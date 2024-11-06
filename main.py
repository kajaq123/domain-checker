import whois
import csv
from tqdm import tqdm

def get_domain_info(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        # We check if the domain has an expiration date, which means it is taken
        if domain_info.expiration_date:
            istaken = True
            expire_date = domain_info.expiration_date
            # Selecting the first date on the list, Some domains have a list of dates
            if isinstance(expire_date, list):
                expire_date = expire_date[0]
            return domain_name, istaken, expire_date
        else:
            return domain_name, False, None
    except Exception as e:
        return domain_name, False, None  # If there's a error it returns as if the domain was available

def process_domains_from_file(file_path, output_csv):
    try:
        with open(file_path, 'r') as file:
            domains = file.readlines()

        # Open CSV
        with open(output_csv, mode='w', newline='') as csv_file:
            fieldnames = ['domain', 'istaken', 'expiredate']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # saving the headers of columns
            writer.writeheader()

            # checking if domain are avialiable with progress bar
            for domain in tqdm(domains, desc="Przetwarzanie domen"):
                domain = domain.strip()
                if domain:
                    domain_name, istaken, expire_date = get_domain_info(domain)
                    # saving data to CSV
                    writer.writerow({
                        'domain': domain_name,
                        'istaken': istaken,
                        'expiredate': expire_date if expire_date else 'N/A'
                    })
                    
        print(f"Dane zostały zapisane do pliku: {output_csv}")

    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")

# File paths
file_path = 'domain.txt'
output_csv = 'domain_results.csv'
process_domains_from_file(file_path, output_csv)
