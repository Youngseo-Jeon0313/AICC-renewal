"""
record_duration에 따라 text를 생성
ex. test test test test test test test test test test test test test
"""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TextResult:
    text: str
    duration: float
    created_at: datetime

class TextGenerator:
    BASE_WORD = "test "
    WORDS_PER_SECOND = 3  # (가정) 초당 생성할 단어 수

    @staticmethod
    def generate_text(record_duration: int) -> TextResult:
        """
        record_duration(초)에 비례하여 텍스트를 생성합니다.
        
        Args:
            record_duration: 녹음 시간 (초)
            
        Returns:
            TextResult: 생성된 텍스트, 소요 시간, 생성 시간을 포함하는 객체
        """
        word_count = record_duration * TextGenerator.WORDS_PER_SECOND        
        text = TextGenerator.BASE_WORD * word_count
        
        elapsed_time = word_count * 0.5  # (가정) 각 단어 생성에 0.5초 소요된다고 가정
        
        return TextResult(
            text=text.strip(),
            duration=elapsed_time,
            created_at=datetime.now()
        )
