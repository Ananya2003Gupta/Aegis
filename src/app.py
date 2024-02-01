import solcx
from clidantic import Parser
from solcx import compile_standard, compile_source
from args import CompileArguments
import numpy as np
from model import predict, reverse_engineer_one_hot_encoding


class CLIController:
    def __init__(self):
        self.cli = Parser(name="tea")
        self.setup_commands()

    def setup_commands(self):
        self.cli.command("setup", "Setup solc")(self.setup)
        self.cli.command(
            "scan", "Scan a file or directory for vulnerabilities")(self.scan)
        self.cli.command("compile", "Compile the solidity code")(self.compile)
        self.cli.command("help", "Get help on a command")(self.help)
        self.cli.command("config", "Configure the application")(self.config)
        self.cli.command(
            "version", "Get the version of the application")(self.version)
        self.cli.command(
            "uninstall", "Uninstall solcx")(self.uninstall)

    def uninstall(self):
        print(f"Uninstalling solc")
        print(solcx)
        solcx.remove("0.8.24")
        print(solcx.get_installed_solc_versions())

    def setup(self):
        print(f"Setting up solc")
        print(solcx.get_installable_solc_versions())
        print("Installing solc version 0.8.24")
        solcx.install_solc("0.8.24")
        print(solcx.get_installed_solc_versions())

    def scan(self):
        print(f"Scanning for vulnerabilities")

    def compile(self, args: CompileArguments):
        """ Compile the solidity code """
        with open(args.path, "r") as f:
            contract_file = f.read()
        # print(contract_file)

        compiled_file = compile_source(
            contract_file,
            output_values=["abi", "bin-runtime"],
            solc_version="0.8.24"
        )
        
        for key, value in compiled_file.items():
            name_of_contract = key
            bytecode = value['bin-runtime']

        labels = {
            0: 'access-control',
            1: 'arithmetic',
            2: 'other',
            3: 'reentrancy',
            4: 'safe',
            5: 'unchecked-calls'
        }
        # print(bytecode)
        prediction = predict(bytecode)
        # print("Prediction:", prediction)
        all_preds_np = np.array(prediction)
        original_labels = reverse_engineer_one_hot_encoding(all_preds_np)
        # print("Original Labels:", original_labels)
        mapped_labels = [[labels[label] for label in sublist] for sublist in original_labels]
        # print("Mapped Labels:")
        for sublist in mapped_labels:
            print(sublist)
        

    def help(self):
        print(f"Get help on a command")

    def config(self):
        print(f"Configure the application")

    def version(self):
        print(f"Get the version of the application")


if __name__ == "__main__":
    controller = CLIController()
    controller.cli()