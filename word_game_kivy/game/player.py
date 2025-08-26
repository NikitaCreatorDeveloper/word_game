from dataclasses import dataclass, asdict


@dataclass
class Player:
    name: str
    wins: int = 0
    losses: int = 0
    score: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(
            name=str(data.get("name", "")),
            wins=int(data.get("wins", 0)),
            losses=int(data.get("losses", 0)),
            score=int(data.get("score", 0)),
        )
