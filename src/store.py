"""Histórico diario en data/AAAA/AAAA-MM-DD.json (se guarda en el repositorio)."""
import json
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


class Store:
    def __init__(self, root=DATA):
        self.root = Path(root)

    def path(self, day):
        return self.root / f"{day.year:04d}" / f"{day.isoformat()}.json"

    def load(self, day):
        p = self.path(day)
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))

    def save(self, day, record):
        """Escribe solo si cambia algo; devuelve True si ha escrito."""
        p = self.path(day)
        text = json.dumps(record, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
        if p.exists() and p.read_text(encoding="utf-8") == text:
            return False
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return True

    def update(self, day, **fields):
        record = self.load(day) or {"date": day.isoformat()}
        record.update(fields)
        return self.save(day, record)

    def days(self):
        return sorted(date.fromisoformat(p.stem) for p in self.root.glob("*/*.json"))

    def all(self):
        return {d: self.load(d) for d in self.days()}
