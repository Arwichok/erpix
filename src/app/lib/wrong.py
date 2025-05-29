from dataclasses import dataclass

@dataclass
class Wrong:
    name: bool = False
    email: bool = False
    password: bool = False
    
    description: str = ""
    
    def __bool__(self):
        return self.name or self.email or self.password