import signal
import sys

def handler(signum, frame):
    print("🚨 Processamento interrompido pelo usuário.")
    sys.exit(1)

def setup_signal_handler():
    signal.signal(signal.SIGINT, handler)