#!/usr/bin/env python3
import argparse
import string
import secrets


def build_character_set(
    use_digits: bool, use_upper: bool, use_lower: bool, use_special: bool
) -> str:
    """Build character set based on enabled options"""
    char_set = [
        (use_digits, string.digits),
        (use_upper, string.ascii_uppercase),
        (use_lower, string.ascii_lowercase),
        (use_special, string.punctuation),
    ]

    return ''.join(chars for enabled, chars in char_set if enabled)


def validate_password_generation(length: int, char_set: str) -> None:
    validators = [
        (length > 0, 'Length must be a positive integer (> 0)'),
        (len(char_set) > 0, 'Must be at least 1 type of symbols enabled'),
    ]
    for condition, message in validators:
        if not condition:
            raise ValueError(message)


def generate_password(
    length: int, use_digits: bool, use_upper: bool, use_lower: bool, use_special: bool
) -> str:
    """Generate cryptographically secure password"""

    char_set = build_character_set(
        use_digits,
        use_upper,
        use_lower,
        use_special,
    )
    validate_password_generation(length, char_set)

    return ''.join(secrets.choice(char_set) for i in range(length))


def parse_ags() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        prog='QuickPass',
        description='QuickPass - secure password generator using cryptographically strong randomness',
        epilog="Usage:\n" "  QuickPass -l 16 --no-digits\n" "  QuickPass -c 5 -l 20",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-l',
        '--length',
        type=int,
        default=20,
        help='length of password (by default - 20)',
    )
    parser.add_argument(
        '--no-digits',
        action='store_false',
        dest='use_digits',
        help='disable digits (0-9, by default - enabled)',
    ),
    parser.add_argument(
        '--no-uppercase',
        action='store_false',
        dest='use_upper',
        help='disable uppercase (A-Z, by default - enabled)',
    ),
    parser.add_argument(
        '--no-lowercase',
        action='store_false',
        dest='use_lower',
        help='disable lowercase (a-z, by default - enabled)',
    ),
    parser.add_argument(
        '--no-special',
        action='store_false',
        dest='use_special',
        help='disable special (by default - enabled)',
    ),
    parser.add_argument(
        '-c',
        '--count',
        type=int,
        default=1,
        help='amount of passwords (by default - 1)',
    )

    args = parser.parse_args()

    return args


def main() -> None:
    try:
        args = parse_ags()

        if args.count < 1:
            raise argparse.ArgumentTypeError('Count must be a positive integer (> 0)')

        for _ in range(args.count):
            password = generate_password(
                args.length,
                use_digits=args.use_digits,
                use_lower=args.use_lower,
                use_special=args.use_special,
                use_upper=args.use_upper,
            )

            print(password)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)


if __name__ == '__main__':
    main()
