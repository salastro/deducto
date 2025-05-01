from deducto.cli.session import run_proof_session

def main():
    run_proof_session()

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        pass
