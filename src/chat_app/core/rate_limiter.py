import time
from collections import deque
from threading import Lock

class RateLimiter:
    def __init__(self, max_requests: int, period_seconds: int):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.requests = deque()
        self.lock = Lock()

    def allow_request(self) -> bool:
        with self.lock:
            current_time = time.time()

            # Remove requests antigos fora da janela de tempo
            while self.requests and self.requests[0] <= current_time - self.period_seconds:
                self.requests.popleft()

            if len(self.requests) < self.max_requests:
                self.requests.append(current_time)
                return True
            else:
                return False

    def wait_for_slot(self):
        """Aguarda o próximo slot disponível, ajustando a espera conforme necessário."""
        while not self.allow_request():
            # Calcula o tempo de espera baseado no número de requisições feitas
            # tempo necessário para respeitar o limite
            current_time = time.time()
            if self.requests:  # Verifica se a lista não está vazia
                earliest_request_time = self.requests[0] 
                remaining_time = max(0, self.period_seconds - (current_time - earliest_request_time))
            else:
                remaining_time = 1  # Espera um segundo se não houver requisições

            # Aguarda o tempo necessário para garantir que a próxima requisição pode ser feita
            time.sleep(remaining_time)