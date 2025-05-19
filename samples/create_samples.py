#!/usr/bin/env python3
"""
This script connects to Crédit Agricole and extracts response structures to understand
the complete schema of objects returned by the API.
Creates separate files for each account, card, etc.

Available modes:
- 'json': saves json representations of the data with the '.json' extension suffix
- 'types': saves type structure of the data with the '.json' extension suffix
- 'string': saves string representations of the data with the '.txt' extension

If no mode is specified, all modes will be executed.
Multiple modes can be specified as comma-separated values.

Mock functionality:
- Use --mocks-dir to specify mock directory
- Use --write-mocks to write API responses to mock files
- Use --use-mocks to use mock data instead of API calls
"""

import json
import os
import sys
import argparse
import re
from datetime import datetime, timedelta
from getpass import getpass
from typing import Any, Dict, List, Union
from collections import defaultdict

from creditagricole_particuliers import (
    authenticator, accounts, regionalbanks, cards, logout, MockConfig
)

def save_json(data, filename, target_dir):
    """Save data to a JSON file"""
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, filename), 'w') as f:
        json.dump(data, f, indent=2)

def save_str(data, filename, target_dir):
    """Save data as string representation to a text file"""
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, filename), 'w') as f:
        if isinstance(data, list):
            # For lists, write each item's string representation on a new line
            for item in data:
                f.write(str(item) + '\n')
        else:
            f.write(str(data))

def convert_to_type_structure(data: Any) -> Any:
    """
    Converts real data to type structure.
    Replaces values with placeholders according to their type.
    """
    if isinstance(data, str):
        # Replace strings with empty string instead of "str"
        return ""
    elif isinstance(data, int):
        return 0
    elif isinstance(data, float):
        return 0.0
    elif isinstance(data, bool):
        return False
    elif isinstance(data, list):
        if data:
            # Only take the first element as an example
            return [convert_to_type_structure(data[0])]
        return []
    elif isinstance(data, dict):
        return {k: convert_to_type_structure(v) for k, v in data.items()}
    elif data is None:
        return None
    else:
        # For unhandled types
        return f"type:{type(data).__name__}"

def create_placeholder(original_id: str) -> str:
    """
    Creates a placeholder for an identifier by replacing all characters with '0'.
    Used to generate filenames without sensitive data.
    """
    if re.match(r'^[0-9]+$', original_id):
        return '0' * len(original_id)
    return 'placeholder'

