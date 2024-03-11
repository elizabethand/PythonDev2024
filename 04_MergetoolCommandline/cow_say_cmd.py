import cmd
import shlex
import cowsay


class CowSayCmd(cmd.Cmd):
    
    intro = "Welcome to the Cowsay command line!"
    prompt = "(cowsay)>>"
    cowsay_commands = ["list_cows", "make_bubble", "cowsay", "cowthink"]

    def do_list_cows(self, args):
        """List available cows.
        
        Usage: list_cows
        """
        print(cowsay.list_cows())

    def do_make_bubble(self, args):
        """Create a speech bubble.
        
        Usage: make_bubble [cowsay|cowthink] <message>
        
        Example: make_bubble "blablabla" cowthink
        """
        arg = shlex.split(args)

        message = arg[0]
        action = arg[1:]

        if len(action) == 0:
            action = "cowsay"
        else:
            action = action[0]

        thought_options = cowsay.THOUGHT_OPTIONS.get(action, {})
        print(cowsay.make_bubble(message, brackets=thought_options))

    def do_cowsay(self, args):
        """Speak as a cow.
        
        Usage: cowsay <message> [OPTIONS]
        
        Example: cowsay "Hello, Cows!" -e ^^ -T UU
        """
        self._execute_command("cowsay", args)

    def do_cowthink(self, args):
        """Think as a cow.
        
        Usage: cowthink <message> [OPTIONS]
        
        Example: cowthink "Pondering cow thoughts..." -e ^^ -T UU
        """
        self._execute_command("cowthink", args)

    def complete_cowsay(self, text, line, begidx, endidx):
        return [cmd for cmd in self.cowsay_commands if cmd.startswith(text)]

    def complete_cowthink(self, text, line, begidx, endidx):
        return [cmd for cmd in self.cowsay_commands if cmd.startswith(text)]

    def _execute_command(self, command, args):
        try:
            args_list = shlex.split(args)
            if command == "cowsay":
                self._parse_cowsay_args(args_list)
            elif command == "cowthink":
                self._parse_cowthink_args(args_list)
        except Exception as e:
            print(f"Error executing command: {e}")

    def _parse_cowsay_args(self, args_list):
        message = args_list[0] if args_list else ""
        cow = self._get_argument_value(args_list, "-f", "default")
        eyes = self._get_argument_value(args_list, "-e", "oo")
        tongue = self._get_argument_value(args_list, "-T", "  ")

        print(cowsay.cowsay(message=message, cow=cow, eyes=eyes, tongue=tongue))

    def _parse_cowthink_args(self, args_list):
        message = args_list[0] if args_list else ""
        cow = self._get_argument_value(args_list, "--cow", "default")
        eyes = self._get_argument_value(args_list, "--eyes", "oo")
        tongue = self._get_argument_value(args_list, "--tongue", "  ")

        print(cowsay.cowthink(message=message, cow=cow, eyes=eyes, tongue=tongue))

    def _get_argument_value(self, args_list, arg_name, default):
        try:
            arg_index = args_list.index(arg_name)
            return args_list[arg_index + 1]
        except (ValueError, IndexError):
            return default

    def do_EOF(self, args):
        print("\nGoodbye!")
        return 1


if __name__ == "__main__":
    CowSayCmd().cmdloop()

