import argparse
import cosense.cli.search

# Initialize the parser
parser = argparse.ArgumentParser(description="The CLI reader for cosense")
subparsers = parser.add_subparsers()

def command_search(args):
    cosense.cli.search.search(args)

def command_version(args):
    print("cosense-cli version" + cosense.__version__)

def command_help(args):
    print(parser.parse_args([args.command, '--help']))

def main():
    # Create the parser for the "search" command
    parser_search = subparsers.add_parser("search", help="Search for a keyword")
    parser_search.add_argument("project", type=str, help="The project to search in")
    parser_search.add_argument("--auth", type=str, help="Input an authentication token")
    parser_search.set_defaults(handler=command_search)

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
