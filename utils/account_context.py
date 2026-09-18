from dataclasses import dataclass


@dataclass
class AccountContext:
    name: str
    email: str
    password: str
    account_number: str | None = None
    initial_balance: float = 0.0
    balance: float = 0.0

    def remember_account_number(self, value: str):
        self.account_number = value

    def set_initial_balance(self, value: float):
        self.initial_balance = value
        self.balance = value