def get_target_dir(base_dir: str, mode: str, single_mode: bool) -> str:
    """
    Determines the target directory based on mode and whether it's a single mode.
    If single_mode is True, returns base_dir directly.
    Otherwise, creates a subdirectory for the mode.
    """
    if single_mode:
        return base_dir
    return os.path.join(base_dir, mode)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Extract Credit Agricole API schemas')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', help='Password (digits only). If not provided, will be prompted securely')
    parser.add_argument('--department', required=True, type=int, help='Department code')
    parser.add_argument('--output-dir', default='./output', help='Output directory for samples')
    parser.add_argument('--mode', default=None,
                       help="Generation modes (comma-separated): 'json' for real data, 'types' for structure with placeholders, 'string' for string representations. If not specified, all modes will be executed.")
    
    # Add mock functionality arguments
    parser.add_argument('--use-mocks-dir', default=None, help='Directory for mock files to use')
    parser.add_argument('--write-mocks-dir', default=None, help='Directory for mock files to write')
    parser.add_argument('--use-mock-suffix', default='mock', help='Suffix for mock files to use')
    parser.add_argument('--write-mock-suffix', default='mock', help='Suffix for mock files to write')
    
    args = parser.parse_args()

    # Determine modes to execute
    if args.mode is None:
        modes = ['json', 'types', 'string']
    else:
        modes = [m.strip() for m in args.mode.split(',')]
        if not all(m in ['json', 'types', 'string'] for m in modes):
            print("Error: Invalid mode specified. Valid modes are: json, types, string")
            return 1

    # Get password either from argument or prompt
    password = args.password
    if not password:
        password = getpass('Enter your password (digits only): ')

    # Convert password string to digits array
    password_digits = [int(d) for d in password]
    
    # Create MockConfig object if mock functionality is enabled
    mock_config = None
    if args.use_mocks_dir or args.write_mocks_dir:
        mock_config = MockConfig(
            useMocksDir=args.use_mocks_dir,
            writeMocksDir=args.write_mocks_dir,
            useMockSuffix=args.use_mock_suffix,
            writeMockSuffix=args.write_mock_suffix
        )
        print(mock_config)

    try:
        # Authenticate
        print("Authenticating...")
        auth = authenticator.Authenticator(
            username=args.username,
            password=password_digits,
            department=args.department,
            mock_config=mock_config
        )
        
        # Get regional banks information
        print("Getting regional banks...")
        rb = regionalbanks.RegionalBanks(mock_config=mock_config)
        
        # Get specific regional bank for the user's department
        print(f"Getting regional bank information for department {args.department}...")
        bank = rb.by_departement(int(args.department))
        
        # Process data for each mode
        for mode in modes:
            target_dir = get_target_dir(args.output_dir, mode, len(modes) == 1)
            
            if mode == 'json':
                save_json(bank, f"regionalBank_{args.department}.json", target_dir)
            elif mode == 'types':
                bank_types = convert_to_type_structure(bank)
                save_json(bank_types, "regionalBank_types.json", target_dir)
            elif mode == 'string':
                save_str(rb.by_departement(int(args.department)), f"regionalBank_{args.department}.txt", target_dir)
        
        # Get accounts
        print("Getting accounts...")
        accs = accounts.Accounts(auth)
        accs_data = json.loads(accs.as_json())
        
        # Process accounts for each mode
        for mode in modes:
            target_dir = get_target_dir(args.output_dir, mode, len(modes) == 1)
            
            if mode == 'json':
                # Group accounts by grandeFamilleProduitCode
                accounts_by_code = defaultdict(list)
                for account in accs_data:
                    code = account.get('grandeFamilleProduitCode', 'unknown')
                    accounts_by_code[code].append(account)
                
                # Save all accounts into a single file
                save_json(accs_data, "accounts.json", target_dir)
                
                # Process each account for operations and IBAN
                for account in accs_data:
                    account_number = account['numeroCompte']
                    print(f"Getting operations for account {account_number}...")
                    
                    # Get operations for this account
                    acc = accs.search(account_number)
                    current_date = datetime.today()
                    previous_date = current_date - timedelta(days=30)
                    date_stop = current_date.strftime('%Y-%m-%d')
                    date_start = previous_date.strftime('%Y-%m-%d')
                    
                    try:
                        ops = acc.get_operations(date_start=date_start, date_stop=date_stop, count=10)
                        ops_data = json.loads(ops.as_json())
                        save_json(ops_data, f"account_{account_number}_operations.json", target_dir)
                    except Exception as e:
                        print(f"Error getting operations for account {account_number}: {e}")
                    
                    # Create empty IBAN file
                    print(f"Creating empty IBAN file for account {account_number}...")
                    try:
                        save_str([], f"account_{account_number}_iban.txt", target_dir)
                    except Exception as e:
                        print(f"Error creating IBAN file for account {account_number}: {e}")
            
            elif mode == 'types':
                if accs_data:
                    # Take only one example
                    first_account = accs_data[0]
                    account_example = convert_to_type_structure(first_account)
                    save_json(account_example, 'account_types.json', target_dir)
                    
                    # Get operations for the first account
                    real_account_number = first_account['numeroCompte']
                    print(f"Retrieving operations for example account...")
                    acc = accs.search(real_account_number)
                    current_date = datetime.today()
                    previous_date = current_date - timedelta(days=30)
                    date_stop = current_date.strftime('%Y-%m-%d')
                    date_start = previous_date.strftime('%Y-%m-%d')
                    
                    try:
                        ops = acc.get_operations(date_start=date_start, date_stop=date_stop, count=10)
                        ops_data = json.loads(ops.as_json())
                        if ops_data:
                            operation_example = convert_to_type_structure(ops_data[0])
                            save_json(operation_example, "operation_types.json", target_dir)
                    except Exception as e:
                        print(f"Error retrieving operations: {e}")
            
            elif mode == 'string':
                # Save all accounts
                accounts_list = json.loads(accs.as_json())
                save_str(accounts_list, "accounts.txt", target_dir)
                
                # Process each account for operations and IBAN
                for account in accounts_list:
                    account_number = account['numeroCompte']
                    print(f"Getting operations for account {account_number}...")
                    
                    # Get operations for this account
                    acc = accs.search(account_number)
                    current_date = datetime.today()
                    previous_date = current_date - timedelta(days=30)
                    date_stop = current_date.strftime('%Y-%m-%d')
                    date_start = previous_date.strftime('%Y-%m-%d')
                    
                    try:
                        ops = acc.get_operations(date_start=date_start, date_stop=date_stop, count=10)
                        ops_list = json.loads(ops.as_json())
                        save_str(ops_list, f"account_{account_number}_operations.txt", target_dir)
                    except Exception as e:
                        print(f"Error getting operations for account {account_number}: {e}")
                    
                    # Create empty IBAN file
                    print(f"Creating empty IBAN file for account {account_number}...")
                    try:
                        save_str([], f"account_{account_number}_iban.txt", target_dir)
                    except Exception as e:
                        print(f"Error creating IBAN file for account {account_number}: {e}")
        
        # Get cards
        print("Getting cards...")
        try:
            user_cards = cards.Cards(auth)
            cards_data = json.loads(user_cards.as_json())
            
            # Process cards for each mode
            for mode in modes:
                target_dir = get_target_dir(args.output_dir, mode, len(modes) == 1)
                
                if mode == 'json':
                    # Save all cards data
                    save_json(cards_data, "cards.json", target_dir)
                    
                    # Process each card individually for operations
                    for card in cards_data:
                        card_id = card['idCarte']
                        card_last_4 = card_id.split()[-1][-4:] if ' ' in card_id else card_id[-4:]
                        print(f"Processing card ending with {card_last_4}...")
                        
                        try:
                            print(f"Getting operations for card {card_last_4}...")
                            card_obj = user_cards.search(card_last_4)
                            deferred_ops = card_obj.get_operations()
                            ops_data = json.loads(deferred_ops.as_json())
                            save_json(ops_data, f"card_{card_last_4}_operations.json", target_dir)
                        except Exception as e:
                            print(f"Error getting operations for card {card_last_4}: {e}")
                
                elif mode == 'types':
                    if cards_data:
                        # Take only one example
                        first_card = cards_data[0]
                        card_example = convert_to_type_structure(first_card)
                        save_json(card_example, 'card_types.json', target_dir)
                        
                        try:
                            print(f"Getting card operations sample structure...")
                            card_id = first_card['idCarte']
                            card_last_4 = card_id.split()[-1][-4:] if ' ' in card_id else card_id[-4:]
                            card_obj = user_cards.search(card_last_4)
                            deferred_ops = card_obj.get_operations()
                            ops_data = json.loads(deferred_ops.as_json())
                            if ops_data:
                                operation_example = convert_to_type_structure(ops_data[0])
                                save_json(operation_example, "operation_card_types.json", target_dir)
                        except Exception as e:
                            print(f"Error getting card operations sample: {e}")
                
                elif mode == 'string':
                    # Save all cards
                    cards_list = json.loads(user_cards.as_json())
                    save_str(cards_list, "cards.txt", target_dir)
                    
                    # Process each card individually for operations
                    for card in cards_list:
                        card_id = card['idCarte']
                        card_last_4 = card_id.split()[-1][-4:] if ' ' in card_id else card_id[-4:]
                        print(f"Processing card ending with {card_last_4}...")
                        
                        try:
                            print(f"Getting operations for card {card_last_4}...")
                            card_obj = user_cards.search(card_last_4)
                            deferred_ops = card_obj.get_operations()
                            ops_list = json.loads(deferred_ops.as_json())
                            save_str(ops_list, f"card_{card_last_4}_operations.txt", target_dir)
                        except Exception as e:
                            print(f"Error getting operations for card {card_last_4}: {e}")
            
        except Exception as e:
            print(f"Error getting cards: {e}")
        
        # Logout properly
        print("Logging out...")
        try:
            logout_handler = logout.Logout(auth)
            logout_handler.logout()
            print("Successfully logged out")
        except Exception as e:
            print(f"Error during logout: {e}")
            
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 