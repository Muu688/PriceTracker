from abc import ABC, abstractmethod
from typing import Optional, Dict


class Notifier(ABC):

    @abstractmethod
    def notify(
        self,
        title: str,
        message: str,
        metadata: Optional[Dict] = None
    ):
        pass