import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="The CLI reader for cosense")
subparsers = parser.add_subparsers()

def command_version(args):
    print("""cosense-python version 0.1.0
This pakage is developing now. Please contribute to this package via GitHub if you find any bugs.
GitHub:admidori/cosense-python""")

def command_help(args):
    print(parser.parse_args([args.command, '--help']))

def main():
    # Create the parser for the "search" command
    parser_search = subparsers.add_parser("search", help="Search for a keyword")
    parser_search.add_argument("--auth", type=str, help="Input an authentication token")
    
    # Create the parser for the "version" command
    parser_version = subparsers.add_parser("version", help="Print the version of cosense")
    parser_version.set_defaults(handler=command_version)

    # Create the parser for the "help" command
    parser_help = subparsers.add_parser("help", help="Print the help message")
    parser_help.add_argument("command", type=str, help="The command to get help for")
    parser_help.set_defaults(handler=command_help)

    # Parse the arguments
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
